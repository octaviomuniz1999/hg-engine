# Laboratório de integração CP03

`tools/hollowtide/map_lab.py` é uma ferramenta externa de ensaio, sem participação no Makefile. Lê a ROM já compilada e grava uma **nova ROM privada**, sem sobrescrever a entrada. O único caso emulado até aqui usa geometria nativa de Elm, uma colisão, um assistente clonado e duas portas experimentais. Não é um mapa autoral ou um export gerado pelo PDSMS.

## Recursos e formato confirmados

| Recurso HGSS | Localização |
| --- | --- |
| Headers estáticos IPKE rev.0 | ARM9 descomprimido, `0xF6BE0`, 540 registros de 24 bytes; recusa o marcador de headers dinâmicos |
| Land-data: modelo, permissões, terreno, edifícios e som | `a/0/6/5` |
| Matrizes | `a/0/4/1` |
| Área / texturas do mapa | `a/0/4/2` / `a/0/4/4`; map-tileset é o **segundo** u16 da área, depois do building-tileset |
| Eventos / scripts / mensagens | `a/0/3/2` / `a/0/1/2` / `a/0/2/7` |
| Modelos de edifícios externos / internos | `a/0/4/0` / `a/1/4/8`; não são incorporados automaticamente ao BIN |

O BIN HGSS começa com quatro u32 little-endian: tamanhos de PER, BLD, NSBMD e terreno. Seguem **BGS, PER, BLD, NSBMD, BDHC/BDHCAM**. BGS tem assinatura `0x1234` e u16 de tamanho, além do cabeçalho de 4 bytes. PER tem 2.048 bytes, dois por tile em ordem de linhas, 32×32. O experimento altera somente o bit `0x80` do segundo byte de um tile, retendo os demais bits; não normaliza permissões a 00/80. BLD contém registros de 48 bytes.

O parser confere limites, tamanho total, envelope Nitro do modelo e tamanho mínimo das tabelas BDHC. Não valida todos os índices internos, materiais, câmera, geometria, semântica de alturas ou custo de renderização. Copia cada seção recebida byte a byte; mantém eventual extensão de câmera opaca. Altitude da célula na matriz é distinta do terreno BDHC e é preservada.

Eventos: contagem u32 seguida de registros, nas categorias background (20 bytes), NPC (32), warp (12) e trigger (16). NPC usa coordenadas X/Z e Y fixed-point, não os eixos Y/Z da interface do DSPRE. A clonagem do ensaio reutiliza gráfico, movimento e script de um NPC conhecido, fornece ID único e flag de ocultação zero. Não constitui criação de um script de diálogo novo. Warp guarda X/Z, header de destino, **índice do warp no destino** e altura; header, matriz, land-data, evento e script são IDs diferentes.

## Reprodução privada a partir do CP02

Usar a ROM normal **congelada do CP02**, hash `f85b23be04e265f63f961326528cb9c080bacf2be34c4dbf9c03ec4ff558ffd5`, preservada privadamente em `/workspace/work/hollowtide/cp02/normal/game.nds`. O `test.nds` atual já incorpora as adições CP04 e é recusado corretamente pelo preparador CP03. Cada destino deve ser novo e externo ao checkout; ajustar `cp03-rerun` para uma pasta inédita.

```bash
source /workspace/.hg-env/activate
python -B tools/hollowtide/map_lab.py inspect /workspace/work/hollowtide/cp02/normal/game.nds 61
python -B tools/hollowtide/prepare_map_calibration.py /workspace/work/hollowtide/cp02/normal/game.nds /workspace/work/hollowtide/cp03-rerun/intake
python -B tools/hollowtide/map_lab.py apply /workspace/work/hollowtide/cp02/normal/game.nds /workspace/work/hollowtide/cp03-rerun/intake/plan.json /workspace/work/hollowtide/cp03-rerun/game.nds
```

O preparador verifica a identidade da ROM; lê o membro 244 (Elm), divide/remonta e exige igualdade integral. Depois bloqueia `(5,11)`, adiciona NPC 8 em `(6,12)` clonando o assistente de índice 2, e configura as portas 61/warp0 ↔ 63/warp0. Arquivos privados: `calibration.bin`, `plan.json`, ROM derivada e relatório `.nds.json`. Nenhum byte extraído é armazenado nos fontes.

O importador acrescenta land-data 676, conserva 244 e muda apenas a célula da matriz 100, exclusiva do header 61. Muda os eventos 58 e 60. Texturas, área, edifícios, scripts e executáveis permanecem idênticos. Verifica novamente o filesystem serializado e todos os membros NARC não envolvidos. Somente os arquivos `a/0/6/5`, `a/0/4/1`, `a/0/3/2` podem mudar; o relatório de empacotamento sempre começa com `emulation_validated: false`.

## Plano para outro BIN

`inspect ROM HEADER` fornece hashes e referências. `export ROM HEADER DESTINO.bin` exporta um único mapa nativo para comparação privada. Para aplicar um BIN recebido, preparar/revisar JSON com os campos abaixo (não são um formato do PDSMS):

- `schema: 1`, `rom_sha256`, `header`, `old_land_sha256`.
- `map_bin`: caminho local relativo à pasta do plano; `map_sha256`.
- `texture_policy: "reuse-existing-area"`, `texture_sha256`: textura **de mapa** selecionada pela área atual. Exige conferir os nomes de materiais/texturas externamente; o hash não prova compatibilidade de um novo modelo.
- `event_edits`: lista opcionalmente vazia; cada entrada contém `header`, `expected_sha256`, `clone_npcs` e/ou `warps`. A estrutura completa é gerada pelo preparador; não é necessário redigir offsets manualmente.

A importação atual exige uma matriz exclusiva 1×1, sem grade de headers. Recusa matriz compartilhada (ex.: casa 63 compartilha matriz 71 com header 66), eventos compartilhados, hashes divergentes, IDs de NPC duplicados e warps de destino inexistentes. Não implementa remapeamento de NSBTX, modelos externos, expansão de matrizes, novos pontos de warp ou scripts. Não usar o gerador de calibração como plano de campanha.

## Sessão real de validação

Usar `emulator_session.py` com `--session-dir` e `--config-dir` externos, separados de CP02. Criar primeiro `CONFIG/desmume/`; copiar apenas para esse laboratório o save de teste do proprietário, com o stem correspondente à ROM. Não reutilizar seu save principal. Configurar XDG antes de importar DeSmuME. O núcleo é real, com renderer headless; screenshots e leituras de campo são gravados no log.

Após carregar o save de Elm `(4,11)`, tentar RIGHT e comparar com a ROM normal; caminhar DOWN no piso livre. Sair pela porta, confirmar header 63, afastar-se da porta, retornar e confirmar header 61. Atravessar a área, interagir com o novo assistente em `(6,12)`, fechar o diálogo e mover novamente. A primeira carga do save antigo não mostrou o clone, comportamento compatível com reaproveitamento dos objetos salvos; **sair e voltar realmente recarregou os eventos e exibiu o NPC**, sem injeção de objetos na memória. A causa interna do carregamento de objetos não foi rastreada no código original.

Gates ainda necessários para um mapa autoral: texturas/materiais corretos, comparação com preview, todos os limites, alturas/rampas nos dois sentidos, entradas, NPCs/scripts próprios, estados persistentes e performance. CP03 não recompilou a engine: aplicou recursos depois do build normal comprovado, evitando reaplicar patches sobre a mesma ROM. A edição de uma base via DSPRE, seguida de build limpo, permanece uma rota futura separada; considerar a precedência das fontes documentada em [MAP_INTEGRATION.md](MAP_INTEGRATION.md).

## Fontes de formato

- [PDSMS 2.2 MapBinHGSS](https://github.com/Trifindo/Pokemon-DS-Map-Studio/blob/4eed1d62cb1534a973ee9cd1cf1665628cb9a705/src/main/java/formats/mapbin/MapBinHGSS.java) e [BdhcWriterHGSS](https://github.com/Trifindo/Pokemon-DS-Map-Studio/blob/4eed1d62cb1534a973ee9cd1cf1665628cb9a705/src/main/java/formats/bdhc/BdhcWriterHGSS.java).
- DSPRE fixado em `e751187b45d6ddf237a24dab8407a5a6cf0d36dd`: [MapFile](https://github.com/DS-Pokemon-Rom-Editor/DSPRE/blob/e751187b45d6ddf237a24dab8407a5a6cf0d36dd/DS_Map/ROMFiles/MapFile.cs), [GameMatrix](https://github.com/DS-Pokemon-Rom-Editor/DSPRE/blob/e751187b45d6ddf237a24dab8407a5a6cf0d36dd/DS_Map/ROMFiles/GameMatrix.cs), [EventFile](https://github.com/DS-Pokemon-Rom-Editor/DSPRE/blob/e751187b45d6ddf237a24dab8407a5a6cf0d36dd/DS_Map/ROMFiles/EventFile.cs), [AreaData](https://github.com/DS-Pokemon-Rom-Editor/DSPRE/blob/e751187b45d6ddf237a24dab8407a5a6cf0d36dd/DS_Map/ROMFiles/AreaData.cs).

As fontes foram lidas para interoperabilidade; nenhum arquivo desses projetos foi copiado para o Git Hollowtide.
