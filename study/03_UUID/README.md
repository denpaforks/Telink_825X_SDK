[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# BLE UUID

This lesson introduces the GATT service and characteristic table in `app_att.c`.

Bluetooth services and characteristics are identified by 16-bit adopted UUIDs or 128-bit vendor-specific UUIDs. The attribute table connects UUID declarations to permissions, value buffers, and read/write callbacks.

## Build and inspect

```bash
make clean
make
```

Start with `my_Attributes` in `app_att.c`, then follow each characteristic's declaration, value buffer, Client Characteristic Configuration descriptor, and callback. The application entry and loop are in `app.c`.

When defining a 128-bit UUID inside another initializer, use the repository's raw-byte macros such as `TELINK_SPP_DATA_SERVER2CLIENT_BYTES`; the brace-wrapped form is intended for standalone array initialization.
