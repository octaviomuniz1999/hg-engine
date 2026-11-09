# Pokémon Hollowtide — base técnica Nintendo DS

Fundação CP01 preservada em `1e2bf5a33`. No **Checkpoint 02**, nova partida, movimento/transições, save/load em processo novo e quatro cenários de batalha passaram no DeSmuME. Mega Slowbro e Primal Kyogre foram verificados no modo de testes; o botão manual de Mega e mapas autorais continuam pendentes. A ROM normal final é idêntica ao CP01. Evidência em [CHECKPOINT02.md](CHECKPOINT02.md); histórico inicial em [ROM_CHECKPOINT.md](ROM_CHECKPOINT.md).

No **Checkpoint 03**, a cópia privada de um mapa nativo foi importada com colisão, NPC e portas experimentais, verificados no DeSmuME. A geometria/BDHC nativos foram preservados; mapa autoral, texturas novas e rampas continuam pendentes. O commit `9e8e0adff` foi publicado na branch [codex/hollowtide-checkpoint-03](https://github.com/octaviomuniz1999/hg-engine/tree/codex/hollowtide-checkpoint-03), após autorização, preservando os checkpoints anteriores. Resultados e limites históricos em [CHECKPOINT03.md](CHECKPOINT03.md).

**Diretriz permanente:** o usuário cuida da direção criativa e construção visual no PDSMS 2.2; o Codex assume toda a programação e integração técnica. Não exigir colisões, alturas técnicas, warps ou scripts prontos do autor. Preservar geometria, decoração, construções e identidade visual sem mudanças não autorizadas. Ler [DEVELOPMENT_DIRECTIVE.md](DEVELOPMENT_DIRECTIVE.md) antes de integrar novos mapas.

No **Checkpoint 04**, a Vila Inicial fornecida foi integrada preservando exatamente modelo, oito objetos BLD, decoração e BDHC. Build real concluído; 31 testes offline, três recusas de integração e 34 verificações de execução no DeSmuME passaram, incluindo duas escadarias, três interiores, NPCs, saída florestal com retorno e save/load em outro processo. Texturas/índices Nitro foram corrigidos. Os interiores e o trecho de rota são nativos provisórios, não a campanha definitiva. Registro local e artefatos privados em [CHECKPOINT04.md](CHECKPOINT04.md); sem novo push.

## Base e autoria

- Upstream: [BluRosie/hg-engine](https://github.com/BluRosie/hg-engine).
- Checkout existente: `/workspace/hg-engine`; origin aponta para o fork `octaviomuniz1999/hg-engine`.
- Commit base: `dbb321327c59b821507f9fc4cb6c41d45a9d2698`.
- CP01: `codex/hollowtide-foundation`; CP02: `codex/hollowtide-checkpoint-02`. Seus commits foram preservados como ancestrais do CP03 publicado; as branches locais anteriores continuam intactas.
- Submódulo nitrogfx: `a8fd94a3e582ded71eda5b9f5f0c69258544bb22`.
- Código C/assembly, dados de jogo rastreados, configurações, Makefiles, lockfiles e créditos originais preservados. As adições Hollowtide ficam em `docs/hollowtide/`, `tools/hollowtide/` e `tests/hollowtide/`. `.gitignore` também protege os textos privados gerados para a prova; os arquivos não são narrativa final.

## Direção criativa preservada

Hollowtide, anteriormente Pokémon PALM, usa ambientes 3D e personagens em sprites 2D de quarta geração. Vínculos, percepção emocional dos lugares e subtexto orientam a narrativa; a direção criativa e a aprovação artística pertencem ao usuário.

A campanha começa na Vila Inicial, passa pela Rota 01 e chega à Vila da Colheita, ligada a agricultura e irrigação. Professor Alex é o professor regional; Snivy, Fennekin e Mudkip são os iniciais. Team Palm é a organização antagonista. Nevard (Estevão), líder de Grama, tem Shroomish nível 12 e Treecko nível 14 planejados; seu ginásio usa comportas e irrigação. Primal Kyogre faz parte da equipe de um personagem relevante.

Essas decisões são requisitos registrados, **não conteúdo implementado**. Nenhuma geometria, narrativa, equipe ou flag definitiva foi inventada ou alterada.

## Documentação

| Arquivo | Conteúdo |
| --- | --- |
| [DEVELOPMENT_DIRECTIVE.md](DEVELOPMENT_DIRECTIVE.md) | Divisão permanente de responsabilidades e proteção da arte autoral |
| [BUILD.md](BUILD.md) | Ativação, dependências, comandos de build e gates de validação |
| [ROM_CHECKPOINT.md](ROM_CHECKPOINT.md) | ROM recebida, três builds e modificação observada no emulador |
| [CHECKPOINT02.md](CHECKPOINT02.md) | Partida, persistência, vitória/retorno e cenários Mega/Primal reais |
| [CHECKPOINT03.md](CHECKPOINT03.md) | Integridade dos checkpoints e ensaio de mapa nativo, colisão/NPC/portas no DeSmuME |
| [CHECKPOINT04.md](CHECKPOINT04.md) | Primeiro mapa autoral integrado, texturas, portas, alturas, conexão e persistência reais |
| [GITHUB_REVIEW.md](GITHUB_REVIEW.md) | Diffs dos checkpoints e branch proposta para revisão antes de publicar |
| [LINKER_AUDIT.md](LINKER_AUDIT.md) | Diagnóstico da Newlib e do linker efetivamente usado |
| [MECHANICS_AUDIT.md](MECHANICS_AUDIT.md) | Evidências estáticas e validações pendentes |
| [MAP_INTEGRATION.md](MAP_INTEGRATION.md) | PDSMS, DSPRE, hg-engine, recebimento e validação de mapas |
| [MAP_EXPORT.md](MAP_EXPORT.md) | Passos no PDSMS 2.2 e pacote a entregar ao Codex |
| [MAP_LAB.md](MAP_LAB.md) | Reprodução do importador experimental, formatos e limites |
| [TEST_REPORT.md](TEST_REPORT.md) | Verificações realmente executadas e seus limites |
| [BLOCKERS.md](BLOCKERS.md) | Dependências que impedem os próximos gates |
| [ROADMAP.md](ROADMAP.md) | Etapas sequenciais e próximo checkpoint |
| [CHANGELOG.md](CHANGELOG.md) | Escopo deste checkpoint |
| [templates/MAP_RECORD.md](templates/MAP_RECORD.md) | Ficha de integração sem IDs arbitrários |

## Reexecutar os testes independentes

Na raiz do checkout, em um shell com o ambiente restaurado:

```bash
source /workspace/.hg-env/activate
mkdir -p /workspace/work
TMPDIR=/workspace/work PYTHONDONTWRITEBYTECODE=1 python -B -m unittest discover -s tests/hollowtide -v
```

Os fixtures são sintéticos e temporários. Nenhum processo de compilação, extração real, empacotamento real ou emulação é executado por essa suíte.
