# CP05-B — Professor Alex e iniciais

Continuação de CP05-A `12a13ba1f`, na branch `codex/hollowtide-checkpoint-05`. Código original preservado no histórico; sem alteração da branch CP04 ou de main. O usuário autorizou publicar código próprio auditado no fork. Nenhum asset gráfico, ROM, save ou dump é incluído no delta.

## Implementação

`src/starters.c` agora oferece **Snivy 545, Fennekin 703 e Mudkip 258**, mantendo as três rotinas existentes da engine: lista, criação no nível 5 e sprites/gritos. Nenhuma dessas rotinas foi reimplementada. São IDs internos hg-engine, não números nacionais.

As famílias novas não estavam na tabela regional. `data/RegionalDex.c` usa os lugares 1–9 dos iniciais antigos para Snivy/Servine/Serperior, Fennekin/Braixen/Delphox e Mudkip/Marshtomp/Swampert. Entradas regionais restantes e registros nacionais permanecem; isso não define uma Pokédex autoral completa. Os nove valores foram conferidos no NARC efetivamente compilado.

`data/hollowtide/cp05_lab.json` contém somente texto original adaptado em inglês: seletor 190 e entradas iniciais específicas do laboratório 543. Alex apresenta os parceiros e orienta o jogador conforme o roteiro; não há renomeação global de Elm. A introdução de Oak e o texto da mãe são CP05-C, ainda pendentes neste registro. O laboratório continua com o overworld nativo de Elm como **placeholder**, sem design definitivo de Alex nem substituição gráfica.

`apply_story_text.py` decodifica os bancos privadamente, substitui apenas as entradas listadas, preserva controles/variáveis, valida charmap e faz encode/decode com a chave original. Confere que somente os membros de mensagem permitidos mudaram, sem alterar executáveis ou mapas. O texto português aprovado está integralmente em CHECKPOINT05_ORDER.md. Não é localização completa em português.

## Auditoria de recursos e dados

Nove espécies verificadas nas três linhas: sprites dianteiros/traseiros para ambos os sexos, ícones, folhas/JSON de seguidores, dados pessoais, evoluções e learnsets. Nos arquivos da ROM, sprites/dados existentes e paletas normal/shiny distintas foram conferidos. Os gritos têm wave archives próprios, com amostras, e o encaminhamento da engine usa o offset correto: Mudkip 258, Snivy 779, Fennekin 937. O emulador está mudo; não se afirma audição dos gritos. Shiny e animações de evolução não foram reproduzidos visualmente.

Evoluções inspecionadas: Snivy nível 17 → Servine, nível 36 → Serperior; Fennekin 16 → Braixen, 36 → Delphox; Mudkip 16 → Marshtomp, 36 → Swampert. A rotina existente de evolução por nível usa a tabela expandida. Nenhuma nova regra de evolução foi criada.

| Parceiro realmente recebido | Nível | Habilidade | Golpes observados |
| --- | --- | --- | --- |
| Snivy | 5 | Overgrow (65) | Tackle, Leer |
| Fennekin | 5 | Blaze (66) | Scratch, Tail Whip, Ember |
| Mudkip | 5 | Torrent (67) | Tackle, Growl, Water Gun |

## Testes reais e seus limites

Os três seletor/previews e confirmações foram executados no DeSmuME; nomes e sprites corretos foram inspecionados. Os três parceiros foram recebidos no nível 5, com dados acima, HP válido e checksum íntegro, lidos sem escrever RAM. Todos retornaram à Vila, foram salvos pelo menu nativo, carregados por CONTINUE em outro processo e voltaram a se mover. Espécie, nível, habilidade, golpes e flags de Pokédex **visto/capturado** persistiram para os três. O menu da Pokédex ainda não é concedido pela campanha neste ponto; sua UI completa não foi aprovada por esses bits.

A base dos três cenários é uma bateria pré-laboratório criada por uma partida nova normal, sem importação ou savestate. Ela foi copiada para configurações independentes para não repetir a introdução a cada escolha. Seu candidato B só difere do B final por uma correção de texto auxiliar do seletor; os relatórios registram os hashes distintos. O novo início narrativo e a protagonista feminina ainda serão testados no CP05-C, sem bateria importada.

A captura `08-party-icon-and-level.png` desse primeiro ensaio não abriu a equipe: o clique foi na célula superior esquerda, reservada à Pokédex. Ela não comprova ícones/nível da equipe. O controle foi corrigido para o botão Pokémon central esquerdo; a revisão visual desse menu e dos seguidores em área descoberta será registrada com os ensaios de batalha/finalização. Não se repetiu o percurso inteiro para corrigir apenas essa captura.

Três contratos sintéticos específicos passaram: seletor nunca exige uma página extra; decodificação de um Pokémon sintético com ordem física não trivial C/A/D/B; corrupção de checksum rejeitada. Depois de acrescentar a leitura de experiência, somente o contrato afetado foi repetido. Nenhuma bateria completa CP01–04 foi reexecutada.

`observe_party.py` observa memória de SaveData/Party com layouts do próprio projeto; o tamanho foi aferido por objeto ARM diagnóstico (PartyPokemon 240 bytes, corrigindo comentário antigo 0xEC). O observador foi controlado contra um Cyndaquil conhecido. O novo build deslocou o símbolo gFieldSysPtr 16 bytes; o controlador usa agora o símbolo desse build, não o endereço antigo do CP04.

As tentativas anteriores que falharam estão preservadas e não contam como aprovação: endereço de telemetria antigo; limites/layouts inicialmente incorretos no observador; caminho que atravessava o NPC de Alex; toque na bola errada (carrossel nativo tem Grama à frente, Fogo à direita, Água à esquerda); contagem fixa de botões que não aguardava o fim dos diálogos/entrega de Potions. O controlador final verifica movimento real e transição antes de prosseguir. Não houve correção especulativa de gameplay por esses erros do ensaio.

## Compilação e reprodução

Um `make` incremental terminou com exit 0, reutilizando toolchain, extração e objetos. As mudanças funcionais compiladas são a lista dos iniciais e as nove entradas regionais. O gerador normalizou a apóstrofe de um teste upstream; a alteração exata foi conferida e seu original restaurado byte a byte. Depois foram reaplicados o mapa CP04, as colisões CP05-A e as mensagens próprias, sem nova compilação da engine.

ROM B privada: `/workspace/work/hollowtide/cp05/b/game.nds`, SHA-256 `77c5e6faa087b2f86fa9dc2cb831897299f5c3d3721b81bbfb62ad5ae218c251`. Relatórios de cada empacotamento ficam ao lado; intermediários reproduzíveis foram removidos para espaço, mantendo hashes/receitas. CP04 final e assets originais permanecem intactos.

```bash
source /workspace/.hg-env/activate
make
# Instalar Vila (integrate_village.py), colisões (fix_village_collisions.py),
# e mensagens (apply_story_text.py ROM data/hollowtide/cp05_lab.json OUT),
# cada etapa para um novo destino privado, conforme os comandos CP04/CP05-A.
TZ=America/Sao_Paulo python -u -B tools/hollowtide/test_starter_choice.py /caminho/privado/game.nds --initial-dsv /caminho/privado/pre-lab/game.dsv --slot 0 --symbols build/rom_gen.ld --work-dir /caminho/privado/ensaio-snivy
# slots 1/2 correspondem a Fennekin/Mudkip.
```

Evidências privadas sob `/workspace/work/hollowtide/cp05/`: `species-audit.json`, `palette-audit.json`, `build-b.log`, `party-layout.*`, `observer-control-verified.json`, `b-new-game-verified/`, `b-choice-summary.json` e `b-complete-choice-0/1/2/` (sessões, inputs, capturas e results.json). O save pré-lab foi criado com os comandos registrados no bootstrap; não houve edição de saves, RAM ou savestates.

## Compatibilidade e próximos testes

O script real do laboratório foi auditado privadamente: obtém a espécie do Pokémon recebido e a grava em VAR_PLAYER_STARTER; não compara os antigos iniciais nessa concessão. Candidatos de dependência get_starter_choice foram identificados nos scripts 7, 23, 96, 110, 111, 819, 850 e 866. Esses eventos futuros não são alcançados pela Vila/trecho técnico isolado; não foram globalmente alterados nem aprovados. Antes de ligar a campanha a eles, será preciso revisar as comparações/equipes rivais. O trecho provisório continua sem ser a Rota 01 definitiva.

Batalhas curtas e revisão visual adicional estão em execução numa variante privada: `prepare_starter_battle.py` substitui somente o script autoral 965 por uma fixture que inicia a batalha nativa contra Rattata nível 2; o outro diálogo permanece. `test_starter_battle.py` usa botões normais, observa o resultado nativo e verifica experiência/movimento após vitória. **A presença dessas ferramentas não significa que as batalhas já passaram.** Seus resultados serão registrados ao concluir; esse evento não faz parte da ROM de produção. Sem rebuild de teste da engine.

Próximo: CP05-C, introdução/mãe em inglês fiel e partida nova feminina, preservando gênero/nome e o mapa. A validação já concluída dos três parceiros será reutilizada se os únicos deltas C forem os bancos de texto 219/545, com comparação dos arquivos para demonstrá-lo.
