#!/usr/bin/env python3
"""Record real DeSmuME input sessions and private screenshots as JSON lines.

Run with a private session directory. Battery saves use an explicit XDG config
directory; savestates are separate navigation aids, never persistence evidence.
No ROM, save, screenshot or memory dump belongs in the source repository.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("--session-dir", type=Path, required=True)
    parser.add_argument("--config-dir", type=Path, required=True)
    args = parser.parse_args()
    rom = args.rom.resolve()
    session = args.session_dir.resolve()
    config = args.config_dir.resolve()
    repository = Path(__file__).resolve().parents[2]
    if session.is_relative_to(repository) or config.is_relative_to(repository):
        parser.error("Session and config directories must be outside the source checkout")
    session.mkdir(parents=True, exist_ok=True)
    (config / "desmume").mkdir(parents=True, exist_ok=True)
    os.environ["XDG_CONFIG_HOME"] = str(config)
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    os.chdir(session)
    from desmume.controls import Keys, keymask
    from desmume.emulator import DeSmuME

    emulator = DeSmuME()
    emulator.volume_set(0)
    emulator.open(str(rom))
    frame = 0
    print("EMULATOR_READY", flush=True)

    def run(count, keys=()):
        nonlocal frame
        if not 0 <= count <= 6000:
            raise ValueError("frames must be between 0 and 6000")
        mask = 0
        for key in keys:
            mask |= keymask(getattr(Keys, "KEY_" + key.upper()))
        emulator.input.keypad_update(mask)
        for _ in range(count):
            emulator.cycle(with_joystick=False)
            frame += 1
        emulator.input.keypad_update(0)

    def local(name):
        if Path(name).name != name:
            raise ValueError("Output must be a filename in the private session directory")
        return session / name

    def field_snapshot(pointer_address):
        # Read-only diagnostics from this build's gFieldSysPtr symbol. The
        # layouts are documented in include/pokemon.h and map_events_internal.h.
        def word(address):
            return int.from_bytes(emulator.memory.unsigned[address:address + 4:1], "little")

        def valid(address):
            return 0x02000000 <= address < 0x02400000

        field = word(pointer_address)
        if not valid(field):
            return {"available": False}
        location = word(field + 0x20)
        if not valid(location):
            return {"available": False}
        result = {name: word(location + offset) for name, offset in (
            ("map_id", 0), ("warp_id", 4), ("x", 8), ("z", 12), ("direction", 16)
        )}
        result["available"] = True
        events = word(field + 0x14)
        if valid(events):
            count = word(events + 8)
            warps = word(events + 24)
            if count <= 64 and valid(warps):
                result["warps"] = []
                for i in range(count):
                    raw = bytes(emulator.memory.unsigned[warps + 12*i:warps + 12*(i+1):1])
                    result["warps"].append({name: int.from_bytes(raw[a:b], "little") for name, a, b in (
                        ("x", 0, 2), ("z", 2, 4), ("destination_header", 4, 6), ("destination_warp", 6, 8)
                    )})
        return result

    try:
        with (session / "input-events.jsonl").open("a", encoding="utf-8") as log:
            for line in sys.stdin:
                started = time.monotonic()
                command = json.loads(line)
                log.write(json.dumps({"frame_before": frame, "input": command}) + "\n")
                log.flush()
                if command.get("quit"):
                    break
                if "load_state" in command:
                    emulator.savestate.load_file(str(local(command["load_state"])))
                for step in command.get("steps", [command]):
                    if "tap" in step:
                        x, y = step["tap"]
                        if not (0 <= x < 256 and 0 <= y < 192):
                            raise ValueError("Touch coordinates are on the 256x192 bottom screen")
                        emulator.input.touch_set_pos(x, y)
                        run(3)
                        emulator.input.touch_release()
                    for _ in range(step.get("pulse", 0)):
                        run(step.get("hold", 3), step.get("keys", ["A"]))
                        run(step.get("gap", 30))
                    run(step.get("frames", 0), step.get("keys", ()))
                result = {"frame": frame, "running": emulator.is_running()}
                if "shot" in command:
                    target = local(command["shot"])
                    emulator.screenshot().save(target)
                    result["screenshot"] = str(target)
                    result["screenshot_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
                if "save_state" in command:
                    emulator.savestate.save_file(str(local(command["save_state"])))
                    result["navigation_savestate"] = command["save_state"]
                if "load_state" in command:
                    result["loaded_navigation_savestate"] = command["load_state"]
                if "export_save" in command:
                    target = local(command["export_save"])
                    result["battery_export_ok"] = emulator.backup.export_file(str(target))
                    result["battery_export_bytes"] = target.stat().st_size if target.exists() else 0
                if "read" in command:
                    result["memory"] = {}
                    for address, size in command["read"]:
                        result["memory"][hex(address)] = list(emulator.memory.unsigned[address:address+size:1])
                if "field_pointer" in command:
                    result["field"] = field_snapshot(command["field_pointer"])
                result["elapsed_seconds"] = round(time.monotonic() - started, 3)
                log.write(json.dumps({"result": result}) + "\n")
                log.flush()
                print(json.dumps(result), flush=True)
    finally:
        emulator.destroy()


if __name__ == "__main__":
    main()
