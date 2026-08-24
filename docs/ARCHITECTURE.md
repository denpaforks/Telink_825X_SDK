[![中文](https://img.shields.io/badge/中文-文档-blue)](ARCHITECTURE.zh.md)

# Architecture

## Layers

| Layer | Source location | Responsibility |
| --- | --- | --- |
| Startup/link | `components/boot/8258/`, `make/*.link` | Reset vectors, runtime startup, RAM/flash placement |
| Chip support | `components/drivers/8258/`, `components/vendor/8258/` | GPIO, clocks, DMA, UART, RF, flash, power management |
| BLE interface | `components/stack/ble/` | Public controller/host interfaces, UUIDs, events, attribute definitions |
| Binary stack | `components/stack/ble/lib/` | Precompiled BLE implementations for bare-metal and FreeRTOS builds |
| Services/helpers | `components/application/`, `components/tinyFlash/`, `components/freertos/` | Printing, keyboard/audio/UI helpers, persistent settings, RTOS support |
| Applications | `example/`, `study/` | Product examples and learning firmware |
| Host tools | `make/*.py`, `tools/`, `tests/` | Build rules, serial monitor, flash utility, validation |

## Memory model

The primary linker script places vectors/RAM code at `0x0`, application text at flash offset `0x4000`, and data/BSS in the TLSR8258 RAM regions. The Ai-Thinker UART bootloader stores the application's first 16 KiB at flash offset `0x2C000` so it can restore RAM code before transferring control.

AT/OTA projects reserve persistent flash through tinyFlash. Their exact addresses are defined in project source and must be reviewed together with the bootloader and firmware layout before changing partitions.

## Build variants

All 18 Make-based projects define `CHIP_TYPE=CHIP_TYPE_8258`. The FreeRTOS example additionally defines `USE_FREE_RTOS=1` and links the RTOS BLE library. AT and OTA builds use the 32 KiB retention configuration. Each project owns a `project.mk` source list and produces an ELF/BIN under its `out/` directory.

## Review boundary

The repository includes precompiled `liblt_8258.a`, `liblt_8258_rtos.a`, and `libfirmware_encrypt.a`. Symbols such as `blt_sdk_main_loop`, `blc_ll_*`, and `bls_*` enter those binaries. Source review and CI compilation can validate their integration but cannot establish their internal correctness, security, or license terms.

Hardware-dependent behavior also remains outside CI: RF performance, timing at voltage/temperature limits, sleep current, flash endurance, UART electrical behavior, OTA interruption recovery, and boot selection.
