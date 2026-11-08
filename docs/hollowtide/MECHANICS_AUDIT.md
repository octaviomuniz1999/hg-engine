# Mecânicas: evidência de código, não de gameplay

Base auditada: `dbb321327c59b821507f9fc4cb6c41d45a9d2698`. Nenhuma mecânica foi reimplementada ou reconfigurada. As entradas abaixo demonstram implementação existente; todas aguardam compilação e teste em uma ROM compatível.

| Sistema | Evidência na árvore atual | Gate de validação |
| --- | --- | --- |
| Mega Evoluções | `MEGA_EVOLUTIONS` ativo em `include/config.h`; tabelas e lógica em `src/battle/mega.c`; `CheckCanDrawMegaButton` verifica a flag de história | Pokémon elegível, item/movimento, flag, seleção, animação, limite e reversão ao sair |
| Reversões Primais | `PRIMAL_REVERSION` ativo; `CanUndergoPrimalReversion` em `src/battle/other_battle_calculators.c`; entrada de batalha em `src/individual/SwitchInAbilityCheck.c` | Kyogre + Blue Orb e Groudon + Red Orb; ausência do item; entrada/troca/fim de batalha |
| Fairy | Valor 1 em C e ARMIPS; `TYPE_FAIRY = 9` em `include/constants/battle_constants.h`; relações na tabela de `src/battle/battle_pokemon.c` | Efetividades, imunidades e dados visuais; não renumerar para outro padrão por suposição |
| Habilidades modernas | `include/constants/ability.h`, `data/AbilityFlags.c`, `data/HiddenAbilityTable.c` e `src/individual/SwitchInAbilityCheck.c`; hidden abilities habilitadas | Exercitar cada habilidade relevante em seu contexto, sem presumir cobertura total |
| Golpes adicionais | `include/constants/moves.h` define `NUM_OF_CANONICAL_MOVES = 923`; dados em `data/Moves.c` e scripts em `data/battle_scripts/` | O número é limite de dados, não prova de 923 golpes funcionais; validar os escolhidos |
| Pokédex e espécies | `data/Species.c`, `data/RegionalDex.c`, `data/PokedexSort.c`, `data/PokedexArea.c`; `ALLOW_SAVE_CHANGES` ativo | Registro, formas, save/load, encontros, sprites e compatibilidade das ferramentas |

## Primal Kyogre: cadeia técnica inspecionada

1. `CanUndergoPrimalReversion` exige Kyogre, Blue Orb, HP não zero e forma base. Há um caminho de debug com Dream Ball; não ativá-lo para Hollowtide.
2. `SWITCH_IN_CHECK_8C_PRIMAL_REVERSION` chama `BattleFormChange(..., 1, ...)`, atualiza a forma e seleciona `BATTLE_SUBSCRIPT_HANDLE_PRIMAL_REVERSION`.
3. `data/Species.c` contém `SPECIES_KYOGRE_PRIMAL` com `ABILITY_PRIMORDIAL_SEA`. O mapeamento para a espécie base existe em `data/FormToSpeciesMapping.c` e os dados de reversão em `data/PokeFormDataTbl.c`.
4. `CheckIsPrimalKyogre` em `src/battle/mega.c` participa da apresentação da forma em `src/battle/battle_input.c`. Há tratamento climático em `src/individual/SwitchInAbilityCheck.c` e scripts `subscript_0368`/`0369` para limpar climas primais.
5. Existe cenário de interação em `data/battle_tests/moves/pursuit/doubles_pursuit_trigger_on_switch_megas_primal.c`. Sua presença não equivale à aprovação de teste; nenhum cenário C foi executado.

Não foi encontrada necessidade de reimplementar Reversão Primal. Falta comprovar a sequência completa, clima, dano, animação e reversão no emulador e, posteriormente, hardware.

## Contratos de história e eventos

As flags C/ASM conferidas têm o mesmo valor: Mega 2518, Z-Move 2519, Dynamax 2520 e Terastalização 2521. Reservar esses IDs para a engine. Hidden ability usa 2600 e starter hidden ability 2601 em C; não atribuir seus valores a eventos de irrigação.

`IMPLEMENT_LEVEL_CAP` e `LEVEL_CAP_VARIABLE` estão comentados. No caminho normal, `GetLevelCap` em `src/pokemon.c` retorna 100 quando a funcionalidade está desabilitada. A equipe planejada de Nevard não implica ativar level cap.

`IMPLEMENT_WILD_DOUBLE_BATTLES` está desabilitado e o próprio comentário avisa sobre instabilidade. Preservar o estado atual. `ALLOW_SAVE_CHANGES`, expansão das caixas e expansão de bolsos estão ativos; planejar saves próprios de teste.

Snivy, Fennekin, Mudkip, Shroomish e Treecko estão definidos em `include/constants/species.h`; os três iniciais possuem entradas em `data/Species.c`. Isso não implementa a seleção de iniciais, os diálogos do Professor Alex ou a equipe de Nevard.

## Estrutura técnica

- `src/` e `asm/`: extensões C/assembly, separadas entre batalha, campo, overlays e rotinas individuais.
- `rom.ld`, `src/**/linker*.ld`, `hooks`, `armhooks`, `repoints`, `routinepointers`, `bytereplacement`: endereços, memória e patches ligados à base compatível.
- `Makefile`, `overlays.mk`, `narcs.mk`, `dump.mk`: build, NARCs e extração.
- `data/Trainers.c`, `data/Species.c`, `data/Moves.c`, `data/Encounters.c`: fontes de treinadores, espécies, golpes e encontros; não usar tutoriais antigos de layout ARMIPS como se fossem atuais.
- `data/scr_seq/`, `asm/include/scriptmacros.inc`, `src/field/script_commands.c`: scripts de campo e extensões.
- `include/config.h` e `armips/include/config.s`: opções que precisam permanecer coerentes entre C e ARMIPS.

## Achados que afetam o desenvolvimento

- O docstring de `dump_event_scripts.py` sugere que os dumps só retornam à ROM mediante toggles, mas `narcs.mk` sempre inclui textos em `data/text/custom/`. Tratar texto de dump como fonte ativa na próxima compilação.
- Esse dumper executa três chamadas a `make contents-*` no nível de módulo. Até importação ou `--help` passa pelo Makefile e por seu gate de ROM. A auditoria leu o arquivo sem importá-lo.
- `scripts/validate_trainers_s.py` é legado; o build atual usa dados C e `trainerdatagen`.
- Ativar/desativar fontes de eventos altera a proveniência dos dados sob `base/`; invalidar caches após uma troca de política. Esses são pontos de atenção identificados, não erros de gameplay demonstrados.
