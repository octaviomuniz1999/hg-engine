# Revisão antes de preservar o Checkpoint 01 no GitHub

**Nada foi publicado.** O pedido exige revisão do diff antes de qualquer publicação; não foi feito push nem criado PR. Este documento prepara a revisão, não constitui aprovação.

## Escopo congelado do CP01

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

Somente após autorização explícita para publicar, confirmar que a branch local ainda aponta ao head revisado e verificar a ref remota antes de executar qualquer push. O escopo de CP01 é apenas `codex/hollowtide-foundation`; o checkpoint 02 exige revisão própria. Não fazer force-push nem publicar a ROM como release/artefato.
