"""Synthetic binary contracts. No Nintendo assets and no emulation here."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace
import struct
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("map_lab", ROOT / "tools/hollowtide/map_lab.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def map_fixture():
    # Minimal envelopes, deliberately not a playable model or terrain.
    model = b"BMD0\xff\xfe\x00\x00" + struct.pack("<IHHI", 28, 16, 1, 20)
    model += b"MDL0" + struct.pack("<I", 8)
    return {"bgs": struct.pack("<HH", 0x1234, 0), "per": b"\x00\x06"*1024,
            "bld": b"", "nsbmd": model, "bdhc": b"BDHC" + bytes(12)}


def event_fixture():
    return {"background": [], "npcs": [struct.pack("<14Hi", *range(14), 0)],
            "warps": [struct.pack("<4Hi", 4, 14, 60, 0, 0)], "triggers": []}


class MapBinaryTests(unittest.TestCase):
    def test_sections_roundtrip_preserves_permissions_and_camera_tail(self):
        s = map_fixture()
        s["bdhc"] += b"OPAQUE-CAMERA-EXTENSION"
        raw = lab.join_map(s)
        self.assertEqual(lab.split_map(raw), s)
        self.assertEqual(lab.join_map(lab.split_map(raw)), raw)

    def test_wrong_game_or_trailing_bytes_rejected(self):
        good = lab.join_map(map_fixture())
        for bad in (good + b"extra", good[:-1], good[:16] + b"DPPT" + good[20:], good[:19]):
            with self.subTest(length=len(bad)), self.assertRaises(ValueError):
                lab.split_map(bad)

    def test_bad_sections_rejected(self):
        changes = {"per": bytes(2047), "bld": bytes(47), "nsbmd": b"BMD0",
                   "bdhc": b"BDHC" + struct.pack("<6H", 100, 0, 0, 0, 0, 0)}
        for name, value in changes.items():
            with self.subTest(section=name), self.assertRaises(ValueError):
                lab.join_map({**map_fixture(), name: value})

    def test_nsbmd_block_bounds_rejected(self):
        s = map_fixture()
        m = bytearray(s["nsbmd"])
        struct.pack_into("<I", m, 16, 999)
        with self.assertRaisesRegex(ValueError, "offset"):
            lab.join_map({**s, "nsbmd": bytes(m)})

    def test_matrix_grids_and_land_offsets(self):
        raw = bytes([2, 1, 1, 1, 1]) + b"x" + struct.pack("<2H2B2H", 61, 62, 0, 1, 244, 245)
        m = lab.parse_matrix(raw)
        self.assertEqual(m["land_ids"], [244, 245])
        self.assertEqual(m["land_offset"], 12)
        for bad in (raw[:-1], bytes([0])+raw[1:], bytes([2,1,2])+raw[3:]):
            with self.assertRaises(ValueError):
                lab.parse_matrix(bad)

    def test_event_roundtrip_and_truncation(self):
        e = event_fixture()
        raw = lab.join_events(e)
        self.assertEqual(lab.parse_events(raw), e)
        for bad in (raw[:-1], raw+b"trailing", struct.pack("<I", 0xffffffff)):
            with self.assertRaises(ValueError):
                lab.parse_events(bad)

    def test_clone_and_warp_preserve_other_records(self):
        e = event_fixture()
        original = e["npcs"][0]
        lab.edit_events(e, {"header": 61, "expected_sha256": "synthetic", "clone_npcs": [
            {"source_index": 0, "id": 8, "x": 6, "z": 12, "y_fixed": -4096}],
            "warps": [{"index": 0, "destination_header": 63, "destination_warp": 1}]})
        self.assertEqual(e["npcs"][0], original)
        n = struct.unpack("<14Hi", e["npcs"][1])
        self.assertEqual(n[0], 8)
        self.assertEqual(n[4], 0)
        self.assertEqual(n[12:], (6, 12, -4096))
        self.assertEqual(e["npcs"][1][10:24], original[10:24])
        self.assertEqual(struct.unpack("<4Hi", e["warps"][0]), (4,14,63,1,0))

    def test_duplicate_npc_and_out_of_range_edits_rejected(self):
        for npc in ({"source_index": 0, "id": 0, "x": 6, "z": 12, "y_fixed": 0},
                    {"source_index": 1, "id": 8, "x": 6, "z": 12, "y_fixed": 0},
                    {"source_index": 0, "id": 8, "x": 32, "z": 12, "y_fixed": 0}):
            with self.assertRaises(ValueError):
                lab.edit_events(event_fixture(), {"clone_npcs": [npc]})

    def test_map_texture_is_second_area_halfword(self):
        headers = [bytearray(24)]
        matrix = bytes([1,1,0,0,0]) + struct.pack("<H", 0)
        archives = {lab.MATRIX: SimpleNamespace(files=[matrix]),
                    lab.EVENTS: SimpleNamespace(files=[b""]),
                    lab.AREAS: SimpleNamespace(files=[struct.pack("<4H", 1, 2, 0, 0)]),
                    lab.TEXTURES: SimpleNamespace(files=[b"a", b"b", b"c"]),
                    lab.LAND: SimpleNamespace(files=[b"land"])}
        self.assertEqual(lab.header_info(headers, archives, 0)["texture"], 2)

    def test_outputs_refuse_checkout_existing_and_symlinks(self):
        with self.assertRaises(ValueError):
            lab.private_new(ROOT / "forbidden.nds")
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)/"proof.nds"
            p.write_bytes(b"synthetic")
            with self.assertRaises(ValueError):
                lab.private_new(p)
            link = Path(directory)/"link.nds"
            link.symlink_to(p)
            with self.assertRaises(ValueError):
                lab.private_new(link)


if __name__ == "__main__":
    unittest.main()
