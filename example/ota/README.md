[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# OTA-capable AT firmware

This project extends the AT/transparent-transmission design with BLE OTA support and additional persistent settings.

## Behavior

When disconnected, the module accepts AT commands. When connected, UART and BLE data are transparently forwarded unless `CONTROL_GPIO` is held low to select AT mode. GPIO definitions and UART RX auto-detection are in `app_config.h` and `app_uart.c`.

The project initializes tinyFlash for persistent AT/OTA settings and exposes command families for reset, sleep, baud, name, MAC, role, connection state, scan/connect/disconnect, sending data, advertising data and enable state, RF power, iBeacon identifiers, service UUID, and connection-range parameters. `at_cmd.c` is the authoritative source for syntax.

## Build

```bash
make clean
make
```

The output is `out/aota.elf` and `out/aota.bin`. OTA behavior, image compatibility, interrupted-transfer recovery, and rollback must be tested on compatible hardware before release; automated repository validation performs compilation only.

## Entry and persistence

`main()` initializes the platform, then selects normal or deep-retention initialization. Normal initialization configures tinyFlash, UART, BLE role/services, advertising, callbacks, and OTA support. `main_loop()` services the precompiled BLE stack, software timers, and UART processing.

Persistent key indices are defined in `tinyFlash_Index.h`. Existing AT indices retain their historical values, while OTA-specific settings are appended to avoid remapping stored data.

## Safety boundary

The repository contains only the application side of this OTA flow and links precompiled BLE libraries. A successful build does not prove radio interoperability, image authenticity, update atomicity, or safe recovery from power loss.
