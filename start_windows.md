[![中文](https://img.shields.io/badge/中文-文档-blue)](start_windows.zh.md)

# Windows development environment

## Prerequisites

Install Git for Windows and Python 3, then verify them in Git Bash or PowerShell:

```text
git --version
python --version
```

Install the flash-tool dependency from the repository root:

```text
python -m pip install -r requirements.txt
```

## TC32 compiler

The historical Windows toolchain archive referenced by this SDK is:

```text
http://shyboy.oss-cn-shenzhen.aliyuncs.com/readonly/tc32_win.rar
```

This legacy URL is HTTP and the repository does not provide a checksum. Verify the archive through a trusted internal source before use. Extract it to a path without non-ASCII characters, add its `bin` directory to `Path`, and verify:

```text
tc32-elf-gcc -v
```

For repeatable repository-wide builds, WSL2 with the checksum-pinned Linux archive described in [Linux setup](start_linux.md) is the validated route.

## Build and flash

From a project directory:

```text
make clean
make
```

Configure `DOWNLOAD_PORT` in that project's `makefile` before running `make flash`. Flashing changes device memory and requires compatible hardware and the Ai-Thinker UART bootloader.
