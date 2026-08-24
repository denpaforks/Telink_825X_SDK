[![中文](https://img.shields.io/badge/中文-文档-blue)](CODE_ENTRY.zh.md)

# Code entry points

## Reset entry

`components/boot/8258/cstartup_8258.S` defines `__start` and the reset-vector path. The linker script `make/boot_16k_retn_8251_8253_8258.link` declares `ENTRY(__start)`, places vectors and RAM code at address `0x0`, and places flash-resident application text from `0x4000`.

The startup code initializes the runtime and calls the application's external `main()`.

## Bare-metal applications

Most projects follow this path:

```text
__start -> reset/startup -> main
        -> CPU/RF/GPIO/clock initialization
        -> user_init_normal or user_init_deepRetn
        -> irq_enable
        -> main_loop (repeated forever)
```

The selected initialization path depends on whether the chip woke from deep-retention sleep. The repeated loop normally calls the precompiled BLE stack through `blt_sdk_main_loop()` and then services project-specific UART, UI, timer, or protocol work.

## Notable entries

| Project | Entry behavior |
| --- | --- |
| `example/blink` | Initializes GPIO and toggles the configured LED in the loop |
| `example/at` | Initializes tinyFlash, UART, BLE role and AT state, then services BLE and UART |
| `example/ota` | Adds OTA services/settings to the AT-style initialization and loop |
| `example/freeRTOS_Demo` | Creates CW/RGB/UART tasks and calls `vTaskStartScheduler()` |
| `example/bootloader` | Reads the SWS boot-selection state, then enters the UART boot loop or transfers to the application |

## How to trace a project

1. Open its `makefile` and `project.mk` to identify sources, defines, linker script, and output name.
2. Find `main()` in the project directory.
3. Follow `user_init_normal()`, `user_init_deepRetn()`, and `main_loop()`.
4. Follow callbacks registered during initialization.
5. Treat calls implemented only by precompiled libraries as an explicit review boundary.
