# Checkpoints técnicos

| Ordem | Etapa | Estado e evidência |
| --- | --- | --- |
| 1 | Checkout, ambiente, auditoria e branch própria | Preparados; commit base exato, versões, Newlib e estrutura registrados |
| 2 | Primeiro build sem mudança de gameplay | **Bloqueado B01**; nenhuma compilação tentada |
| 3 | Boot e modificação mínima recompilada | **Bloqueado B01 e gate 2**; candidato Joey `[8]` documentado, sem alteração aplicada |
| 4 | Preparação de mapas | Fluxo pesquisado, ficha, validador de integridade e testes sintéticos prontos; integração real **bloqueada B01/B02/B03** |
| 5 | Mecânicas necessárias | Auditoria estática pronta; Mega, Primal Kyogre, Fairy, habilidades, golpes e expansão identificados; gameplay pendente |

## Próximo checkpoint

A `rom.nds` foi anexada, mas o transporte foi recusado pelo limite de 32 MiB. O próximo passo é receber o mesmo arquivo compactado ou dividido e disponibilizá-lo no checkout. Depois: conferir game code/revisão/hash, executar o build serial do baseline, registrar log/exit code e identificar exatamente o artefato recém-gerado. Em caso de falha, investigar o primeiro erro antes de reinstalar componentes.

Após o baseline compilar: testar boot no emulador; aplicar a pequena prova de modificação de treinador; recompilar e verificar o delta do NARC e a batalha. Não avançar para a campanha inteira antes dessa evidência.

Com um primeiro mapa real fornecido: validar o pacote, preencher a ficha e executar o experimento PDSMS → DSPRE → hg-engine com comparação de bytes e teste visual. A campanha Vila Inicial → Rota 01 → Vila da Colheita é o recorte criativo inicial; este checkpoint não atribuiu geometria nem IDs a ela.

Cada checkpoint futuro deve registrar separadamente planejamento, arquivos escritos, compilação, teste automatizado, execução observada e aprovação artística. Fazer commits locais pequenos; push e publicação dependem de autorização específica.
