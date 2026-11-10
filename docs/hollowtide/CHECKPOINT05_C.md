# Checkpoint 05-C — abertura de Hollowtide

Branch: `codex/hollowtide-checkpoint-05`. Base preservada: CP04 finalização `a679364bc`; CP05-A `12a13ba1f`; CP05-B `49b9e8ecd`. Ordem e texto português do diretor preservados em [CHECKPOINT05_ORDER.md](CHECKPOINT05_ORDER.md). A versão jogável usa inglês, mantendo os controles nativos. Não houve avanço à Rota 01 definitiva.

## Implementação

- `data/hollowtide/cp05_intro.json`: introdução de Alex sobre encontros e vínculos; escolha nativa de nome/gênero; diálogo acolhedor da mãe. Mensagens dos bancos 219/545, sem alteração dos scripts de eventos, entregas de itens ou flags da mãe.
- O tutorial opcional recebeu instruções neutras de exploração, retirando a lição nativa de crescimento pessoal. Não antecipa Team Palm nem inventa região definitiva.
- `apply_story_text.py` preserva a espera final original quando o manifesto solicita: o impressor da introdução depende dela. Controles YESNO/variáveis, criptografia e entradas não selecionadas são preservados e verificados por encode/decode.
- O laboratório e os iniciais do [CP05-B](CHECKPOINT05_B.md) permanecem. `src/starters.c` e `data/RegionalDex.c` são as únicas alterações funcionais compiladas desse subcheckpoint; as nove famílias existentes foram reutilizadas.
- Controles de teste corrigidos: botão Pokémon, fechamento efetivo da equipe antes de SAVE/batalha e endereço gFieldSysPtr do build em uso. Sem escrita em RAM, edição de bateria ou injeção de código.

**Arte provisória:** Alex ainda usa o NPC nativo Elm, gráfico 99 (`data/graphics/overworlds/0099.png`, JSON e paleta correspondentes); a introdução mantém o retrato nativo Oak e a demonstração Marill. Esses gráficos não são arte final de Alex. Não há sprite de batalha novo do professor. Interiores e conexão técnica usam mapas nativos provisórios. Não houve alteração de geometria, decoração, BLD, texturas ou alturas autorais neste subcheckpoint.

## Resultados efetivamente executados

| Recorte | Resultado e limite |
| --- | --- |
| CP05-A: fonte e dois mastros | 15 verificações localizadas no DeSmuME; colisões corrigidas em 11 tiles. Duas escadarias, acesso ao laboratório e conectividade continuam acessíveis. Outros contatos parciais não classificados não foram bloqueados por suposição. |
| Build B | Um `make` incremental, exit 0. Sem reinstalação, clean global ou nova compilação C. |
| Três escolhas B | Snivy/Fennekin/Mudkip, nível 5, habilidades/golpes/checksum corretos; retorno à vila, SAVE e CONTINUE em processo novo; espécie e flags visto/capturado persistentes. Protagonista masculino, nome de teste NOVO. |
| Recursos B | Nove espécies auditadas no código/dados/arquivos compilados: evoluções, learnsets, sprites, paletas normal/shiny, ícones, cries e seguidores. Três menus, sprites traseiros e seguidores em chão aberto inspecionados no emulador. Auditoria de cry não equivale a áudio ouvido. |
| Três batalhas B | Variante privada isolada, Rattata nível 2: vitória nativa flag 1; experiência 135 → 145, HP positivo e movimento no overworld após retorno para os três parceiros. Fixture não instalada na ROM de produção. |
| Contratos de teste | Três contratos específicos passaram; após acrescentar experiência ao observador, somente seu teste afetado foi repetido. Não foi repetida a suíte CP01–04. |
| Nova partida C final | Configuração vazia, sem bateria inicial/savestate. 15.963 frames reais no DeSmuME; protagonista feminina, nome alva; introdução, casa, escada, mãe, menus, chegada à Vila e SAVE nativo. 32 capturas registradas/conferidas. |
| Laboratório C final | Usa a bateria legítima criada na linha anterior; Alex, seleção/recebimento de Snivy nível 5, retorno, menu Pokémon, SAVE, encerramento e CONTINUE em processo novo. Espécie 545, Overgrow 65, movimentos 33/43, HP 20/20 e checksum válidos; visto/capturado persistem; movimento após carga verificado. |
| Tutorial opcional C final | Seis mensagens novas exibidas integralmente e retorno ao menu, revisão visual das capturas. As primeiras duas navegações abriram CONTROL INFO por erro de entrada; não contam como validação de ADVENTURE INFO. |
| Patch final | Aplicação xdelta em stream à base original: 193.015.496 bytes e SHA-256 exatamente iguais à ROM final. Sem gerar outra ROM em disco. |

Os três iniciais e batalhas B não foram repetidos no C: somente mensagens foram alteradas, com comparação de arquivos e roundtrip dos bancos. Um candidato C anterior já passou a partida/laboratório feminino; a edição posterior de seis entradas do tutorial mudou somente banco 219, entradas 28–33. A partida completa e Snivy foram verificados também na **ROM final**, para não misturar hashes. Os registros distinguem os dois candidatos.

As falhas anteriores do controlador (endereço de campo/layout do observador, caminho pelo professor, seleção errada do carrossel, menu ainda aberto e avanço insuficiente de diálogo) não contam como aprovação. Os ensaios finais corrigidos passaram. Não se alterou gameplay por falhas do roteiro de teste.

## ROM e evidências privadas

Raiz: `/workspace/work/hollowtide/cp05/`.

- ROM final: `final/game.nds`, **193.015.496 bytes**.
- SHA-256 final: `e0fb3b69821e93b86f50f5455f2957a72838c24ef9091c3c4c6196b522ef6b2e`.
- Base original: `/workspace/hg-engine/rom.nds`, 134.217.728 bytes, SHA-256 `65f02a56842b75aa92d775d56d657a56fe3fa993550b04dc20704ab82d760105`, preservada somente leitura.
- Patch: `Hollowtide_CP05.xdelta`, **36.906.334 bytes**, SHA-256 `8d94f0ac35b7a5bd9e757a742a0a63cb38e1fa9b2a09cb1ec20169094fd26724`; validação em `patch-validation.json`.
- Partida: `final-new-game/results.json`, `session01/` (32 PNG e input-events.jsonl), configuração nova e bateria gerada pelo jogo.
- Laboratório/persistência: `final-girl-snivy/results.json`, `session01/`, `session02-cold-load/`. A bateria de entrada corresponde exatamente ao SHA do save da partida nova.
- Tutorial: `final-adventure-help-touch/session/help-page-0.png` até `help-page-6.png` e log; `final-equivalence/results.json` comprova o delta final restrito.
- Outros resultados: `build-b.log`, `b-choice-summary.json`, `b-battle-summary.json`, `b-runtime-summary.json`, diretórios individuais referenciados em A/B e recibos de integração ao lado das ROMs.

Capturas úteis: `final-new-game/session01/20-world-beyond-window.png`, `26-mother-village.png`, `30-first-arrival-village.png`; `final-girl-snivy/session01/01-alex-introduction.png`, `08-party-icon-and-level.png`; `session02-cold-load/11-persistent-continue.png`. Nenhum PNG extraído do jogo foi incluído no Git público.

DeSmuME 0.9.12/py-desmume 0.0.9, renderização de software, TZ America/Sao_Paulo, som silenciado. Não houve validação em hardware nem alegação de áudio ouvido.

## Reprodução sem sobrescrever a base

A execução já foi concluída; os comandos abaixo são receita, não uma solicitação de repetir testes/builds. Usar destinos privados novos e assets originais CP04. `test.nds` é a saída intermediária da engine e não contém, sozinho, toda a integração final.

```bash
source /workspace/.hg-env/activate
# make somente após mudanças que exijam compilar a engine/dados.
# Aqui test.nds já corresponde ao build B validado.
python -B tools/hollowtide/integrate_village.py test.nds /privado/Hollowtide_Vila_Inicial /privado/vila.nds
python -B tools/hollowtide/fix_village_collisions.py /privado/vila.nds /privado/Hollowtide_Vila_Inicial /privado/colisoes.nds
python -B tools/hollowtide/apply_story_text.py /privado/colisoes.nds data/hollowtide/cp05_lab.json /privado/laboratorio.nds
python -B tools/hollowtide/apply_story_text.py /privado/laboratorio.nds data/hollowtide/cp05_intro.json /privado/final/game.nds
```

Roteiro próprio de ações, registrado em partida real e executado integralmente na ROM final: `tools/hollowtide/inputs/cp05_intro_girl.jsonl`. Não contém save, savestate ou dados extraídos da ROM. Reprodução com configuração vazia:

```bash
TZ=America/Sao_Paulo python -u -B tools/hollowtide/emulator_session.py /privado/final/game.nds --session-dir /privado/nova-sessao --config-dir /privado/nova-config < tools/hollowtide/inputs/cp05_intro_girl.jsonl
```

Depois, `test_starter_choice.py` aceita a bateria pré-lab gerada legitimamente nessa sessão, `--slot 0`, `--symbols build/rom_gen.ld` e outro `--work-dir` privado. Slots 1/2 correspondem a Fennekin/Mudkip. Não usar save de candidato anterior como evidência de nova partida da ROM final.

## Preservação, entrega e próximos gates

Publicação autorizada somente na branch CP05 do fork, sem force push, main ou PR, após auditoria do delta. CP01–04 e os subcheckpoints A/B permanecem ancestrais. O público recebe apenas código próprio, dados textuais próprios e documentação; nenhum arquivo de ROM, save, dump ou recurso comercial novo.

Patch entregue somente em [xdeltatests privado / branch cp05-download](https://github.com/octaviomuniz1999/xdeltatests/tree/cp05-download/cp05), conservando o CP04 na branch anterior. Requer login do proprietário; instruções/hash acompanham o patch. Não usar a ROM CP04 como base do xdelta: usar a ROM original com o hash acima. O recibo com commits remotos fica fora do Git em `cp05/source-publication.json` e `cp05/private-github-delivery.json`.

Para espaço, foram removidos dois caches obsoletos reproduzíveis (build anterior e extração de diagnóstico antigo), e ROMs temporárias reproduzíveis de batalha/candidato C. Inventários/receitas/hashes preservados em `retired-build-cache.json`, `retired-diagnostic-extraction.json` e relatórios dos candidatos; ROM-base, ROM final CP04, originais autorais, logs, capturas e baterias foram mantidos. Não se limpou o build atual.

**Adiados explicitamente:** áudio ouvido; encontros shiny; animação de evolução; UI completa da Pokédex ainda não entregue pela campanha; interações completas de campanha/rival, com dependências candidatas nos scripts 7, 23, 96, 110, 111, 819, 850 e 866; hardware; arte definitiva de Alex/interiores; contatos parciais de objetos ainda não demonstrados. Mega/Primal não foram revalidados no CP05, pois não houve delta nesses sistemas. A evidência histórica continua no CP02.

Próximo checkpoint: revisão pelo diretor da experiência inicial e das colisões remanescentes; integrar arte de Alex quando aprovada. Revisar dependências rivais antes de conectar novos eventos. A Rota 01 definitiva permanece fora do escopo.
