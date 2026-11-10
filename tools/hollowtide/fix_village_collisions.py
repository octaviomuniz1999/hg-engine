#!/usr/bin/env python3
"""Apply CP05's reviewed solid-object permissions without changing authored art.

Input/output ROMs and the owner's original map stay private. This is a separate
post-build step so the CP04 installation recipe remains reproducible unchanged.
"""
import argparse
import json
from pathlib import Path

import map_lab as lab
import integrate_village as village

# Fountain basin and the two northern flagpole bases, measured against BLD
# anchors and confirmed by keyboard walking into these objects in DeSmuME.
SOLID_TILES = frozenset({(x,z) for x in range(23,26) for z in range(6,9)} |
                        {(21,5),(27,5)})


def solid_permissions(original):
    lab.require(len(original) == 2048, "Invalid permission grid")
    result = bytearray(original)
    edits = []
    for x,z in sorted(SOLID_TILES):
        i = 2*(32*z+x)
        before = bytes(result[i:i+2])
        result[i+1] |= 0x80
        if before != result[i:i+2]:
            edits.append({"x":x,"z":z,"before":before.hex(),"after":result[i:i+2].hex()})
    return bytes(result), edits


def apply(rom_path, assets, output):
    from ndspy.narc import NARC
    from ndspy.rom import NintendoDSRom
    output = lab.private_new(output)
    report_path = lab.private_new(str(output)+".json")
    supplied = Path(assets)/"teste2_00_00.bin"
    lab.require(lab.digest(supplied.read_bytes()) == village.ASSET_HASHES[supplied.name],
                "Unrecognized authored map revision")
    reference = lab.split_map(supplied.read_bytes())
    raw, rom, headers, archives = lab.open_rom(rom_path)
    info = lab.header_info(headers,archives,60)
    lab.require(info["matrix_info"]["land_ids"] == [676], "Expected isolated CP04 village")
    archive = archives[lab.LAND]
    sections = lab.split_map(archive.files[676])
    for key in ("bgs","bld","nsbmd","bdhc"):
        lab.require(sections[key] == reference[key], "Protected authored section differs: "+key)
    sections["per"], edits = solid_permissions(sections["per"])
    lab.require(edits, "No permission changes needed")
    archive.files[676] = lab.join_map(sections)
    rom.setFileByName(lab.LAND,archive.save())
    packed = rom.save()
    original, check = NintendoDSRom(raw), NintendoDSRom(packed)
    changed = [i for i,(a,b) in enumerate(zip(original.files,check.files)) if a != b]
    lab.require(len(original.files) == len(check.files) and
                changed == [original.filenames.idOf(lab.LAND)], "Unexpected filesystem delta")
    for key in ("arm9","arm7","arm9OverlayTable","arm7OverlayTable"):
        lab.require(getattr(original,key) == getattr(check,key), "Executable changed: "+key)
    before, after = NARC(original.getFileByName(lab.LAND)),NARC(check.getFileByName(lab.LAND))
    lab.require(len(before.files) == len(after.files) and
                all(a == b for i,(a,b) in enumerate(zip(before.files,after.files)) if i != 676),
                "Unrelated map changed")
    lab.require(after.files[676] == lab.join_map(sections), "Map serialization mismatch")
    report = {"input_sha256":lab.digest(raw),"output_sha256":lab.digest(packed),
              "edits":edits,"protected_visual_sections_exact":True,
              "only_land_member_changed":676,"emulation_validated":False}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(packed)
    report_path.write_text(json.dumps(report,indent=2)+"\n")
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom",type=Path);p.add_argument("assets",type=Path);p.add_argument("output",type=Path)
    a = p.parse_args()
    print(json.dumps(apply(a.rom,a.assets,a.output),indent=2))
