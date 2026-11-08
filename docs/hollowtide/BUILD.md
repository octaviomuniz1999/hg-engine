# Build reproduzível: comandos e gates

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

## Gate bloqueado: ROM-base

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

Esse comando é um passo futuro documentado; não foi usado com uma ROM nesta tarefa. O game code sozinho não autentica a integridade ou revisão do dump. Registrar tamanho, SHA-256 privado, origem/revisão declarada e alterações de DSPRE antes do primeiro build.

Não usar `VALID_GAMECODE=0` para ultrapassar o gate. Não executar `make -n` como auditoria presumidamente inofensiva: o Makefile contém `$(shell ...)` e regras de inclusão de dependências que merecem avaliação própria. O dumper de eventos também chama `make` durante importação.

## Primeiro build — ainda não executado

Com uma base compatível disponível, guardar os artefatos antigos fora do checkout e executar o procedimento do README, inicialmente serial para facilitar o diagnóstico:

```bash
set -o pipefail
mkdir -p /workspace/work/hollowtide
make 2>&1 | tee /workspace/work/hollowtide/build-initial.log
```

Resultado esperado, ainda não obtido: `test.nds` na raiz. Registrar o código de saída, log, tamanho e hash. Não atribuir sucesso ao simples fato de existir um arquivo de uma execução anterior. A toolchain e os auxiliares já existem; investigar reconstruções ou downloads inesperados antes de reinstalar qualquer coisa.

Ao trocar a ROM de entrada, arquivar os resultados e invalidar `base/`, `base_dsrom/` e os caches de `build/` de forma controlada. Não depender apenas do mtime de `base/arm9.bin`. Após a ROM estar validada, revisar o alvo `make clean` e usá-lo para um build limpo; nunca apagar conteúdo criativo não versionado sem preservá-lo.

## Prova mínima de modificação — bloqueada após o baseline

Um candidato concreto é o treinador `[8]`, Joey, em `data/Trainers.c`: atualmente um Rattata nível 4. Após o baseline, alterar somente o nível para 5 em um commit de teste, regenerar os dados pelo build normal e confirmar o delta no membro correto de `a/0/5/6`. Nenhuma alteração foi aplicada agora.

A participação desse arquivo está demonstrada por `narcs.mk`: `build/trainers/.generated` depende de `data/Trainers.c` e executa `tools/trainerdatagen`; são produzidos `a/0/5/5`, `a/0/5/6`, mensagens e nomes. O antigo `scripts/validate_trainers_s.py` mira um layout `trainers.s` que não é a fonte atual.

Recompilar, iniciar `test.nds` no emulador e observar a batalha/equipe alterada. Registrar save de teste, condições, captura e log. Depois reverter a prova ou separá-la da campanha. Esse teste não define o treinador Nevard.

## Emulação e testes de batalha — bloqueados

DeSmuME foi inicializado sem ROM para verificar a dependência. Isso não valida boot, gráficos, save, batalha ou gameplay.

Após o build inicial e a prova mínima, preparar um build separado com `AUTO_TEST=Y` e só então usar `scripts/run_tests.sh -c`. O gerador `scripts/build_tests.py` normaliza e pode reescrever arquivos em `data/battle_tests/`; revisar o diff e preservar o baseline. Não executá-lo apenas para verificar Python. Os 512 arquivos C de cenários existentes não foram executados nesta tarefa.
