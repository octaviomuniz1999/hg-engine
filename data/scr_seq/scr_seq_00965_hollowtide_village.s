.include "asm/include/interop_macros.inc"
.include "asm/include/scriptmacros.inc"

// Local dialogue prototypes for the isolated authored-map integration.
// Message archive 854; these are not the final campaign dialogue.
.data
scrdef hollowtide_village_greeting
scrdef hollowtide_village_laboratory
scrdef_end

hollowtide_village_greeting:
    SimpleNPCMessage 0
    end

hollowtide_village_laboratory:
    SimpleNPCMessage 1
    end
