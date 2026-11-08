# Checkpoints técnicos

| Ordem | Etapa | Estado e evidência |
| --- | --- | --- |
| 1 | Checkout, ambiente, auditoria e branch própria | Preparados; commit base exato, versões, Newlib e estrutura registrados |
| 2 | Primeiro build sem mudança de gameplay | **Comprovado**: make serial exit 0, test.nds de 256 MiB |
| 3 | Boot e modificação mínima recompilada | **Comprovado no recorte de boot/texto**: marcador do tutorial recompilado e observado no DeSmuME; candidato Joey não foi alterado |
| 4 | Preparação de mapas | Fluxo pesquisado, ficha, validador de integridade e testes sintéticos prontos; integração real **bloqueada B02/B03** |
| 5 | Mecânicas necessárias | Auditoria estática pronta; Mega, Primal Kyogre, Fairy, habilidades, golpes e expansão identificados; gameplay pendente |

## Próximo checkpoint

A `rom.nds` foi recebida em volumes, conferida e usada em três builds bem-sucedidos. O próximo gate de runtime é validar persistência de save/load e uma batalha direcionada, preservando o baseline e isolando a prova técnica de texto da campanha.

O boot e a prova mínima de texto já estão comprovados em ROM_CHECKPOINT.md. A prova alternativa de treinador `[8]` não foi aplicada; pode servir a um checkpoint posterior de equipe/batalha. Para Primal Kyogre, preparar casos direcionados antes de concluir que a mecânica funciona nesta ROM. Não avançar para a campanha inteira com base apenas no boot.

Com um primeiro mapa real fornecido: validar o pacote, preencher a ficha e executar o experimento PDSMS → DSPRE → hg-engine com comparação de bytes e teste visual. A campanha Vila Inicial → Rota 01 → Vila da Colheita é o recorte criativo inicial; este checkpoint não atribuiu geometria nem IDs a ela.

Cada checkpoint futuro deve registrar separadamente planejamento, arquivos escritos, compilação, teste automatizado, execução observada e aprovação artística. Fazer commits locais pequenos; push e publicação dependem de autorização específica.
