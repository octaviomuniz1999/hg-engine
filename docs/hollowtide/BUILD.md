# Build reproduzível: comandos e gates

Estado ao fim do CP01: três builds com exit 0 e prova de texto observada no emulador. Veja [ROM_CHECKPOINT.md](ROM_CHECKPOINT.md) para logs e limites. Os passos abaixo documentam como repetir e quais gates continuam necessários.

Atualização CP02: save/load e quatro cenários reais de batalha passaram; a saída normal foi recompilada com extração limpa e ficou idêntica ao CP01. Ao alternar AUTO_TEST/normal, invalidar **objetos e extração antes de aplicar hooks**, não somente o arquivo final. Veja [CHECKPOINT02.md](CHECKPOINT02.md) para o isolamento dos casos e a configuração XDG que habilitou o save persistente.

## Ambiente já restaurado

Não executar novamente o instalador por rotina. Em cada novo shell:

```bash
cd /workspace/hg-engine
source /workspace/.hg-env/activate
```

Versões observadas: ARM GCC 14.2.1; binutils ARM 2.44; Python 3.12.14 em `.venv`; Rust/Cargo 1.99.1; GNU Make 4.4.1; CMake 3.31.10; GCC/G++ nativos 14.2.0; libpng 1.6.48. São versões restauradas e verificadas, não uma alegação de reconstrução bit a bit em máquina vazia.

Verificações independentes:

```bash
python -m pip --no-cache-dir check
arm-none-eabi-gcc --version
rustc --version
cargo --version
make --version
tools/dsrom --help
```

A Newlib foi investigada em [LINKER_AUDIT.md](LINKER_AUDIT.md). Não adicionar `-lc` ao build atual.

## Gate de entrada: ROM-base

O Makefile exige `rom.nds` com game code `IPKE`, isto é, HeartGold USA/inglês. O proprietário deve fornecer legitimamente esse arquivo. Não obter ROMs comerciais de outras fontes.

Antes de executar qualquer alvo do Makefile, confirmar a presença e ler o game code sem modificar o arquivo:

```bash
python - <<'PY'
from pathlib import Path
p = Path('rom.nds')
if not p.is_file():
    raise SystemExit('BLOQUEADO: rom.nds ausente; nao executar make')
with p.open('rb') as f:
    f.seek(12)
    code = f.read(4)
if code != b'IPKE':
    raise SystemExit(f'BLOQUEADO: game code {code!r}; esperado IPKE')
print('Game code compativel; integridade/revisao ainda requerem registro')
PY
```

Uma checagem equivalente foi executada com a ROM recebida: IPKE, revisão 0, 128 MiB, CRCs de cabeçalho/logo corretos. O game code sozinho não autentica a integridade ou revisão do dump. O SHA-256 e os metadados da entrada ficaram em área privada. Não foram aplicadas edições DSPRE.

Não usar `VALID_GAMECODE=0` para ultrapassar o gate. Não executar `make -n` como auditoria presumidamente inofensiva: o Makefile contém `$(shell ...)` e regras de inclusão de dependências que merecem avaliação própria. O dumper de eventos também chama `make` durante importação.

## Primeiro build — comprovado

Com uma base compatível disponível, guardar os artefatos antigos fora do checkout e executar o procedimento do README, inicialmente serial para facilitar o diagnóstico:

```bash
set -o pipefail
mkdir -p /workspace/work/hollowtide
make 2>&1 | tee /workspace/work/hollowtide/build-initial.log
```

Resultado obtido: `test.nds` de 256 MiB, com exit 0 e hash registrado. O baseline foi arquivado antes das provas seguintes; a saída atual inclui somente o marcador do tutorial. A toolchain e os auxiliares foram reutilizados, sem instalação. Em futuras execuções, registrar código de saída, log, tamanho e hash; não atribuir sucesso à presença de um artefato antigo.

Ao trocar a ROM de entrada, arquivar os resultados e invalidar `base/`, `base_dsrom/` e os caches de `build/` de forma controlada. Não depender apenas do mtime de `base/arm9.bin`. Após a ROM estar validada, revisar o alvo `make clean` e usá-lo para um build limpo; nunca apagar conteúdo criativo não versionado sem preservá-lo.

## Prova mínima de modificação — recompilada e observada

A prova escolhida usa `tools/hollowtide/prepare_text_smoke_test.py`: gera privadamente o texto 219 do tutorial, com `Hollowtide build test.`. O build normal o incorpora por `narcs.mk`; `verify_text_smoke_test.py` conferiu uma única entrada de texto alterada. O marcador foi observado no DeSmuME. As instruções e o procedimento de reversão estão em ROM_CHECKPOINT.md. Os textos gerados são ignorados pelo Git.

### Alternativa de treinador, não aplicada

Um candidato para um checkpoint posterior é o treinador `[8]`, Joey, em `data/Trainers.c`: atualmente um Rattata nível 4. Uma prova futura pode alterar somente o nível para 5 em um commit de teste, regenerar os dados pelo build normal e confirmar o delta no membro correto de `a/0/5/6`. Nenhuma alteração de treinador foi aplicada.

A participação desse arquivo está demonstrada por `narcs.mk`: `build/trainers/.generated` depende de `data/Trainers.c` e executa `tools/trainerdatagen`; são produzidos `a/0/5/5`, `a/0/5/6`, mensagens e nomes. O antigo `scripts/validate_trainers_s.py` mira um layout `trainers.s` que não é a fonte atual.

Recompilar, iniciar `test.nds` no emulador e observar a batalha/equipe alterada. Registrar save de teste, condições, captura e log. Depois reverter a prova ou separá-la da campanha. Esse teste não define o treinador Nevard.

## Emulação: limites do CP01 e validação posterior

DeSmuME iniciou o baseline até título/tutorial e exibiu o marcador na prova final. O emulador operou com save em RAM; persistência de save/load, exploração e batalhas não foram testadas. A inspeção visual realizada limita-se a essas telas.

Esse parágrafo descreve o CP01. No CP02, XDG_CONFIG_HOME privado corrigiu o diretório ausente, e persistência, movimento/transições e quatro batalhas direcionadas foram testados. A prova Mega automatiza a solicitação e não valida a liberação pelo botão/flag da campanha.

Após o build inicial e a prova mínima, preparar um build separado com `AUTO_TEST=Y` e só então usar `scripts/run_tests.sh -c`. O gerador `scripts/build_tests.py` normaliza e pode reescrever arquivos em `data/battle_tests/`; revisar o diff e preservar o baseline. Não executá-lo apenas para verificar Python. Os 512 arquivos C de cenários existentes não foram executados nesta tarefa.
