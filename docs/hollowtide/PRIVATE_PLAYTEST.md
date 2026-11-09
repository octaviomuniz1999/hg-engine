# Teste privado da ROM CP04 no Windows

Destino escolhido pelo proprietário: `C:\Users\tavin\OneDrive\Área de Trabalho\ROM JOGAVEL`.
Esse caminho pertence ao computador do usuário. O ambiente Cloud não o monta e não pode escrever diretamente nele. O arquivo preparado aqui precisa ser baixado pelo proprietário; não foi enviado ao OneDrive e não terá link público.

## Arquivo completo

ROM jogável privada: `/workspace/work/hollowtide/cp04-finalization/private-delivery/Hollowtide_CP04_Final.nds`.
Ela contém a Vila autoral integrada. Não confundir com `/workspace/hg-engine/test.nds`, que é o build normal anterior à instalação dos recursos visuais.

- Tamanho: **193.020.616 bytes**.
- SHA-256: `e6a1e7d6ca24cf8bd722c861905ddfe8249c463c532bcc1ee8bdebed2c1cdcb2`.
- Mesma ROM usada na nova partida documentada em [CHECKPOINT04_FINALIZATION.md](CHECKPOINT04_FINALIZATION.md).
- ROM-base, saves técnicos e savestates não acompanham a entrega. A ROM completa e as capturas ficam fora do Git; não são releases nem anexos de PR.

## Baixar e abrir

1. Baixe o arquivo pelo painel de arquivos deste ambiente ou pelo link privado da conversa. Se baixar o pacote ZIP, extraia seu conteúdo.
2. Coloque `Hollowtide_CP04_Final.nds` na pasta Windows acima. Crie a pasta se necessário; mantenha-a privada no OneDrive.
3. Opcionalmente confira no PowerShell:

   ```powershell
   Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\Users\tavin\OneDrive\Área de Trabalho\ROM JOGAVEL\Hollowtide_CP04_Final.nds'
   ```

4. No DeSmuME para Windows, escolha **File → Open ROM** e abra esse arquivo. Não é necessário aplicar patch ou selecionar a ROM-base.
5. Confira as teclas em **Config → Control Config**. Comece uma partida nova sem importar bateria ou savestate. Complete a introdução, desça a escada da casa, converse com a mãe e saia pela porta sul para a Vila.
6. Teste as casas, o laboratório, os dois NPCs e as duas escadarias. A abertura inferior direita leva somente a um trecho nativo provisório com retorno; não é a Rota 01 definitiva.
7. Use **SAVE dentro do jogo**, aguarde a confirmação, feche o emulador normalmente, abra novamente a mesma ROM e selecione **CONTINUE**. Preserve a pasta de bateria/saves configurada no emulador. Savestates não substituem esse teste.

O teste Cloud usa o núcleo DeSmuME 0.9.12, renderer software, por py-desmume 0.0.9. A instalação Windows do proprietário e hardware físico não foram testados aqui. O protótipo mantém introdução, interiores, nomes e iniciais nativos; a campanha definitiva ainda não foi implementada. As texturas deste mapa foram conferidas no percurso registrado, sem aprovação artística automática ou cobertura de todos os horários/tiles.

A entrega só estará na pasta local escolhida após o download e a cópia pelo proprietário. Nenhuma ROM é publicada no GitHub.
