# Relatório de verificações — 2026-11-08

Este arquivo preserva o histórico do **Checkpoint 01**. O relatório de save/load e batalhas está em [CHECKPOINT02.md](CHECKPOINT02.md); a calibração está em [CHECKPOINT03.md](CHECKPOINT03.md). A integração autoral e os resultados atuais estão em [CHECKPOINT04.md](CHECKPOINT04.md).

Base: `dbb321327c59b821507f9fc4cb6c41d45a9d2698`. Branch: `codex/hollowtide-foundation`.

## Estado atual: build e prova visual realizados

O bloqueio de transferência foi resolvido pelo envio de oito volumes RAR. Foram executados três `make` seriais, todos com exit 0, sem overrides; cada saída tem 256 MiB. O baseline iniciou até título/tutorial no DeSmuME. A prova final exibiu `Hollowtide build test.` no tutorial, por captura inspecionada após 1.924 frames. Detalhes, comandos e caminhos em [ROM_CHECKPOINT.md](ROM_CHECKPOINT.md).

Verificações adicionais efetivamente executadas:

- CRCs de cabeçalho e logo e leitura estrutural da base IPKE revisão 0: passaram.
- Comparação de ROMs por `verify_text_smoke_test.py`, para menu e tutorial: passou; somente `a/0/2/7`, o membro pretendido e uma entrada decodificada mudaram. ARM9, ARM7, tabelas de overlays e FNT serializada permaneceram iguais.
- Recusa de sobrescrever texto privado existente: exit 2 esperado e conteúdo inalterado.
- Recusa de aprovar a ROM do tutorial como se fosse a prova de menu: exit 1 esperado.
- Nova execução da suíte offline: 14 testes, zero falhas/erros, 0,085 s.
- Sintaxe dos dois novos scripts Python de prova: passou.
- Logs dos três builds: nenhuma linha `warning:` ou `error:`; nenhuma instalação realizada.
- Comparação de hashes dos arquivos originais: somente `.gitignore` mudou intencionalmente. O teste de batalha normalizado pelo gerador foi restaurado exatamente.

A primeira checagem ad hoc da FNT usou igualdade direta entre objetos `Folder` de ndspy e falhou. O instrumento de verificação foi corrigido para comparar sua serialização; a checagem repetida e o verificador versionado passaram. Isso não foi uma falha de build ou de conteúdo da ROM.

As capturas pretas iniciais após o título eram transições: avançar frames levou ao tutorial. A prova `NEW GAME` → `TEST RUN` não foi observada visualmente porque a primeira inicialização sem save pula esse menu. A prova final usa o tutorial visível; o delta de menu foi removido antes dela.

O emulador informou operação de save em RAM. Não foram exercitados save/load persistente, exploração, treinadores, batalhas, Primal Kyogre, hardware ou mapas personalizados. Os registros abaixo preservam as etapas históricas independentes de ROM e a tentativa inicial de transferência, não descrevem o estado atual de ausência de ROM.

## Histórico: fase anterior sem ROM acessível

## Testes automatizados executados

```bash
source /workspace/.hg-env/activate
TMPDIR=/workspace/work PYTHONDONTWRITEBYTECODE=1 python -B -m unittest discover -s tests/hollowtide -v
```

Resultado observado: **14 testes passaram**, execução de 0,093 s; zero falhas e zero erros. Há subcasos adicionais dentro dos testes de flags e manifestos, sem contá-los como testes independentes.

| Grupo | Evidência testada |
| --- | --- |
| 8 testes do adaptador existente | Round-trip de bits de tamanho/compressão/assinatura; preservação dos bytes e diretórios vazios sem copiar metadados do host; recusa de destino existente e symlinks; materialização da tabela de overlays e assets; publicação de `arm9.bin` apenas após sucesso em extração nova; propagação de alterações; retenção/remoção condicional de `dsprot` |
| 6 testes do recebimento de assets | Integridade sem escrita; saída da CLI explicita limites; corrupção retorna exit 1; manifestos/caminhos/tamanhos/hashes inválidos são recusados; duplicatas e symlinks são recusados |

Nos testes do adaptador, `subprocess.run` é substituído por mocks. Os arquivos ARM7/ARM9/overlays/eventos são bytes sintéticos em diretórios temporários. Os testes verificam o contrato Python com esses fixtures; **não executam dsrom, não extraem uma ROM e não constroem um jogo**. Os testes da CLI do validador executam somente o novo script Python sobre esses assets sintéticos.

A rejeição de dados inválidos é um resultado esperado e aprovado, não uma falha da suíte.

## Verificações estáticas e de dependências executadas

| Comando ou inspeção | Resultado real |
| --- | --- |
| `python tools/source/dumptools/validate_text_archive.py charmap.txt data/text/*.txt` | Exit 0 para os 45 arquivos de texto da engine |
| `bash -n scripts/run_tests.sh` | Exit 0; somente sintaxe shell, sem executar cenários |
| `ast.parse` nos 56 arquivos Python originalmente rastreados | Nenhum erro de sintaxe; não importa nem executa os scripts |
| `ast.parse` nos dois novos arquivos Python | Ambos passaram |
| Comparação dos valores C/ASM das quatro flags de gimmicks | 2518, 2519, 2520 e 2521 coincidem |
| Inventário de scripts de campo | Membros 3 e 953; nenhum ID duplicado entre as fontes atuais |
| Inventário de conteúdo | 0 JSONs de zone_event; 0 textos custom; 512 arquivos C de testes de batalha, apenas contados |
| `python -m pip --no-cache-dir check` | Exit 0, sem requisitos quebrados |
| `arm-none-eabi-gcc -print-file-name=libc.a` | Exit 0, mas retorna apenas `libc.a`: a resolução padrão não está configurada |
| `arm-none-eabi-gcc -print-file-name=libgcc.a` | Resolve o arquivo no GCC restaurado |
| `arm-none-eabi-ar t .../newlib/libc.a` | Exit 0, arquivo legível |
| Leitura dos `postinst` dos pacotes Newlib preservados | Confirmou criação de alternativas que `dpkg-deb -x` não executa |
| Inspeção de Makefile, overlays e linker scripts | Ligação direta via ld, sem pedido de libc; detalhes em LINKER_AUDIT |
| SHA-256 dos 33.262 arquivos regulares originalmente rastreados | Nenhum arquivo original alterado em relação ao snapshot capturado antes das adições |
| `git diff --check` e revisão das adições | Sem erros de whitespace; somente os caminhos Hollowtide previstos |

Os resultados estruturados das verificações finais ficaram em `/workspace/work/hollowtide-checks.json`, arquivo intermediário privado não versionado. Esse arquivo registra cada comando e código de saída, incluindo a listagem completa do arquivo Newlib.

## Verificações da restauração já executadas neste thread

Antes deste checkpoint: versões de ARM GCC, assembler/linker/objcopy, Python, Rust/Cargo, Make/CMake, GCC/G++, Git e pkg-config; imports de ndspy, pandas, Pillow, py-desmume, PyYAML e numpy; bibliotecas dinâmicas dos 13 auxiliares e `cc1`; sintaxe de `ntrWavTool.py`; `tools/dsrom --help`; inicialização/encerramento headless de DeSmuME sem ROM. Esses resultados fundamentam a disponibilidade do ambiente; não foram convertidos em alegação de teste de jogo.

## Não executado / não comprovado

- Nenhum comando de compilação/assembly/ligação, alvo Makefile ou cenário de batalha.
- Nenhuma ROM comercial baixada, aberta, extraída, modificada ou gerada.
- Nenhum boot de `test.nds`, save/load, batalha, modificação mínima recompilada ou validação gráfica.
- Nenhuma execução de PDSMS/DSPRE ou importação de mapa real.
- Nenhuma aprovação artística ou definição de IDs de campanha.

`rom.nds` e `test.nds` estão ausentes. O build inicial, a prova mínima, os testes reais de Primal Kyogre e a integração visual permanecem bloqueados. Nenhuma ferramenta foi instalada ou reinstalada.

## Tentativa posterior de receber o anexo `rom.nds`

Em 2026-11-08, a configuração do ambiente continuou indicando execução conectada. A transferência do anexo foi tentada e falhou com `file exceeds the executor transfer limit of 32 MiB`. A inspeção dos diretórios de arquivos compartilhados e a busca por ROMs no workspace não encontraram cópia local. O checkout estava limpo antes da atualização da documentação.

Nenhum teste de conteúdo da ROM, compilação, extração ou emulação foi executado nessa tentativa. A suíte offline anterior não foi repetida, pois somente os registros do bloqueio foram atualizados. Não há novo resultado de build a relatar.

## Atualização CP03

24 testes sintéticos passaram (14 anteriores + 10 de formatos do laboratório). Quatro recusas do importador com a ROM real passaram sem escrever NDS. A calibração nativa de mapa, a colisão, o assistente clonado com diálogo e a transição de ida/volta foram executados no DeSmuME; controle com ROM normal confirmou o tile originalmente transitável. Sem build novo ou emulação de mapa autoral. Comandos, artefatos, hashes, capturas e limites em [CHECKPOINT03.md](CHECKPOINT03.md).

## Atualização CP04

Build oficial com exit 0 após invalidar o marcador gerado de learnsets; 31 testes offline e três recusas do CLI passaram. A mesma ROM final concluiu 34 checkpoints no DeSmuME: Vila autoral, alturas/escadarias, limites, NPCs/diálogos, três interiores, saída florestal com ida/volta e SAVE/CONTINUE em processo novo. Fonte/postes e textos foram inspecionados nas capturas. Originais e seções visuais preservados, inclusive cores/pixels. Relatório completo, falhas e limites em CHECKPOINT04.md. Não houve teste de hardware, campanha completa ou nova partida CP04; batalhas CP02 não foram repetidas nem reatribuídas.
