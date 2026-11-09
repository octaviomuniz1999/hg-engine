#!/usr/bin/env python3
"""Private HGSS map experiment: inspect, export and apply a reviewed JSON plan.

No Makefile hook and no changes to the base ROM. Only static IPKE headers and
exclusive single-cell matrices are supported. Textures/building models/scripts
are reused, never silently converted. All derived files stay outside Git.
"""

import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
LAND = "a/0/6/5"
MATRIX = "a/0/4/1"
EVENTS = "a/0/3/2"
TEXTURES = "a/0/4/4"
AREAS = "a/0/4/2"
HEADER_OFFSET = 0xF6BE0
HEADER_COUNT = 540
SECTION_NAMES = ("bgs", "per", "bld", "nsbmd", "bdhc")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def private_new(path):
    path = Path(path)
    require(not path.is_symlink(), "Output cannot be a symlink")
    path = path.resolve()
    require(not path.is_relative_to(ROOT), "Derived output must be outside checkout")
    require(not path.exists(), "Output already exists; choose a fresh private path")
    return path


def split_map(data):
    """Validate section boundaries, not the model's artistic/runtime correctness."""
    require(len(data) >= 20, "Truncated HGSS map header")
    per, bld, model, terrain = struct.unpack_from("<4I", data)
    magic, sound_size = struct.unpack_from("<2H", data, 16)
    require(magic == 0x1234, "Missing HGSS BGS signature (wrong game/export?)")
    require(per == 2048, "Expected 32x32 permission pairs")
    require(bld % 48 == 0, "Building records must be 48 bytes")
    lengths = (sound_size + 4, per, bld, model, terrain)
    require(16 + sum(lengths) == len(data), "Section lengths do not cover file exactly")
    sections = {}
    offset = 16
    for name, size in zip(SECTION_NAMES, lengths):
        sections[name] = data[offset:offset + size]
        offset += size
    m = sections["nsbmd"]
    require(len(m) >= 20 and m[:6] == b"BMD0\xff\xfe", "Invalid NSBMD envelope")
    size, header, count = struct.unpack_from("<IHH", m, 8)
    require(size == len(m) and header == 16 and count > 0 and 16 + count*4 <= len(m),
            "Invalid NSBMD size/block table")
    for i in range(count):
        p = struct.unpack_from("<I", m, 16 + 4*i)[0]
        require(p >= 16 + 4*count and p + 8 <= len(m), "Invalid NSBMD block offset")
        n = struct.unpack_from("<I", m, p + 4)[0]
        require(n >= 8 and p + n <= len(m), "Invalid NSBMD block length")
    t = sections["bdhc"]
    require(len(t) >= 16 and t[:4] == b"BDHC", "Invalid BDHC header")
    points, slopes, heights, plates, stripes, indices = struct.unpack_from("<6H", t, 4)
    minimum = 16 + points*8 + slopes*12 + heights*4 + plates*8 + stripes*8 + indices*2
    require(minimum <= len(t), "Truncated BDHC tables")
    # Camera extensions may follow the core BDHC. Preserve rather than guess.
    return sections


def join_map(sections):
    data = struct.pack("<4I", *(len(sections[k]) for k in SECTION_NAMES[1:]))
    data += b"".join(sections[k] for k in SECTION_NAMES)
    split_map(data)
    return data


def parse_matrix(data):
    require(len(data) >= 5, "Truncated matrix")
    width, height, headers, altitude, name_len = data[:5]
    require(width > 0 and height > 0 and headers in (0, 1) and altitude in (0, 1),
            "Invalid matrix flags/dimensions")
    count = width * height
    offset = 5 + name_len
    land_offset = offset + count * (2*headers + altitude)
    require(land_offset + count*2 == len(data), "Invalid matrix size")
    return {"width": width, "height": height, "has_headers": bool(headers),
            "has_altitudes": bool(altitude), "land_offset": land_offset,
            "land_ids": list(struct.unpack_from(f"<{count}H", data, land_offset))}


def parse_events(data):
    result = {}
    offset = 0
    for name, size in (("background", 20), ("npcs", 32), ("warps", 12), ("triggers", 16)):
        require(offset + 4 <= len(data), "Truncated event count")
        count = struct.unpack_from("<I", data, offset)[0]
        offset += 4
        require(count <= (len(data) - offset)//size, "Truncated event records")
        result[name] = [data[offset + i*size:offset + (i+1)*size] for i in range(count)]
        offset += count*size
    require(offset == len(data), "Unexpected event trailing bytes")
    ids = [struct.unpack_from("<H", b)[0] for b in result["npcs"]]
    require(len(ids) == len(set(ids)), "Duplicate NPC IDs")
    return result


def join_events(events):
    data = b"".join(struct.pack("<I", len(events[k])) + b"".join(events[k])
                    for k in ("background", "npcs", "warps", "triggers"))
    parse_events(data)
    return data


def edit_events(events, edit):
    """Clone existing graphics/script; no invented script commands or SDK data."""
    require(set(edit) <= {"header", "expected_sha256", "clone_npcs", "warps"},
            "Unknown event edit field")
    for npc in edit.get("clone_npcs", []):
        require(set(npc) == {"source_index", "id", "x", "z", "y_fixed"}, "Invalid NPC edit")
        require(0 <= npc["source_index"] < len(events["npcs"]), "NPC source out of range")
        require(0 <= npc["id"] <= 65535 and 0 <= npc["x"] < 32 and 0 <= npc["z"] < 32,
                "NPC ID/coordinates out of range")
        raw = bytearray(events["npcs"][npc["source_index"]])
        struct.pack_into("<H", raw, 0, npc["id"])
        struct.pack_into("<H", raw, 8, 0)  # Visible; no story-flag allocation.
        struct.pack_into("<2H", raw, 24, npc["x"], npc["z"])
        struct.pack_into("<i", raw, 28, npc["y_fixed"])
        events["npcs"].append(bytes(raw))
    for warp in edit.get("warps", []):
        require(set(warp) == {"index", "destination_header", "destination_warp"}, "Invalid warp edit")
        require(0 <= warp["index"] < len(events["warps"]), "Warp source out of range")
        raw = bytearray(events["warps"][warp["index"]])
        struct.pack_into("<2H", raw, 4, warp["destination_header"], warp["destination_warp"])
        events["warps"][warp["index"]] = bytes(raw)
    join_events(events)


def open_rom(path):
    from ndspy.rom import NintendoDSRom
    from ndspy import codeCompression, narc
    raw = Path(path).read_bytes()
    rom = NintendoDSRom(raw)
    require(rom.idCode == b"IPKE" and rom.version == 0, "Only IPKE revision 0 is supported")
    arm9 = codeCompression.decompress(rom.arm9)
    require(arm9[0x3B268:0x3B26A] == b"\x08\xb5", "Unsupported/dynamic header patch")
    require(len(arm9) >= HEADER_OFFSET + HEADER_COUNT*24, "Header table unavailable")
    headers = [arm9[HEADER_OFFSET + i*24:HEADER_OFFSET + (i+1)*24] for i in range(HEADER_COUNT)]
    archives = {p: narc.NARC(rom.getFileByName(p)) for p in (LAND, MATRIX, EVENTS, TEXTURES, AREAS)}
    return raw, rom, headers, archives


def header_info(headers, archives, index):
    require(0 <= index < len(headers), "Header ID out of range")
    b = headers[index]
    matrix_id = struct.unpack_from("<H", b, 4)[0]
    event_id = struct.unpack_from("<H", b, 16)[0]
    require(matrix_id < len(archives[MATRIX].files) and event_id < len(archives[EVENTS].files),
            "Header resource IDs out of range")
    require(b[1] < len(archives[AREAS].files), "Area ID out of range")
    # HGSS area-data starts with building tileset, then map tileset (DSPRE).
    area = archives[AREAS].files[b[1]]
    require(len(area) >= 8, "Truncated area data")
    texture_id = struct.unpack_from("<H", area, 2)[0]
    require(texture_id < len(archives[TEXTURES].files), "Texture ID out of range")
    matrix = parse_matrix(archives[MATRIX].files[matrix_id])
    require(all(i == 65535 or i < len(archives[LAND].files) for i in matrix["land_ids"]),
            "Matrix land ID out of range")
    return {"header": index, "area": b[1], "matrix": matrix_id, "event": event_id,
            "texture": texture_id, "matrix_info": matrix,
            "matrix_users": [i for i,h in enumerate(headers) if h[4:6] == b[4:6]],
            "event_users": [i for i,h in enumerate(headers) if h[16:18] == b[16:18]]}


def inspect(path, index):
    raw, rom, headers, archives = open_rom(path)
    info = header_info(headers, archives, index)
    info["rom_sha256"] = digest(raw)
    info["texture_sha256"] = digest(archives[TEXTURES].files[info["texture"]])
    info["event_sha256"] = digest(archives[EVENTS].files[info["event"]])
    info["lands"] = []
    for i in info["matrix_info"]["land_ids"]:
        if i != 65535:
            data = archives[LAND].files[i]
            sections = split_map(data)
            info["lands"].append({"id": i, "sha256": digest(data), "sections": {
                k: {"bytes": len(v), "sha256": digest(v)} for k,v in sections.items()}})
    return info


def apply_plan(rom_path, plan_path, output):
    output = private_new(output)
    report_path = private_new(str(output) + ".json")
    plan_path = Path(plan_path).resolve()
    plan = json.loads(plan_path.read_text())
    require(set(plan) == {"schema", "rom_sha256", "header", "old_land_sha256", "map_bin",
                         "map_sha256", "texture_policy", "texture_sha256", "event_edits"},
            "Unknown/missing plan fields")
    require(plan["schema"] == 1, "Unsupported plan schema")
    raw, rom, headers, archives = open_rom(rom_path)
    require(digest(raw) == plan["rom_sha256"], "ROM hash mismatch")
    info = header_info(headers, archives, plan["header"])
    matrix = info["matrix_info"]
    require(matrix["width"] == matrix["height"] == 1 and not matrix["has_headers"],
            "Prototype requires a single-cell matrix without header grid")
    require(info["matrix_users"] == [plan["header"]], "Shared matrix; isolate explicitly before import")
    old_id = matrix["land_ids"][0]
    require(old_id != 65535, "Empty target cell")
    require(digest(archives[LAND].files[old_id]) == plan["old_land_sha256"], "Land hash mismatch")
    require(plan["texture_policy"] == "reuse-existing-area", "Texture import is not implemented")
    require(digest(archives[TEXTURES].files[info["texture"]]) == plan["texture_sha256"],
            "Area texture hash mismatch")
    asset_path = plan_path.parent / plan["map_bin"]
    require(not asset_path.is_symlink() and asset_path.resolve().is_relative_to(plan_path.parent),
            "Map BIN must be local to the plan directory")
    new_land = asset_path.read_bytes()
    require(digest(new_land) == plan["map_sha256"], "Map BIN hash mismatch")
    sections = split_map(new_land)
    new_id = len(archives[LAND].files)
    require(new_id < 65535, "Land archive ID exhausted")
    archives[LAND].files.append(new_land)
    m = bytearray(archives[MATRIX].files[info["matrix"]])
    struct.pack_into("<H", m, matrix["land_offset"], new_id)
    archives[MATRIX].files[info["matrix"]] = bytes(m)
    touched = set()
    for edit in plan["event_edits"]:
        e = header_info(headers, archives, edit["header"])
        require(e["matrix_info"]["width"] == e["matrix_info"]["height"] == 1,
                "Event edits require single-cell coordinates")
        require(e["event_users"] == [edit["header"]], "Shared event resource")
        require(e["event"] not in touched, "Duplicate event edit")
        data = archives[EVENTS].files[e["event"]]
        require(digest(data) == edit["expected_sha256"], "Event hash mismatch")
        events = parse_events(data)
        edit_events(events, edit)
        archives[EVENTS].files[e["event"]] = join_events(events)
        touched.add(e["event"])
    # Check destinations after all edits. No automatic reciprocal warp invention.
    for event_id in touched:
        for warp in parse_events(archives[EVENTS].files[event_id])["warps"]:
            destination, index = struct.unpack_from("<2H", warp, 4)
            d = header_info(headers, archives, destination)
            count = len(parse_events(archives[EVENTS].files[d["event"]])["warps"])
            require(index < count, "Destination warp out of range")
    for p in (LAND, MATRIX, EVENTS):
        rom.setFileByName(p, archives[p].save())
    packed = rom.save()
    # Verify serialized resource membership, not just in-memory edits.
    from ndspy.rom import NintendoDSRom
    from ndspy.narc import NARC
    check = NintendoDSRom(packed)
    original = NintendoDSRom(raw)
    changed = [i for i,(a,b) in enumerate(zip(original.files, check.files)) if a != b]
    allowed = {original.filenames.idOf(p) for p in (LAND, MATRIX, EVENTS)}
    require(len(original.files) == len(check.files) and set(changed) <= allowed,
            "Unexpected filesystem changes")
    require(check.arm9 == original.arm9 and check.arm7 == original.arm7 and
            check.arm9OverlayTable == original.arm9OverlayTable and
            check.arm7OverlayTable == original.arm7OverlayTable, "Executable changed")
    require(NARC(check.getFileByName(LAND)).files[new_id] == new_land, "Map bytes changed while packing")
    for p, ids in ((LAND, {new_id}), (MATRIX, {info["matrix"]}), (EVENTS, touched)):
        before, after = NARC(original.getFileByName(p)), NARC(check.getFileByName(p))
        require(all(a == after.files[i] for i,a in enumerate(before.files) if i not in ids),
                "Unrelated archive member changed")
    report = {"schema": 1, "input_sha256": digest(raw), "output_sha256": digest(packed),
              "plan_sha256": digest(plan_path.read_bytes()), "header": plan["header"],
              "old_land": old_id, "new_land": new_id, "matrix": info["matrix"],
              "event_members": sorted(touched), "changed_file_ids": changed,
              "sections": {k: digest(v) for k,v in sections.items()},
              "texture_policy": plan["texture_policy"], "emulation_validated": False}
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents overwriting a base, save or prior proof.
    with output.open("xb") as f:
        f.write(packed)
    with report_path.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("inspect")
    p.add_argument("rom", type=Path)
    p.add_argument("header", type=int)
    p = sub.add_parser("export")
    p.add_argument("rom", type=Path)
    p.add_argument("header", type=int)
    p.add_argument("output", type=Path)
    p = sub.add_parser("apply")
    p.add_argument("rom", type=Path)
    p.add_argument("plan", type=Path)
    p.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            result = inspect(args.rom, args.header)
        elif args.command == "export":
            target = private_new(args.output)
            _, _, headers, archives = open_rom(args.rom)
            info = header_info(headers, archives, args.header)
            require(len(info["matrix_info"]["land_ids"]) == 1, "Export requires one cell")
            land_id = info["matrix_info"]["land_ids"][0]
            require(land_id != 65535, "Empty cell")
            data = archives[LAND].files[land_id]
            split_map(data)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as f:
                f.write(data)
            result = {"land": land_id, "sha256": digest(data), "private_output": str(target)}
        else:
            result = apply_plan(args.rom, args.plan, args.output)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError, struct.error) as e:
        parser.exit(1, f"Map experiment refused: {e}\n")


if __name__ == "__main__":
    main()
