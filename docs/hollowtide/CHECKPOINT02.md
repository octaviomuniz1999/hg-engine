# Checkpoint 02 — nova partida, persistência e batalhas reais

Data de registro: 2026-11-08, America/Sao_Paulo. Base preservada: `1e2bf5a33`, branch `codex/hollowtide-foundation`. Trabalho desta etapa: `codex/hollowtide-checkpoint-02`.

## Resultados e limites

| Funcionalidade | Resultado efetivamente observado |
| --- | --- |
| Nova partida | Aprovada no recorte testado: introdução, criação do personagem técnico CPDEX e início no quarto |
| Movimento e transições | Aprovados: quarto 64 → térreo 63 → New Bark Town 60 → laboratório 61, com imagens e leitura do mapa/posição |
| Save persistente | Aprovado: save pelo menu nativo, processo encerrado, processo novo sem import/savestate, CONTINUE e retorno ao mapa 60 nas coordenadas 695,397 |
| Pokémon inicial | Cyndaquil padrão recebido, seguidor observado e estado com Pokémon salvo/carregado; não altera os iniciais definitivos do Hollowtide |
| Batalha controlada | Aprovada no build AUTO_TEST: Mewtwo nocauteou Rattata; vitória, recompensa e resultado nativo WIN = 1 observados |
| Retorno após vitória | Aprovado: mapa 61, posição 4,11; movimento normal de teclado levou a 1,11 após o fim da batalha |
| Mega Evolução | Mega Slowbro: forma 0 → 1, habilidade Shell Armor 75, mensagens e retorno à forma 0 aprovados no modo de testes |
| Primal Kyogre | Blue Orb 535, forma 1, Primordial Sea 189 e chuva intensa 0x02000000 observados; Ember bloqueado e HP mantido em 160; forma 0 após a batalha |
| Kyogre sem Blue Orb | Controle negativo aprovado: forma 0 e Drizzle, sem reversão primal no cenário ensaiado |
| Mapas próprios | Procedimento documentado; nenhum mapa existente substituído e nenhuma importação autoral realizada |

Mega foi solicitada automaticamente pelo `DEBUG_BATTLE_SCENARIOS` original. **Seleção manual pelo botão, desbloqueio da flag 2518 e integração à história ainda não foram exercitados.** Primal foi ensaiada com Blue Orb e sem `DEBUG_PRIMAL_REVERSION`. Os resultados não certificam todas as espécies, interações, batalhas naturais da campanha ou hardware.

Uma exploração adicional da ROM normal parou no diálogo de progressão na saída oeste de New Bark Town. Não se registrou essa tentativa como transição para Route 29 ou como batalha natural aprovada. A batalha completa comprovada é o cenário controlado descrito acima.

## Artefatos privados

- ROM normal final: `/workspace/hg-engine/test.nds`, 268.435.456 bytes (256 MiB).
- SHA-256 normal: `f85b23be04e265f63f961326528cb9c080bacf2be34c4dbf9c03ec4ff558ffd5` — **idêntico byte a byte ao resultado normal do Checkpoint 01**.
- ROM AUTO_TEST: `/workspace/work/hollowtide/cp02/battle-tests/test.nds`.
- Metadados, logs, saves, telemetria e capturas: `/workspace/work/hollowtide/cp02/`.
- Resultados estruturados: `targeted-battle-results.json`, `native-save-before-restart.json`, `normal-final-build.json` e os `battle-case-*/results.json`.

Nenhuma ROM, parte RAR, save, dump de mensagens, screenshot ou ELF compilado foi adicionado ao Git. A ROM-base continua somente leitura e seu hash privado foi conferido contra o recebimento. Não houve instalação/reinstalação de ferramentas.

## Persistência: causa e correção de ambiente

`strace` mostrou que o py-desmume tentava criar `game.dsv` em `/home/agent/.config/desmume`, diretório ausente. A mensagem anterior de operação apenas em RAM não era um resultado de save aprovado.

A correção foi configurar **somente o processo de teste**, antes de carregar a biblioteca:

```bash
mkdir -p /workspace/work/hollowtide/cp02/config/desmume
export XDG_CONFIG_HOME=/workspace/work/hollowtide/cp02/config
```

A nova captura de chamadas confirmou criação bem-sucedida de `config/desmume/game.dsv`; não se escreveu na home nem se alterou a biblioteca. O save nativo ficou com 524.410 bytes. O processo seguinte detectou o backup de 4 Mbit e carregou personagem, mapa e posição esperados. Um segundo carregamento recuperou o estado salvo após receber Cyndaquil.

O savestate `bedroom-start.dst` foi apenas criado como recurso de navegação e **não foi carregado para demonstrar persistência**. A bateria exportada posteriormente, `owner-starter.sav`, tem 524.288 bytes e foi usada apenas como entrada privada dos cenários controlados.

## Procedimento de reprodução

### Partida normal

```bash
source /workspace/.hg-env/activate
PYTHONDONTWRITEBYTECODE=1 python -u tools/hollowtide/emulator_session.py \
  /workspace/work/hollowtide/cp02/normal/game.nds \
  --session-dir /workspace/work/hollowtide/cp02/normal/nova-sessao \
  --config-dir /workspace/work/hollowtide/cp02/config
```

O controlador recebe JSON por stdin, registra inputs/frames e grava imagens privadas. Exemplos realmente usados: `{"frames":120}`, `{"frames":16,"keys":["DOWN"]}`, `{"tap":[124,74],"frames":120,"shot":"save.png"}` e `{"quit":true}`. Toques usam coordenadas da tela inferior 256×192. Os logs completos de entrada estão em `normal/session*/input-events.jsonl`.

Para o teste de persistência, usar o menu SAVE, aguardar a confirmação, encerrar o processo e abrir outro com a mesma ROM/configuração. Escolher CONTINUE. Não substituir isso por importação de bateria ou load de savestate. As leituras opcionais de posição são diagnósticas; o endereço de `gFieldSysPtr` deve vir do ELF correspondente à ROM.

### Builds de modos diferentes

**Antes da primeira compilação em um novo modo, arquivar juntos `build/`, `base/`, `base_dsrom/` e os diretórios de fontes/headers gerados.** Fazer isso antes de qualquer etapa que possa instalar hooks. Reutilizar `.venv`, toolchains e executáveis auxiliares.

Com `rom.nds` compatível presente, foram executados:

```bash
make AUTO_TEST=Y TEST_FILTER=hollowtide
make
```

Esses comandos pertencem a builds separados, com extração coerente para cada modo. O segundo comando é normal, com AUTO_TEST e TEST_FILTER ausentes. Logs: `build-battle-tests-retry.log` e `build-normal-clean-extraction.log`; ambos terminaram em exit 0.

Não basta reusar uma extração que recebeu hooks AUTO_TEST: desativar as defines não desfaz patches já aplicados. A saída normal final foi conferida por hash e conteúdo ARM9/filesystem contra o Checkpoint 01. O teste original que o gerador normaliza tipograficamente foi restaurado byte a byte após os builds, como no checkpoint anterior.

### Cenários de batalha

As quatro fontes em `data/battle_tests/hollowtide/` entram no gerador original por `TEST_FILTER=hollowtide`. O manifesto registra vitória como índice 0, Kyogre sem Orb 1, Mega Slowbro 2 e Primal Kyogre 3.

Preparar para cada caso um diretório privado com a mesma ROM AUTO_TEST, a bateria do proprietário como `test.sav`, `build/battle_tests/test_manifest.json` e `include/constants/generated/test_battle.h`. Guardar o ELF de símbolos do build de testes; não usar o ELF normal após trocar de modo.

O layout do observador foi obtido com o compilador ARM e os headers efetivos:

```bash
arm-none-eabi-gcc -Iinclude -mthumb -mcpu=arm946e-s \
  -Wno-builtin-declaration-mismatch -c tools/hollowtide/battle_layout.c -o layout.o
arm-none-eabi-objcopy -O binary --only-section=.rodata layout.o layout.bin
```

Executar esses comandos em área privada, ajustando caminhos para o checkout. Os oito u32 little-endian são: tamanho de BattlePokemon, offset de battlemon, espécie, byte da forma, HP, item, habilidade e condição de campo. O JSON usado ficou em `cp02/battle-layout.json`. O objeto de diagnóstico nunca é ligado à ROM.

Exemplo executado com a CLI isolada:

```bash
PYTHONDONTWRITEBYTECODE=1 python -u tools/hollowtide/run_battle_checkpoint.py \
  --case-index 3 \
  --work-dir /workspace/work/hollowtide/cp02/battle-case-3-cli-check \
  --config-dir /workspace/work/hollowtide/cp02/battle-case-3-cli-check-config \
  --symbols /workspace/work/hollowtide/cp02/battle-symbols.o \
  --layout /workspace/work/hollowtide/cp02/battle-layout.json
```

Usar índices 0–3, um processo/diretório por caso. Para a vitória, `--verify-return` avança a saída da batalha e usa o teclado para comprovar movimento no overworld. O wrapper chama o runner original, observa registradores/memória por hooks de execução e salva capturas; os observadores não alteram HP, forma, habilidade ou resultado. O mailbox de seleção de cenário é controlado pelo runner original.

## Testes efetivamente executados

- Quatro cenários reais de batalha: quatro aprovados isoladamente, sem testes conhecidos como falhos ou ignorados.
- Primal repetida após acrescentar `--case-index`: aprovada novamente; não contada como um quinto cenário distinto.
- Vitória: outcome nativo 1 e deslocamento 4,11 → 1,11 no mapa 61 aprovados. Os três testes de mecânica terminam pelo encerramento programado, outcome 5; não são provas adicionais de vitória.
- Nova partida, quatro mapas originais, save pelo menu e carregamento em outro processo: observados.
- Sonda de layout ARM compilada e conferida contra os headers; sintaxe das ferramentas Python aprovada.
- 14 testes offline herdados: aprovados novamente, zero falhas, 0,094 s.
- Quatro rejeições de CLI esperadas: diretórios de artefatos dentro do checkout (duas ferramentas), índice de cenário inválido e execução conjunta sem isolamento. Nenhum emulador iniciado nesses casos.
- `git diff --check`, integridade da base e comparação binária da ROM normal final: aprovados.

## Falhas investigadas, sem ocultar tentativas

1. **Build com limpeza parcial:** `build/a015` ausente quando `build/` foi arquivado e a extração antiga permaneceu. O primeiro AUTO_TEST terminou em exit 2. A extração foi arquivada e o build repetido com sucesso.
2. **Agendador depois de vitória natural:** a primeira execução conjunta aprovou o caso de vitória e retornou ao campo, mas expirou antes do cenário seguinte. `TestBattle_QueueNextTest`/`HasMoreTests` dependem do bit de conclusão definido pelo fim dos scripts; a vitória por nocaute com ações restantes não segue esse caminho. Corrigiu-se o procedimento executando cada cenário em processo isolado, sem mudar o código original da engine. O wrapper agora exige isolamento para manifestos com múltiplos casos.
3. **Hooks antigos em uma extração reutilizada:** um build normal intermediário terminou em exit 0, mas a comparação encontrou patches AUTO_TEST residuais em ARM9/overlays. Ele foi marcado `do-not-use.nds` e não usado nas validações normais. Nova extração da ROM-base e novo build eliminaram as diferenças; o hash final coincide exatamente com CP01.

As tentativas e seus logs foram preservados em área privada. Nenhuma dessas falhas foi apresentada como aprovação da etapa afetada antes da repetição e da evidência correspondente.

## Capturas selecionadas

Todas sob `/workspace/work/hollowtide/cp02/`, fora do Git:

| Evidência | Caminho relativo privado |
| --- | --- |
| Quarto inicial | `normal/session01/11-bedroom-start.png` |
| Térreo | `normal/session01/18-first-transition-confirmed.png` |
| Exterior | `normal/session01/23-new-bark-outside.png` |
| Save confirmado | `normal/session01/27-save-complete.png` |
| CONTINUE em processo novo | `normal/session02-cold-load/29-cold-start-continue-menu.png` |
| Posição após carregar | `normal/session02-cold-load/30-cold-load-overworld.png` |
| Laboratório | `normal/session02-cold-load/31-lab-approach.png` |
| Vitória: campo após mover | `battle-case-0/screens/return-after-movement.png` |
| Mega Slowbro | `battle-case-2/screens/case-00-frame-001800.png` |
| Primal Kyogre, HP 160/175 | `battle-case-3/screens/case-00-frame-001620.png` |

## Próximo checkpoint

Exercitar o botão manual de Mega e a flag de história em fixture separada; ampliar o cenário primal para adversário e interações adicionais conforme a campanha exigir. Receber um export autoral PDSMS e executar o protocolo de [MAP_INTEGRATION.md](MAP_INTEGRATION.md), começando por um único mapa em cópia privada. Não alterar mapas existentes nesta etapa. A preparação de publicação do CP01 está em [GITHUB_REVIEW.md](GITHUB_REVIEW.md); nenhum push/PR foi realizado.

## Arquivos versionados nesta etapa

- Novos cenários: `data/battle_tests/hollowtide/controlled_victory.c`, `kyogre_without_orb.c`, `mega_slowbro.c` e `primal_kyogre_blue_orb.c`.
- Novas ferramentas: `tools/hollowtide/emulator_session.py`, `run_battle_checkpoint.py` e `battle_layout.c`.
- Novos relatórios: `docs/hollowtide/CHECKPOINT02.md` e `GITHUB_REVIEW.md`.
- Documentação atualizada em `docs/hollowtide/`: `README.md`, `BUILD.md`, `BLOCKERS.md`, `MECHANICS_AUDIT.md`, `ROADMAP.md`, `TEST_REPORT.md`, `MAP_INTEGRATION.md` e `CHANGELOG.md`.

Nenhuma alteração líquida em C/assembly, Makefiles, dados ou configurações originais da engine. Os novos testes C participam apenas do framework de testes existente; a saída normal final coincide com CP01.
