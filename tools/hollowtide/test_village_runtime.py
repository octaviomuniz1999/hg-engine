#!/usr/bin/env python3
"""Exercise CP04 through real DeSmuME inputs, with private logs/screenshots.

The owner-provided CP02 battery save is copied only to a NEW private config.
The persistence test subsequently uses the game's SAVE and a new process; no
savestate, imported battery or memory write is used to prove persistence.
Dialogue and graphical screenshots still require visual review.
"""

import argparse
from collections import deque
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

import map_lab as lab

FIELD_POINTER = 0x023DDE58
DIRECTIONS = {"UP":(0,-1),"DOWN":(0,1),"LEFT":(-1,0),"RIGHT":(1,0)}


class Session:
    def __init__(self,rom,root,config,extra_args=()):
        self.root=root
        self.process=subprocess.Popen([sys.executable,"-u","-B",str(Path(__file__).with_name("emulator_session.py")),
                                       str(rom),"--session-dir",str(root),"--config-dir",str(config),*extra_args],
                                      stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        for line in self.process.stdout:
            if "EMULATOR_READY" in line:break
        else:raise RuntimeError("DeSmuME did not become ready")

    def send(self,**command):
        self.process.stdin.write(json.dumps(command)+"\n");self.process.stdin.flush()
        for line in self.process.stdout:
            try:result=json.loads(line)
            except json.JSONDecodeError:continue
            if "frame" in result:return result
        raise RuntimeError("Emulator closed before command result")

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.write('{"quit":true}\n');self.process.stdin.flush()
            self.process.stdin.close();self.process.wait(timeout=30)
        if self.process.returncode:raise RuntimeError(f"DeSmuME exit {self.process.returncode}")

    def boot(self):
        return self.send(steps=[{"frames":900},{"frames":2,"keys":["START"]},{"frames":120},
                                {"frames":2,"keys":["START"]},{"frames":600},
                                {"frames":2,"keys":["A"]},{"frames":400}],field_pointer=FIELD_POINTER)


def shortest_path(per,start,target,blocked):
    queue=deque([start]);previous={start:None}
    while queue:
        point=queue.popleft()
        if point==target:break
        for direction,(dx,dz) in DIRECTIONS.items():
            p=(point[0]+dx,point[1]+dz)
            if p in previous or p in blocked or not (0<=p[0]<32 and 0<=p[1]<32):continue
            if per[2*(p[1]*32+p[0])+1]&0x80:continue
            previous[p]=(point,direction);queue.append(p)
    lab.require(target in previous,f"No permission path from {start} to {target}")
    path=[];point=target
    while previous[point] is not None:
        point,direction=previous[point];path.append(direction)
    return path[::-1]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom",type=Path)
    p.add_argument("--initial-dsv",type=Path,required=True)
    p.add_argument("--work-dir",type=Path,required=True)
    args=p.parse_args()
    rom=args.rom.resolve();root=lab.private_new(args.work_dir);root.mkdir(parents=True)
    config=root/"config";(config/"desmume").mkdir(parents=True)
    shutil.copyfile(args.initial_dsv,config/"desmume"/(rom.stem+".dsv"))
    _,_,headers,archives=lab.open_rom(rom)
    cases=[];session=Session(rom,root/"session01",config)
    report={"rom_sha256":lab.digest(rom.read_bytes()),"timezone":os.environ.get("TZ"),
            "no_memory_writes_or_savestates":True,"cases":cases,
            "visual_review_required":True,"completed":False}

    def checkpoint(name,map_id,x=None,z=None,height=None):
        r=session.send(shot=name+".png",field_pointer=FIELD_POINTER);f=r["field"]
        lab.require(f.get("available") and f["map_id"]==map_id,f"{name}: unexpected map {f}")
        if x is not None:lab.require(f["x"]==x,f"{name}: unexpected X {f}")
        if z is not None:lab.require(f["z"]==z,f"{name}: unexpected Z {f}")
        if height is not None:lab.require(math.isclose(f["player_height_tiles"],height,abs_tol=0.01),f"{name}: height {f}")
        cases.append({"case":name,**r,"coordinate_assertions_passed":True})
        print(json.dumps({"case":name,"map":f["map_id"],"x":f["x"],"z":f["z"],
                          "height":f.get("player_height_tiles")}),flush=True)
        (root/"results.json").write_text(json.dumps(report,indent=2)+"\n")
        return f

    def walk(x,z):
        f=session.send(field_pointer=FIELD_POINTER)["field"];header=f["map_id"]
        info=lab.header_info(headers,archives,header)
        lab.require(len(info["matrix_info"]["land_ids"])==1,"Runtime walking requires one-cell matrix")
        data=archives[lab.LAND].files[info["matrix_info"]["land_ids"][0]]
        per=lab.split_map(data)["per"]
        blocked={(w["x"],w["z"]) for w in f.get("warps",[])}
        if header==60:blocked|={(8,17),(17,26)}
        route=shortest_path(per,(f["x"],f["z"]),(x,z),blocked)
        steps=[]
        for direction in route:
            if steps and steps[-1]["keys"]==[direction]:steps[-1]["pulse"]+=1
            else:steps.append({"pulse":1,"keys":[direction],"hold":8,"gap":30})
        if steps:session.send(steps=steps,field_pointer=FIELD_POINTER)
        result=session.send(field_pointer=FIELD_POINTER)["field"]
        lab.require((result["map_id"],result["x"],result["z"])==(header,x,z),
                    f"Keyboard walk failed: expected {header}/{x}/{z}, got {result}")

    def interior(label,point,expected,warp,exit_direction="DOWN"):
        walk(*point)
        session.send(steps=[{"frames":40,"keys":["UP"]},{"frames":300}])
        checkpoint(label+"-inside",expected)
        away={"DOWN":"UP","RIGHT":"LEFT"}[exit_direction]
        session.send(steps=[{"pulse":2,"keys":[away],"hold":8,"gap":30},
                            {"frames":40,"keys":[exit_direction]},{"frames":300}])
        checkpoint(label+"-return",60)
        walk(warp[0],warp[1]+1)
        checkpoint(label+"-outside-door",60,warp[0],warp[1]+1)

    try:
        session.boot();checkpoint("01-cold-load-lab",61,4,11)
        session.send(steps=[{"frames":72,"keys":["DOWN"]},{"frames":300}])
        checkpoint("02-village-arrival",60,8,None,1)
        # An exterior 69/80 door may spawn on its own tile; step out normally.
        walk(8,9)
        walk(8,11);checkpoint("03-left-stair-top",60,8,11,1)
        walk(8,12);checkpoint("04-left-stair-middle",60,8,12,0.5)
        walk(8,13);checkpoint("05-left-stair-bottom",60,8,13,0)
        walk(8,11);checkpoint("06-left-stair-return",60,8,11,1)
        walk(11,11)
        session.send(steps=[{"frames":24,"keys":["DOWN"]},{"frames":40}])
        checkpoint("07-cliff-blocked",60,11,11,1)
        walk(8,16)
        session.send(steps=[{"frames":2,"keys":["DOWN"]},{"frames":20},{"frames":2,"keys":["A"]},{"frames":160}])
        checkpoint("08-greeting-dialogue",60,8,16,0)
        session.send(pulse=4,keys=["B"],hold=3,gap=45)
        walk(9,16);checkpoint("09-dialogue-released",60,9,16,0)
        interior("10-west-house",(4,24),62,(4,23),"RIGHT")
        interior("11-player-house",(13,26),63,(13,25))
        walk(23,21);checkpoint("12-right-stair-bottom",60,23,21,0)
        walk(23,20);checkpoint("13-right-stair-middle",60,23,20,0.5)
        walk(23,19);checkpoint("14-right-stair-top",60,23,19,1)
        walk(23,21);checkpoint("15-right-stair-return",60,23,21,0)
        walk(24,10);checkpoint("16-fountain-and-windmills",60,24,10,1)
        interior("17-laboratory",(8,9),61,(8,8))
        walk(2,26)
        session.send(steps=[{"frames":24,"keys":["LEFT"]},{"frames":40}])
        checkpoint("18-tree-boundary-blocked",60,2,26,0)
        walk(20,29)
        session.send(steps=[{"frames":24,"keys":["DOWN"]},{"frames":40}])
        checkpoint("19-south-boundary-blocked",60,20,29,0)
        walk(27,27);checkpoint("19a-forest-entrance",60,27,27,0)
        session.send(steps=[{"frames":40,"keys":["RIGHT"]},{"frames":300}])
        checkpoint("19b-temporary-route-entry",33)
        walk(20,14);checkpoint("19c-temporary-route-walk",33,20,14)
        walk(13,14)
        session.send(steps=[{"frames":40,"keys":["LEFT"]},{"frames":300}])
        checkpoint("19d-forest-return",60)
        walk(27,27);checkpoint("19e-forest-outside",60,27,27,0)
        walk(17,27)
        session.send(steps=[{"frames":2,"keys":["UP"]},{"frames":20},{"frames":2,"keys":["A"]},{"frames":160}])
        checkpoint("20-laboratory-dialogue",60,17,27,0)
        session.send(pulse=4,keys=["B"],hold=3,gap=45)
        walk(16,27);checkpoint("21-before-save",60,16,27,0)
        session.send(tap=[124,74],frames=120,shot="22-save-prompt.png")
        session.send(steps=[{"pulse":5,"keys":["A"],"gap":90},{"frames":1600}],shot="23-save-complete.png")
        session.send(export_save="village-save.sav")
        session.close()
        battery=config/"desmume"/(rom.stem+".dsv")
        lab.require(battery.is_file() and battery.stat().st_size>=524288,"Native battery save missing")
        report["battery_sha256"]=lab.digest(battery.read_bytes())
        session=Session(rom,root/"session02-cold-load",config)
        session.boot();checkpoint("24-persistent-cold-load",60,16,27,0)
        walk(15,27);checkpoint("25-movement-after-load",60,15,27,0)
        report["completed"]=True
    except Exception as error:
        report["failure"]=str(error)
        try:session.send(shot="failure.png",field_pointer=FIELD_POINTER)
        except Exception:pass
        raise
    finally:
        session.close()
        (root/"results.json").write_text(json.dumps(report,indent=2)+"\n")


if __name__ == "__main__":main()
