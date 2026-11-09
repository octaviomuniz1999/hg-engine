// Test: Hollowtide - Slowbro Mega Evolves and reverts after battle
#include "../battle_tests.h"
BEGIN_TEST {
    .battleType = BATTLE_TYPE_TRAINER,
    .weather = FIELD_CONDITION_NONE,
    .terrain = TERRAIN_NONE,
    .playerParty = { {
        .species = SPECIES_SLOWBRO, .level = 50, .form = 0,
        .ability = ABILITY_OBLIVIOUS, .item = ITEM_SLOWBRONITE,
        .moves = { MOVE_SLEEP_TALK, MOVE_NONE, MOVE_NONE, MOVE_NONE }, .hp = FULL_HP,
    } },
    .enemyParty = { {
        .species = SPECIES_MAGIKARP, .level = 5, .form = 0,
        .ability = ABILITY_SWIFT_SWIM, .item = ITEM_NONE,
        .moves = { MOVE_SPLASH, MOVE_NONE, MOVE_NONE, MOVE_NONE }, .hp = FULL_HP,
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
          .expectationValue.message = "Slowbro's Slowbronite is reacting to the Key Stone!" },
        { .expectationType = EXPECTATION_TYPE_MESSAGE,
          .expectationValue.message = "Slowbro has Mega Evolved into Mega Slowbro!" },
        { .expectationType = EXPECTATION_TYPE_PARTY_FORM,
          .battlerIDOrPartySlot = 0, .expectationValue.formID = 1 },
        { .expectationType = EXPECTATION_TYPE_MESSAGE,
          .expectationValue.message = "Slowbro used Sleep Talk!" },
        { .expectationType = EXPECTATION_OVERWORLD_FORM,
          .battlerIDOrPartySlot = 0, .expectationValue.formID = 0 },
    },
} END_TEST
