# Checkpoints técnicos

| Ordem | Etapa | Estado e evidência |
| --- | --- | --- |
| 1 | Checkout, ambiente, auditoria e branch própria | Preparados; commit base exato, versões, Newlib e estrutura registrados |
| 2 | Primeiro build sem mudança de gameplay | **Comprovado**: make serial exit 0, test.nds de 256 MiB |
| 3 | Boot e modificação mínima recompilada | **Comprovado no recorte de boot/texto**: marcador do tutorial recompilado e observado no DeSmuME; candidato Joey não foi alterado |
| 4 | Preparação de mapas | Fluxo pesquisado, ficha, validador de integridade e testes sintéticos prontos; integração real **bloqueada B02/B03** |
| 5 | Mecânicas necessárias | CP02: Mega Slowbro, Primal Kyogre/Blue Orb/Primordial Sea e controle sem Orb passaram em testes reais; demais interações e seleção manual de Mega pendentes |

## Próximo checkpoint

A `rom.nds` foi recebida em volumes e preservada. O CP02 validou persistência em processo novo, transições, vitória e retorno/movimento no overworld, Mega e Primal no recorte de cenários descrito em CHECKPOINT02.md. O próximo gate é a seleção manual de Mega/flag de história ou um primeiro mapa autoral fornecido, mantendo cada experimento isolado.

O boot e a prova mínima de texto estão comprovados em ROM_CHECKPOINT.md; o CP02 acrescenta evidência de runtime. A prova alternativa de treinador `[8]` não foi aplicada. Os cenários de batalha ficam somente em data/battle_tests/hollowtide/; a campanha não recebeu times ou eventos novos.

Com um primeiro mapa real fornecido: validar o pacote, preencher a ficha e executar o experimento PDSMS → DSPRE → hg-engine com comparação de bytes e teste visual. A campanha Vila Inicial → Rota 01 → Vila da Colheita é o recorte criativo inicial; este checkpoint não atribuiu geometria nem IDs a ela.

Cada checkpoint futuro deve registrar separadamente planejamento, arquivos escritos, compilação, teste automatizado, execução observada e aprovação artística. Fazer commits locais pequenos; push e publicação dependem de autorização específica.
