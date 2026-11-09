# Entrega do primeiro mapa autoral

O diretor cria e aprova a arte; o Codex integra os recursos, programa eventos e testa. Para reduzir o primeiro ensaio, enviar **uma célula de 32×32 tiles**, preferencialmente um interior simples, com uma entrada e piso plano. Isso é uma sugestão técnica para o ensaio, não um redesenho da campanha. Não atribuir IDs definitivos de ROM no editor.

Pela [diretriz permanente](DEVELOPMENT_DIRECTIVE.md), não é necessário entregar permissões, colisões, alturas técnicas, warps, NPCs ou scripts finalizados. Enviar o projeto visual e os exports disponíveis; o Codex audita, gera/corrige os dados técnicos e resolve a integração. Uma limitação do protótipo 1×1 não exige redesenhar o seu mapa.

## Exportar no Pokémon DS Map Studio 2.2

Os nomes abaixo vêm do código da versão 2.2, não de uma sessão de GUI executada no Cloud. Se usar outro fork/versão, informar qual e guardar uma captura dos diálogos de exportação.

1. Selecionar **HeartGold/SoulSilver** como jogo-alvo. Preservar a pasta editável inteira: `.pdsmap`, tileset e imagens referenciadas; o arquivo do projeto sozinho não substitui esses recursos. Anotar quais coordenadas da matriz correspondem ao primeiro mapa.
2. Salvar a construção visual com **File → Save Map...**. Na 2.2, salvar grava também PER, BGS, BDHC, BDHCAM e BLD. Esses componentes podem conservar valores padrão ou estar tecnicamente incompletos: o Codex os audita e implementa colisões/alturas/som/câmera quando necessário. Não é preciso configurar mecânicas no editor. Salvar não exporta automaticamente um NSBMD atualizado.
3. Exportar a geometria pelo botão **Export Map as OBJ with Textures**; depois **Export Map as IMD**; depois **Export Map as NSBMD**. Selecionar o mesmo mapa e conservar nomes e pastas coerentes entre as etapas. O botão NSBMD da barra usa o fluxo de conversão em lote IMD → NSBMD; o menu **File → Export Map as NSBMD...** abre a conversão de IMD individual. A conversão precisa terminar com sucesso no seu editor; se faltar conversor ou houver erro, enviar a mensagem e o projeto/OBJ/IMD, sem renomear esses arquivos para `.nsbmd`.
4. Exportar também **Export Map NSBTX** (ou **Export Area NSBTX** se o modelo usar o conjunto de texturas da área). O menu individual é **File → Export Map's NSBTX...**. Informar qual opção foi usada e enviar o arquivo `.nsbtx` resultante. O exportador BIN remove TEX0 embutido do NSBMD: o BIN **não leva automaticamente todas as texturas**.
5. Colocar o NSBMD atualizado junto dos componentes de mesmo nome-base `.bgs`, `.per`, `.bld` e `.bdhc`, na pasta do projeto usada pelo exportador. Não renomear arquivos intermediários isoladamente. Clicar **Export Map as BIN** e escolher **Export Only Current Map Binary File** (o padrão da 2.2 é exportar todos). O exportador procura os componentes na pasta do `.pdsmap` e grava `<nome-do-mapa>.bin` ali; em matrizes, conservar os sufixos de coordenadas gerados pelo editor. Confirmar **SUCCESSFULLY EXPORTED** na janela **Resulting Map Bin files info**. Se algum componente estiver ausente, o exportador informa qual e não produz um BIN válido.
6. Se houver `.bdhcam` não vazio, enviá-lo também. Na 2.2 ele substitui o bloco BDHC do BIN quando seu tamanho excede BDHC + 10 bytes; não remover para contornar um problema sem registrar a decisão.
7. Enviar preview do mapa. Se houver uma intenção criativa que a imagem não mostre, indicar a função dos lugares, conexões ou personagens desejados. Marcações de grade, portas, NPCs, passagens e desníveis são opcionais; o Codex as infere com segurança e configura os dados técnicos. Perguntas adicionais serão feitas somente para intenções criativas ambíguas ou arquivos indispensáveis indisponíveis.

## Pacote a fornecer

| Recurso | Necessidade |
| --- | --- |
| `<mapa>.bin` HGSS | Obrigatório para importação direta experimental; não enviar BIN de DPPt/Gen V |
| `.nsbtx` e imagens/tileset usados | Obrigatórios quando houver texturas próprias; informar se a intenção é reutilizar texturas nativas |
| `.pdsmap` e pasta editável completa | Necessários para preservar/reproduzir a criação visual; incluir arquivos referenciados, não apenas o projeto |
| `.nsbmd`, `.per`, `.bdhc`, `.bld`, `.bgs`, `.bdhcam` se houver | Componentes para diagnosticar ou remontar o export; podem acompanhar o BIN mesmo quando já incorporados |
| OBJ/MTL/texturas, IMD, logs do conversor | Recomendados para diagnosticar conversão; isoladamente não são um mapa pronto para HGSS |
| Preview e informações criativas disponíveis | Nome/revisão, versão/fork e autoria; função dos locais/conexões/personagens quando não for evidente. A ficha e o mapeamento técnico ficam com o Codex |

Pode enviar uma pasta compactada com **somente recursos autorais ou cuja licença permita o compartilhamento**. Não incluir ROM completa, save, dump do jogo ou SDK/conversor comercial. Não precisa fornecer um NARC, dump ARM9 ou editar o código. O Codex calcula tamanhos/hashes, prepara `manifest.json` e preenche os IDs técnicos da [ficha](templates/MAP_RECORD.md).

## O que acontece após receber

Validar integridade e envelope do BIN; conferir geometria com o preview; resolver texturas/materiais e modelos externos; reservar uma área experimental e registrar todos os IDs. Preparar uma ROM derivada privada, comparar os membros alterados e executar os percursos no DeSmuME. Testar colisões, todas as alturas, diálogo, entradas/saídas nos dois sentidos e persistência quando houver estados.

O importador CP03 reutiliza a área/texturas nativas e uma matriz exclusiva 1×1. **Importação de novas texturas, matrizes maiores, novos scripts e rampas autorais não está comprovada**; receber os recursos permite implementar/validar essa etapa, sem alterar a arte por iniciativa técnica. Um log de exportação ou a aprovação do parser não substitui a validação visual.

## Fontes fixadas

- [PDSMS 2.2, MainFrame.java: salvar e botões de exportação](https://github.com/Trifindo/Pokemon-DS-Map-Studio/blob/4eed1d62cb1534a973ee9cd1cf1665628cb9a705/src/main/java/editor/MainFrame.java).
- [Seleção de mapa e mensagens de exportação](https://github.com/Trifindo/Pokemon-DS-Map-Studio/blob/4eed1d62cb1534a973ee9cd1cf1665628cb9a705/src/main/java/formats/mapbin/ExportMapBinInfoDialog.java).
- [Montagem HGSS e retirada de texturas embutidas](https://github.com/Trifindo/Pokemon-DS-Map-Studio/blob/4eed1d62cb1534a973ee9cd1cf1665628cb9a705/src/main/java/formats/mapbin/MapBinHGSS.java).

Consulta técnica no CP03 em 2026-11-09 UTC. Nenhum desses editores/conversores foi instalado ou executado nesta etapa.
