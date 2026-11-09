#!/usr/bin/env python3
"""Generate a private, reproducible CP03 fixture from the owner's normal build.

This is a native Elm-lab calibration, NOT an authored Hollowtide map or a PDSMS
export. Adds one blocked tile, clones an assistant and pairs two existing doors.
"""

import argparse
import json
from pathlib import Path

import map_lab as lab

NORMAL_SHA256 = "f85b23be04e265f63f961326528cb9c080bacf2be34c4dbf9c03ec4ff558ffd5"


def prepare(rom, directory):
    directory = lab.private_new(directory)
    raw, _, headers, archives = lab.open_rom(rom)
    lab.require(lab.digest(raw) == NORMAL_SHA256, "Expected validated CP01/02 normal build")
    info = lab.header_info(headers, archives, 61)
    native = archives[lab.LAND].files[info["matrix_info"]["land_ids"][0]]
    sections = lab.split_map(native)
    lab.require(lab.join_map(sections) == native, "Native map round-trip differs")
    per = bytearray(sections["per"])
    offset = 2*(11*32 + 5) + 1
    lab.require(not per[offset] & 0x80, "Calibration tile already blocked")
    per[offset] |= 0x80  # Retain all the other permission bits.
    sections["per"] = bytes(per)
    fixture = lab.join_map(sections)
    edits = []
    for header, destination in ((61, 63), (63, 61)):
        target = lab.header_info(headers, archives, header)
        edit = {"header": header,
                "expected_sha256": lab.digest(archives[lab.EVENTS].files[target["event"]]),
                "warps": [{"index": 0, "destination_header": destination, "destination_warp": 0}]}
        if header == 61:
            edit["clone_npcs"] = [{"source_index": 2, "id": 8, "x": 6, "z": 12, "y_fixed": 0}]
        edits.append(edit)
    plan = {"schema": 1, "rom_sha256": lab.digest(raw), "header": 61,
            "old_land_sha256": lab.digest(native), "map_bin": "calibration.bin",
            "map_sha256": lab.digest(fixture), "texture_policy": "reuse-existing-area",
            "texture_sha256": lab.digest(archives[lab.TEXTURES].files[info["texture"]]),
            "event_edits": edits}
    directory.mkdir(parents=True)
    (directory / "calibration.bin").write_bytes(fixture)
    (directory / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    return {"plan": str(directory / "plan.json"), "native_roundtrip_exact": True,
            "native_geometry": True, "custom_visual_map": False,
            "permission_delta": {"x": 5, "z": 11, "bit": "0x80"},
            "bdhc_preserved": True, "emulation_validated": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom", type=Path)
    p.add_argument("directory", type=Path)
    args = p.parse_args()
    try:
        print(json.dumps(prepare(args.rom, args.directory), indent=2))
    except (ValueError, OSError) as e:
        p.exit(1, f"Calibration refused: {e}\n")


if __name__ == "__main__":
    main()
