# Checkpoints técnicos

| Ordem | Etapa | Estado e evidência |
| --- | --- | --- |
| 1 | Checkout, ambiente, auditoria e branch própria | Preparados; commit base exato, versões, Newlib e estrutura registrados |
| 2 | Primeiro build sem mudança de gameplay | **Comprovado**: make serial exit 0, test.nds de 256 MiB |
| 3 | Boot e modificação mínima recompilada | **Comprovado no recorte de boot/texto**: marcador do tutorial recompilado e observado no DeSmuME; candidato Joey não foi alterado |
| 4 | Integração de mapas | CP04: Vila autoral integrada com geometria preservada, texturas corrigidas, portas/alturas/NPCs/conexão/save/load emulados; GUI dos editores e mapas autorais seguintes pendentes |
| 5 | Mecânicas necessárias | CP02: Mega Slowbro, Primal Kyogre/Blue Orb/Primordial Sea e controle sem Orb passaram em testes reais; demais interações e seleção manual de Mega pendentes |

## Próximo checkpoint

A `rom.nds` foi recebida em volumes e preservada. O CP02 validou persistência em processo novo, transições, vitória e retorno/movimento no overworld, Mega e Primal no recorte de cenários descrito em CHECKPOINT02.md. O próximo gate é a seleção manual de Mega/flag de história ou um primeiro mapa autoral fornecido, mantendo cada experimento isolado.

O boot e a prova mínima de texto estão comprovados em ROM_CHECKPOINT.md; o CP02 acrescenta evidência de runtime. A prova alternativa de treinador `[8]` não foi aplicada. Os cenários de batalha ficam somente em data/battle_tests/hollowtide/; a campanha não recebeu times ou eventos novos.

No CP03, CP01/02 foram conferidos e preservados e a calibração nativa foi emulada em ROM privada. O CP04 cumpriu o primeiro gate autoral com comparação de recursos e testes reais de colisões/alturas/transições. A campanha Vila Inicial → Rota 01 → Vila da Colheita continua sendo o recorte criativo inicial; os IDs do protótipo não são reservas definitivas para ela. Publicação exige revisão e autorização.

**Atualização CP04:** esse primeiro pacote chegou e o gate técnico da Vila foi comprovado no percurso descrito em CHECKPOINT04.md. O próximo gate visual é a Rota 01 autoral, substituindo o trecho nativo de teste sem alterar a saída planejada pelo diretor. Em seguida, integrar interiores autorais e validar o início/progressão da campanha na ROM modificada. A publicação CP04 ainda requer autorização própria; os checkpoints anteriores continuam ancestrais.

Cada checkpoint futuro deve registrar separadamente planejamento, arquivos escritos, compilação, teste automatizado, execução observada e aprovação artística. Fazer commits locais pequenos; push e publicação dependem de autorização específica.
