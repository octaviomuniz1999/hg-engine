#!/usr/bin/env python3
"""Run the original battle runner with read-only telemetry and screenshots.

The private work directory must contain test.nds, an owner's battery test.sav,
build/battle_tests/test_manifest.json and include/constants/generated/test_battle.h.
Execution hooks observe actual ARM9 arguments; they do not change game memory.
The original runner alone controls its documented test communication mailbox.
"""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys


def symbol(path, name):
    lines = subprocess.check_output(["arm-none-eabi-nm", str(path)], text=True).splitlines()
    for line in lines:
        fields = line.split()
        if len(fields) == 3 and fields[2] == name:
            return int(fields[0], 16) & ~1
    raise ValueError(f"Missing symbol: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--config-dir", type=Path, required=True)
    parser.add_argument("--symbols", type=Path, required=True)
    parser.add_argument("--layout", type=Path, required=True)
    parser.add_argument("--case-index", type=int,
                        help="Run one manifest entry in a fresh emulator process")
    parser.add_argument("--verify-return", action="store_true",
                        help="After the last result, check overworld movement using normal keypad input")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    work = args.work_dir.resolve()
    config = args.config_dir.resolve()
    if work.is_relative_to(root) or config.is_relative_to(root):
        parser.error("Private work/config directories must be outside the source checkout")
    manifest = json.loads((work / "build/battle_tests/test_manifest.json").read_text())
    total = manifest["total_tests"]
    if args.case_index is not None:
        if not 0 <= args.case_index < total:
            parser.error("case-index is outside this manifest")
        os.environ["TEST_RUNNER_PARTITION_COUNT"] = str(total)
        os.environ["TEST_RUNNER_PARTITION_INDEX"] = str(args.case_index)
    elif total > 1 and int(os.environ.get("TEST_RUNNER_PARTITION_COUNT", "1")) == 1:
        parser.error("Use --case-index to isolate each scenario; a native victory does not advance the scripted-flee scheduler")
    layout = json.loads(args.layout.read_text())
    context_address = symbol(args.symbols.resolve(), "BattleContext_Main")
    outcome_address = symbol(args.symbols.resolve(), "BattleSystem_SetBattleOutcomeFlags")
    field_pointer_address = symbol(args.symbols.resolve(), "gFieldSysPtr")
    (config / "desmume").mkdir(parents=True, exist_ok=True)
    (work / "screens").mkdir(exist_ok=True)
    os.environ["XDG_CONFIG_HOME"] = str(config)
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    os.environ["TEST_RUNNER_RESULT_FILE"] = str(work / "results.json")
    spec = importlib.util.spec_from_file_location("hollowtide_original_runner", root / "scripts/run_tests.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    original_emulator = runner.DeSmuME
    telemetry = (work / "battle-telemetry.jsonl").open("w", buffering=1)

    class ObservedEmulator(original_emulator):
        def __init__(self):
            super().__init__()
            self.volume_set(0)
            self.frame = 0
            self.last_sample = None
            self.pending_shot = None
            self.checked_return = False

            def emit(kind, data):
                telemetry.write(json.dumps({"kind": kind, "frame": self.frame,
                                           "test_index": runner.current_test_case,
                                           "global_test_index": runner.TEST_START_INDEX + runner.current_test_case,
                                           **data}) + "\n")

            def observe_context(address, size):
                if self.frame % 30:
                    return
                context = self.memory.register_arm9.r1
                if not 0x02000000 <= context < 0x02400000:
                    return
                def integer(address, size):
                    return int.from_bytes(self.memory.unsigned[address:address + size:1], "little")
                mons = []
                for slot in range(2):
                    mon = context + layout["battlemon_offset"] + slot * layout["pokemon_size"]
                    mons.append({
                        "slot": slot, "species": integer(mon + layout["species_offset"], 2),
                        "form": integer(mon + layout["form_offset"], 1) & 31,
                        "ability": integer(mon + layout["ability_offset"], 2),
                        "item": integer(mon + layout["item_offset"], 2),
                        "hp": integer(mon + layout["hp_offset"], 4),
                    })
                data = {"pokemon": mons, "field_condition": integer(context + layout["field_condition_offset"], 4)}
                sample = (runner.current_test_case, json.dumps(data, sort_keys=True))
                if sample != self.last_sample:
                    emit("battle_state", data)
                    if any(mon["form"] == 1 for mon in mons):
                        self.pending_shot = self.frame + 60
                    self.last_sample = sample

            def observe_outcome(address, size):
                emit("native_outcome", {"value": self.memory.register_arm9.r1 & 0xFF})

            self.memory.register_exec(context_address, observe_context)
            self.memory.register_exec(outcome_address, observe_outcome)

        def cycle(self, with_joystick=True):
            self.frame += 1
            super().cycle(with_joystick)
            if self.frame % 600 == 0 or self.pending_shot == self.frame:
                path = work / "screens" / f"case-{runner.current_test_case:02}-frame-{self.frame:06}.png"
                self.screenshot().save(path)
                telemetry.write(json.dumps({"kind": "screenshot", "frame": self.frame,
                                            "test_index": runner.current_test_case, "path": str(path)}) + "\n")

        def destroy(self):
            if args.verify_return and not self.checked_return and runner.has_finished_testing():
                self.checked_return = True
                for _ in range(360):
                    self.cycle(False)
                def word(address):
                    return int.from_bytes(self.memory.unsigned[address:address + 4:1], "little")
                def position():
                    field = word(field_pointer_address)
                    if not 0x02000000 <= field < 0x02400000:
                        raise RuntimeError("No active field system after battle")
                    location = word(field + 0x20)
                    return {"map_id": word(location), "x": word(location + 8), "z": word(location + 12)}
                before = position()
                self.screenshot().save(work / "screens/return-before-movement.png")
                from desmume.controls import Keys, keymask
                self.input.keypad_update(keymask(Keys.KEY_LEFT))
                for _ in range(24):
                    self.cycle(False)
                self.input.keypad_update(0)
                for _ in range(30):
                    self.cycle(False)
                after = position()
                self.screenshot().save(work / "screens/return-after-movement.png")
                result = {"before": before, "after": after,
                          "movement_verified": before["map_id"] == after["map_id"] and before != after}
                (work / "overworld-return.json").write_text(json.dumps(result, indent=2) + "\n")
                if not result["movement_verified"]:
                    super().destroy()
                    raise RuntimeError("The battle result passed but overworld movement was not observed")
            super().destroy()

    runner.DeSmuME = ObservedEmulator
    os.chdir(work)
    try:
        return runner.run_single_partition(argparse.Namespace(video=False, continuous_integration=True, jobs=1))
    finally:
        if runner.emu is not None:
            runner.emu.destroy()
            runner.emu = None
        telemetry.close()


if __name__ == "__main__":
    sys.exit(main())
