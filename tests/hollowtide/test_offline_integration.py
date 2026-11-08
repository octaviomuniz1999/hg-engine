"""Synthetic contract tests: no ROM, compiler, dsrom process or emulator."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bridge = load_module("hollowtide_dsrom_bridge", "scripts/dsrom_bridge.py")
intake = load_module("hollowtide_map_intake", "tools/hollowtide/validate_map_bundle.py")


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_overlay_flags_round_trip(self):
        for size in (0, 1, 0x12345, 0xFFFFFF):
            for compressed in (False, True):
                for signed in (False, True):
                    with self.subTest(size=size, compressed=compressed, signed=signed):
                        flags = bridge.pack_flags(size, compressed, signed)
                        self.assertEqual(
                            bridge.unpack_flags(flags),
                            (size if compressed else 0, compressed, signed),
                        )

    def test_asset_tree_preserves_bytes_without_copying_metadata(self):
        source = self.root / "source"
        (source / "a/0/3").mkdir(parents=True)
        (source / "empty").mkdir()
        payload = bytes(range(256))
        (source / "a/0/3/2").write_bytes(payload)
        destination = self.root / "destination"
        with patch("shutil.copystat", side_effect=AssertionError("metadata copy")):
            bridge.copy_asset_tree(source, destination)
        self.assertEqual((destination / "a/0/3/2").read_bytes(), payload)
        self.assertEqual((source / "a/0/3/2").read_bytes(), payload)
        self.assertTrue((destination / "empty").is_dir())

    def test_asset_tree_refuses_existing_destination(self):
        source, destination = self.root / "source", self.root / "destination"
        source.mkdir()
        destination.mkdir()
        with self.assertRaises(FileExistsError):
            bridge.copy_asset_tree(source, destination)

    def test_asset_tree_rejects_symlinks(self):
        source = self.root / "source"
        source.mkdir()
        (source / "link").symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            bridge.copy_asset_tree(source, self.root / "destination")

    def make_extraction_fixture(self):
        extracted = self.root / "extracted"
        for directory in ("arm7", "arm9", "arm9_overlays", "files/a/0/3"):
            (extracted / directory).mkdir(parents=True)
        (extracted / "arm7/arm7.bin").write_bytes(b"synthetic-arm7")
        (extracted / "arm9/arm9.bin").write_bytes(b"synthetic-arm9")
        (extracted / "files/a/0/3/2").write_bytes(b"synthetic-event-archive")
        overlays = []
        for oid in (0, 1):
            entry = {
                "id": oid, "base_address": 0x02200000 + oid * 0x1000,
                "code_size": 32, "bss_size": 8, "ctor_start": 0,
                "ctor_end": 0, "file_id": 100 + oid,
                "compressed": bool(oid), "signed": bool(oid),
                "file_name": f"ov{oid:03}.bin", "dsprot": {"fixture": oid},
            }
            overlays.append(entry)
            (extracted / "arm9_overlays" / entry["file_name"]).write_bytes(bytes([oid]) * 32)
        bridge.write_yaml(extracted / "arm9_overlays/overlays.yaml", {"overlays": overlays})
        return extracted, overlays

    def extract_fixture(self, extracted):
        base = self.root / "base"
        filesys = base / "root"
        # The subprocess is mocked: no real ROM is opened or extracted.
        with self.mock_extractor(extracted) as runner:
            bridge.extract("not-executed-dsrom", "not-a-rom.nds", str(extracted), str(base), str(filesys))
        runner.assert_called_once_with(
            ["not-executed-dsrom", "extract", "-r", "not-a-rom.nds", "-o", str(extracted)], check=True
        )
        return base, filesys

    def mock_extractor(self, extracted):
        # extract() removes the previous extraction; emulate dsrom producing a
        # fresh tree from the synthetic input, including deliberately bad links.
        staged = self.root / "fixture-input"
        shutil.copytree(extracted, staged, symlinks=True)

        def fake_extract(command, check):
            shutil.copytree(staged, command[-1], symlinks=True)

        return patch.object(bridge.subprocess, "run", side_effect=fake_extract)

    def test_extract_preserves_overlay_table_and_assets(self):
        extracted, overlays = self.make_extraction_fixture()
        base, filesys = self.extract_fixture(extracted)
        self.assertEqual((base / "arm9.bin").read_bytes(), b"synthetic-arm9")
        self.assertEqual((base / "arm7.bin").read_bytes(), b"synthetic-arm7")
        self.assertEqual((filesys / "a/0/3/2").read_bytes(), b"synthetic-event-archive")
        table = (base / "overarm9.bin").read_bytes()
        self.assertEqual(len(table), 2 * bridge.OVERLAY_ENTRY_SIZE)
        for entry in overlays:
            fields = struct.unpack_from("<8I", table, entry["id"] * 32)
            self.assertEqual(fields[:7], tuple(entry[key] for key in (
                "id", "base_address", "code_size", "bss_size", "ctor_start", "ctor_end", "file_id"
            )))
            self.assertEqual(bridge.unpack_flags(fields[7]), (
                entry["code_size"] if entry["compressed"] else 0, entry["compressed"], entry["signed"]
            ))

    def test_failed_extraction_does_not_publish_arm9_marker(self):
        extracted, _ = self.make_extraction_fixture()
        (extracted / "files/link").symlink_to(self.root, target_is_directory=True)
        base = self.root / "base"
        with self.mock_extractor(extracted):
            with self.assertRaisesRegex(ValueError, "symlink"):
                bridge.extract("not-executed", "not-a-rom.nds", str(extracted), str(base), str(base / "root"))
        self.assertFalse((base / "arm9.bin").exists())

    def test_pack_keeps_changes_and_overlay_metadata(self):
        extracted, original = self.make_extraction_fixture()
        base, filesys = self.extract_fixture(extracted)
        (filesys / "a/0/3/2").write_bytes(b"edited-synthetic-event")
        (base / "overlay/overlay_0001.bin").write_bytes(b"edited-synthetic-overlay")
        with patch.object(bridge.subprocess, "run") as runner:
            bridge.pack("not-executed-dsrom", "not-a-rom.nds", str(extracted), str(base), str(filesys))
        runner.assert_called_once_with(
            ["not-executed-dsrom", "build", "-c", str(extracted / "config.yaml"), "-o", "not-a-rom.nds"],
            check=True,
        )
        self.assertEqual((extracted / "files/a/0/3/2").read_bytes(), b"edited-synthetic-event")
        self.assertEqual((extracted / "arm9_overlays/ov001.bin").read_bytes(), b"edited-synthetic-overlay")
        self.assertEqual(bridge.read_yaml(extracted / "arm9_overlays/overlays.yaml")["overlays"], original)
        self.assertFalse((self.root / "not-a-rom.nds").exists())

    def test_pack_drops_stale_dsprot_when_code_size_changes(self):
        extracted, _ = self.make_extraction_fixture()
        base, filesys = self.extract_fixture(extracted)
        table = bytearray((base / "overarm9.bin").read_bytes())
        struct.pack_into("<I", table, 8, 48)
        (base / "overarm9.bin").write_bytes(table)
        with patch.object(bridge.subprocess, "run"):
            bridge.pack("not-executed", "not-a-rom.nds", str(extracted), str(base), str(filesys))
        entries = bridge.read_yaml(extracted / "arm9_overlays/overlays.yaml")["overlays"]
        self.assertNotIn("dsprot", entries[0])
        self.assertIn("dsprot", entries[1])


class MapBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        payload = b"SYNTHETIC INTEGRITY FIXTURE - NOT A NINTENDO DS MAP"
        (self.root / "map.bin").write_bytes(payload)
        self.manifest = {
            "schema_version": 1, "map_key": "pipeline-fixture",
            "target_game": "heartgold-us",
            "exporter": {"name": "synthetic-test", "version": "1"},
            "assets": [{"path": "map.bin", "kind": "map_bin", "size": len(payload),
                        "sha256": hashlib.sha256(payload).hexdigest()}],
        }
        self.path = self.root / "manifest.json"

    def write_manifest(self, manifest=None):
        self.path.write_text(json.dumps(self.manifest if manifest is None else manifest), encoding="utf-8")

    def test_minimal_handoff_is_read_only(self):
        self.write_manifest()
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertEqual(intake.validate_bundle(self.path), 1)
        self.assertEqual({p.name: p.read_bytes() for p in self.root.iterdir()}, before)

    def test_cli_reports_its_validation_limits(self):
        self.write_manifest()
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/hollowtide/validate_map_bundle.py"), str(self.path)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NAO validados", result.stdout)

    def test_corrupt_asset_is_rejected_by_cli(self):
        self.write_manifest()
        (self.root / "map.bin").write_bytes(b"X" * self.manifest["assets"][0]["size"])
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/hollowtide/validate_map_bundle.py"), str(self.path)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("SHA-256 divergente", result.stderr)

    def test_unsafe_or_inconsistent_manifests_are_rejected(self):
        cases = [
            ("schema_version", True), ("target_game", "emerald"), ("map_key", "../map"),
            ("exporter", {}), ("assets", []),
        ]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                manifest = copy.deepcopy(self.manifest)
                manifest[field] = value
                self.write_manifest(manifest)
                with self.assertRaises(ValueError):
                    intake.validate_bundle(self.path)
        for field, value in [
            ("path", "../map.bin"), ("path", "/tmp/map.bin"), ("path", "C:\\map.bin"),
            ("path", "missing.bin"), ("path", "map.nds"), ("kind", []),
            ("kind", "unknown"), ("size", True), ("size", 0), ("size", 10000),
            ("sha256", "bad-hash"), ("sha256", "0" * 64),
        ]:
            with self.subTest(field=field, value=value):
                manifest = copy.deepcopy(self.manifest)
                manifest["assets"][0][field] = value
                self.write_manifest(manifest)
                with self.assertRaises(ValueError):
                    intake.validate_bundle(self.path)

    def test_duplicate_assets_are_rejected(self):
        self.manifest["assets"].append(copy.deepcopy(self.manifest["assets"][0]))
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "duplicado"):
            intake.validate_bundle(self.path)

    def test_symlink_assets_are_rejected(self):
        (self.root / "link.bin").symlink_to(self.root / "map.bin")
        self.manifest["assets"][0]["path"] = "link.bin"
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "simbolico"):
            intake.validate_bundle(self.path)


if __name__ == "__main__":
    unittest.main()
