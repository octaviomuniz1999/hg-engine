# Histórico Hollowtide

## 2026-11-08 — Checkpoint 02

- Nova partida, movimento/transições e save/load persistente em novo processo do DeSmuME validados; causa do save em RAM corrigida por XDG_CONFIG_HOME privado, sem alterar a biblioteca.
- Quatro novos cenários de teste: vitória controlada, Kyogre sem Orb, Mega Slowbro e Primal Kyogre com Blue Orb/Primordial Sea. Todos passaram isoladamente; vitória nativa 1 seguida de movimento no campo comprovada.
- Controlador de sessões, observador do runner original e sonda de layout ARM adicionados. Telemetria de forma/habilidade/item/HP/clima somente de leitura; solicitação Mega automatizada pelo modo original de testes.
- Falhas de limpeza parcial, hooks residuais e avanço da fila após vitória natural investigadas. Procedimento corrigido: isolamento de processos e extração limpa na troca de modo. Saída normal final idêntica ao CP01.
- Protocolo de mapas atualizado, sem substituir mapas. Diff completo do CP01 preparado para revisão local; nenhum push/PR.
- ROM-base e código original preservados; normalização tipográfica automática restaurada. Saves, screenshots, ROMs e logs privados fora do Git.

## 2026-11-08 — primeiro build e prova observada no emulador

- Oito volumes RAR extraídos pela libarchive existente; ROM IPKE revisão 0, 128 MiB, CRCs de cabeçalho/logo conferidos.
- Três `make` seriais com exit 0: baseline, prova de menu e prova final de tutorial; saídas de 256 MiB.
- Prova final com `Hollowtide build test.` observada no DeSmuME. Apenas a entrada 7 do arquivo de mensagens 219 difere do baseline; ARM9/ARM7, tabelas de overlays e demais arquivos do filesystem permaneceram idênticos.
- Acrescentados preparador e verificador reproduzíveis em `tools/hollowtide/`; `.gitignore` protege os textos gerados com dados da base. ROMs, dumps e screenshots permanecem privados, fora dos commits.
- Arquivo de teste normalizado automaticamente pelo build restaurado byte a byte. Sem alterações em C/assembly, Makefiles ou configurações; nenhuma instalação e nenhum push.
- 14 testes offline passaram novamente. Save/load persistente, batalhas e mapas autorais ainda não testados.

## 2026-11-08 — recebimento bloqueado por tamanho do anexo

- `rom.nds` fornecida pelo proprietário no chat; transferência recusada pela ferramenta por exceder 32 MiB.
- Nenhuma cópia local alternativa encontrada; cabeçalho e hash ainda não verificados.
- Atualizados somente os registros de bloqueio, roadmap, relatório e histórico. Nenhuma instalação, compilação, extração ou emulação tentada.

## 2026-11-08 — preparação independente de ROM

- Branch local `codex/hollowtide-foundation`, a partir de `dbb321327c59b821507f9fc4cb6c41d45a9d2698`.
- Documentação de requisitos criativos, build, auditorias de linker e mecânicas, bloqueios e checkpoints.
- Protocolo de integração PDSMS/DSPRE com proveniência por categoria, ficha de mapa e limites explícitos.
- Ferramenta somente de leitura `tools/hollowtide/validate_map_bundle.py` para conferir integridade de um pacote privado de assets.
- Suíte independente em `tests/hollowtide/test_offline_integration.py` para o contrato de transporte de arquivos/overlays existente e o recebimento de assets.

Sem alterações em código/dados de gameplay, Makefiles, configurações da engine, testes de batalha ou toolchains. Sem instalação, compilação, ROM gerada, execução de gameplay ou publicação. Os resultados efetivos estão em [TEST_REPORT.md](TEST_REPORT.md).
