# Histórico Hollowtide

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
