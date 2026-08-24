[![中文](https://img.shields.io/badge/中文-文档-blue)](VALIDATION.zh.md)

# Build and validation evidence

## Reproducible firmware build

The repository-wide build helper discovers 18 Make projects below `example/` and `study/` and performs a clean build for each one:

```bash
TC32_TOOLCHAIN_BIN=/opt/tc32/bin bash tools/build_all.sh
```

The validated compiler archive is `tc32_gcc_v2.0.tar.bz2` with SHA-256:

```text
33b854be3e3db3dba4b4dacdda2cd4ea1c94dfd4d562864a095956de7991b430
```

The helper reports one `PASS` or `FAIL` record per project, compiler-warning counts, ELF/BIN sizes, ELF entry address, and BIN SHA-256. It exits nonzero if any project fails. OTA build identity is derived from the configured SDK, firmware, and AT version macros rather than compiler wall-clock macros, so identical source and toolchain inputs produce identical firmware bytes.

## Host-side validation

```bash
python -m pip install -r requirements.txt
python tools/validate_repository.py
python -m unittest discover -s tests -v
```

The unit tests use fake serial objects. They cover invalid flash ranges, read timeout/response handling, firmware-size checks before device mutation, chunked firmware writes, secret redaction, and CRC framing. They do not open a serial port or modify hardware.

## CI scope

The workflow runs repository structure/document checks, strict Python compilation, host tests, and all firmware builds on Ubuntu 22.04. It downloads the toolchain over HTTPS and rejects a checksum mismatch.

## Remaining warnings and limits

The legacy TC32 compiler reports warnings in several historical projects, including missing prototypes, pointer signedness, unused variables, and old keyboard-table typing. Build success is recorded separately from warning count; warnings are not represented as zero or silently discarded.

CI does not perform flashing, board boot, BLE interoperability, RF tests, timing/power measurements, or OTA fault-injection. Those require a controlled hardware test plan. Precompiled libraries cannot be source-audited from this repository.
