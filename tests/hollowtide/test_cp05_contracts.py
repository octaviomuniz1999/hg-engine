"""CP05-only contracts: selector size and independently arranged test Pokémon.

Fixtures are synthetic; no game/save bytes are embedded here.
"""
import json
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/hollowtide"))
from apply_story_text import wrap_dialogue
from observe_party import crypt,decode_mon


class CP05Contracts(unittest.TestCase):
    def test_selector_text_never_requests_an_extra_page(self):
        manifest = json.loads((ROOT/"data/hollowtide/cp05_lab.json").read_text())
        for paragraphs in manifest["archives"]["190"].values():
            text = wrap_dialogue(paragraphs)
            self.assertNotIn("\\r",text)
            self.assertLessEqual(len(text.split("\\n")),2)

    def fixture(self):
        # Shuffle 13 maps A/B/C/D to physical 1/3/0/2. Deliberately arrange
        # C,A,D,B literally, without consulting the observer's permutation table.
        pid = 13<<13
        a,b,c,d = (bytearray(32) for _ in range(4))
        struct.pack_into('<H',a,0,545);a[13] = 65
        struct.pack_into('<4H',b,0,33,43,0,0)
        payload = c+a+d+b
        checksum = sum(struct.unpack('<64H',payload))&0xFFFF
        tail = bytearray(104);tail[4] = 5
        struct.pack_into('<2H',tail,6,20,20)
        return struct.pack('<IHH',pid,0,checksum)+crypt(payload,checksum)+crypt(tail,pid)

    def test_nontrivial_shuffle_reports_species_moves_and_level(self):
        self.assertEqual(decode_mon(self.fixture()),
                         {"species":545,"level":5,"experience":0,"ability":65,"moves":[33,43,0,0],
                          "hp":20,"max_hp":20,"checksum_valid":True})

    def test_corrupted_box_payload_is_rejected(self):
        raw = bytearray(self.fixture());raw[12] ^= 1
        with self.assertRaisesRegex(AssertionError,"checksum"):decode_mon(raw)


if __name__ == "__main__":unittest.main()
