#!/usr/bin/env python3
"""Verify the built ROM delta for a Hollowtide text proof; do not emulate it."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from ndspy.fnt import save as save_fnt
from ndspy.narc import NARC
from ndspy.rom import NintendoDSRom

from prepare_text_smoke_test import PROOFS


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify(baseline_path, modified_path, target, work_dir):
    baseline = NintendoDSRom.fromFile(str(baseline_path))
    modified = NintendoDSRom.fromFile(str(modified_path))
    require(save_fnt(baseline.filenames) == save_fnt(modified.filenames), "Filename table changed")
    for field in ("arm9", "arm7", "arm9OverlayTable", "arm7OverlayTable"):
        require(getattr(baseline, field) == getattr(modified, field), f"Unexpected change: {field}")
    require(len(baseline.files) == len(modified.files), "Filesystem entry count changed")
    changed_files = [i for i, (a, b) in enumerate(zip(baseline.files, modified.files)) if a != b]
    message_id = modified.filenames.idOf("a/0/2/7")
    require(changed_files == [message_id], f"Unexpected changed filesystem entries: {changed_files}")
    a, b = NARC(baseline.files[message_id]), NARC(modified.files[message_id])
    require(len(a.files) == len(b.files), "Message archive count changed")
    archive_id, entry_id, original, marker = PROOFS[target]
    changed_archives = [i for i, (x, y) in enumerate(zip(a.files, b.files)) if x != y]
    require(changed_archives == [archive_id], f"Unexpected changed message archives: {changed_archives}")
    work_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=work_dir) as directory:
        decoded = []
        for name, archive in (("baseline", a), ("modified", b)):
            binary = Path(directory) / f"{name}.bin"
            text = Path(directory) / f"{name}.txt"
            binary.write_bytes(archive.files[archive_id])
            subprocess.run(["tools/msgenc", "-d", "-c", "charmap.txt", str(binary), str(text)], check=True)
            decoded.append(text.read_bytes().splitlines())
        old, new = decoded
        require(len(old) == len(new), "Decoded message count changed")
        changed_entries = [i for i, (x, y) in enumerate(zip(old, new)) if x != y]
        require(changed_entries == [entry_id], f"Unexpected changed text entries: {changed_entries}")
        require(old[entry_id].startswith(original.encode()), "Baseline text differs from audited base")
        require(new[entry_id] == old[entry_id].replace(original.encode(), marker.encode(), 1),
                "Built replacement does not match the intended proof")
    return {
        "target": target, "baseline_sha256": digest(baseline_path),
        "modified_sha256": digest(modified_path), "modified_bytes": modified_path.stat().st_size,
        "changed_filesystem_ids": changed_files, "changed_message_members": changed_archives,
        "changed_entries": changed_entries, "arm9_arm7_overlay_tables_unchanged": True,
        "binary_delta_verified": True, "gameplay_verified_by_this_tool": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("modified", type=Path)
    parser.add_argument("--target", choices=PROOFS, default="intro")
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = verify(args.baseline, args.modified, args.target, args.work_dir)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Verification failed: {error}\n")
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
