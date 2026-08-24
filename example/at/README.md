[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# AT firmware

This project implements an AT-command interface and BLE transparent transmission for TB-series TLSR8258 modules.

## Operating modes

When disconnected, the module accepts AT commands. After a BLE connection, it enters transparent-transmission mode: UART data is forwarded to BLE and BLE data is forwarded to UART. Pulling `CONTROL_GPIO` low temporarily selects AT mode even while connected.

| Module | UART TX | UART RX | Control | Low-power status | Connection status |
| --- | --- | --- | --- | --- | --- |
| TB-01 | PB1 | PB0 | PC5 | — | — |
| TB-02+ | PB1 | PA0 | PC5 | PC3 | PC4 |
| TB-02_Kit | PB1 | PB7 | PC5 | PC3 | PC4 |

Pin definitions are in `app_config.h`. `app_uart.c` uses PB1 for TX and detects PA0, PB0, or PB7 for RX at startup.

## Command forms

| Form | Purpose |
| --- | --- |
| `AT+<x>?` | Query current value |
| `AT+<x>=<value>` | Set a value |
| `AT+<x>` | Execute an action |
| `AT+<x>=?` | Request command help |

Implemented command families include firmware/version and reset, sleep and restore, baud/name/MAC/mode/state, scan/connect/disconnect, data send, advertising data, RF power, and iBeacon UUID/Major/Minor settings. Consult `at_cmd.c` for the authoritative parser and accepted parameters.

## Central mode

```text
AT+MODE=1
AT+SCAN
AT+CONNECT=AC04187852AD
AT+SEND=5,12345
```

Replace the example MAC address with the peripheral's address. Central mode uses AT-command mode only.

## Low power and iBeacon

The firmware provides deep and light sleep commands and an iBeacon mode. Sleep behavior depends on connection state, configured wake pins, advertising parameters, and baud rate. Validate power and wake behavior on the exact module revision before production use.

To select iBeacon mode and configure identifiers:

```text
AT+MODE=2
AT+IBCNUUID=11223344556677889900AABBCCDDEEFF
AT+MAJOR=1234
AT+MINOR=4567
```

These settings are persisted and take effect after restart as described by the command implementation.

## Code entry

`main()` initializes clocks and hardware, calls `user_init_normal()` or `user_init_deepRetn()` according to wake state, enables interrupts, and repeatedly executes `main_loop()`. The loop services the precompiled BLE stack and UART command/transport handling.
