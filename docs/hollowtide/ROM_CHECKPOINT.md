# Checkpoint: build, modificação e boot comprovados

Data: 2026-11-08. Base hg-engine: `dbb321327c59b821507f9fc4cb6c41d45a9d2698`. Branch: `codex/hollowtide-foundation`.

## ROM recebida e proteção dos arquivos

As oito partes RAR fornecidas pelo proprietário foram baixadas e processadas pela `libarchive.so.13` já instalada. A leitura completa e a extração não reportaram erros. Nenhum descompactador ou dependência foi instalado.

O membro extraído é `rom.nds`, 134.217.728 bytes (128 MiB), título `POKEMON HG`, game code `IPKE`, revisão 0 e unit code 0. Os CRCs de cabeçalho e logo conferem. `ndspy` leu ARM9, ARM7 e 513 arquivos de filesystem. Isso confirma os checks descritos, não autentica o dump inteiro como original de fábrica.

Tamanhos/hashes das partes e SHA-256 da ROM recebida estão em `/workspace/work/hollowtide/incoming/`, fora do Git. A base no checkout está ignorada pelo Git e foi colocada em modo somente leitura. Os antigos caches gerados foram arquivados em `before-initial-build/`; as ferramentas restauradas foram reutilizadas.

## Três builds efetivamente executados

Todos usaram o ambiente ativado e `make` serial normal, sem override de game code, linker ou flags de gameplay. Cada execução retornou **exit 0**, terminou com `Done. See output test.nds.` e gerou uma ROM de 268.435.456 bytes (256 MiB). Não houve linhas `warning:` ou `error:` nos logs.

| Build | Alteração | Log privado |
| --- | --- | --- |
| Baseline | Engine sem mudança de texto da prova | `/workspace/work/hollowtide/build-initial.log` |
| Prova de menu | `NEW GAME` → `TEST RUN`, arquivo de mensagens 442, entrada 1 | `/workspace/work/hollowtide/build-menu-proof.log` |
| Prova final de tutorial | Marcador `Hollowtide build test.` no arquivo 219, entrada 7; prova anterior removida | `/workspace/work/hollowtide/build-intro-proof.log` |

O resultado final está em `/workspace/hg-engine/test.nds`. Cópias privadas e relatórios de hash estão em `baseline/`, `menu-proof/` e `intro-proof/` sob `/workspace/work/hollowtide/`. Nenhuma ROM ou texto completo extraído foi adicionado ao Git ou publicado.

A Newlib não precisou de qualquer ajuste. A ligação real com os scripts originais passou; a limitação de resolução para usos ARM genéricos continua explicada em [LINKER_AUDIT.md](LINKER_AUDIT.md).

## Reprodução da prova final

O script versionado contém somente a transformação mínima. Ele lê os dados do proprietário e gera o arquivo privado `data/text/custom/219.txt`, ignorado pelo Git. `narcs.mk` já inclui textos custom no arquivo `a/0/2/7`; nenhuma regra de build foi acrescentada.

```bash
source /workspace/.hg-env/activate
python -B tools/hollowtide/prepare_text_smoke_test.py \
    --rom rom.nds --target intro --work-dir /workspace/work/hollowtide/intro-proof
make
python -B tools/hollowtide/verify_text_smoke_test.py \
    /workspace/work/hollowtide/baseline/test.nds test.nds \
    --target intro --work-dir /workspace/work/hollowtide/intro-proof \
    --report /workspace/work/hollowtide/intro-proof/verification.json
```

O preparador recusa sobrescrever o texto gerado existente. Para repetir, primeiro arquivar esse arquivo privado. Para retirar a prova, arquivar/remover o texto gerado **e restaurar a proveniência do NARC de mensagens**, invalidando a extração ou repondo o NARC do baseline antes do build. Remover o `.txt` sozinho não desfaz o arquivo já modificado em `base/root/`.

Entre a prova de menu e a de tutorial, o texto 442 foi arquivado fora do checkout e o NARC de mensagens de `base/root/` foi reposto a partir do baseline, antes da compilação seguinte. A verificação final confirmou ausência do marcador antigo.

## Evidência estrutural e visual

Para cada prova, o verificador confirmou:

- Tabela de nomes serializada, ARM9, ARM7 e tabelas de overlays idênticos ao baseline.
- Único arquivo de filesystem diferente: ID 179, caminho `a/0/2/7`.
- Único membro de mensagens e única entrada decodificada modificados, exatamente com o texto planejado.

O baseline iniciou no DeSmuME 0.9.12/py-desmume 0.0.9, exibiu a tela de título e chegou ao tutorial após 2.104 frames observados. A versão final chegou ao tutorial após 1.924 frames e a captura foi inspecionada: **`Hollowtide build test.` / `Technical preview.` visíveis**, com os botões do tutorial preservados. Captura privada: `/workspace/work/hollowtide/intro-proof/screens/intro-proof.png`.

A primeira prova de menu compila e passa na comparação estrutural, mas seu rótulo não foi observado: sem save, o jogo entra direto no tutorial. Por isso, a prova final usa texto imediatamente acessível. Capturas pretas intermediárias foram transições normais, superadas ao avançar os frames; não se concluiu travamento a partir delas.

O emulador informou ausência de save acessível e operação em RAM. Persistência de save/load, exploração do mundo, treinadores, batalhas, Primal Kyogre e hardware **não foram testados**. Boot e texto observado não equivalem a validação completa do jogo.

## Efeitos automáticos e preservação

O build chama `scripts/build_tests.py`, que substituiu um apóstrofo tipográfico em `data/battle_tests/abilities/competitive/intimidate_after_pursuit.c`. Esse efeito foi identificado e o arquivo original foi restaurado byte a byte após as compilações. Nenhum cenário de batalha foi executado.

A comparação com os hashes do baseline confirmou que o único arquivo original rastreado alterado neste checkpoint é `.gitignore`, para proteger os textos gerados. C, assembly, dados de gameplay, Makefiles, configs e testes originais permanecem intactos. As ferramentas Python de prova são adições isoladas do Hollowtide.

Os 14 testes offline foram reexecutados e passaram. Os detalhes estão em [TEST_REPORT.md](TEST_REPORT.md). O próximo checkpoint é validar save/load e um cenário de batalha direcionado, ou integrar o primeiro export autoral quando fornecido, sem confundir esses gates com o boot já comprovado.
