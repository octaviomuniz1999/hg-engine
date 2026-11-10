#!/usr/bin/env python3
"""Localized CP05-A DeSmuME regression; an existing battery is allowed here.

This does NOT claim new-game coverage. Logs and screenshots remain private.
"""
import argparse
import json
import math
from pathlib import Path
import shutil

import map_lab as lab
from test_village_runtime import Session, shortest_path, FIELD_POINTER


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom",type=Path)
    p.add_argument("--initial-dsv",type=Path,required=True)
    p.add_argument("--work-dir",type=Path,required=True)
    a = p.parse_args()
    rom = a.rom.resolve();root = lab.private_new(a.work_dir);root.mkdir(parents=True)
    config = root/"config";(config/"desmume").mkdir(parents=True)
    shutil.copyfile(a.initial_dsv,config/"desmume"/(rom.stem+".dsv"))
    raw,_,headers,archives = lab.open_rom(rom)
    info = lab.header_info(headers,archives,60)
    per = lab.split_map(archives[lab.LAND].files[info["matrix_info"]["land_ids"][0]])["per"]
    blocked = {(8,8),(13,25),(4,23),(28,27),(8,17),(17,26)}
    cases = [];report = {"rom_sha256":lab.digest(raw),"new_game_test":False,
                         "initial_battery_copied":True,"cases":cases,"completed":False}
    s = Session(rom,root/"session",config)

    def checkpoint(name,map_id,x=None,z=None,height=None):
        r = s.send(shot=name+".png",field_pointer=FIELD_POINTER);f = r["field"]
        lab.require(f["map_id"] == map_id, (name,f))
        if x is not None:lab.require((f["x"],f["z"]) == (x,z),(name,f))
        if height is not None:
            lab.require(math.isclose(f["player_height_tiles"],height,abs_tol=.01),(name,f))
        cases.append({"name":name,**r});print(json.dumps({"name":name,"field":f}),flush=True)

    def walk(x,z):
        f = s.send(field_pointer=FIELD_POINTER)["field"]
        lab.require(f["map_id"] == 60,"Not in village")
        path = shortest_path(per,(f["x"],f["z"]),(x,z),blocked)
        steps = []
        for d in path:
            if steps and steps[-1]["keys"] == [d]:steps[-1]["pulse"] += 1
            else:steps.append({"keys":[d],"pulse":1,"hold":8,"gap":30})
        r = s.send(steps=steps,field_pointer=FIELD_POINTER)["field"]
        lab.require((r["map_id"],r["x"],r["z"]) == (60,x,z),r)

    try:
        s.boot()
        # All existing access points must remain connected around the objects.
        for target in ((8,9),(4,24),(13,26),(8,16),(17,27),(27,27),(8,11),(23,19)):
            shortest_path(per,(16,27),target,blocked)
        for name,x,z,key in (("fountain-south",24,9,"UP"),("fountain-west",22,7,"RIGHT"),
                             ("fountain-north",24,5,"DOWN"),("fountain-east",26,7,"LEFT"),
                             ("west-mast",21,6,"UP"),("east-mast",27,6,"UP")):
            walk(x,z);s.send(steps=[{"frames":24,"keys":[key]},{"frames":40}])
            checkpoint(name,60,x,z,1)
        for name,x,z,height in (("right-bottom",23,21,0),("right-middle",23,20,.5),
                                ("right-top",23,19,1),("left-bottom",8,13,0),
                                ("left-middle",8,12,.5),("left-top",8,11,1)):
            walk(x,z);checkpoint(name,60,x,z,height)
        walk(8,9);s.send(steps=[{"frames":40,"keys":["UP"]},{"frames":300}])
        checkpoint("lab-inside",61)
        s.send(steps=[{"pulse":2,"keys":["UP"],"hold":8,"gap":30},
                      {"frames":40,"keys":["DOWN"]},{"frames":300}])
        checkpoint("lab-return",60)
        walk(8,9);checkpoint("movement-after-return",60,8,9,1)
        report["completed"] = True
    finally:
        s.close();(root/"results.json").write_text(json.dumps(report,indent=2)+"\n")


if __name__ == "__main__":main()
