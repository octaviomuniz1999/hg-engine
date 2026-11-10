#!/usr/bin/env python3
"""Prepare a private native-battle fixture without changing production events.

Only the owned village script 965 changes. No engine compilation or save edits.
The normal source script and final gameplay ROM remain untouched.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

import map_lab as lab


def main():
    from ndspy.rom import NintendoDSRom
    from ndspy.narc import NARC
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom",type=Path);p.add_argument("output",type=Path)
    a = p.parse_args();output = lab.private_new(a.output)
    report_path = lab.private_new(str(output)+".json")
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        tmp = Path(tmp);obj = tmp/"fixture.o";elf = tmp/"fixture.elf";binary = tmp/"fixture.bin"
        subprocess.run(["arm-none-eabi-gcc","-x","assembler-with-cpp","-mthumb","-mcpu=arm946e-s",
                        "-I"+str(lab.ROOT),"-I"+str(lab.ROOT/"include"),
                        "-c",str(Path(__file__).with_name("fixtures")/"starter_battle.s"),"-o",str(obj)],check=True)
        subprocess.run(["arm-none-eabi-ld","-T",str(lab.ROOT/"src/linker.ld"),"-o",str(elf),str(obj)],check=True)
        subprocess.run(["arm-none-eabi-objcopy","-O","binary",str(elf),str(binary)],check=True)
        fixture = binary.read_bytes()
    raw,rom,headers,_ = lab.open_rom(a.rom)
    lab.require(int.from_bytes(headers[60][6:8],'little') == 965,"Unexpected village script")
    path = "a/0/1/2";scripts = NARC(rom.getFileByName(path))
    old_script = scripts.files[965];lab.require(len(old_script) < 256,"Unexpected owned script size")
    scripts.files[965] = fixture;rom.setFileByName(path,scripts.save());packed = rom.save()
    original,check = NintendoDSRom(raw),NintendoDSRom(packed)
    lab.require(len(original.files) == len(check.files) and
                [i for i,(a,b) in enumerate(zip(original.files,check.files)) if a != b] ==
                [original.filenames.idOf(path)],"Unexpected file delta")
    before,after = NARC(original.getFileByName(path)),NARC(check.getFileByName(path))
    lab.require(len(before.files) == len(after.files) and
                all(a == b for i,(a,b) in enumerate(zip(before.files,after.files)) if i != 965),
                "Unrelated script changed")
    for key in ("arm9","arm7","arm9OverlayTable","arm7OverlayTable"):
        lab.require(getattr(original,key) == getattr(check,key),"Executable changed")
    output.write_bytes(packed)
    report = {"production_sha256":lab.digest(raw),"fixture_rom_sha256":lab.digest(packed),
              "fixture_script_sha256":lab.digest(fixture),"private_test_variant_only":True,
              "only_script_member_changed":965,"enemy_species":19,"enemy_level":2,
              "emulation_validated":False}
    report_path.write_text(json.dumps(report,indent=2)+"\n");print(json.dumps(report))


if __name__ == "__main__":main()
