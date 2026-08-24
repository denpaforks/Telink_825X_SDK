[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# BLE slave connection

This lesson extends the advertising example with connection and slave-role modules. A phone can discover the device named `ABCD` and connect, although this lesson does not add an application service.

## Run the example

```bash
make clean
make
make flash
make monitor
```

Open a BLE test application, scan for `ABCD`, and connect. UART output reports `+BLE_CONNECTED` and `+BLE_DISCONNECTED` through the registered event callbacks.

## Initialization path

`user_init_normal()` in `app.c`:

1. Initializes the random generator and public/static random MAC addresses.
2. Initializes the MCU, standby, advertising, connection, and slave-role modules.
3. Selects `No_Security` for this teaching example.
4. Sets connectable undirected advertising at a 50 ms interval.
5. Enables advertising and registers connect, terminate, and connection-parameter callbacks.
6. Initializes UART diagnostics and enables interrupts.

The main loop calls `blt_sdk_main_loop()` continuously. The BLE stack implementation is supplied by a precompiled Telink library, so its internals are outside the source-review boundary.
