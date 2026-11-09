# Checkpoint 03 — fundação visual experimental

Execução em 2026-11-09 UTC (noite de 2026-11-08 no Brasil). Branch local `codex/hollowtide-checkpoint-03`, descendente direta de CP02. **Nenhum push ou PR realizado.** A campanha, os fontes originais e as ROMs de entrada foram preservados.

## Preservação

- CP01 permanece `1e2bf5a3375c23b9cf761b3a1c89c087a7fb140a`, branch `codex/hollowtide-foundation`.
- CP02 permanece `6f3625641c697747d631a90c208ebae92fe62513`, branch `codex/hollowtide-checkpoint-02`.
- `git fsck --full --no-reflogs`: exit 0, sem erros; ancestralidade confirmada. São três commits CP01 e um CP02 desde `dbb321327c59b821507f9fc4cb6c41d45a9d2698`.
- Auditoria de **cada versão adicionada/modificada em cada commit**, não apenas do head: CP01 tem 16 caminhos e 29 blobs de texto únicos; até CP02, 25 caminhos e 46 blobs. Todos nos namespaces Hollowtide e `.gitignore`; nenhum blob binário, ROM, save, dump ou arquivo comercial detectado nas alterações. Assets herdados do upstream não são uma nova auditoria de licenciamento de todo o jogo.
- Destino preparado: fork público `octaviomuniz1999/hg-engine`, `origin`; metadados consultados somente para leitura. Branch de desenvolvimento proposta: `codex/hollowtide-checkpoint-03`, preservando CP01/CP02 como ancestrais. Revisão em [GITHUB_REVIEW.md](GITHUB_REVIEW.md).

## Implementação

- `map_lab.py`: inspeção, export privado, parser de seções HGSS, plano com hashes, importação por membro NARC e verificação do delta serializado. Não modifica Makefile, fontes ou código executável.
- `prepare_map_calibration.py`: gera a calibração privada a partir da ROM normal conhecida. Geometria, edifícios, texturas, som e BDHC **nativos**, sem mapa autoral fictício.
- Matriz 100/header 61 passa a usar o novo land-data 676, mantendo 244. Permissão `(5,11)` recebe somente o bit bloqueado `0x80`. NPC 8 em `(6,12)` clona o assistente de índice 2 e seu script original. As portas existentes dos headers 61 e 63 apontam uma para a outra, somente na ROM experimental.
- `.gitignore` passa a proteger também DSV, DST, DS0–DS9 e DUC. Saves e derivados continuam fora do checkout.
- Instruções de exportação/recursos e limitações em [MAP_EXPORT.md](MAP_EXPORT.md), [MAP_LAB.md](MAP_LAB.md) e [MAP_INTEGRATION.md](MAP_INTEGRATION.md).

## Comandos e testes efetivamente executados

```bash
source /workspace/.hg-env/activate
git fsck --full --no-reflogs
TMPDIR=/workspace/work PYTHONDONTWRITEBYTECODE=1 python -B -m unittest discover -s tests/hollowtide -v
python -B tools/hollowtide/map_lab.py inspect test.nds 61
python -B tools/hollowtide/map_lab.py export test.nds 61 /workspace/work/hollowtide/cp03/native-lab.bin
python -B tools/hollowtide/prepare_map_calibration.py test.nds /workspace/work/hollowtide/cp03/calibration
python -B tools/hollowtide/map_lab.py apply test.nds /workspace/work/hollowtide/cp03/calibration/plan.json /workspace/work/hollowtide/cp03/emulator/game.nds
git diff --check
```

24 testes sintéticos passaram: 14 anteriores + 10 novos para limites de seções/modelo/terreno, round-trip, matriz, eventos, ID de NPC, coordenadas, seleção correta do map-tileset e proteção dos destinos. Fixtures sintéticos não são modelos jogáveis. Quatro ensaios negativos do CLI com a ROM real recusaram hash de ROM incorreto, hash de BIN incorreto, matriz compartilhada e caminho fora da pasta do plano; exit 1, nenhum NDS escrito.

A divisão/remontagem do mapa nativo produziu os mesmos bytes. No empacotamento experimental mudaram apenas file IDs 184/193/217 (`a/0/3/2`, `a/0/4/1`, `a/0/6/5`), eventos 58/60, matriz 100 e novo land-data 676. Executáveis, tabelas de overlays, demais arquivos/membros e todas as texturas foram conferidos; permaneceram idênticos. O hash BDHC continuou `07584c4215ceed2216ba6928d51273b36fa3345815e076390ed5e8ca340980e1`.

### Execução real no DeSmuME

Núcleo DeSmuME 0.9.12, py-desmume 0.0.9, software renderer headless, screenshots reais. Usou-se cópia privada do save de Elm do CP02, não savestate ou escrita de memória. `gFieldSysPtr=0x023DDE58` foi lido para registrar mapa/coordenadas/warps; os controles são botões emulados.

| Teste | Resultado observado | Captura em `cp03/session02/` |
| --- | --- | --- |
| Carga da ROM derivada | Elm 61, `(4,11)`, porta aponta para 63 | `01-cold-load.png` |
| RIGHT contra tile bloqueado | Continua `(4,11)` | `03-right-attempt.png` |
| DOWN em piso livre | Vai a `(4,12)` | `04-walkable-tile.png` |
| Saída do laboratório | Entra na casa 63, warp 0, `(3,11)` | `06-lab-to-house.png` |
| Retorno da casa | Entra no laboratório 61, warp 0, `(4,15)` | `08-house-to-lab.png` |
| Novo assistente | Clone visível em `(6,12)` após recarga real do mapa | `09-reloaded-lab-npc.png` |
| Interação | De `(5,12)`, abre diálogo original; screenshot conferido | `11-npc-dialogue-full.png` |
| Fechar diálogo e caminhar | Sem travamento; move a `(4,12)` | `12-after-dialogue-movement.png` |
| Controle normal separado | Mesmo RIGHT a partir de `(4,11)` chega a `(6,11)` | `cp03/control-session/02-control-right.png` |

As sete asserções de mapa/coordenadas do relatório privado passaram. Não são um teste visual automatizado; as capturas de carga, casa, laboratório recarregado e diálogo foram inspecionadas. A primeira sessão sem stdin persistente encerrou normalmente sem avançar frames; a segunda usou terminal com comandos JSON. Na primeira carga do save antigo, o clone não apareceu; sair/voltar recarregou os eventos e exibiu o NPC. Isso é compatível com objetos reaproveitados do save, mas a causa interna não foi rastreada no código original. O procedimento foi corrigido, sem patch na engine.

Todos os processos do emulador foram encerrados. Não houve novo teste de persistência de save nesta etapa; sua evidência permanece no CP02. Não foram reinstaladas ferramentas ou recompilada a engine. O artefato CP03 é um **empacotamento de recursos após o build normal**, não uma nova compilação C.

## Artefatos privados e identidade

| Artefato | Caminho / SHA-256 |
| --- | --- |
| ROM normal compilada CP01/02, inalterada | `/workspace/hg-engine/test.nds` — `f85b23be04e265f63f961326528cb9c080bacf2be34c4dbf9c03ec4ff558ffd5` |
| ROM experimental CP03 | `/workspace/work/hollowtide/cp03/emulator/game.nds` — `283e0026364375c548dd73c3e338e17e85e442963f7e4c0ee2a02dd06bc25ec3` |
| Plano e relatório de delta | `cp03/calibration/plan.json`, `cp03/emulator/game.nds.json` sob `/workspace/work/hollowtide/` |
| Comandos, screenshots e resultados | `cp03/session02/`, `cp03/control-session/`, `cp03/runtime-results.json`, `cp03/rejection-tests.json` |
| Auditoria de histórico e patches de revisão | `/workspace/work/hollowtide/cp03/review/` |

ROM-base `rom.nds` continua 128 MiB, modo 0444, hash `65f02a56842b75aa92d775d56d657a56fe3fa993550b04dc20704ab82d760105`. ROM normal tem 256 MiB; a derivada tem **192.935.112 bytes**: o serializador ndspy reorganiza offsets/alinhamento e não conserva o padding final de 256 MiB. O delta descrito acima compara conteúdo de arquivos/membros, não igualdade dos offsets físicos da ROM. Nenhuma ROM, save, arquivo extraído, captura ou fonte externa de editor acompanha o commit.

## Limites e próximo gate

**Aprovado no recorte testado:** substituição do membro nativo por cópia alterada, colisão controlada, preservação binária de BDHC, eventos/NPC e transição de ida/volta no DeSmuME. **Pendente:** export PDSMS real, aparência autoral, novas texturas/materiais, edifícios próprios, rampas/alturas novas, câmera, matrizes maiores, novos scripts e validação em hardware. A preservação de bytes de terreno plano não prova rampas corretas.

O próximo checkpoint técnico é receber o primeiro pacote da [ficha de exportação](MAP_EXPORT.md), conferir materiais/recursos, importar uma célula isolada e percorrer cada colisão/altura/entrada no emulador comparando com o preview. A aprovação artística permanece com o diretor. A publicação dos commits é outro gate: exige revisão do diff e autorização explícita antes de push ou PR.
