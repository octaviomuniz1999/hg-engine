# Ficha de integração de mapa

Modelo a preencher com evidências. Nenhum ID está reservado por este arquivo. Não contém mapa ou narrativa novos.

**Preenchimento técnico: Codex.** O usuário entrega a criação visual; a ficha não exige dele colisões, alturas técnicas, warps, NPCs ou scripts prontos. Aplicar a [diretriz permanente](../DEVELOPMENT_DIRECTIVE.md), registrar inferências e pedir esclarecimento somente para intenções criativas ambíguas.

| Campo | Valor a obter |
| --- | --- |
| Chave e localidade | Pendente |
| Revisão criativa e aprovação | Pendente |
| Autor/licença dos recursos | Pendente |
| Editor/fork e versão exata | Pendente |
| Projeto editável e export original | Caminhos privados pendentes |
| Hashes dos originais e cópia de trabalho | A registrar pelo Codex |
| Geometria, decoração e transformações BLD preservadas | Comparar bytes/estrutura e preview; alteração visual exige autorização |
| Manifesto, tamanhos e SHA-256 | Pendente |
| Seções presentes no BIN | Pendente de inspeção |
| Modelos/texturas/edifícios complementares | Pendente |
| Dimensões, orientação e escala | Pendente de arquivo real |
| Versão DSPRE e modo/patch de headers | Pendente |
| ROM de referência e hash | Pendente, somente em registro privado |
| Header ID e nome interno | Não atribuído |
| Matriz ID e células/land-data IDs | Não atribuídos |
| NARCs e membros de geometria/texturas | Pendente de identificação |
| Event/script/level-script/text IDs | Não atribuídos |
| Encontros, música, câmera e permissões | Pendente |
| Proveniência por categoria: DSPRE ou fonte hg-engine | Pendente |
| Flags e variáveis de progressão | Não atribuídas; evitar IDs reservados pela engine |

## Warps e transições

Preencher por warp: header de origem, índice do warp, coordenadas e altura, header de destino, índice de destino, condições e caminho de retorno. Para conexões sem warp, registrar a célula da matriz, a continuidade do terreno e as coordenadas esperadas nos dois sentidos.

Implementar e testar esses dados acompanhando as portas e desníveis visuais existentes. Não mover construções ou remodelar o cenário para acomodar os dados técnicos sem autorização.

## Estados do ginásio de irrigação

Receber do diretor criativo: estado inicial, interações das comportas, mudanças de colisão/passagem, persistência após sair/recarregar e condição de conclusão. Mapear para flags/variáveis somente após a auditoria de alocação de IDs da ROM real.

## Evidência por gate

- Recebimento: manifesto e hashes conferidos; não equivale a formato válido.
- Importação: log/versão do editor, mapa reaberto e IDs registrados.
- Compilação: comando, exit code, hash de saída e delta dos recursos.
- Execução: save de teste, percurso, estados, screenshots e resultado observado.
- Arte: geometria preservada e aprovação do diretor, separada do resultado técnico.
