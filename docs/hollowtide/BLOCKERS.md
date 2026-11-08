# Bloqueios e limites

| ID | Bloqueio comprovado | O que impede | Como liberar |
| --- | --- | --- | --- |
| B01 | `rom.nds` ausente no checkout | Primeiro build, `test.nds`, prova mínima recompilada, boot/gameplay e cenários de batalha | Proprietário disponibilizar legitimamente HeartGold USA/inglês compatível, game code IPKE; registrar revisão e hash em área privada |
| B02 | Nenhum export de mapa autoral disponível nas áreas compartilhadas consultadas | Inspeção do formato real, importação DSPRE, colisões, warps e validação visual | Receber projeto/export e componentes complementares com versões e ficha |
| B03 | PDSMS/DSPRE não executados; DSPRE declara compatibilidade parcial com hg-engine | Comprovar o pipeline gráfico e os patches da versão escolhida | Experimento controlado com um mapa, base compatível e versões identificadas |

A busca padrão de Newlib é uma limitação explicada em [LINKER_AUDIT.md](LINKER_AUDIT.md), não um bloqueio demonstrado do linker atual. Não foi feita correção especulativa.

Decisões criativas adicionais, como geometria, diálogos completos, IDs definitivos de mapas, alocação de flags da irrigação e progressão, permanecem sem implementação. Os requisitos já fornecidos foram preservados em [README.md](README.md).

Não há artefato de jogo produzido nesta tarefa. DeSmuME inicializado sem ROM e testes sintéticos não liberam B01/B02/B03. A execução inicial da ordem mestre permanece parcialmente bloqueada, não concluída.
