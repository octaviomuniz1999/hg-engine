// PRIVATE TEST VARIANT ONLY. Never installed by the production build.
// Reuse the existing village NPC solely to exercise native wild-battle flow.
#include "constants/species.h"
.include "asm/include/interop_macros.inc"
.include "asm/include/scriptmacros.inc"
.data
scrdef starter_battle
scrdef original_second_dialogue
scrdef_end
starter_battle:
    lockall
    faceplayer
    wild_battle SPECIES_RATTATA, 2, 0
    releaseall
    end
original_second_dialogue:
    SimpleNPCMessage 1
    end
