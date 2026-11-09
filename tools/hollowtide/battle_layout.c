/* Read-only observer offsets, compiled with the same ARM headers as the ROM.
 * Extract .rodata as eight little-endian u32 values; see CHECKPOINT02.md.
 * This object is diagnostic only and is never linked into the game.
 */
#include "battle.h"

const unsigned int hollowtide_layout[] = {
    sizeof(struct BattlePokemon),
    __builtin_offsetof(struct BattleStruct, battlemon),
    __builtin_offsetof(struct BattlePokemon, species),
    __builtin_offsetof(struct BattlePokemon, type1) + 2, /* form bitfield byte */
    __builtin_offsetof(struct BattlePokemon, hp),
    __builtin_offsetof(struct BattlePokemon, item),
    __builtin_offsetof(struct BattlePokemon, ability),
    __builtin_offsetof(struct BattleStruct, field_condition),
};
