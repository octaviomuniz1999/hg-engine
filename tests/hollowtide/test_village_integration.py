"""Synthetic regressions for name binding, event ABI and protected map data."""

from pathlib import Path
from types import SimpleNamespace
import struct
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools/hollowtide"))
import integrate_village as village
import map_lab


def names(values):
    return [(v,SimpleNamespace(unk00=0,unk02=0,pixels=b"unchanged")) for v in values]


class VillageIntegrationTests(unittest.TestCase):
    def test_rebuild_resolves_prefixes_and_255_names_preserving_order_and_pixels(self):
        for values in (["a"], ["a","aa","aaa","z","za"],
                       [f"texture_{i:03d}" for i in reversed(range(255))]):
            items=names(values)
            village.rebuild_dictionary(items)
            self.assertEqual([n for n,_ in items],values)
            self.assertTrue(all(village.dictionary_lookup(items,n)==n for n in values))
            self.assertIsNone(village.dictionary_lookup(items,"not_a_resource"))
            self.assertTrue(all(v.pixels==b"unchanged" for _,v in items))

    def test_merging_old_node_links_breaks_new_names_until_rebuilt(self):
        original=names([f"base_{i:02d}" for i in range(35)])
        additions=names([f"added_{i:02d}" for i in range(5)])
        village.rebuild_dictionary(original)
        village.rebuild_dictionary(additions)
        merged=original+additions
        self.assertTrue(any(village.dictionary_lookup(merged,n)!=n for n,_ in additions))
        village.rebuild_dictionary(merged)
        self.assertTrue(all(village.dictionary_lookup(merged,n)==n for n,_ in merged))

    def test_duplicate_overlong_and_excessive_keys_refused(self):
        for values in (["duplicate","duplicate"], ["a"*17], [""], [str(i) for i in range(256)]):
            with self.assertRaises(ValueError):village.rebuild_dictionary(names(values))

    def test_resource_merge_preserves_existing_and_refuses_conflicting_pixels(self):
        a=SimpleNamespace(width=16,height=16,format=3,data1=b"a",data2=b"",isColor0Transparent=True)
        b=SimpleNamespace(**vars(a));c=SimpleNamespace(**{**vars(a),"data1":b"b"})
        target=[("native",a)]
        self.assertEqual(village.merge_named(target,[("native",b),("new",c)],"textures"),["new"])
        self.assertIs(target[0][1],a)
        with self.assertRaises(ValueError):village.merge_named(target,[("native",c)],"textures")

    def test_permission_edits_are_limited_to_doors_and_lab_approach(self):
        original=b"\x00\x04"*1024
        result,_=village.door_permissions(original)
        allowed={(x,z) for x,z,_ in village.DOORS}|{(8,9),village.VILLAGE_PORTAL}
        for z in range(32):
            for x in range(32):
                if (x,z) not in allowed:
                    p=2*(z*32+x);self.assertEqual(result[p:p+2],original[p:p+2])
        for x,z,_ in village.DOORS:
            p=2*(z*32+x);self.assertEqual(result[p:p+2],b"\x69\x80")

    def test_npc_local_scripts_use_one_based_event_abi(self):
        parsed=[struct.unpack("<14Hi",r) for r in village.village_npcs()]
        self.assertEqual([r[5] for r in parsed],[1,2])
        self.assertEqual(len({r[0] for r in parsed}),2)

    def test_interior_exit_changes_only_destination_index(self):
        e={"background":[],"npcs":[],"warps":[struct.pack("<4Hi",3,10,60,4,123)],"triggers":[]}
        raw=map_lab.join_events(e);out=village.repoint_exit(raw,2)
        self.assertEqual(struct.unpack("<4Hi",map_lab.parse_events(out)["warps"][0]),(3,10,60,2,123))
        e["warps"]=[struct.pack("<4Hi",3,10,61,0,0)]
        with self.assertRaises(ValueError):village.repoint_exit(map_lab.join_events(e),2)


if __name__ == "__main__":unittest.main()
