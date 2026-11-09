// Test: Hollowtide - Blue Orb activates Primal Kyogre and heavy rain blocks Fire
#include "../battle_tests.h"
BEGIN_TEST {
    .battleType = BATTLE_TYPE_TRAINER,
    .weather = FIELD_CONDITION_NONE,
    .terrain = TERRAIN_NONE,
    .playerParty = { {
        .species = SPECIES_KYOGRE, .level = 50, .form = 0,
        .ability = ABILITY_DRIZZLE, .item = ITEM_BLUE_ORB,
        .moves = { MOVE_SLEEP_TALK, MOVE_NONE, MOVE_NONE, MOVE_NONE }, .hp = 160,
    } },
    .enemyParty = { {
        .species = SPECIES_CHARMANDER, .level = 50, .form = 0,
        .ability = ABILITY_BLAZE, .item = ITEM_NONE,
        .moves = { MOVE_EMBER, MOVE_NONE, MOVE_NONE, MOVE_NONE }, .hp = FULL_HP,
    } },
    .playerScript = { {
        { ACTION_MOVE_SLOT_1, BATTLER_ENEMY_FIRST },
        { ACTION_MOVE_SLOT_1, BATTLER_ENEMY_FIRST },
        { ACTION_NONE, 0 },
    } },
    .enemyScript = { {
        { ACTION_MOVE_SLOT_1, BATTLER_PLAYER_FIRST },
        { ACTION_MOVE_SLOT_1, BATTLER_PLAYER_FIRST },
        { ACTION_NONE, 0 },
    } },
    .expectations = {
        { .expectationType = EXPECTATION_TYPE_MESSAGE,
          .expectationValue.message = "Kyogre's Primal Reversion! It reverted to its primal state!" },
        { .expectationType = EXPECTATION_TYPE_MESSAGE,
          .expectationValue.message = "A heavy rain began to fall!" },
        { .expectationType = EXPECTATION_TYPE_PARTY_FORM,
          .battlerIDOrPartySlot = 0, .expectationValue.formID = 1 },
        { .expectationType = EXPECTATION_TYPE_MESSAGE,
          .expectationValue.message = "The Fire-type attack fizzled out in the heavy rain!" },
        { .expectationType = EXPECTATION_CURRENT_HP,
          .battlerIDOrPartySlot = BATTLER_PLAYER_FIRST, .expectationValue.currentHP = 160 },
        { .expectationType = EXPECTATION_OVERWORLD_FORM,
          .battlerIDOrPartySlot = 0, .expectationValue.formID = 0 },
    },
} END_TEST
