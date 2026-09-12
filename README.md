[![中文](https://img.shields.io/badge/中文-README-blue)](README.zh.md)

# Telink TLSR825X SDK

This repository contains the Ai-Thinker TLSR825X Bluetooth SDK, example firmware, learning projects, a UART bootloader, and host-side flash tools. The examples target `CHIP_TYPE_8258` and use the Telink TC32 toolchain.

## Start here

- [Linux setup](start_linux.md)
- [Windows setup](start_windows.md)
- [macOS status](start_macos.md)
- [Code entry points](docs/CODE_ENTRY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Build validation](docs/VALIDATION.md)
- [BLE learning projects](study/README.md)

Clone the repository:

```bash
git clone https://github.com/Ai-Thinker-Open/Telink_825X_SDK.git
cd Telink_825X_SDK
```

After installing the TC32 toolchain, build one example:

```bash
cd example/blink
make
```

Build every Make-based example and study project on 64-bit Linux:

```bash
TC32_TOOLCHAIN_BIN=/path/to/tc32/bin bash tools/build_all.sh
```

The helper discovers all project `makefile` files below `example/` and `study/`, performs clean builds, and reports warnings, ELF/BIN sizes, entry addresses, and SHA-256 hashes.

## Flashing

TLSR825X does not provide the UART flashing flow by itself. The repository includes an Ai-Thinker UART bootloader and `make/Telink_Tools.py`. A board/module must already contain the compatible bootloader. Configure `DOWNLOAD_PORT` in the selected project's `makefile`, then run:

```bash
python -m pip install -r requirements.txt
make flash
```

See [the bootloader protocol](example/bootloader/README.md) before using erase or write operations. Hardware flashing is deliberately excluded from automated validation.

## Repository layout

| Path | Purpose |
| --- | --- |
| `components/` | Chip drivers, BLE headers, application helpers, FreeRTOS, and precompiled libraries |
| `example/` | BLE, AT, OTA, bootloader, RTOS, driver, and peripheral projects |
| `study/` | Step-by-step BLE learning projects |
| `make/` | Shared make rules, linker scripts, serial monitor, and flash tool |
| `tools/` | Repository-wide build and validation helpers |
| `tests/` | Host-only tests for flash-tool safety behavior |

## Audit boundary

The repository contains proprietary Telink notices and precompiled libraries (`liblt_8258.a`, `liblt_8258_rtos.a`, and `libfirmware_encrypt.a`). Their internal implementation cannot be reviewed from this source tree. No root license file is present, so do not infer redistribution or relicensing rights from repository visibility alone.

## Validation scope

Automated checks compile all 18 discovered firmware projects and test host-side flash-tool logic without opening a serial device. Passing CI does not replace testing on the target board, RF qualification, power measurements, or production programming checks.

## Acknowledgements

Includes driver improvements, multi-page flash routines, JEDEC/UID flash helpers, and BLE API enhancements originally contributed by [pvvx](https://github.com/pvvx) in the [ATC_MiThermometer](https://github.com/pvvx/ATC_MiThermometer) project.

