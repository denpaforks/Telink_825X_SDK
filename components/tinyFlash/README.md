[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# tinyFlash

tinyFlash is a compact key/value store for MCU internal flash. It is intended for small settings rather than a general filesystem.

## Storage model

The current design alternates between two 4096-byte sectors. An active sector begins with a 32-byte header followed by key/value records:

| Byte | Meaning |
| --- | --- |
| 0 | Key (`0x01` to `0xFE`) |
| 1 | Bitwise inverse of Key; `0x00` marks an obsolete record |
| 2 | Value length (`0x01` to `0xFF`) |
| 3... | Value bytes |

## API

```c
bool tinyFlash_Init(unsigned long start_addr, unsigned long len);
int tinyFlash_Read(unsigned char key, unsigned char *buf, unsigned char *len);
int tinyFlash_Write(unsigned char key, unsigned char *buf, unsigned char len);
void tinyFlash_Format(void);
```

- `tinyFlash_Init` selects the flash region.
- `tinyFlash_Read` reads a value. A null `buf` requests length only; the historical API uses a null `len` to delete the key.
- `tinyFlash_Write` stores a value of at most 255 bytes.
- `tinyFlash_Format` erases the tinyFlash region.

Callers must choose an aligned region that does not overlap firmware, bootloader, calibration, or other persistent data. Power-loss hardening, encryption, multi-sector expansion, and lookup optimization remain future work in the original design.
