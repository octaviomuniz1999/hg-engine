// Test: Hollowtide - Kyogre without Blue Orb remains in its base form
#include "../battle_tests.h"
BEGIN_TEST {
    .battleType = BATTLE_TYPE_TRAINER,
    .weather = FIELD_CONDITION_NONE,
    .terrain = TERRAIN_NONE,
    .playerParty = { {
        .species = SPECIES_KYOGRE, .level = 50, .form = 0,
        .ability = ABILITY_DRIZZLE, .item = ITEM_NONE,
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
        { .expectationType = EXPECTATION_TYPE_PARTY_FORM,
          .battlerIDOrPartySlot = 0, .expectationValue.formID = 0 },
        { .expectationType = EXPECTATION_TYPE_MESSAGE,
          .expectationValue.message = "Kyogre used Sleep Talk!" },
        { .expectationType = EXPECTATION_OVERWORLD_FORM,
          .battlerIDOrPartySlot = 0, .expectationValue.formID = 0 },
    },
} END_TEST
