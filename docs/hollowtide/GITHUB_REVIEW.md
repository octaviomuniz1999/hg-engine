# Revisão antes de preservar os checkpoints no GitHub

Este documento preserva a **revisão histórica preparada no CP03**. Posteriormente, o usuário autorizou exclusivamente o head `9e8e0adff` e seus ancestrais, e essa branch foi publicada no fork, sem force push, mudança de main ou PR. A diretriz `16316f079` e o CP04 são posteriores e **não foram publicados**. Novos commits exigem nova autorização; a revisão histórica abaixo não a constitui.

## Proposta acumulada do CP03

Destino consultado somente para leitura: fork público [octaviomuniz1999/hg-engine](https://github.com/octaviomuniz1999/hg-engine). Publicação proposta **somente da branch de desenvolvimento `codex/hollowtide-checkpoint-03`**, com CP01 e CP02 como ancestrais, sem squash, alteração de main ou force-push. As branches locais congeladas dos checkpoints anteriores permanecem intactas. Não é proposta a distribuição de ROMs ou saves.

O head definitivo é registrado após o commit em `/workspace/work/hollowtide/cp03/review/review-head.txt` e na resposta do checkpoint. Confirmar esse SHA antes de qualquer publicação. **Revisão humana e autorização continuam pendentes**, incluindo qualquer PR futuro.

| Etapa | Diff a revisar | Escopo |
| --- | --- | --- |
| CP01 | base → `1e2bf5a33` | 16 arquivos, +1.089/−1; detalhes abaixo |
| CP02 | `1e2bf5a33` → `6f3625641` | 17 arquivos, +747/−9: cenários de batalha, controlador/telemetria e documentação de runtime |
| CP03 | `6f3625641` → branch CP03 | Importador/preparador de calibração, dez testes sintéticos, instruções/relatório/revisão e ignores de saves |

CP03 acrescenta `tools/hollowtide/map_lab.py`, `prepare_map_calibration.py`, `tests/hollowtide/test_map_lab.py`, `docs/hollowtide/CHECKPOINT03.md`, `MAP_EXPORT.md` e `MAP_LAB.md`. Atualiza `.gitignore` e os documentos de integração, README, bloqueios, roadmap, relatório, histórico e esta revisão. Não há mudança em fontes C/assembly originais, Makefiles ou lockfiles; os quatro arquivos C de teste são exclusivamente adições CP02 em `data/battle_tests/hollowtide/`.

O diretório privado `/workspace/work/hollowtide/cp03/review/` contém:

```text
checkpoint01.patch
checkpoint02.patch
checkpoint03.patch
full-development.patch
full-development-stat.txt
review-head.txt
checkpoints01-02-audit.json
publication-audit.json
patch-hashes.json
```

Reproduzir a revisão local:

```bash
git diff --stat dbb321327c59b821507f9fc4cb6c41d45a9d2698 codex/hollowtide-checkpoint-03
git diff dbb321327c59b821507f9fc4cb6c41d45a9d2698 codex/hollowtide-checkpoint-03
git log --oneline --reverse dbb321327c59b821507f9fc4cb6c41d45a9d2698..codex/hollowtide-checkpoint-03
```

A auditoria percorreu cada versão de cada blob adicionado/modificado em **todos os commits desde a base**, inclusive versões intermediárias depois substituídas. Nos commits CP01/02, 29/46 blobs únicos respectivamente: UTF-8, sem NUL/binários, extensões de código/documentação e caminhos Hollowtide esperados. O CP03 recebe a mesma varredura após o commit. Não foram detectados ROMs, saves, dumps, fontes externas copiadas ou arquivos comerciais nos deltas; os textos foram revisados como documentação/código autoral. Isso não é certificação jurídica dos assets já herdados do upstream.

Validação acumulada: histórico CP01/02 íntegro; ROM-base/normal com hashes preservados; 24 testes sintéticos e quatro recusas de integração CP03; calibração nativa executada no DeSmuME. Build e batalhas CP01/02 não foram repetidos nem atribuídos a CP03. Export PDSMS autoral e alturas novas seguem pendentes.

Após aprovação explícita, conferir novamente head local, diff e ref de destino; somente então realizar o push normal desta branch. Se a ref já existir com conteúdo divergente, investigar sem forçar. Criar PR requer autorização própria; nenhuma dessas operações foi executada neste checkpoint.

## Revisão histórica: escopo congelado do CP01

- Branch local: `codex/hollowtide-foundation`.
- Head a revisar: `1e2bf5a33`.
- Base: `dbb321327c59b821507f9fc4cb6c41d45a9d2698`.
- Remote local de destino: `origin`, fork `octaviomuniz1999/hg-engine`. Nenhuma ref remota foi alterada.
- CP02 continua separadamente em `codex/hollowtide-checkpoint-02`.

Commits do CP01:

```text
269bf027c Prepare Hollowtide offline audits and map asset handoff
7dd82e579 Record ROM attachment transfer size blocker
1e2bf5a33 Validate Hollowtide ROM builds and visible text proof
```

## Diff para revisão

O diff completo, sem truncamento, está em:

```text
/workspace/work/hollowtide/cp02/review/checkpoint01.patch
/workspace/work/hollowtide/cp02/review/checkpoint01-stat.txt
```

Reproduzir sem acessar ou escrever no GitHub:

```bash
git diff --stat dbb321327c59b821507f9fc4cb6c41d45a9d2698 1e2bf5a33
git diff dbb321327c59b821507f9fc4cb6c41d45a9d2698 1e2bf5a33
```

São **16 arquivos, 1.089 linhas adicionadas e uma removida**. Os arquivos adicionados são texto/documentação/código; não há adição de ROM, save, screenshot, dump privado ou arquivo binário.

| Arquivos do CP01 | Resumo do diff |
| --- | --- |
| `.gitignore` | Ignora os textos privados gerados 219/442; adiciona newline final |
| `docs/hollowtide/README.md`, `BUILD.md`, `ROADMAP.md`, `BLOCKERS.md`, `CHANGELOG.md`, `TEST_REPORT.md`, `ROM_CHECKPOINT.md` | Estado do projeto, procedimentos e evidências reais dos builds/boot |
| `docs/hollowtide/LINKER_AUDIT.md`, `MECHANICS_AUDIT.md` | Auditorias técnicas, sem reimplementar a engine |
| `docs/hollowtide/MAP_INTEGRATION.md`, `templates/MAP_RECORD.md` | Fluxo de integração e ficha sem IDs arbitrários |
| `tests/hollowtide/test_offline_integration.py` | 14 testes sintéticos independentes de ROM |
| `tools/hollowtide/validate_map_bundle.py` | Validação de integridade, sem importação de mapas |
| `tools/hollowtide/prepare_text_smoke_test.py`, `verify_text_smoke_test.py` | Geração privada da pequena prova de texto e conferência do delta da ROM |

Trecho completo da mudança funcional na configuração do Git:

```diff
 /data/generated/
+# Private text generated from the owner's ROM for Hollowtide technical proofs.
+/data/text/custom/219.txt
+/data/text/custom/442.txt
 /armips/include/generated/
```

O restante deve ser revisado no patch completo. O CP01 não altera C/assembly, dados de gameplay rastreados ou Makefiles originais. Os resultados de CP02 não foram retroativamente atribuídos aos testes de CP01.

## Descrição proposta para preservação/revisão

Título: `Prepare Hollowtide development foundation and reproducible ROM smoke proof`.

Descrição: documenta o ambiente restaurado e os gates de build, explica a resolução de Newlib no linker atual e acrescenta ferramentas para receber assets e produzir/verificar uma pequena mudança de texto com uma ROM fornecida pelo proprietário. A prova foi recompilada e observada no DeSmuME; mapas personalizados e mecânicas de batalha eram pendentes naquele checkpoint.

Validação do CP01: 14 testes offline; checagens Python/texto; três builds com exit 0; delta de uma entrada de texto conferido; boot e marcador observados. Nenhuma ROM ou asset extraído acompanha o diff.

## Depois da revisão

Somente após autorização explícita para publicar, confirmar que a branch local ainda aponta ao head revisado e verificar a ref remota antes de executar qualquer push. O escopo histórico isolado de CP01 é `codex/hollowtide-foundation`; a proposta acumulada atual inclui também CP02/CP03, conforme a revisão no início deste documento. Não fazer force-push nem publicar a ROM como release/artefato.
