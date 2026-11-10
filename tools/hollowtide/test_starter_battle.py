#!/usr/bin/env python3
"""Play a real short battle in the separate private CP05 test variant.

Uses ordinary keypad actions, native outcome observation and read-only party
data. The production ROM has no added battle event.
"""
import argparse
import json
from pathlib import Path
import re
import shutil

import map_lab as lab
from observe_party import snapshot
from test_village_runtime import Session,shortest_path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom",type=Path);p.add_argument("--initial-dsv",type=Path,required=True)
    p.add_argument("--species",type=int,choices=(545,703,258),required=True)
    p.add_argument("--symbols",type=Path,required=True);p.add_argument("--work-dir",type=Path,required=True)
    a = p.parse_args();rom = a.rom.resolve();root = lab.private_new(a.work_dir);root.mkdir(parents=True)
    config = root/"config";(config/"desmume").mkdir(parents=True)
    shutil.copyfile(a.initial_dsv,config/"desmume"/(rom.stem+".dsv"))
    fp = int(re.search(r"^gFieldSysPtr = (0x[0-9a-fA-F]+);",a.symbols.read_text(),re.M)[1],16)
    raw,_,headers,archives = lab.open_rom(rom)
    info = lab.header_info(headers,archives,60)
    per = lab.split_map(archives[lab.LAND].files[info["matrix_info"]["land_ids"][0]])["per"]
    report = {"fixture_rom_sha256":lab.digest(raw),"expected_species":a.species,
              "private_test_variant_only":True,"completed":False}
    s = Session(rom,root/"session",config,["--observe-battle-outcomes"])
    try:
        s.boot(field_pointer=fp);before = snapshot(s);mon = before["members"][0]
        lab.require(before["count"] == 1 and mon["species"] == a.species,mon)
        lab.require(mon["level"] == 5 and mon["hp"] > 0,mon);report["before"] = before
        s.send(frames=180)
        s.send(tap=[44,74],frames=180,shot="00-party-menu-before-battle.png")
        s.send(tap=[228,176],frames=240)
        f = s.send(field_pointer=fp)["field"]
        path = shortest_path(per,(f["x"],f["z"]),(8,16),
                             {(8,8),(13,25),(4,23),(28,27),(8,17),(17,26)})
        steps = []
        for d in path:
            if steps and steps[-1]["keys"] == [d]:steps[-1]["pulse"] += 1
            else:steps.append({"keys":[d],"pulse":1,"hold":8,"gap":30})
        f = s.send(steps=steps,field_pointer=fp)["field"]
        lab.require((f["map_id"],f["x"],f["z"]) == (60,8,16),
                    "Party menu did not close or path did not reach test NPC")
        s.send(steps=[{"frames":2,"keys":["DOWN"]},{"frames":30},
                      {"frames":2,"keys":["A"]},{"frames":900}],shot="01-battle-start.png")
        win = False
        for i in range(80):
            command = {"pulse":1,"keys":["A"],"hold":2,"gap":180}
            if i%4 == 0:command["shot"] = f"02-battle-progress-{i:02d}.png"
            r = s.send(**command)
            if any(e["flags"]&3 == 1 for e in r["battle_outcomes"]):
                report["native_outcomes"] = r["battle_outcomes"];win = True;break
        lab.require(win,"No native win outcome observed")
        s.send(shot="03-native-win.png")
        # B advances the end messages but cannot start a second NPC battle.
        s.send(steps=[{"pulse":30,"keys":["B"],"gap":60},{"frames":1200}],
               shot="04-return-to-village.png",field_pointer=fp)
        after = snapshot(s);report["after"] = after
        lab.require(after["members"][0]["species"] == a.species and
                    after["members"][0]["hp"] > 0,after)
        lab.require(after["members"][0]["experience"] > mon["experience"],"No experience gained")
        f = s.send(steps=[{"frames":8,"keys":["RIGHT"]},{"frames":30}],
                   shot="05-movement-after-victory.png",field_pointer=fp)["field"]
        lab.require((f["map_id"],f["x"],f["z"]) == (60,9,16),f)
        report["completed"] = True
    except Exception as error:
        report["failure"] = str(error)
        try:s.send(shot="failure.png",field_pointer=fp)
        except Exception:pass
        raise
    finally:
        s.close();(root/"results.json").write_text(json.dumps(report,indent=2)+"\n")


if __name__ == "__main__":main()
