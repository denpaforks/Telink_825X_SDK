[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# Your first program

This project prints `Hello World` over UART and provides a quick check of the compiler, flash tool, and monitor.

## Build

```bash
make clean
make
```

A successful build creates `out/iBeacon.elf` and `out/iBeacon.bin`.

## Flash

Connect the board, set `DOWNLOAD_PORT` in this directory's `makefile`, and run:

```bash
make flash
```

The target must already contain the compatible Ai-Thinker UART bootloader. Confirm the serial port and close other programs using it before flashing.

## Monitor

```bash
make monitor
```

The expected UART output includes `Ai-Thinker Ble Demo` followed by repeating `Hello World` lines. Press `Ctrl+]` to exit the monitor.
