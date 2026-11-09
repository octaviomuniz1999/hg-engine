# Checkpoint 04 — Vila Inicial autoral

Data: 2026-11-09, America/Sao_Paulo. Branch de desenvolvimento: `codex/hollowtide-checkpoint-03`, continuando `16316f079`. CP01 `1e2bf5a33`, CP02 `6f3625641` e CP03 `9e8e0adff` são preservados como ancestrais. Nenhuma publicação nova está autorizada ou foi feita nesta etapa.

## Recebimento confirmado antes da integração

O anexo `Hollowtide_Vila_Inicial.rar` foi acessado e extraído com a libarchive já instalada: **89.358 bytes compactados, 15 arquivos, 1.042.737 bytes extraídos**. Arquivos em `/workspace/work/hollowtide/cp04/incoming/Hollowtide_Vila_Inicial/`, originais em modo somente leitura, inventário e SHA-256 em `cp04/intake.json`. Não foram executadas instruções do anexo; seu conteúdo é tratado como assets.

Vieram projeto `.pdsmap`, tileset `.pdsts`, dois pares OBJ/MTL, dois IMD, dois NSBMD e a célula `teste2_00_00` em BIN, BLD, BDHC, BDHCAM e BGS. Não veio NSBTX separado ou PER avulso. Isso não bloqueou a integração: o PER tem 2.048 bytes dentro do BIN e o NSBMD completo contém TEX0 com 16 texturas e 16 paletas. O MDL0 do NSBMD completo coincide exatamente com o modelo do BIN. Os intermediários e a biblioteca editável foram mantidos como referência; não foi necessário descartar nenhum original.

O usuário esclareceu que **removeu as flores**: elas não fazem parte deste mapa, não foram acrescentadas e não há teste de flores a aprovar. O usuário também autorizou saída no canto inferior direito e eventual remoção da tile de árvores. O modelo já contém a abertura de floresta nessa região; a implementação aproveita a abertura, **sem remover ou deslocar geometria**.

## Implementação e proteção visual

`tools/hollowtide/integrate_village.py` instala exclusivamente a revisão recebida, conferindo os hashes dos inputs. Trabalha sobre uma ROM normal recém-compilada e cria outra ROM externa ao checkout. O original recebido e a ROM-base não são sobrescritos.

| Recurso | Integração |
| --- | --- |
| Vila, header 60 | Nova matriz exclusiva 288, land-data 676, evento 491, área 106 |
| Modelo e decoração | NSBMD, oito registros BLD, BDHC e BGS **byte a byte idênticos** ao BIN recebido |
| Texturas de mapa | TEX0 recuperado do NSBMD completo → novo NSBTX 106; materiais/UVs e pixels preservados |
| Objetos BLD | IDs 20/21/27/53/239/332 preservados; config/texturas de edifícios 104 com os recursos necessários |
| Portas | Laboratório `(8,8)` → interior 61; casa `(13,25)` → 63; casa oeste `(4,23)` → 62; retorno de cada um à sua porta |
| Permissões | Somente as três portas, aproximação do laboratório `(8,9)` e entrada da floresta `(28,27)` são ajustadas na célula autoral |
| NPCs | Dois NPCs estáticos, `(8,17)` e `(17,26)`, com diálogos neutros de protótipo em português; não são narrativa definitiva |
| Scripts e mensagens | Novo script 965, mensagens 854; scripts locais de NPC 1/2, header de entrada vazio 619 |
| Saída inferior direita | Passagem `(28,27)` para um trecho nativo isolado de rota, com retorno à Vila |

Os interiores reutilizam mapas nativos temporariamente; não são interiores autorais definitivos. O cenário de rota é uma cópia da célula nativa `(20,12)`, land-data original 3 de **Route 29**, header 33 (`MAP_R29` no código). Usa land 677, matriz 289 e evento 492, com bordas técnicas fechadas, sem encontros aleatórios e portal de retorno `(12,14)`. **Não é a Rota 01 autoral** nem uma aprovação criativa de seu desenho. Essa conexão comprova a infraestrutura enquanto o mapa definitivo não foi fornecido.

Os recursos anteriores continuam no filesystem. Os três backlinks dos interiores são conferidos e configurados; o empacotador verifica todos os membros e arquivos fora do conjunto permitido. No ARM9, alteram-se apenas dados dos headers 60/33 e o marcador de tamanho da recompressão. Não há alteração de instruções executáveis, ARM7 ou tabelas de overlays. Fontes C/assembly originais, Makefiles e lockfiles permanecem intactos.

As fontes próprias são `data/scr_seq/scr_seq_00965_hollowtide_village.s` e `data/text/854.txt`. O texto autoral fica na categoria mantida pela engine, protegida pela detecção automática do dumper, em vez de no diretório de dumps `data/text/custom/`. Não executar dumps com `--include-engine-managed` por rotina.

## Texturas: causa investigada e correção

O primeiro pacote mesclado continha os pixels/paletas, mas mantinha os links de dicionário dos pacotes antigos. Os campos `unk00/unk02` do ndspy codificam nós da árvore Patricia Nitro: não são flags independentes que possam ser simplesmente copiadas durante uma mescla. Uma simulação da busca usada pelo SDK resolveu todos os nomes dos pacotes nativos, mas falhou para **cinco texturas e cinco paletas** adicionadas: `funsui_a/b/c` e `tmms_sl2/3`. No emulador, os postes exibiram quadrados brancos.

Foi implementada reconstrução dos índices, mantendo a ordem dos recursos e seus dados visuais. A busca é repetida no NSBTX efetivamente serializado. O teste de controle usou os mesmos postes em cenário nativo, sem alterar seus modelos. Após a correção, o DeSmuME exibiu os postes com luz/transparência e a fonte com suas texturas. A correção não troca arte, não altera UVs e não remove polígonos.

## Compilação real e falhas registradas

O build anterior, `build/`, `base/` e `base_dsrom/` foram arquivados em `cp04/before-build/`. O primeiro `make` limpo terminou com exit 2: `build/learnset/MachineMoveLearnsets.c: No such file or directory`. O marcador ignorado `include/constants/generated/learnsets.h`, mantido fora de `build/`, fez o Make pular a geração de seus arquivos C. Arquivá-lo também e repetir o **procedimento oficial** regenerou os dados; o segundo `make` terminou com **exit 0**. Não foi adicionada uma correção especulativa à engine.

O gerador normalizou a apóstrofe de `intimidate_after_pursuit.c`; a alteração conhecida foi conferida e o original foi restaurado byte a byte. A ROM normal nova tem 256 MiB, SHA-256 `80bcad0066fe9d79c99b1e022dc846c436647d850c2334d50f32c47616222fcb`. Comparação com o build CP03: ARM9, ARM7, overlays e todos os membros anteriores idênticos; apenas `a/0/1/2` e `a/0/2/7` crescem com script 965 e mensagens 854. O log contém as etapas de compilação/assembly/encoding correspondentes.

A ROM jogável é gerada em seguida pelo integrador. Isso é **compilação normal + integração de recursos**, não compilação C do BIN nem reaplicação do hg-engine sobre uma ROM já patchada. Não houve reinstalação de dependências.

Uma execução incremental de `make`, após colocar o texto autoral na categoria protegida `data/text/854.txt`, também terminou com exit 0 e reproduziu exatamente o hash normal acima. Portanto, a organização final das fontes reproduz a mesma base usada na ROM testada.

Outras tentativas revelaram: script local zero não abre o primeiro diálogo (corrigido para 1/2); portas externas precisam do comportamento nativo `69/80`, não do `65/00` de saída interior; a casa 62 tem saída lateral, portanto o controlador de teste precisa caminhar para a direita; a chegada numa porta externa pode permanecer no tile da porta antes de o jogador dar o passo de saída. As tentativas e capturas foram mantidas em área privada, separadas dos resultados finais. ROMs diagnósticas obsoletas foram removidas para espaço, mantendo originais, hashes e logs.

O primeiro retorno da rota foi colocado no meio de piso livre e não disparou. Normalizar os atributos do tile não bastou. A [rotina de referência HGSS](https://github.com/pret/pokeheartgold/blob/master/src/field/field_control.c) verifica colisão do tile à frente antes das saídas direcionais; o portal de retorno foi reposicionado **no trecho nativo de teste**, em `(12,14)`, voltado ao obstáculo nativo `(11,14)`. Ida e volta passaram depois dessa correção. O evento da Vila e sua geometria não foram deslocados para contornar o problema.

## Procedimento reproduzível

Pré-condições: ROM-base legítima IPKE rev.0, ambiente ativado, originais do pacote em área privada e fontes próprias deste checkpoint. Para um build limpo, invalidar conjuntamente objetos, extração e marcadores gerados externos, conforme o diagnóstico acima. Reutilizar compilador e auxiliares existentes.

```bash
source /workspace/.hg-env/activate
make
python -B tools/hollowtide/integrate_village.py test.nds /caminho/privado/Hollowtide_Vila_Inicial /caminho/privado/novo/game.nds
TZ=America/Sao_Paulo python -u -B tools/hollowtide/test_village_runtime.py /caminho/privado/novo/game.nds --initial-dsv /caminho/privado/cp02/game.dsv --work-dir /caminho/privado/novo-ensaio
TMPDIR=/workspace/work PYTHONDONTWRITEBYTECODE=1 python -B -m unittest discover -s tests/hollowtide -v
```

Os destinos devem ser inéditos e externos ao checkout; os scripts recusam sobrescrever arquivos. O save inicial é copiado para configuração nova. A persistência é comprovada depois pelo SAVE do jogo, encerramento do processo e CONTINUE em outro; não por importação de bateria ou savestate. A telemetria de campo/altura é somente leitura. O fuso explícito serve para registrar a condição visual de iluminação no ensaio, sem alterar a hora do sistema.

## Evidências e resultados

**ROM final:** `/workspace/work/hollowtide/cp04/final/game.nds`, **193.020.616 bytes**, SHA-256 `e6a1e7d6ca24cf8bd722c861905ddfe8249c463c532bcc1ee8bdebed2c1cdcb2`. O serializador não conserva o padding de 256 MiB do build normal. O hash do relatório de emulação foi comparado ao arquivo final e ao relatório de instalação; todos coincidem.

O percurso completo **na mesma ROM final** terminou com exit 0 e **34 checkpoints de execução aprovados**, em `cp04/runtime-verified/results.json`. O núcleo é DeSmuME 0.9.12 via py-desmume 0.0.9, renderer software headless; não é simulação do resultado do jogo. Comandos, frames, posições, alturas e hashes das capturas estão nos logs.

| Teste real | Resultado | Evidência sob `runtime-verified/` |
| --- | --- | --- |
| Entrada na Vila a partir do laboratório | Header 60 acessível e protagonista controlável | `session01/02-village-arrival.png` |
| Escadaria esquerda | Topo 1 tile → meio 0,49969 → base 0; subida de volta também passou | `03-left-stair-top`, `04-left-stair-middle`, `05-left-stair-bottom`, `06-left-stair-return` em `session01/` |
| Escadaria direita | Base 0 → meio 0,50053 → topo 1; descida de volta passou | `12-right-stair-bottom` a `15-right-stair-return` em `session01/` |
| Limites/colisões | Escarpa, árvores à esquerda e borda sul bloquearam o movimento nos pontos ensaiados | `07-cliff-blocked`, `18-tree-boundary-blocked`, `19-south-boundary-blocked` |
| Dois NPCs e diálogos próprios | Texto exibido; fechar diálogo libera movimento | `08-greeting-dialogue`, `09-dialogue-released`, `20-laboratory-dialogue` |
| Três interiores e portas | Entrada, saída e retorno ao ponto correto da Vila em todos | Prefixos `10-west-house`, `11-player-house`, `17-laboratory` |
| Fonte, postes e materiais | Fonte texturizada e postes sem os planos brancos; recursos visuais conferidos | `16-fountain-and-windmills`; diagnóstico antes/depois em `fixed-night-session/` e `probe-session/` |
| Saída pela floresta e retorno | Vila 60 → trecho 33, caminhada → Vila 60, com passo para fora da passagem | `19a-forest-entrance` a `19e-forest-outside` |
| Salvamento nativo e recarga persistente | SAVE no jogo, fechamento do processo, CONTINUE em outro; recupera `(16,27)`, depois move a `(15,27)` | `session01/22-save-prompt.png`, `23-save-complete.png`, `session02-cold-load/24-persistent-cold-load.png`, `25-movement-after-load.png` |

Nomes sem extensão na tabela são PNGs. Capturas finais de ambos os diálogos, fonte/postes, campo recarregado e entrada florestal foram inspecionadas; as asserções do controlador não substituem revisão visual. O relatório mantém `visual_review_required: true` para não atribuir aprovação artística automática ao script. Todos os processos de emulação foram encerrados.

31 testes sintéticos independentes passaram: 24 anteriores + 7 regressões de índices Nitro, mescla de recursos, restrição dos ajustes PER, ABI dos NPCs e backlinks. Não contêm assets Nintendo e não contam como emulação. Três ensaios negativos reais do CLI recusaram reaplicar a integração, usar um asset alterado e escrever a ROM dentro do checkout; exit 1, nenhum NDS escrito. `visual-preservation.json` confirma os 15 originais intactos, seções protegidas exatas e igualdade dos pixels, parâmetros das 16 texturas de mapa/40 de edifícios e cores das paletas; só os índices reconstruídos diferem.

Artefatos privados, sob `/workspace/work/hollowtide/cp04/`: `intake.json`, `build-results.json`, `build-normal.log`, `build-normal-retry.log`, `integration-final.log`, `final/game.nds`, `final/game.nds.json`, relatórios/inputs/screenshots das sessões e patches para revisão. A ROM normal compilada é `/workspace/hg-engine/test.nds`. A ROM-base permanece `/workspace/hg-engine/rom.nds`, hash `65f02a56842b75aa92d775d56d657a56fe3fa993550b04dc20704ab82d760105`.

Nenhuma ROM, save, dump, arquivo de mapa, imagem extraída ou captura de emulador é incluída no Git. São versionados somente ferramentas/testes próprios, script e duas linhas de diálogo originais, documentação e instruções de continuidade. Integração técnica não substitui aprovação artística do diretor, nem validação em hardware ou teste integral da campanha.

## Limites e próximo checkpoint

O ensaio parte do save técnico CP02 após receber Cyndaquil. Nova partida e progressão completa **na ROM CP04** não foram repetidas; as evidências CP02 não são reatribuídas a esse build. A cobertura é o percurso registrado, não a inspeção de cada tile ou de todas as condições horárias. Nomes/seções globais e os interiores ainda são nativos; NPCs e diálogos são protótipos. A GUI PDSMS/DSPRE e hardware não foram executados.

A base técnica está pronta, no recorte testado, para receber a Rota 01 e interiores autorais. O próximo checkpoint deve substituir o cenário de rota provisório pelo export autoral, manter o retorno já ensaiado e validar os estados de início/progressão da campanha. A direção visual permanece com o usuário; novas revisões dos assets exigem nova auditoria, sem adaptar a arte por suposição.

## Arquivos versionados

- Novos: `tools/hollowtide/integrate_village.py`, `tools/hollowtide/test_village_runtime.py`, `tests/hollowtide/test_village_integration.py`, `data/scr_seq/scr_seq_00965_hollowtide_village.s`, `data/text/854.txt` e este relatório.
- Atualizado `tools/hollowtide/emulator_session.py` com leitura de posição/altura, sem escrita de memória.
- Atualizados `AGENTS.md` e os documentos README, BUILD, ROADMAP, BLOCKERS, TEST_REPORT, CHANGELOG, DEVELOPMENT_DIRECTIVE, GITHUB_REVIEW, MAP_EXPORT, MAP_INTEGRATION e MAP_LAB.
- Diff e inventário completos: `/workspace/work/hollowtide/cp04/review/checkpoint04.patch` e `checkpoint04-stat.txt`. O head local e a auditoria de publicação ficam no mesmo diretório; não houve push.
