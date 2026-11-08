#!/usr/bin/env python3
"""Generate a private, reversible text proof from the owner's HeartGold ROM.

The generated archive contains base-game text and must not be committed.
Run from the repository root, then use the ordinary hg-engine Makefile.
"""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

from ndspy.narc import NARC
from ndspy.rom import NintendoDSRom


PROOFS = {
    "menu": (442, 1, "NEW GAME", "TEST RUN"),
    "intro": (219, 7, "I will first tell you important\\nthings about this game.",
              "Hollowtide build test.\\nTechnical preview."),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, default=Path("rom.nds"))
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--target", choices=PROOFS, default="intro")
    args = parser.parse_args()
    archive_id, entry_id, original, marker = PROOFS[args.target]
    output = Path(f"data/text/custom/{archive_id:03}.txt")
    if output.exists():
        parser.error(f"Refusing to overwrite existing text: {output}")
    if not Path("tools/msgenc").is_file():
        parser.error("Run from the configured hg-engine root")
    with args.rom.open("rb") as stream:
        stream.seek(12)
        if stream.read(4) != b"IPKE":
            parser.error("Expected the owner's compatible HeartGold USA base (IPKE)")
    rom = NintendoDSRom.fromFile(str(args.rom))
    messages = NARC(rom.getFileByName("a/0/2/7"))
    args.work_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.work_dir) as directory:
        binary = Path(directory) / "menu.bin"
        text = Path(directory) / "menu.txt"
        binary.write_bytes(messages.files[archive_id])
        subprocess.run(["tools/msgenc", "-d", "-c", "charmap.txt", str(binary), str(text)], check=True)
        raw = text.read_bytes()
        lines = raw.splitlines(keepends=True)
        if len(lines) <= entry_id or not lines[entry_id].startswith(original.encode()):
            parser.error(f"Archive {archive_id} entry {entry_id} differs from the audited base; no file was generated")
        lines[entry_id] = lines[entry_id].replace(original.encode(), marker.encode(), 1)
        modified = b"".join(lines)
        if modified == raw:
            parser.error("No replacement was made")
        # Validate all characters/control codes before publishing a build input.
        text.write_bytes(modified)
        subprocess.run([
            sys.executable, "tools/source/dumptools/validate_text_archive.py", "charmap.txt", str(text)
        ], check=True)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(modified)
    print(f"Generated {output}: archive {archive_id}, entry {entry_id}: {original!r} -> {marker!r}")
    print("This is a technical marker, not final Hollowtide narrative.")
    print("Rebuild normally. To revert, archive/remove this generated file, invalidate")
    print("the extraction/build caches, and rebuild from the owner's original base.")


if __name__ == "__main__":
    main()
