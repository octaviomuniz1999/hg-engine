# Bloqueios e limites

| ID | Bloqueio comprovado | O que impede | Como liberar |
| --- | --- | --- | --- |
| B01 — resolvido | O envio em oito volumes RAR permitiu extrair a base IPKE; cabeçalho/CRCs conferidos | Build/boot passaram no CP01; save/load e recorte de gameplay passaram no CP02 | Evidência em ROM_CHECKPOINT.md e CHECKPOINT02.md |
| B02 — resolvido para a Vila | Primeiro pacote autoral recebido e integrado no CP04 | Não bloqueia mais a Vila: geometria/texturas/alturas, portas e persistência foram exercitadas | Evidências em CHECKPOINT04.md; aprovação artística permanece com o diretor |
| B03 — limite da rota GUI | PDSMS/DSPRE não executados no Cloud; DSPRE declara compatibilidade parcial com hg-engine | Somente comprovação do caminho por essas GUIs; não bloqueia a importação direta demonstrada | O caminho BIN/NSBMD fornecidos → hg-engine → DeSmuME foi demonstrado no CP04 |
| B04 — gate pendente | Botão manual e flag de história da Mega não exercitados | Aprovar a experiência de desbloqueio/seleção na campanha | Fixture separada com flag 2518 e seleção manual; a transformação automática já passou no CP02 |
| B05 | Rota 01 e interiores autorais ainda não fornecidos | Substituir os cenários nativos provisórios pela arte definitiva | Receber os próximos mapas; conexão técnica com retorno já passou no CP04 |

A busca padrão de Newlib é uma limitação explicada em [LINKER_AUDIT.md](LINKER_AUDIT.md), não um bloqueio demonstrado do linker atual. Não foi feita correção especulativa.

Decisões criativas adicionais, como geometria, diálogos completos, IDs definitivos de mapas, alocação de flags da irrigação e progressão, permanecem sem implementação. Os requisitos já fornecidos foram preservados em [README.md](README.md).

CP01 liberou build/boot, CP02 comprovou o recorte de persistência e batalha e CP03 acrescentou a calibração nativa de mapas. No CP04 a Vila autoral foi integrada em ROM derivada privada, sem alterar seus recursos visuais; texturas foram recuperadas e seus índices corrigidos. B02 está liberado para esse mapa, e B03 não bloqueia o caminho direto. B04/B05 e os limites de cobertura descritos em CHECKPOINT04.md permanecem. As evidências antigas continuam nos respectivos relatórios e commits.

## Tentativa de recebimento em 2026-11-08

O proprietário anexou `rom.nds`. A ferramenta de transferência retornou literalmente `file exceeds the executor transfer limit of 32 MiB`. Não informou o tamanho exato e não entregou um caminho local utilizável. A procura no workspace, incluindo `library-files/` e `shared/downloads/`, não encontrou uma cópia alternativa.

Isso é um bloqueio de transporte, não uma falha demonstrada da ROM, da toolchain ou do build. Não foi possível ler o game code nem calcular o hash. Nenhum Makefile, compilador ou emulador foi iniciado nessa tentativa. O arquivo não deve ser substituído por outra ROM obtida externamente.

O registro acima é histórico: o bloqueio foi superado pelo envio posterior dos oito volumes. Nenhuma ferramenta de extração foi instalada; usou-se a libarchive existente.
