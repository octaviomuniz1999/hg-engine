# Integração de mapas: fluxo e limites demonstrados

## Situação

Não há mapas autorais exportados nos diretórios compartilhados consultados. A ROM-base foi recebida, o baseline compilou e uma prova de texto foi observada no emulador, conforme [ROM_CHECKPOINT.md](ROM_CHECKPOINT.md). Não foi feita importação visual de mapas, conversão de geometria, alteração de colisões ou configuração de warps reais.

O [release oficial PDSMS 2.2](https://github.com/Trifindo/Pokemon-DS-Map-Studio/releases/tag/2.2) documenta exportação BIN com seções de modelo, permissões, edifícios, terreno, som e câmera para importação no DSPRE. O [README oficial do DSPRE](https://github.com/DS-Pokemon-Rom-Editor/DSPRE/blob/main/README.md) documenta importação/exportação de BIN e NSBMD, edição de colisões, headers, matrizes e eventos. Ele declara suporte **parcial** a ROMs hg-engine. Fontes consultadas em 2026-11-08; nenhum desses editores foi instalado ou executado nesta tarefa.

Portanto, a rota candidata é **PDSMS → DSPRE → ROM de trabalho compatível → hg-engine**, a validar com as versões exatas dos editores e um mapa real. Não existe importador PDSMS direto no hg-engine demonstrado nesta entrega.

## Recebimento sem alterar a arte

Manter o projeto editável original e os exports fornecidos pelo diretor criativo em área privada de trabalho, por exemplo `/workspace/work/hollowtide/maps/<chave>/`. Não adicioná-los automaticamente ao Git. Receber:

- Nome e versão exatos do editor, inclusive o fork; alvo HGSS e dimensões do mapa.
- Export BIN e, quando separados, NSBMD, NSBTX, PER, BDHC, BLD, BGS e BDHCAM. A extensão sozinha não prova que o formato está correto; nem todo export contém todas as seções.
- Projeto editável, lista dos recursos usados e autoria/licenças.
- Preview e indicação dos tiles transitáveis, alturas, entradas, saídas, conexões e posicionamento de NPCs.
- Para o ginásio: estados previstos das comportas, efeito nas rotas transitáveis e forma de persistência. Não atribuir flags ou redesenhar o puzzle sem o design fornecido.

Registrar tamanhos e SHA-256 na entrega, preservando os bytes recebidos. A geometria e direção artística não são modificadas pelo processo de recebimento.

## Validador de integridade disponível

`tools/hollowtide/validate_map_bundle.py` lê um `manifest.json` e verifica metadados mínimos, arquivo presente, extensão declarada, tamanho e hash. Recusa arquivos vazios, duplicatas de caminho, caminhos externos, symlinks e extensões incompatíveis com o tipo. Somente lê os arquivos.

Esse manifesto é um **contrato próprio de recebimento do Hollowtide**, não um formato oficial dos editores. Ele não entende os binários DS, não confirma colisões, não importa dados e não participa do Makefile. O stdout explicita esses limites.

Exemplo de geração do manifesto para um `map.bin` **real já recebido**, a executar dentro da pasta do pacote. Preencher nome/versão reais antes de usar; o script não gera o mapa:

```python
import hashlib
import json
from pathlib import Path

asset = Path("map.bin")
manifest = {
    "schema_version": 1,
    "map_key": "vila-inicial",
    "target_game": "heartgold-us",
    "exporter": {"name": "Pokemon DS Map Studio", "version": "2.2"},
    "assets": [{
        "path": asset.name,
        "kind": "map_bin",
        "size": asset.stat().st_size,
        "sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
    }],
}
Path("manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
```

Adicionar uma entrada por recurso complementar. Os tipos aceitos estão em `ASSET_EXTENSIONS` no validador. O nome `vila-inicial` apenas identifica um pacote; não reserva um ID do jogo.

```bash
python -B tools/hollowtide/validate_map_bundle.py /caminho/privado/do/pacote/manifest.json
```

O exemplo mínimo reproduzível **sem mapa real** é a suíte `tests/hollowtide/test_offline_integration.py`, executada conforme [TEST_REPORT.md](TEST_REPORT.md). Seus bytes são explicitamente sintéticos. Ela prova somente integridade/transporte, inclusive a recusa de corrupção, e não produz uma ROM.

## Mapeamento de recursos no checkout

| Recurso | Participação confirmada pelo código atual |
| --- | --- |
| Headers e matrizes | O dumper lê headers originais de ARM9, ou `a/0/5/0` se detectar o patch dinâmico; também consulta `fielddata/maptable/mapname.bin`. Não aplicar offsets vanilla a um hack sem identificar o modo |
| Modelos, terreno, permissões, texturas e matriz | Não há regra demonstrada para importar o BIN PDSMS. Usar os editores e registrar os NARCs/membros efetivos descobertos na ROM, sem copiar o BIN como se fosse um NARC inteiro |
| Scripts de campo | `data/scr_seq/*.s` → membros de `a/0/1/2`; fontes próprias 3 e 953 sempre incluídas |
| Eventos e warps | `data/eventdata/zone_event/*.json` → `a/0/3/2`, sob `BUILD_DUMPED_EVENTDATA`; template em `data/eventdata/zone_event.json.txt` |
| Diálogos | `data/text/*.txt`, `data/text/custom/*.txt` e textos gerados → `a/0/2/7`; custom é sempre compilado |
| Encontros | `data/Encounters.c` → `a/0/3/7`; alterações de DSPRE nessa categoria podem ser substituídas pela fonte C |
| Treinadores | `data/Trainers.c` → `a/0/5/5`, `a/0/5/6` e mensagens; fonte C tem precedência no build |
| Sprites de campo | `data/graphics/overworlds/`, `src/field/overworld_table.c` e tabelas de Pokémon; tag de sprite não é automaticamente o índice do arquivo gráfico |

O header referencia arquivos de evento, script e texto por índices distintos. Um ID de header não é um ID de matriz, membro NARC, warp ou script. Usar a [ficha de integração](templates/MAP_RECORD.md).

## Fluxo técnico futuro

1. Concluir primeiro o build e boot do hg-engine sem mapas personalizados. Guardar ROM original e resultado em armazenamento privado com hashes; nunca sobrescrever o original recebido.
2. Abrir uma cópia de trabalho compatível no DSPRE. Anotar versão, modo de headers e patches. Pela compatibilidade parcial declarada, não aplicar patches genéricos, editor de treinadores ou comandos de script sobre uma ROM hg-engine sem verificar a categoria afetada.
3. Importar o BIN de um único mapa no editor apropriado do DSPRE. Conferir componentes presentes; importar texturas/edifícios externos separadamente quando necessário. Salvar, reabrir e comparar geometria com o preview recebido. A disponibilidade de conversores de modelo necessários à exportação é responsabilidade do fluxo do editor; não instalá-los por suposição no Cloud.
4. Atribuir/mapear matriz e células de terreno, header, área/texturas, câmera, permissões e conexões. Registrar IDs e contagem/dimensões na ficha. Validar colisões caminhando, rampas e alturas; um preview 3D não testa colisão.
5. Definir para cada warp origem, coordenadas/altura, `dest_header_id` e `dest_warp_id`; verificar o destino real e o retorno quando o design exigir. Esses campos são os do template JSON atual, não offsets a deduzir visualmente. Registrar script de entrada, saída e condições de progressão.
6. Manter uma única fonte por categoria. Na primeira integração, deixar `BUILD_DUMPED_EVENTDATA` e `BUILD_DUMPED_SCR_SEQ` desativados e preservar os dados de mapas da base preparada no DSPRE. Os scripts próprios 3/953 e os dados que a engine gera continuam sob controle do hg-engine. Não usar `test.nds` já patchado como nova base sem validar a reaplicação dos patches; preferir uma cópia da base original com somente as edições de mapa.
7. Se migrar eventos/scripts para fontes, usar `make dump_scripts DUMP_ROM=...` somente com o gate de ROM satisfeito, backups e diretórios de trabalho controlados. Revisar os arquivos e labels gerados antes de ativar cada toggle. Manter scripts 3/953 e textos gerados protegidos; não passar `--include-engine-managed` por rotina. O dumper prepara e altera árvores de extração, não é uma simples inspeção de leitura.
8. Invalidar os caches de extração/build ao mudar a base ou a política de fontes. Compilar pelo fluxo oficial, extrair o resultado em área privada separada e comparar hashes dos recursos esperados e dos recursos que deveriam permanecer idênticos.
9. No emulador, validar boot, caminho até o mapa, gráficos, colisão, NPCs, diálogos, entrada/saída, warps, save/load e estados persistentes. Para o ginásio, testar cada estado de irrigação e caminhos de saída para evitar softlock. Só então registrar integração visual aprovada; a aprovação artística continua com o diretor.

O primeiro experimento real deve usar um único export fornecido ou um mapa técnico explicitamente separado da campanha. Porymap/Emerald não fornece binários diretamente compatíveis com esse pipeline DS; tratar eventual migração como conversão de conteúdo e recursos, não cópia de arquivos.
