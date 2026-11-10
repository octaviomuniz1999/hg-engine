#!/usr/bin/env python3
"""Encode only authored message replacements; never version native text dumps.

Unchanged entries, original bank keys and all non-message ROM files are checked.
Run after normal build and authored-map installation. CP05 manifests contain
English technical adaptations; the approved Portuguese is kept in documentation.
"""
import argparse
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

import map_lab as lab

MESSAGES = "a/0/2/7"
EXPECTED_COUNTS = {190:9,219:63,543:106,545:39}


def wrap_dialogue(paragraphs):
    pages = []
    for paragraph in paragraphs:
        lines = [];line = [];width = 0
        for word in re.findall(r"\{[^}]*\}[.,!?]?|\S+",paragraph):
            size = 7 if word.startswith("{STRVAR_") else 0 if word.startswith("{") else len(word)
            if line and width+1+size > 33:
                lines.append(" ".join(line));line = [];width = 0
            width += size+bool(line);line.append(word)
        if line:lines.append(" ".join(line))
        pages.extend("\\n".join(lines[i:i+2]) for i in range(0,len(lines),2))
    return "\\r".join(pages)


def apply(rom_path, manifest, output):
    from ndspy.rom import NintendoDSRom
    from ndspy.narc import NARC
    output = lab.private_new(output);report_path = lab.private_new(str(output)+".json")
    plan = json.loads(Path(manifest).read_text())
    lab.require(plan["schema"] == 1,"Unknown message manifest")
    raw = Path(rom_path).read_bytes();rom = NintendoDSRom(raw)
    lab.require(rom.idCode == b"IPKE" and rom.version == 0,"Expected owner IPKE rev.0")
    banks = NARC(rom.getFileByName(MESSAGES));changed_entries = {}
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        tmp = Path(tmp)
        for key,replacements in plan["archives"].items():
            bank = int(key);lab.require(bank in EXPECTED_COUNTS,"Unexpected message bank")
            original = banks.files[bank];binary = tmp/f"{bank}.bin";text = tmp/f"{bank}.txt"
            binary.write_bytes(original)
            subprocess.run([str(lab.ROOT/"tools/msgenc"),"-d","-c",str(lab.ROOT/"charmap.txt"),str(binary),str(text)],check=True,capture_output=True)
            before = text.read_text().splitlines();after = list(before)
            lab.require(len(before) == EXPECTED_COUNTS[bank],"Unexpected original bank size")
            for index,paragraphs in replacements.items():
                i = int(index);lab.require(0 <= i < len(before),"Message index out of bounds")
                after[i] = wrap_dialogue(paragraphs)
                # Interactive controls and variable buffers are part of the
                # event ABI. New text may not silently remove these operands.
                for control in re.findall(r"\{(?:YESNO|STRVAR_)[^}]*\}",before[i]):
                    lab.require(control in after[i],f"Missing control {control} in {bank}/{i}")
            text.write_text("\n".join(after)+"\n",encoding="utf-8")
            validation = subprocess.run([sys.executable,str(lab.ROOT/"tools/source/dumptools/validate_text_archive.py"),str(lab.ROOT/"charmap.txt"),str(text)],capture_output=True,text=True)
            lab.require(validation.returncode == 0,validation.stdout+validation.stderr)
            encoded = tmp/f"{bank}-new.bin"
            subprocess.run([str(lab.ROOT/"tools/msgenc"),"-e","-k",str(struct.unpack_from('<H',original,2)[0]),"-c",str(lab.ROOT/"charmap.txt"),str(text),str(encoded)],check=True,capture_output=True)
            decoded = tmp/f"{bank}-verify.txt"
            subprocess.run([str(lab.ROOT/"tools/msgenc"),"-d","-c",str(lab.ROOT/"charmap.txt"),str(encoded),str(decoded)],check=True,capture_output=True)
            lab.require(decoded.read_text().splitlines() == after,"Message encode/decode mismatch")
            lab.require(all(a == b for i,(a,b) in enumerate(zip(before,after)) if str(i) not in replacements),"Unrelated message changed")
            banks.files[bank] = encoded.read_bytes();changed_entries[bank] = sorted(map(int,replacements))
    rom.setFileByName(MESSAGES,banks.save());packed = rom.save();check = NintendoDSRom(packed)
    original = NintendoDSRom(raw)
    lab.require(len(original.files) == len(check.files) and
                [i for i,(a,b) in enumerate(zip(original.files,check.files)) if a != b] ==
                [original.filenames.idOf(MESSAGES)],"Unexpected filesystem delta")
    for key in ("arm9","arm7","arm9OverlayTable","arm7OverlayTable"):
        lab.require(getattr(original,key) == getattr(check,key),"Executable changed")
    old,new = NARC(original.getFileByName(MESSAGES)),NARC(check.getFileByName(MESSAGES))
    lab.require(len(old.files) == len(new.files) and all(a == b for i,(a,b) in enumerate(zip(old.files,new.files)) if i not in changed_entries),"Unrelated bank changed")
    output.write_bytes(packed)
    report = {"input_sha256":lab.digest(raw),"output_sha256":lab.digest(packed),
              "manifest_sha256":lab.digest(Path(manifest).read_bytes()),
              "changed_entries":changed_entries,"encode_decode_verified":True,
              "only_message_archive_changed":True,"emulation_validated":False}
    report_path.write_text(json.dumps(report,indent=2)+"\n");return report


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("rom",type=Path);p.add_argument("manifest",type=Path);p.add_argument("output",type=Path)
    a = p.parse_args();print(json.dumps(apply(a.rom,a.manifest,a.output),indent=2))
