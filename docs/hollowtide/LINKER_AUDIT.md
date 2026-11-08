# Auditoria Newlib e linker

## Conclusão

Não foi identificado um erro de configuração do **linker usado pelo hg-engine** relacionado a `libc.a`. Existe uma limitação real na instalação relocada de Newlib para programas ARM genéricos que esperem seus caminhos padrão. Ela não demonstra uma falha deste build e não exige reinstalação para a configuração auditada. Nenhuma compilação ou ligação foi realizada para chegar a essa conclusão.

## Evidências verificadas

1. `Makefile` define `LD = $(PREFIX)ld`, `LDFLAGS = rom.ld -T $(C_SUBDIR)/linker.ld` e liga `$(OBJS)` diretamente. A compilação C usa GCC com `-c`; o driver GCC não faz a ligação final.
2. `overlays.mk` também usa `$(LD)` diretamente com os scripts de símbolos gerados e os linker scripts de cada overlay. Inclui `$(THUMB_HELP)` nos comandos de ligação dos overlays adicionais.
3. Os linker scripts rastreados não contêm `INPUT`, `GROUP`, `SEARCH_DIR` ou pedidos explícitos de Newlib/libgcc. Não há `-lc` ou `-lgcc` nos comandos de ligação auditados.
4. `asm/thumb_help.s`, incluído entre os objetos de assembly principais, define `memcpy`, `memset`, `sprintf`, divisões/multiplicações `__aeabi_*` e auxiliares Thumb. Várias rotinas encaminham chamadas a endereços da ROM HeartGold, como `0x020E5AD8` para a cópia e `0x020E5B44` para preenchimento. A validade desses endereços exige a ROM compatível.
5. `include/types.h` declara as rotinas próprias. O `stdint.h` fornecido por este GCC define os tipos por macros intrínsecas; ele não redireciona para os headers de Newlib.
6. `arm-none-eabi-gcc -print-file-name=libgcc.a` encontra o arquivo no GCC 14.2.1. O executável interno `cc1` também está presente e suas bibliotecas dinâmicas foram resolvidas.

## Por que `-print-file-name=libc.a` retorna somente o nome

A biblioteca existe em:

```text
/workspace/.hg-env/sysroot/usr/lib/arm-none-eabi/newlib/libc.a
```

Os headers existem em `.../sysroot/usr/include/newlib/`. A listagem do arquivo com `arm-none-eabi-ar t` funcionou. O caminho `.../usr/lib/arm-none-eabi/lib` não existe.

Os scripts `postinst` dos pacotes Debian preservados no ambiente explicam a diferença:

- `libnewlib-arm-none-eabi` usa `update-alternatives` para ligar `/usr/lib/arm-none-eabi/lib` a `/usr/lib/arm-none-eabi/newlib`.
- `libnewlib-dev` faz o mesmo para `/usr/lib/arm-none-eabi/include` e `/usr/include/newlib`.

O instalador restaurado usa `dpkg-deb -x`, que extrai arquivos e não executa esses scripts. O GCC relocável procura `.../arm-none-eabi/lib`, enquanto o linker padrão também informa `/usr/lib/arm-none-eabi/lib`. `PKG_CONFIG_SYSROOT_DIR` não configura o sysroot do GCC nem altera a busca do linker ARM.

## Decisão técnica e limite

Preservar a toolchain, os linker scripts e as rotinas originais. Não executar `postinst`, criar links globais ou acrescentar `-lc` ao hg-engine: isso não atende a uma necessidade demonstrada e pode introduzir conflitos de símbolos, requisitos de syscalls e consumo extra de overlay.

Se uma futura funcionalidade realmente precisar da Newlib, ela deverá ter um diagnóstico próprio de ABI, headers, caminhos, syscalls, dependências e espaço. A instalação atual não deve ser apresentada como um SDK Newlib genérico completo.

O próximo gate é a primeira compilação com uma `rom.nds` legítima e compatível. Se houver símbolos indefinidos, registrar seus nomes e referências de objetos antes de decidir qualquer alteração. Esta auditoria estática não comprova ausência de outros erros de build.
