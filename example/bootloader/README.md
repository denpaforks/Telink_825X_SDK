[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# UART bootloader

TLSR8258 does not natively provide this repository's UART flashing flow. The Ai-Thinker bootloader occupies the first 16 KiB and selects bootloader or application behavior from the SWS pin at reset.

## Boot flow

- In download mode, the bootloader waits for UART commands.
- In run mode, it copies the application's RAM-code mirror from flash address `0x2C000` to RAM address `0x0`, then starts the application.

## Flash layout

| Region | Address | Maximum | Content |
| --- | --- | --- | --- |
| Bootloader | `0x00000`–`0x03FFF` | 16 KiB | UART bootloader |
| Application non-RAM code | `0x04000`–`0x2BFFF` | 160 KiB | Application text/data stored in place |
| Application RAM-code mirror | `0x2C000`–`0x2FFFF` | 16 KiB | First 16 KiB of the normal application image |

The host flash tool therefore maps application offsets below `0x4000` to the mirror at `0x2C000` and limits a firmware image to 176 KiB.

## UART frame

Each command begins with a one-byte command, a two-byte parameter length, and parameters.

| Command | Operation | Parameters |
| --- | --- | --- |
| `0x00` | Read version | None |
| `0x01` | Write flash | Address, checksum, data |
| `0x02` | Read flash | Address, length |
| `0x03` | Erase flash | Address, sector count |

Erasing and writing are destructive. Confirm the selected port, address range, device type, and presence of a compatible bootloader before use.
