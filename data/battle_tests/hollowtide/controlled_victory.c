// Test: Hollowtide - controlled knockout reaches the native trainer victory flow
#include "../battle_tests.h"
BEGIN_TEST {
    .battleType = BATTLE_TYPE_TRAINER,
    .weather = FIELD_CONDITION_NONE,
    .terrain = TERRAIN_NONE,
    .playerParty = { {
        .species = SPECIES_MEWTWO, .level = 100, .form = 0,
        .ability = ABILITY_PRESSURE, .item = ITEM_NONE,
        .moves = { MOVE_PSYCHIC, MOVE_NONE, MOVE_NONE, MOVE_NONE }, .hp = FULL_HP,
    } },
    .enemyParty = { {
        .species = SPECIES_RATTATA, .level = 5, .form = 0,
        .ability = ABILITY_RUN_AWAY, .item = ITEM_NONE,
        .moves = { MOVE_TACKLE, MOVE_NONE, MOVE_NONE, MOVE_NONE }, .hp = 1,
    } },
    // Keep actions pending after turn one: the test harness must not terminate
    // this battle by its scripted-flee shortcut before the native victory.
    .playerScript = { {
        { ACTION_MOVE_SLOT_1, BATTLER_ENEMY_FIRST },
        { ACTION_MOVE_SLOT_1, BATTLER_ENEMY_FIRST },
        { ACTION_MOVE_SLOT_1, BATTLER_ENEMY_FIRST },
        { ACTION_NONE, 0 },
    } },
    .enemyScript = { {
        { ACTION_MOVE_SLOT_1, BATTLER_PLAYER_FIRST },
        { ACTION_MOVE_SLOT_1, BATTLER_PLAYER_FIRST },
        { ACTION_MOVE_SLOT_1, BATTLER_PLAYER_FIRST },
        { ACTION_NONE, 0 },
    } },
    .expectations = {
        { .expectationType = EXPECTATION_TYPE_MESSAGE,
          .expectationValue.message = "Mewtwo used Psychic!" },
        { .expectationType = EXPECTATION_TYPE_MESSAGE,
          .expectationValue.message = "The opposing Rattata fainted!" },
        { .expectationType = EXPECTATION_TYPE_MESSAGE_CONTAINS,
          .expectationValue.message = "defeated" },
    },
} END_TEST
