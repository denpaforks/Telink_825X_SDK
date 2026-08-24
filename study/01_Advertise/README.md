[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# BLE advertising

This lesson enables non-connectable advertising, sets advertising data, and explains the important advertising parameters. The example intentionally does not implement scan response or connection behavior.

## Run the example

```bash
make clean
make
make flash
make monitor
```

Set `DOWNLOAD_PORT` in the local `makefile` before flashing.

## Code path

`user_init_normal()` in `app.c` initializes the MCU, standby module, and advertising module; supplies the public MAC address; sets advertising data and parameters; chooses RF power; and enables advertising.

The example advertises the complete local name `ABCD`:

```c
u8 tbl_advData[] = {0x05, 0x09, 'A', 'B', 'C', 'D'};
```

Each AD structure is encoded as `Length`, `AD Type`, then `AD Data`. The complete advertising payload is limited to 31 bytes. Common types used here are `0x09` for complete local name, `0x19` for appearance, and `0xFF` for manufacturer-specific data.

## Advertising parameters

`bls_ll_setAdvParam()` configures minimum and maximum interval, advertising type, own and direct address types, channel map, and filter policy. This example uses all three advertising channels (37, 38, and 39). `rf_set_power_level_index()` selects transmit power.

Refer to the source and the applicable Bluetooth Core Specification when changing payload formats or timing; the historical Chinese document contains a longer introductory table.
