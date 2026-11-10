# Pokémon Hollowtide

Read `docs/hollowtide/DEVELOPMENT_DIRECTIVE.md` and the project README before
working on Hollowtide. This records the user's permanent division of work:
the user owns creative direction and visual map construction in Pokémon DS Map
Studio 2.2; the agent owns technical integration, programming and verification.

Preserve authored geometry, decoration, building placement and visual identity.
Do not change these without explicit user authorization. Implement collisions,
heights, warps, connections, NPCs, scripts, resource bindings and texture fixes
within that boundary. Resolve routine technical decisions autonomously; ask
about creative decisions only when established design cannot safely resolve them.

Preserve checkpoint commits `1e2bf5a33`, `6f3625641` and `9e8e0adff` as ancestors.
Preserve later checkpoints as ancestors too; read `docs/hollowtide/CHECKPOINT04.md`
for the first authored village, resource-binding pitfalls and reproducible tests.
CP05 now continues on `codex/hollowtide-checkpoint-05` from `a679364bc`; preserve
`codex/hollowtide-checkpoint-03` and its checkpoint ancestry. Read
`docs/hollowtide/CHECKPOINT05_ORDER.md` and `CHECKPOINT05_A.md`. The owner
authorizes audited CP05 code/docs to their hg-engine fork on this separate
branch; no main changes, force push, PR, ROMs, saves, dumps or commercial assets.
Use incremental stages A/B/C and delta-specific tests, reuse existing builds,
and do not repeat approved suites without evidence of regression.
Keep base ROMs, saves, extracted commercial assets and emulator artifacts private
and outside Git. The owner authorized the CP04 finalization development branch
containing CP01–04 for the fork `octaviomuniz1999/hg-engine` only, after auditing
all added/modified blob versions. No force push, main change or PR is authorized.
Read `docs/hollowtide/CHECKPOINT04_FINALIZATION.md` for the fresh-game validation
and publication receipt location. Future unrelated publication needs authorization.

For the restored environment, read `/workspace/.hg-env/START.md` when present and
source `/workspace/.hg-env/activate` in each shell. Do not reinstall unnecessarily.
Do not build without a compatible owner-provided ROM. Distinguish code written,
build results and observed DeSmuME behavior; never report unexecuted tests.
