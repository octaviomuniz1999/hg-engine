# Checkpoint 04 — finalização e partida nova

Continuação de `4784b55b7`, em 2026-11-09. Branch `codex/hollowtide-checkpoint-03`. CP01 `1e2bf5a33`, CP02 `6f3625641`, CP03 `9e8e0adff` e CP04 `4784b55b7` preservados como ancestrais, sem reescrita. O usuário autorizou push desta finalização exclusivamente ao fork `octaviomuniz1999/hg-engine`, sem force, mudança de main ou PR.

## Resultado real

A mesma ROM CP04 foi testada desde uma configuração inexistente, sem bateria importada, save técnico ou savestate. Personagem novo: **NOVO**. Núcleo DeSmuME 0.9.12, py-desmume 0.0.9, renderer software headless. Não houve mudança funcional, reinstalação ou recompilação nesta finalização. A ROM já compilada e integrada no CP04 foi reutilizada e seu SHA-256 permaneceu idêntico.

| Verificação executada | Resultado e evidência |
| --- | --- |
| Introdução e nova partida | Nome NOVO, quarto 64, descida ao térreo 63, conversa com a mãe, primeira chegada à Vila 60: capturas 01–15 |
| Movimento e NPCs | Dois diálogos próprios exibidos e movimento retomado: 16–17 e percurso posterior |
| Laboratório | Entrada 61, diálogo nativo, escolha de Cyndaquil por touchscreen, recebimento e saída à Vila: 22–35 |
| Casas | Casa oeste 62 com saída lateral e casa do protagonista 63 com saída sul; retornos corretos: 36–39 |
| Escadaria esquerda | Base `(8,13)` altura 0, meio `(8,12)` 0,49969, topo `(8,11)` 1; caminhada posterior também desce: 18–20 e percurso 36 |
| Escadaria direita | `(23,21)` 0 → `(23,20)` 0,50053 → `(23,19)` 1 → retorno à base: 40–43 |
| Colisões | Escarpa `(11,11)`, árvores `(2,26)` e borda sul `(20,29)` bloquearam os movimentos ensaiados: 45–47 |
| Texturas | Fonte e postes texturizados nas capturas novas: 21 e 44. As flores foram removidas pelo autor e não fazem parte do teste |
| Saída da cidade | Vila → trecho nativo isolado 33, caminhada, retorno à Vila: 48–51. Não foi criada a Rota 01 definitiva |
| Persistência | SAVE nativo em `(16,27)`, encerramento exit 0, outro processo usando a mesma bateria, CONTINUE em `(16,27)`, movimento a `(15,27)`, encerramento exit 0: 52–56 |

**33 verificações de campo aprovadas**, com posições/alturas lidas sem escrita de memória; **57 capturas verificadas por hash**. Foram inspecionadas visualmente as capturas de introdução, diálogos, interiores, construções, escadas, fonte/postes e recarga. Os hashes não substituem essa inspeção nem representam aprovação artística. A bateria nativa gerada tem 524.410 bytes e fica privada; não acompanha a entrega.

Também foram executados 31 testes offline existentes, todos aprovados, antes da diretriz posterior de eficiência. Não foram repetidas batalhas, Mega/Primal, compilações ou as baterias completas CP01–03. `git fsck --full` terminou com exit 0; dois blobs documentais soltos anteriores não comprometem a integridade dos commits.

Uma interrupção transitória do canal de comandos foi contornada conservando o mesmo processo e frame. Na primeira tentativa de reabrir o núcleo, stdin sem TTY encerrou o processo sem executar frames; essa inicialização vazia não foi contada como teste. A recarga efetiva foi repetida com TTY, sem importar ou copiar saves. Nenhum defeito funcional novo foi observado no percurso; não houve correção no código nem nos recursos visuais.

## Artefatos e reprodução

ROM jogável: `/workspace/work/hollowtide/cp04/final/game.nds`, **193.020.616 bytes**.
SHA-256: `e6a1e7d6ca24cf8bd722c861905ddfe8249c463c532bcc1ee8bdebed2c1cdcb2`.
Build normal anterior à instalação do mapa: `/workspace/hg-engine/test.nds`, SHA-256 `80bcad0066fe9d79c99b1e022dc846c436647d850c2334d50f32c47616222fcb`.
ROM-base preservada somente leitura: SHA-256 `65f02a56842b75aa92d775d56d657a56fe3fa993550b04dc20704ab82d760105`.
Os 15 originais autorais foram novamente conferidos contra o inventário; hashes e permissões somente leitura preservados. A ROM idêntica conserva a proteção visual demonstrada no CP04.

Evidências privadas em `/workspace/work/hollowtide/cp04-finalization/`:

- `preflight-audit.json`: configuração inicialmente ausente e ausência de saves importados.
- `fresh/session01/input-events.jsonl`: comandos reais desde frame zero até SAVE e quit, com resultados e capturas.
- `fresh/session02-interactive/input-events.jsonl`: boot/CONTINUE em outro processo e movimento; nenhum savestate.
- `fresh/results.json`: 33 verificações de campo, 57 hashes de capturas, ROM e ciclo de vida.
- `fresh/battery-before-reload.json`, `fresh/lifecycle.json`, `offline-tests.log`, `git-fsck.json`.

Comandos principais executados, com ambiente ativado:

```bash
source /workspace/.hg-env/activate
TZ=America/Sao_Paulo python -u -B tools/hollowtide/emulator_session.py /workspace/work/hollowtide/cp04/final/game.nds --session-dir /workspace/work/hollowtide/cp04-finalization/fresh/session01 --config-dir /workspace/work/hollowtide/cp04-finalization/fresh/config
# Repetido em novo processo TTY com session02-interactive e a mesma configuração.
TMPDIR=/workspace/work PYTHONDONTWRITEBYTECODE=1 python -B -m unittest discover -s tests/hollowtide -v
python -B /workspace/work/hollowtide/cp04-finalization/verify_fresh_run.py
git fsck --full
```

Para reproduzir uma partida do zero, usar diretórios de configuração e sessão inéditos e seguir a introdução pelo controle/touch. Os comandos completos e frames estão nos JSONL. **Não usar o controlador antigo `test_village_runtime.py` como prova de partida nova:** ele inicia de bateria técnica CP02. Nesta finalização somente seu planejador de caminhos foi reutilizado, sem executar seu main.

## Preservação, entrega e limites

A auditoria de publicação examina todas as versões de blobs adicionados/modificados desde a base upstream `dbb321327`, inclusive versões intermediárias. Os deltas Hollowtide contêm apenas fontes e documentação próprias: nenhuma ROM, save, dump, captura ou asset comercial adicionado. Isso não é uma declaração sobre os assets preexistentes herdados do upstream. Diff e auditoria final ficam em `full-development.patch`, `finalization.patch`, `full-development-stat.txt` e `publication-audit.json`. O recibo posterior ao push fica em `publication-receipt.json`, com SHA remoto e comparação de main antes/depois.

A entrega completa fica privada em `private-delivery/Hollowtide_CP04_Final.nds`; instruções em [PRIVATE_PLAYTEST.md](PRIVATE_PLAYTEST.md). O caminho Windows escolhido não é montado no Cloud: o usuário precisa baixar e copiar o arquivo para `C:\Users\tavin\OneDrive\Área de Trabalho\ROM JOGAVEL`. Nenhum upload ao OneDrive é alegado. ROMs e capturas não são publicadas no GitHub.

A cobertura é o percurso descrito, não todos os tiles, horários, hardware ou campanha completa. Interiores, introdução, nomes e iniciais nativos são provisórios. Batalhas/Mega/Primal não foram repetidos por ausência de alteração relacionada; seleção manual de Mega continua pendente. GUI dos editores e Windows do usuário não foram testados aqui. O próximo checkpoint imediato é o teste privado pelo proprietário e sua revisão da Vila; **não avançar para a Rota 01 definitiva**.

Foram alterados somente AGENTS.md e documentação: este relatório, PRIVATE_PLAYTEST.md, CHECKPOINT04.md, README.md, GITHUB_REVIEW.md, DEVELOPMENT_DIRECTIVE.md, ROADMAP.md, TEST_REPORT.md e CHANGELOG.md. Código, geometria, decoração e construções permanecem intactos.

## Política de eficiência posterior

Reutilizar ferramentas e builds existentes. Executar somente verificações ligadas ao delta; repetir testes aprovados apenas diante de regressão ou em marco importante. Priorizar salvar checkpoints pequenos antes de ampliar o trabalho. Registrar testes adiados explicitamente. A validação acima já estava concluída quando o usuário estabeleceu essa diretriz; não foi repetida depois dela.
