# CP05-A — preservação e colisões localizadas

Base funcional: CP04 `4784b55b7`, finalização `a679364bc`. Branch própria `codex/hollowtide-checkpoint-05`; a branch anterior permanece congelada. Ordem atual em [CHECKPOINT05_ORDER.md](CHECKPOINT05_ORDER.md). CP01–04 conferidos como ancestrais, sem reescrita. ROM CP04 e 15 assets originais presentes; hash da ROM corresponde exatamente ao relatório anterior.

Reproduzido no DeSmuME: jogador entra na fonte `(24,7)` e nas bases dos mastros `(21,5)`/`(27,5)`. PER liberava esses objetos. Nova ferramenta `fix_village_collisions.py` bloqueia 11 tiles: bacia da fonte x23–25/z6–8 e os dois mastros. Só o bit de colisão é acrescentado; nenhum comportamento/flag anterior removido. Aplicação separada após instalação CP04 mantém sua receita original intacta.

Os dois postes luminosos foram inspecionados em `(12,14)` e `(4,14)`. As capturas mostram o jogador junto à lateral da base; não justificam ampliar automaticamente o bloqueio ou mover o poste. Bordas desses objetos e possíveis contatos parciais da fonte/mastros ficam para revisão visual localizada. Não se afirma cobertura de todos os objetos/tiles. Casas, árvores e geometria não foram movidas ou removidas.

## Evidência executada

15 checkpoints localizados aprovados em DeSmuME 0.9.12: quatro lados da fonte, os dois mastros, base/meio/topo das duas escadas, entrada/retorno do laboratório e movimento posterior. O controlador também verifica conectividade até as três portas, NPCs e passagem florestal. As demais casas não foram reemuladas porque seus dados não mudaram. Sem repetição da bateria completa CP04 ou batalhas. Este teste usa uma cópia privada da bateria legítima criada na partida nova anterior: não representa teste de nova partida CP05.

Empacotamento sem compilação: apenas membro 676 do arquivo land-data é diferente; seções BGS, BLD, NSBMD, BDHC exatas, todos os outros membros/arquivos e ARM9/ARM7/overlays preservados. Hash da ROM: `3d4f4eba16b4a00720c32ef10492f0ef42f19bc43295bc4225323d295424589d`. Nenhuma reinstalação.

Artefatos privados em `/workspace/work/hollowtide/cp05/`: `object-probe/` e `lamp-probe/` (antes), `a/game.nds`, `a/game.nds.json`, `a-integration.log`, `a-runtime/` (depois), `a-runtime.log`. Resultados completos, posições, alturas, comandos e capturas estão em `a-runtime/results.json` e `session/input-events.jsonl`.

```bash
source /workspace/.hg-env/activate
python -B tools/hollowtide/fix_village_collisions.py /workspace/work/hollowtide/cp04/final/game.nds /workspace/work/hollowtide/cp04/incoming/Hollowtide_Vila_Inicial /caminho/privado/novo/game.nds
TZ=America/Sao_Paulo python -u -B tools/hollowtide/test_village_object_collisions.py /caminho/privado/novo/game.nds --initial-dsv /caminho/privado/game.dsv --work-dir /caminho/privado/ensaio-novo
```

A auditoria desta subetapa se limita ao delta novo: ferramentas próprias e Markdown, sem ROMs/saves/dumps/assets. A autorização CP05 permite preservar esse código no fork em branch separada; sem main, force ou PR. O commit remoto e recibo ficam em `/workspace/work/hollowtide/cp05/`.

O disco estava com 115 MiB livres. Foi removido somente o cache obsoleto `cp04/before-build/build` (525 MiB), com inventário em `retired-build-cache.json`; o build atual, todas as ROMs, saves, logs e assets anteriores foram preservados. Não foi necessário reconstruir a engine nesta etapa.

Próximo: CP05-B, auditoria dos recursos completos de Snivy/Fennekin/Mudkip antes de alterar escolhas e laboratório. CP05-C introdução/mãe permanece pendente. Nada da Rota 01 definitiva foi implementado.
