#!/usr/bin/env python3
"""Install the owner's CP04 village into a fresh, normal hg-engine build.

Assets, ROMs and reports are private and external to the checkout. This recipe
is pinned to the received revision; it preserves NSBMD/BLD/BDHC byte for byte.
It adds resource members, patches static headers 60/33 and connects native interiors.
Run make first: script 965 and authored messages 854 must already be compiled.
"""

import argparse
import json
from pathlib import Path
import struct

import map_lab as lab

ASSET_HASHES = {
    "teste2_00_00.bin": "f82de8cf031d17f737f45f797730e2cb8eea3dd3113e6efe74112aacf59125e8",
    "teste2_00_00.nsbmd": "bd5286aaf3027498f2ad66272fb27ecda5da968bae0e0d444ecbe0ad977c57b2",
    "teste2.pdsmap": "6c60c5e7e8ef408fbe7b4cfb525cf18307a404b768d8e6bf1a234ea3d651ca76",
}
BUILD_MODELS = "a/0/4/0"
BUILD_CONFIG = "a/0/4/3"
BUILD_TEXTURES = "a/0/7/0"
SCRIPTS = "a/0/1/2"
MESSAGES = "a/0/2/7"
SCRIPT_ID, MESSAGE_ID, EMPTY_LEVEL_ID = 965, 854, 619
ROUTE_HEADER = 33  # MAP_R29 in include/constants/maps.h, temporary test scenery.
VILLAGE_PORTAL = (28,27)
ROUTE_PORTAL = (12,14)
# The house/lab door offsets are measured from equivalent native HGSS models.
# Coordinates refer to the author's unchanged BLD transforms, not moved models.
DOORS = ((8, 8, 61), (13, 25, 63), (4, 23, 62))
EXPECTED_HEADER_60 = bytes.fromhex("00020f0000004a0367021e02fa03fa0339007e02000108f6")


def info_dictionary(data, offset):
    """Read the fixed 4-byte-entry Nitro dictionaries used by MDL0."""
    lab.require(offset + 12 <= len(data), "Truncated Nitro dictionary")
    count = data[offset + 1]
    entries_at = offset + 4 + 8 + count*4
    lab.require(entries_at + 4 <= len(data), "Truncated Nitro entry header")
    unit, _ = struct.unpack_from("<2H", data, entries_at)
    lab.require(unit == 4, "Unsupported Nitro dictionary entry width")
    entries_at += 4
    names_at = entries_at + count*4
    end = names_at + count*16
    lab.require(end <= len(data), "Truncated Nitro dictionary names")
    entries = []
    for i in range(count):
        name = data[names_at+i*16:names_at+(i+1)*16].split(b"\0")[0].decode("ascii")
        entries.append((name, data[entries_at+i*4:entries_at+(i+1)*4]))
    return entries, end


def model_bindings(mdl):
    lab.require(mdl[:4] == b"MDL0", "Invalid model block")
    models, _ = info_dictionary(mdl, 8)
    result = []
    for name, raw in models:
        offset = struct.unpack("<I", raw)[0]
        lab.require(offset + 20 <= len(mdl), "Model offset out of bounds")
        material = offset + struct.unpack_from("<I", mdl, offset+8)[0]
        mats, end = info_dictionary(mdl, material+4)
        textures, end = info_dictionary(mdl, end)
        palettes, _ = info_dictionary(mdl, end)
        result.append({"model": name, "materials": [n for n,_ in mats],
                       "textures": [n for n,_ in textures],
                       "palettes": [n for n,_ in palettes]})
    return result


def merge_named(destination, additions, kind):
    """Keep existing ordering/bytes and reject ambiguous resource-name reuse."""
    known = dict(destination)
    lab.require(len(known) == len(destination), "Duplicate resource name")
    added = []
    for name, value in additions:
        if name not in known:
            destination.append((name, value))
            known[name] = value
            added.append(name)
        else:
            before = known[name]
            if kind == "textures":
                fields = ("width", "height", "format", "data1", "data2", "isColor0Transparent")
                same = all(getattr(before, k) == getattr(value, k) for k in fields)
            else:
                same = before.colors == value.colors
            lab.require(same, f"Conflicting {kind} binding: {name}")
    return added


def dictionary_lookup(items, name):
    """Mirror Nitro's descending-bit Patricia lookup, including final key check."""
    key = name.encode("ascii").ljust(16,b"\0")
    lab.require(len(key) == 16, "Nitro names are at most 16 ASCII bytes")
    if not items:
        return None
    nodes = [(127,1,0,0)] + [struct.unpack("<4B",struct.pack("<2H",o.unk00,o.unk02)) for _,o in items]
    parent, child = 0, 1
    for _ in range(len(nodes)+1):
        if child >= len(nodes):
            return None
        bit,left,right,index = nodes[child]
        if nodes[parent][0] <= bit:
            if index < len(items) and items[index][0].encode("ascii").ljust(16,b"\0") == key:
                return items[index][0]
            return None
        parent = child
        child = right if key[bit//8] >> (bit%8) & 1 else left
    raise ValueError("Cyclic Nitro dictionary")


def rebuild_dictionary(items):
    """Rebuild node links after merging; texture/palette pixels stay exact.

    ndspy preserves each entry's old unk00/unk02 bytes when saving. Those bytes
    are Patricia links into the OLD dictionary, not portable entry flags.
    Reusing them made the five appended building textures unresolvable.
    """
    lab.require(len(items) <= 255, "Nitro dictionary entry limit exceeded")
    keys = [name.encode("ascii").ljust(16,b"\0") for name,_ in items]
    lab.require(len(set(keys)) == len(keys) and all(len(k)==16 and any(k) for k in keys),
                "Invalid/duplicate Nitro names")
    if not items:
        return
    nodes = [[127,0,0,0]]

    def bit(key, index):
        return key[index//8] >> (index%8) & 1

    for entry,key in enumerate(keys):
        parent, child = 0, nodes[0][1]
        while nodes[parent][0] > nodes[child][0]:
            parent = child
            child = nodes[child][2 if bit(key,nodes[child][0]) else 1]
        previous = keys[nodes[child][3]] if child else bytes(16)
        differences = [i*8+j for i,(a,b) in enumerate(zip(key,previous)) for j in range(8) if (a^b)>>j&1]
        lab.require(differences, "Duplicate Patricia key")
        branch = max(differences)
        parent, child = 0, nodes[0][1]
        while nodes[parent][0] > nodes[child][0] and nodes[child][0] > branch:
            parent = child
            child = nodes[child][2 if bit(key,nodes[child][0]) else 1]
        index = len(nodes)
        node = [branch,child,child,entry]
        node[2 if bit(key,branch) else 1] = index
        nodes.append(node)
        nodes[parent][2 if bit(key,nodes[parent][0]) else 1] = index
    # The fixed ndspy save header emits root.left=1. Renumber the finished
    # tree to that root child while preserving resource-name/data ordering.
    order = [0,nodes[0][1]] + [i for i in range(1,len(nodes)) if i != nodes[0][1]]
    indices = {old:new for new,old in enumerate(order)}
    reordered = [[b,indices[l],indices[r],e] for b,l,r,e in (nodes[i] for i in order)]
    for (_,obj),(b,l,r,e) in zip(items,reordered[1:]):
        obj.unk00 = b | l<<8
        obj.unk02 = r | e<<8
    lab.require(all(dictionary_lookup(items,name)==name for name,_ in items), "Rebuilt Nitro lookup failed")


def village_npcs():
    # Field-event script numbers are one-based; zero is not the first scrdef.
    return [struct.pack("<14Hi",i,g,0,0,0,i+1,1,0,0,0,0,0,x,z,0)
            for i,g,x,z in ((0,148,8,17),(1,325,17,26))]


def door_permissions(original):
    per = bytearray(original)
    lab.require(len(per) == 2048, "Invalid permission grid")
    edits = []
    for x,z,_ in DOORS:
        offset = 2*(z*32+x)
        # HGSS exterior north-facing doors use 69/80 (checked against the
        # owner's native New Bark lab/house). Interior exit 65/00 is different.
        edits.append({"x": x, "z": z, "before": per[offset:offset+2].hex(), "after": "6980"})
        per[offset:offset+2] = b"\x69\x80"
    # PDSMS' supplied footprint covers the lab's front approach as well.
    offset = 2*(9*32+8)
    edits.append({"x": 8, "z": 9, "before": per[offset:offset+2].hex(), "after": "0000"})
    per[offset:offset+2] = b"\0\0"
    # The author approved an exit in this corner. The forest-entrance mesh
    # already has an opening here, so no geometry/tree removal is necessary.
    x,z=VILLAGE_PORTAL;offset=2*(z*32+x)
    edits.append({"x":x,"z":z,"before":per[offset:offset+2].hex(),"after":"6c00"})
    per[offset:offset+2]=b"\x6c\x00"  # TILE_BEHAVIOR_WARP_EAST
    return bytes(per), edits


def route_sample(headers,archives):
    """Clone one native Route 29 cell; no authored Route 01 is claimed."""
    info=lab.header_info(headers,archives,ROUTE_HEADER)
    matrix=archives[lab.MATRIX].files[info["matrix"]]
    width,height,has_headers,has_altitudes,name_len=matrix[:5]
    x,z=20,12
    lab.require(has_headers and x<width and z<height,"Unsupported native route matrix")
    cell=z*width+x;offset=5+name_len
    lab.require(struct.unpack_from("<H",matrix,offset+2*cell)[0]==ROUTE_HEADER,"Native route cell changed")
    altitude=matrix[offset+2*width*height+cell] if has_altitudes else 0
    land_id=info["matrix_info"]["land_ids"][cell]
    sections=lab.split_map(archives[lab.LAND].files[land_id])
    per=bytearray(sections["per"])
    for row in range(32):
        for col in range(32):
            if row in (0,31) or col in (0,31):per[2*(row*32+col)+1]|=0x80
    x,z=ROUTE_PORTAL;offset=2*(z*32+x)
    lab.require(not per[offset+1]&0x80,"Native return portal is blocked")
    # HGSS directional exits are checked while standing on the warp and
    # pressing against a blocked facing tile (field_control.c), not mid-path.
    lab.require(per[2*(z*32+x-1)+1]&0x80,"West return portal requires a blocked western neighbor")
    per[offset:offset+2]=b"\x6d\x00"  # Match native warp's movement attributes, not grass/ground flags.
    sections["per"]=bytes(per)
    return sections,altitude,land_id


def repoint_exit(data, index):
    events = lab.parse_events(data)
    lab.require(events["warps"], "Native interior has no exit")
    warp = bytearray(events["warps"][0])
    lab.require(struct.unpack_from("<H", warp, 4)[0] == 60, "Unexpected native exit target")
    struct.pack_into("<2H", warp, 4, 60, index)
    events["warps"][0] = bytes(warp)
    return lab.join_events(events)


def patch_header(rom, index, new_header):
    """Recompress without relocating ARM9; account for the size marker explicitly."""
    from ndspy import code, codeCompression
    original = bytes(codeCompression.decompress(rom.arm9))
    modified = bytearray(original)
    start = lab.HEADER_OFFSET + index*24
    lab.require(len(new_header) == 24 and start+24 <= len(modified), "Invalid header patch")
    modified[start:start+24] = new_header
    cso = code.MainCodeFile(rom.arm9, rom.arm9RamAddress).codeSettingsOffs
    lab.require(cso is not None and cso+24 < 0x4000, "Unsupported compression size marker")
    packed = bytearray(codeCompression.compress(modified, True))
    struct.pack_into("<I", packed, cso+20, rom.arm9RamAddress+len(packed))
    check = codeCompression.decompress(packed)
    differences = [i for i,(a,b) in enumerate(zip(original,check)) if a != b]
    allowed = set(range(start,start+24)) | set(range(cso+20,cso+24))
    lab.require(len(check) == len(original) and set(differences) <= allowed,
                "ARM9 changed beyond header and compression marker")
    rom.arm9 = bytes(packed)
    return {"header": index, "table_offset": start, "code_settings_offset": cso,
            "changed_decompressed_offsets": differences, "executable_instructions_preserved": True}


def install(rom_path, asset_dir, output):
    from ndspy import model, texture, narc
    from ndspy.rom import NintendoDSRom
    output = lab.private_new(output)
    report_path = lab.private_new(str(output)+".json")
    assets = Path(asset_dir).resolve()
    for name, expected in ASSET_HASHES.items():
        p = assets/name
        lab.require(not p.is_symlink() and p.is_file(), f"Missing regular input: {name}")
        lab.require(lab.digest(p.read_bytes()) == expected, f"Asset revision mismatch: {name}")
    raw, rom, headers, archives = lab.open_rom(rom_path)
    original = NintendoDSRom(raw)
    lab.require(headers[60] == EXPECTED_HEADER_60, "Unexpected base header 60")
    for p in (BUILD_MODELS, BUILD_CONFIG, BUILD_TEXTURES, SCRIPTS, MESSAGES):
        archives[p] = narc.NARC(rom.getFileByName(p))
    lab.require(len(archives[SCRIPTS].files) > SCRIPT_ID and len(archives[MESSAGES].files) > MESSAGE_ID,
                "Compile authored script 965/messages 854 with normal make before integration")
    lab.require(archives[SCRIPTS].files[EMPTY_LEVEL_ID] == bytes(4), "Unexpected empty level script")
    supplied = (assets/"teste2_00_00.bin").read_bytes()
    sections = lab.split_map(supplied)
    visual_before = {k: bytes(sections[k]) for k in ("nsbmd", "bld", "bdhc", "bgs")}
    full = model.NSBMD((assets/"teste2_00_00.nsbmd").read_bytes())
    lab.require(model.NSBMD(sections["nsbmd"])._MDL0 == full._MDL0,
                "Embedded-texture model geometry differs from supplied BIN")
    bindings = model_bindings(full._MDL0)
    map_texture = full.exportNSBTX()
    for entry in bindings:
        lab.require(set(entry["textures"]) <= set(dict(map_texture.textures)), "Missing map texture")
        lab.require(set(entry["palettes"]) <= set(dict(map_texture.palettes)), "Missing map palette")
    map_tex_id = len(archives[lab.TEXTURES].files)
    archives[lab.TEXTURES].files.append(map_texture.save())
    building_ids = sorted({struct.unpack_from("<I", sections["bld"],i)[0]
                           for i in range(0,len(sections["bld"]),48)})
    lab.require(building_ids == [20,21,27,53,239,332], "Unexpected building revision")
    building_texture = texture.NSBTX(archives[BUILD_TEXTURES].files[0])
    resources_added = {"textures": [], "palettes": []}
    building_bindings = []
    for bid in building_ids:
        bm = model.NSBMD(archives[BUILD_MODELS].files[bid])
        building_bindings.extend({"building": bid, **entry} for entry in model_bindings(bm._MDL0))
        for attr in ("textures", "palettes"):
            resources_added[attr].extend(merge_named(getattr(building_texture,attr), getattr(bm,attr), attr))
    for entry in building_bindings:
        lab.require(set(entry["textures"]) <= set(dict(building_texture.textures)), "Missing building texture")
        lab.require(set(entry["palettes"]) <= set(dict(building_texture.palettes)), "Missing building palette")
    for attr in ("textures","palettes"):
        rebuild_dictionary(getattr(building_texture,attr))
    building_id = len(archives[BUILD_TEXTURES].files)
    lab.require(building_id == len(archives[BUILD_CONFIG].files), "Building archive indices differ")
    archives[BUILD_TEXTURES].files.append(building_texture.save())
    old = archives[BUILD_CONFIG].files[0]
    count = struct.unpack_from("<H", old)[0]
    lab.require(len(old) == 2+2*count, "Invalid native building config")
    ids = list(struct.unpack_from(f"<{count}H",old,2))
    ids.extend(i for i in building_ids if i not in ids)
    archives[BUILD_CONFIG].files.append(struct.pack("<H",len(ids))+struct.pack(f"<{len(ids)}H",*ids))
    area_id = len(archives[lab.AREAS].files)
    lab.require(area_id < 256, "Static header area byte exhausted")
    area = bytearray(archives[lab.AREAS].files[2])
    struct.pack_into("<2H",area,0,building_id,map_tex_id)
    archives[lab.AREAS].files.append(area)
    sections["per"], per_edits = door_permissions(sections["per"])
    land_id = len(archives[lab.LAND].files)
    archives[lab.LAND].files.append(lab.join_map(sections))
    matrix_id = len(archives[lab.MATRIX].files)
    archives[lab.MATRIX].files.append(bytes([1,1,0,0,0])+struct.pack("<H",land_id))
    npcs = village_npcs()
    events = {"background": [], "npcs": npcs,
              "warps": [struct.pack("<4Hi",x,z,d,0,0) for x,z,d in DOORS]+
                       [struct.pack("<4Hi",*VILLAGE_PORTAL,ROUTE_HEADER,0,0)], "triggers": []}
    event_id = len(archives[lab.EVENTS].files)
    archives[lab.EVENTS].files.append(lab.join_events(events))
    sample,altitude,source_land=route_sample(headers,archives)
    route_land=len(archives[lab.LAND].files)
    archives[lab.LAND].files.append(lab.join_map(sample))
    route_matrix=len(archives[lab.MATRIX].files)
    archives[lab.MATRIX].files.append(bytes([1,1,0,1,0,altitude])+struct.pack("<H",route_land))
    route_events={"background":[],"npcs":[],"triggers":[],
                  "warps":[struct.pack("<4Hi",*ROUTE_PORTAL,60,3,0)]}
    route_event=len(archives[lab.EVENTS].files)
    archives[lab.EVENTS].files.append(lab.join_events(route_events))
    event_edits = {}
    for index,(_,_,interior) in enumerate(DOORS):
        info = lab.header_info(headers,archives,interior)
        lab.require(info["event_users"] == [interior], "Interior event resource is shared")
        eid = info["event"]
        archives[lab.EVENTS].files[eid] = repoint_exit(archives[lab.EVENTS].files[eid],index)
        event_edits[eid] = {"interior": interior, "village_warp": index}
    header = bytearray(headers[60])
    header[1] = area_id
    for offset,value in ((4,matrix_id),(6,SCRIPT_ID),(8,EMPTY_LEVEL_ID),(10,MESSAGE_ID),(16,event_id)):
        struct.pack_into("<H",header,offset,value)
    arm9_audit = [patch_header(rom,60,header)]
    header=bytearray(headers[ROUTE_HEADER]);header[0]=0xFF  # No random encounters in this technical fixture.
    for offset,value in ((4,route_matrix),(6,SCRIPT_ID),(8,EMPTY_LEVEL_ID),(10,MESSAGE_ID),(16,route_event)):
        struct.pack_into("<H",header,offset,value)
    arm9_audit.append(patch_header(rom,ROUTE_HEADER,header))
    modified = {lab.LAND:{land_id,route_land}, lab.MATRIX:{matrix_id,route_matrix}, lab.AREAS:{area_id},
                lab.TEXTURES:{map_tex_id}, BUILD_CONFIG:{building_id}, BUILD_TEXTURES:{building_id},
                lab.EVENTS:set(event_edits)|{event_id,route_event}}
    for p in modified:
        rom.setFileByName(p,archives[p].save())
    packed = rom.save()
    check = NintendoDSRom(packed)
    changed = {i for i,(a,b) in enumerate(zip(original.files,check.files)) if a != b}
    lab.require(len(original.files) == len(check.files) and
                changed == {original.filenames.idOf(p) for p in modified}, "Unexpected filesystem delta")
    lab.require(check.arm7 == original.arm7 and check.arm9OverlayTable == original.arm9OverlayTable and
                check.arm7OverlayTable == original.arm7OverlayTable, "Unrelated executable changed")
    for p, allowed in modified.items():
        before,after = narc.NARC(original.getFileByName(p)), narc.NARC(check.getFileByName(p))
        added=sum(i>=len(before.files) for i in allowed)
        lab.require(len(after.files) == len(before.files)+added, "Unexpected archive expansion")
        lab.require(all(a == after.files[i] for i,a in enumerate(before.files) if i not in allowed),
                    "Unrelated member changed")
    installed = lab.split_map(narc.NARC(check.getFileByName(lab.LAND)).files[land_id])
    lab.require(all(installed[k] == v for k,v in visual_before.items()), "Protected visual/terrain section changed")
    serialized_textures = texture.NSBTX(narc.NARC(check.getFileByName(BUILD_TEXTURES)).files[building_id])
    for attr in ("textures","palettes"):
        entries = getattr(serialized_textures,attr)
        lab.require(all(dictionary_lookup(entries,name)==name for name,_ in entries),
                    "Serialized texture dictionary cannot resolve all resources")
    report = {"schema":1, "input_sha256":lab.digest(raw), "output_sha256":lab.digest(packed),
              "output_bytes":len(packed), "asset_hashes":ASSET_HASHES, "header":60,
              "land":land_id,"matrix":matrix_id,"area":area_id,"map_texture":map_tex_id,
              "building_bundle":building_id,"event":event_id,"script":SCRIPT_ID,"messages":MESSAGE_ID,
              "route_sample":{"header":ROUTE_HEADER,"source_land":source_land,"land":route_land,
                              "matrix":route_matrix,"event":route_event,"altitude":altitude,
                              "temporary_native_scenery":True,"authored_route_01":False,
                              "village_portal":VILLAGE_PORTAL,"return_portal":ROUTE_PORTAL},
              "door_permissions":per_edits,"interior_exit_edits":event_edits,"arm9":arm9_audit,
              "map_bindings":bindings,"building_bindings":building_bindings,
              "building_resources_added":resources_added,"changed_file_ids":sorted(changed),
              "serialized_nitro_dictionaries_valid":True,
              "protected_sections":{k:lab.digest(v) for k,v in visual_before.items()},
              "geometry_buildings_decoration_and_bdhc_exact":True,"emulation_validated":False}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("xb") as f:f.write(packed)
    with report_path.open("x") as f:json.dump(report,f,indent=2);f.write("\n")
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom",type=Path)
    p.add_argument("assets",type=Path)
    p.add_argument("output",type=Path)
    args=p.parse_args()
    try:
        r=install(args.rom,args.assets,args.output)
        print(json.dumps({k:v for k,v in r.items() if k not in ("map_bindings","building_bindings")},indent=2))
    except (ValueError,OSError,KeyError,struct.error) as e:
        p.exit(1,f"Village integration refused: {e}\n")


if __name__ == "__main__":
    main()
