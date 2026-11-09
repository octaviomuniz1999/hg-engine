# Diretriz permanente de desenvolvimento

Estabelecida pelo usuário em 2026-11-09, após a publicação do CP03. Aplica-se às próximas integrações e ao desenvolvimento da campanha. Não declara concluídas funcionalidades ainda pendentes.

## Responsabilidades

O usuário responde exclusivamente pela direção criativa e pela construção visual dos mapas no **Pokémon DS Map Studio 2.2**. Não precisa programar ou finalizar colisões, permissões, alturas técnicas, warps, NPCs ou scripts antes de entregar um mapa.

O Codex assume a infraestrutura para tornar os mapas jogáveis:

- Auditar os arquivos recebidos e integrar BIN, BLD, PER, NSBMD, NSBTX, BDHC e recursos complementares.
- Implementar colisões, permissões, alturas físicas e transições entre níveis, acompanhando a geometria visual fornecida.
- Configurar entradas/saídas, interiores, conexões e transições entre mapas.
- Posicionar e programar NPCs; implementar scripts, diálogos e eventos conforme a direção criativa estabelecida.
- Corrigir bindings, texturas ausentes e demais problemas gráficos preservando a aparência pretendida pelo autor.
- Compilar, executar testes reais no DeSmuME, investigar falhas, corrigir e repetir os testes pertinentes.
- Registrar proveniência, IDs, alterações, evidências, limitações e checkpoints versionados.

Decisões técnicas rotineiras cabem ao Codex. Solicitar esclarecimento criativo somente quando a intenção não puder ser inferida com segurança a partir do mapa, do preview e do design já aprovado. Não exigir do usuário offsets, IDs internos, flags, manifestos ou implementação de mecânicas.

## Proteção dos mapas autorais

**Não modificar geometria, decoração, posicionamento das construções ou identidade visual sem autorização explícita do usuário.** Isso inclui remodelar, simplificar, deslocar ou remover elementos visuais para contornar limitações técnicas.

Manter os arquivos recebidos intactos, com hashes, e trabalhar em cópias privadas derivadas. Ajustes em PER/BDHC, eventos e referências devem acompanhar o cenário visual existente. BLD contém posicionamento de edifícios: sua integração não autoriza alterar transformações ou decoração. Correções de texturas devem usar os recursos pretendidos e preservar materiais/UVs e aparência; não substituir por arte arbitrária para esconder uma falha.

Quando uma solução exigir mudança visual, preparar o diagnóstico e uma proposta concreta, avançar nas partes independentes e solicitar autorização antes de aplicá-la. Um interior que exija nova arte/geometria continua sujeito à direção criativa; sua ligação técnica pode ser preparada separadamente. Não inventar conteúdo narrativo que contradiga ou amplie decisões criativas incertas.

## Procedimento ao receber um mapa

1. Inventariar o pacote, identificar a versão/alvo e calcular tamanhos/hashes. Preservar o original. Auditar seções e recursos, inclusive referências externas de modelos/texturas.
2. Comparar com o preview e identificar portas, caminhos, desníveis e pontos de interesse. Usar essas evidências para definir os dados técnicos sem redesenhar o cenário.
3. Preencher a [ficha técnica](templates/MAP_RECORD.md), alocar IDs e resolver recursos compartilhados em uma área experimental isolada. Dados técnicos ausentes ou ainda padrão do editor são trabalho do Codex, não uma exigência de acabamento pelo usuário.
4. Implementar permissões, alturas, warps, conexões, NPCs e scripts necessários. Conferir qual fonte participa do build para evitar que uma categoria sobrescreva outra.
5. Gerar uma ROM derivada privada; comparar recursos alterados e verificar a preservação das partes visuais protegidas. Compilar quando o procedimento exigir; distinguir empacotamento após build de nova compilação da engine.
6. No DeSmuME, testar gráficos/texturas, limites e colisões, todos os níveis, portas e retorno, NPCs/diálogos, eventos e persistência relevante. Registrar capturas e resultados reais, sem aprovar integração apenas pelo parser ou build.
7. Versionar código/documentação próprios, registrar bloqueios e apresentar o checkpoint. A aprovação artística continua com o usuário.

Se um recurso indispensável estiver ausente, tentar recuperá-lo do projeto/export fornecido ou gerá-lo tecnicamente sem alterar a arte; registrar o bloqueio e solicitar apenas o arquivo indispensável quando necessário. Isso não transfere a integração técnica ao usuário.

## Continuidade e evidências

Preservar integralmente CP01 `1e2bf5a33`, CP02 `6f3625641` e CP03 `9e8e0adff`, sem reescrever esses commits. Continuar na branch `codex/hollowtide-checkpoint-03`. O CP03 foi publicado no fork `octaviomuniz1999/hg-engine`; sua autorização de push foi exclusiva desse head e ancestrais. Novas publicações continuam sujeitas à revisão/autorização aplicável.

A ROM-base e os saves permanecem privados, fora do Git. Reutilizar o ambiente validado, sem reinstalações desnecessárias. Não declarar funcionalidades aprovadas sem evidência. O CP03 comprovou somente calibração nativa; o primeiro mapa autoral e os testes posteriores estão em [CHECKPOINT04.md](CHECKPOINT04.md). Manter distintos os limites históricos e os resultados atuais.
