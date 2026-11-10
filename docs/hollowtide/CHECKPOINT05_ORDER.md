# POKÉMON HOLLOWTIDE
## ORDEM DE DESENVOLVIMENTO — CHECKPOINT 05
### O início de uma nova jornada

**Engine:** hg-engine / Pokémon HeartGold
**Base de referência:** Checkpoint 04, commit `4784b55b7`
**Agente responsável:** Codex
**Direção criativa:** usuário

---

# 1. OBJETIVO

Transformar a introdução provisória de HeartGold na primeira experiência narrativa própria de Pokémon Hollowtide.

O CP04 já possui uma Vila Inicial autoral integrada, início de nova partida funcional, laboratório acessível, casas com entradas e saídas, NPCs e salvamento.

O usuário testou pessoalmente a ROM e confirmou esses recursos.

Porém, o início ainda contém elementos originais de HeartGold:

- Professor Oak apresenta o jogo.
- O jogador escolhe nome e gênero.
- O protagonista começa dentro de sua casa.
- A mãe entrega os itens iniciais.
- O laboratório oferece Chikorita, Cyndaquil e Totodile.

A partir deste checkpoint, queremos começar a substituir os elementos narrativos e de gameplay de Johto por elementos próprios do Hollowtide.

**Preserve tudo que já funciona. Não reconstrua sistemas sem necessidade.**

# 2. PRESERVAÇÃO DO CHECKPOINT 04

Antes de modificar o jogo:

1. Localize o CP04 funcional e confirme o commit e os arquivos de origem.
2. Verifique que as alterações de mapas, eventos e scripts da Vila Inicial estão presentes.
3. Preserve o CP04 em uma branch de desenvolvimento.
4. Audite os arquivos que serão versionados.
5. Publique no meu fork `octaviomuniz1999/hg-engine` apenas código e materiais cuja distribuição seja permitida, em branch separada, sem alterar a principal e sem force push.
6. Mantenha ROMs, dumps, saves e recursos comerciais fora do Git.

Se os arquivos do CP04 não estiverem disponíveis na tarefa atual, interrompa as modificações dependentes deles e informe o impedimento. Não restaure uma versão antiga fingindo que é a atual.

# 3. COLISÕES DA VILA INICIAL

Existem algumas colisões incorretas em objetos do mapa criado pelo usuário.

Sua responsabilidade:

- Identificar objetos que podem ser atravessados indevidamente.
- Corrigir permissões de movimento e colisões.
- Preservar os limites e as alturas do terreno.
- Verificar as duas escadarias.
- Preservar os acessos às casas e ao laboratório.
- Impedir travamentos ou situações em que o jogador fique preso.

**É proibido alterar a geometria, remover árvores, reposicionar casas ou redesenhar o cenário para contornar problemas técnicos sem autorização.**

Faça testes localizados das colisões alteradas. Não repita toda a bateria do CP04 sem necessidade.

Caso não seja possível identificar com segurança todos os pontos problemáticos, documente os pontos restantes para uma revisão visual posterior do usuário.

# 4. PROFESSOR ALEX

O Professor Alex será o professor Pokémon oficial de Hollowtide.

Ele deve substituir as funções narrativas iniciais dos professores originais de HeartGold:

- Apresentação do mundo na introdução.
- Orientação do protagonista.
- Entrega do primeiro Pokémon no laboratório.
- Explicações iniciais necessárias à jornada.

A substituição deve ser localizada aos eventos envolvidos, sem renomear globalmente personagens de HeartGold que ainda possam existir em outros scripts.

## Caracterização

O Professor Alex deve transmitir inteligência, gentileza, curiosidade e certa sensibilidade.

Não é necessário transformá-lo num personagem excessivamente melancólico.

Ele estuda Pokémon, mas também se interessa pela maneira como a convivência com eles transforma a vida das pessoas.

Seu texto deve combinar o encanto clássico de Pokémon com a identidade narrativa do Hollowtide.

## Aparência

Audite quais sprites de batalha, retratos e overworld são utilizados pela introdução e pelo laboratório.

Não invente uma aparência definitiva para Alex.

Na ausência de sprites personalizados aprovados, utilize provisoriamente recursos compatíveis já existentes, identificados como placeholders na documentação.

Não substitua arquivos gráficos permanentemente sem necessidade.

# 5. A NOVA INTRODUÇÃO

O principal sentimento que queremos explorar é o **vínculo**.

Hollowtide não precisa explicar esse tema de maneira direta. Queremos que o jogador o perceba por meio das relações, dos ambientes e dos acontecimentos.

A introdução deve ser poética, mas continuar parecendo a abertura de um jogo Pokémon.

Utilize o roteiro abaixo como referência narrativa principal.

## CENA 01 — A apresentação

A tela começa com o Professor Alex.

**PROFESSOR ALEX:**

"Olá. Que bom encontrar você."

"Há caminhos que ligam cidades. Outros acabam ligando pessoas."

"Este mundo é habitado por criaturas extraordinárias que chamamos Pokémon."

"Vivemos ao lado deles. Às vezes, aprendemos mais com essa convivência do que imaginávamos."

"Alguns encontros passam depressa. Outros permanecem conosco por muito tempo."

"Meu nome é Alex. Sou um pesquisador Pokémon."

"Estudo essas criaturas e as muitas maneiras como nossas vidas se encontram."

A apresentação visual de um Pokémon deve continuar funcionando, com uma espécie compatível com a nova Pokédex.

O Professor Alex prossegue:

"Mas esta história não é sobre minhas pesquisas."

"É sobre a jornada que está prestes a começar."

## CENA 02 — Identidade do protagonista

Preserve a escolha de gênero e nome do jogador.

Antes da escolha:

"Antes de continuar, há uma coisa que gostaria de saber."

"Como devo chamar você?"

Após a escolha:

"Então é assim que você se chama."

"É um prazer conhecer você."

## CENA 03 — Início da jornada

O professor conclui:

"Existe um mundo inteiro além da sua janela."

"Você encontrará lugares que ainda não conhece. E pessoas que talvez nunca esqueça."

"Não é preciso saber aonde todos os caminhos vão levar."

"Por enquanto, basta dar o primeiro passo."

A introdução termina e o protagonista aparece em sua casa na Vila Inicial.

### Diretrizes narrativas

- Não mencionar explicitamente a história completa.
- Não introduzir antecipadamente a Team Palm.
- Não apresentar a mensagem do jogo como uma lição moral.
- Não criar uma explicação literal sobre solidão, perda ou relacionamentos.
- Preservar o mistério e a liberdade de interpretação.
- Não inventar o nome definitivo da região.

O texto poderá ser adaptado tecnicamente para caber nas caixas de diálogo do Nintendo DS, sem perder seu significado.

A ROM-base está em inglês. Utilize tradução inglesa fiel quando necessário, mantendo o texto original em português na documentação. Não declare suporte completo a português sem implementar e testar a localização.

# 6. A MÃE DO PROTAGONISTA

O evento original da mãe já funciona no CP04.

Preserve sua estrutura técnica, mas adapte o diálogo para a identidade da nova Vila Inicial.

Proposta:

**MÃE:**

"Já vai sair?"

"Engraçado... parece que foi ontem que você começou a explorar cada cantinho desta vila."

"Bem, acho que o mundo ficou pequeno demais para sua curiosidade."

Entregue os mesmos itens que o evento funcional já entrega, sem modificar desnecessariamente o inventário.

Após entregar os itens:

"Cuide bem das suas coisas."

"E não esqueça: você sempre pode voltar para casa."

O tom deve ser acolhedor e natural, sem dramatização excessiva.

# 7. NOVOS POKÉMON INICIAIS

Substitua os iniciais originais de HeartGold por:

| Inicial antigo | Novo inicial | Tipo |
|---|---|---|
| Chikorita | Snivy | Grama |
| Cyndaquil | Fennekin | Fogo |
| Totodile | Mudkip | Água |

Todos devem ser oferecidos no nível 5.

## Linhas evolutivas

**Snivy**
- Snivy → Servine → Serperior

**Fennekin**
- Fennekin → Braixen → Delphox

**Mudkip**
- Mudkip → Marshtomp → Swampert

## Auditoria obrigatória

Antes de implementar, verifique a disponibilidade e o funcionamento de:

- Identificadores internos das espécies.
- Dados de tipos, atributos, habilidades e ataques.
- Sprites de batalha dianteiros e traseiros.
- Paletas normais e shiny.
- Ícones dos menus.
- Gritos dos Pokémon.
- Evoluções e aprendizagem de movimentos.
- Registro na Pokédex.
- Compatibilidade com save/load.
- Sprites de Pokémon seguidores no overworld de HGSS.

A expansão da Pokédex do hg-engine não garante que todos os recursos visuais estejam completos.

Não substitua uma espécie apenas pelo nome ou número interno sem validar seus dados.

Se algum recurso estiver ausente, identifique-o e implemente uma solução técnica legítima ou documente o bloqueio. Não use sprites incorretos silenciosamente.

## Escolha do inicial

Preserve a estrutura da escolha original, adaptando-a aos três novos Pokémon.

Ao selecionar cada inicial, exiba seu nome e permita que o jogador confirme.

A escolha deverá realmente adicionar a espécie correta à equipe, com dados e movimentos adequados.

O sistema deve funcionar para ambos os gêneros de protagonista.

# 8. PROFESSOR ALEX — EVENTO DO LABORATÓRIO

Quando o protagonista entrar no laboratório, apresente o Professor Alex.

**ALEX:**

"Ah, você chegou!"

"Estava esperando por você."

"Existem muitas coisas que podemos descobrir sobre os Pokémon estudando livros."

"Mas algumas só aprendemos quando começamos a caminhar ao lado deles."

Alex apresenta os três Pokémon iniciais.

"Estes três estão esperando por alguém com quem compartilhar uma jornada."

"Snivy, Fennekin e Mudkip."

"Cada um tem sua própria maneira de descobrir o mundo."

"Não existe uma escolha perfeita."

"Escolha aquele com quem você gostaria de começar."

Após a escolha:

"Então está decidido!"

"Acho que vocês ainda vão descobrir muita coisa juntos."

"Cuide bem desse Pokémon."

"E permita que ele também surpreenda você."

A partir daí, mantenha a progressão funcional do jogo, adaptando os diálogos seguintes somente quando necessário.

Não invente acontecimentos novos que alterem a sequência aprovada da campanha.

# 9. COMPATIBILIDADE DA CAMPANHA

A introdução deve conduzir naturalmente à Vila Inicial já construída.

Verifique:

- Início no quarto correto.
- Descida à casa.
- Evento da mãe.
- Saída para a cidade.
- Entrada do laboratório.
- Apresentação do Professor Alex.
- Seleção de Snivy, Fennekin ou Mudkip.
- Retorno ao overworld com o Pokémon escolhido.
- Salvamento e carregamento.

Se os eventos seguintes do HeartGold dependerem de Chikorita, Cyndaquil ou Totodile, identifique as dependências e adapte somente o necessário para evitar inconsistências.

Não implemente a Rota 01 definitiva neste checkpoint.

# 10. TESTES E VALIDAÇÃO

Utilize o DeSmuME e as ferramentas já disponíveis.

Priorize os testes diretamente relacionados às modificações.

## Testes obrigatórios

**Introdução**
- Nova partida sem save técnico.
- Introdução exibida corretamente.
- Nome e gênero preservados.

**Laboratório**
- Diálogos funcionais.
- Escolha dos três iniciais.
- Pokémon correto recebido em cada cenário.
- Interface sem sprites incorretos ou gráficos corrompidos.

**Gameplay**
- Movimento após receber o Pokémon.
- Uma batalha curta com cada inicial, quando viável.
- Evoluções e dados conferidos por testes automatizados ou inspeção técnica.
- SAVE, encerramento e CONTINUE após as alterações de scripts e espécies.

**Colisões**
- Testar apenas as áreas alteradas e a passagem pelas escadas e portas próximas.

Não é necessário repetir os 34 testes do CP04 se o código correspondente não tiver sido alterado.

Nenhuma funcionalidade deve ser considerada aprovada sem evidência.

# 11. ECONOMIA DE TEMPO E TOKENS

Este projeto já possui um ambiente de desenvolvimento funcional e diversos checkpoints aprovados.

A partir de agora:

1. Não reinstale dependências já disponíveis.
2. Não execute builds completos quando testes locais forem suficientes.
3. Reutilize os scripts e ferramentas existentes.
4. Evite pesquisas repetidas sobre funcionalidades já documentadas.
5. Faça commits pequenos e rastreáveis.
6. Evite executar cenários redundantes no DeSmuME.
7. Faça uma compilação integrada depois que as alterações estiverem prontas, em vez de recompilar a cada diálogo.
8. Interrompa tentativas repetidas de download ou upload que já demonstraram bloqueio de rede.
9. Registre objetivamente os problemas e seus resultados.

A eficiência não deve comprometer a integridade do jogo.

# 12. CHECKPOINTS INTERNOS

Execute em três etapas, nesta ordem:

### CP05-A — Segurança e colisões

- Confirmar e preservar o CP04.
- Corrigir colisões identificáveis.
- Validar apenas os pontos afetados.
- Registrar checkpoint.

### CP05-B — Professor Alex e iniciais

- Auditar recursos de sprites e espécies.
- Integrar os três iniciais.
- Adaptar a sequência do laboratório.
- Validar o recebimento dos Pokémon.
- Registrar checkpoint.

### CP05-C — Narrativa inicial

- Integrar a nova introdução do Professor Alex.
- Adaptar o diálogo da mãe.
- Verificar nome, gênero, textos e progressão.
- Executar os testes finais necessários.
- Registrar checkpoint.

Execute as etapas de maneira incremental. Se uma etapa encontrar um bloqueio material, preserve o trabalho válido e relate o problema antes de avançar para funcionalidades dependentes.

# 13. ENTREGA E VERSIONAMENTO

Ao concluir cada subetapa, informe:

- Commit e branch.
- Arquivos modificados.
- Sistemas implementados.
- Testes aprovados e falhados.
- Pendências.
- Próximo passo recomendado.

Preserve os commits no fork apenas após auditoria de arquivos e sem publicar ROMs, dumps ou saves.

Não crie Pull Requests sem autorização.

Se gerar uma ROM, mantenha-a privada. Prefira fornecer um patch `.xdelta` reproduzível e validado, caso a transferência direta de uma ROM completa não funcione.

Não gaste tempo repetindo métodos de transferência já bloqueados.

# 14. RESULTADO FINAL DESEJADO

Ao iniciar uma nova partida de Pokémon Hollowtide, o jogador deverá:

1. Ser apresentado ao mundo pelo Professor Alex.
2. Escolher seu nome e gênero.
3. Despertar na casa da Vila Inicial autoral.
4. Conversar com a mãe.
5. Explorar a vila.
6. Entrar no laboratório.
7. Escolher Snivy, Fennekin ou Mudkip.
8. Receber seu Pokémon e iniciar a jornada.

A Vila Inicial deve continuar visualmente idêntica à construção aprovada pelo usuário.

A experiência deverá transmitir a identidade inicial de Hollowtide sem perder a jogabilidade clássica dos títulos Pokémon.

**Comece pela auditoria e preservação do CP04. Trabalhe de maneira incremental, priorizando o que já está funcional.**

Não amplie o escopo para a Rota 01, ginásios ou novos sistemas antes de concluir a introdução.

**Pokémon Hollowtide não deve ser apenas um HeartGold com outro mapa. Estamos começando a construir uma história própria.**
