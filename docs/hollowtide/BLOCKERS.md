# Bloqueios e limites

| ID | Bloqueio comprovado | O que impede | Como liberar |
| --- | --- | --- | --- |
| B01 | `rom.nds` enviada no chat, mas não transferida ao checkout: o anexo excede o limite de 32 MiB da ferramenta | Leitura do cabeçalho/hash, primeiro build, `test.nds`, prova mínima recompilada e boot/gameplay | Transferir o mesmo arquivo em ZIP de até 32 MiB ou em partes menores; reconstruir em área privada, conferir game code IPKE/revisão/hash e só então compilar |
| B02 | Nenhum export de mapa autoral disponível nas áreas compartilhadas consultadas | Inspeção do formato real, importação DSPRE, colisões, warps e validação visual | Receber projeto/export e componentes complementares com versões e ficha |
| B03 | PDSMS/DSPRE não executados; DSPRE declara compatibilidade parcial com hg-engine | Comprovar o pipeline gráfico e os patches da versão escolhida | Experimento controlado com um mapa, base compatível e versões identificadas |

A busca padrão de Newlib é uma limitação explicada em [LINKER_AUDIT.md](LINKER_AUDIT.md), não um bloqueio demonstrado do linker atual. Não foi feita correção especulativa.

Decisões criativas adicionais, como geometria, diálogos completos, IDs definitivos de mapas, alocação de flags da irrigação e progressão, permanecem sem implementação. Os requisitos já fornecidos foram preservados em [README.md](README.md).

Não há artefato de jogo produzido nesta tarefa. DeSmuME inicializado sem ROM e testes sintéticos não liberam B01/B02/B03. A execução inicial da ordem mestre permanece parcialmente bloqueada, não concluída.

## Tentativa de recebimento em 2026-11-08

O proprietário anexou `rom.nds`. A ferramenta de transferência retornou literalmente `file exceeds the executor transfer limit of 32 MiB`. Não informou o tamanho exato e não entregou um caminho local utilizável. A procura no workspace, incluindo `library-files/` e `shared/downloads/`, não encontrou uma cópia alternativa.

Isso é um bloqueio de transporte, não uma falha demonstrada da ROM, da toolchain ou do build. Não foi possível ler o game code nem calcular o hash. Nenhum Makefile, compilador ou emulador foi iniciado nessa tentativa. O arquivo não deve ser substituído por outra ROM obtida externamente.
