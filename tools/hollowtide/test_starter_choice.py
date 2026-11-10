#!/usr/bin/env python3
"""Validate one actual starter choice, field return and native persistence.

Use a pre-lab battery created through a recorded genuine new game. This test
does not claim to replay that introduction. No RAM writes or savestates.
"""
import argparse
import json
from pathlib import Path
import re
import shutil

import map_lab as lab
from observe_party import snapshot, dex_flags
from test_village_runtime import Session, shortest_path

# Native carousel: Grass is the front/bottom ball, Fire top-right, Water top-left.
CHOICES = ((545,65,[33,43,0,0],(128,126)),
           (703,66,[10,39,52,0],(182,42)),
           (258,67,[33,45,55,0],(72,42)))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom",type=Path);p.add_argument("--initial-dsv",type=Path,required=True)
    p.add_argument("--slot",type=int,choices=range(3),required=True)
    p.add_argument("--symbols",type=Path,required=True)
    p.add_argument("--work-dir",type=Path,required=True)
    a = p.parse_args();rom = a.rom.resolve();root = lab.private_new(a.work_dir)
    root.mkdir(parents=True);config = root/"config";(config/"desmume").mkdir(parents=True)
    shutil.copyfile(a.initial_dsv,config/"desmume"/(rom.stem+".dsv"))
    fp = int(re.search(r"^gFieldSysPtr = (0x[0-9a-fA-F]+);",a.symbols.read_text(),re.M)[1],16)
    raw,_,headers,archives = lab.open_rom(rom)
    species,ability,moves,tap = CHOICES[a.slot]
    s = Session(rom,root/"session01",config)
    report = {"rom_sha256":lab.digest(raw),"slot":a.slot,"expected_species":species,
              "field_pointer":fp,"completed":False,"new_game_test":False,
              "initial_battery_sha256":lab.digest(a.initial_dsv.read_bytes())}

    def shot(name):return s.send(shot=name+".png",field_pointer=fp)

    def walk(x,z):
        f = s.send(field_pointer=fp)["field"]
        info = lab.header_info(headers,archives,f["map_id"])
        lab.require(len(info["matrix_info"]["land_ids"]) == 1,"Expected one-cell map")
        per = lab.split_map(archives[lab.LAND].files[info["matrix_info"]["land_ids"][0]])["per"]
        blocked = {(w["x"],w["z"]) for w in f["warps"]}
        if f["map_id"] == 60:blocked |= {(8,17),(17,26)}
        steps = []
        for d in shortest_path(per,(f["x"],f["z"]),(x,z),blocked):
            if steps and steps[-1]["keys"] == [d]:steps[-1]["pulse"] += 1
            else:steps.append({"keys":[d],"pulse":1,"hold":8,"gap":30})
        end = s.send(steps=steps,field_pointer=fp)["field"]
        lab.require((end["map_id"],end["x"],end["z"]) == (f["map_id"],x,z),end)

    def party():
        observed = snapshot(s)
        lab.require(observed["count"] == 1,observed)
        mon = observed["members"][0]
        lab.require(mon["species"] == species and mon["level"] == 5,mon)
        lab.require(mon["ability"] == ability and mon["moves"] == moves,mon)
        lab.require(mon["hp"] == mon["max_hp"] and mon["hp"] > 0,mon)
        return observed

    try:
        s.boot(field_pointer=fp);lab.require(snapshot(s)["count"] == 0,"Pre-lab battery already has a Pokemon")
        walk(8,9)
        s.send(steps=[{"frames":40,"keys":["UP"]},{"frames":300},
                      {"frames":144,"keys":["UP"]},{"frames":180}],shot="01-alex-introduction.png",field_pointer=fp)
        s.send(pulse=50,keys=["B"],gap=50)
        # Go around the professor at (4,5); a PER-only shortest path through
        # his occupied tile would leave the player one tile off the device.
        s.send(steps=[{"frames":64,"keys":["RIGHT"]},{"frames":32,"keys":["UP"]},
                      {"pulse":2,"keys":["A"],"gap":90},{"frames":180}],
               shot="02-choice-interface.png",field_pointer=fp)
        s.send(tap=list(tap),frames=150,shot="03-species-preview.png")
        s.send(pulse=1,keys=["A"],gap=180,shot="04-species-confirmation.png")
        s.send(steps=[{"frames":2,"keys":["A"]},{"frames":600}],
               shot="05-received-or-nickname.png",field_pointer=fp)
        s.send(pulse=30,keys=["B"],gap=50,shot="06-alex-after-choice.png",field_pointer=fp)
        report["received_party"] = party();print(json.dumps(report["received_party"]),flush=True)
        # Timing differs with the new text. First observe an actual step out
        # of Alex's conversation; one A press at a time avoids reopening it.
        for _ in range(30):
            f = s.send(steps=[{"frames":8,"keys":["DOWN"]},{"frames":30}],field_pointer=fp)["field"]
            if (f["x"],f["z"]) != (4,7):break
            s.send(pulse=1,keys=["A"],gap=90)
        lab.require((f["x"],f["z"]) != (4,7),"Alex conversation did not release control")
        # The native assistant interrupts the first exit at (4,11). Allow
        # its item fanfare and messages to finish before asserting a warp.
        s.send(steps=[{"frames":96,"keys":["DOWN"]},{"frames":300}])
        for _ in range(20):
            f = s.send(field_pointer=fp)["field"]
            if f["map_id"] == 60:break
            s.send(steps=[{"pulse":1,"keys":["A"],"gap":120},
                          {"frames":64,"keys":["DOWN"]},{"frames":180}])
        lab.require(shot("07-follower-in-village")["field"]["map_id"] == 60,"Did not return to village")
        walk(8,9)
        # Pokémon is the middle-left button; the top-left cell is Pokédex.
        s.send(tap=[44,74],frames=180,shot="08-party-icon-and-level.png")
        s.send(tap=[228,176],frames=240)
        walk(8,10);walk(8,9)  # prove the party overlay closed before SAVE
        s.send(tap=[124,74],frames=120,shot="09-save-prompt.png")
        s.send(steps=[{"pulse":5,"keys":["A"],"gap":90},{"frames":1600}],shot="10-save-complete.png")
        s.close();report["native_save_sha256"] = lab.digest((config/"desmume"/(rom.stem+".dsv")).read_bytes())
        s = Session(rom,root/"session02-cold-load",config);s.boot(field_pointer=fp)
        f = shot("11-persistent-continue")["field"]
        lab.require((f["map_id"],f["x"],f["z"]) == (60,8,9),f)
        report["reloaded_party"] = party()
        report["reloaded_dex_flags"] = dex_flags(s,species)
        lab.require(all(report["reloaded_dex_flags"].values()),report["reloaded_dex_flags"])
        walk(8,10);shot("12-movement-after-load")
        report["completed"] = True
    except Exception as error:
        report["failure"] = str(error)
        try:shot("failure")
        except Exception:pass
        raise
    finally:
        s.close();(root/"results.json").write_text(json.dumps(report,indent=2)+"\n")


if __name__ == "__main__":main()
