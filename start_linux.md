[![中文](https://img.shields.io/badge/中文-文档-blue)](start_linux.zh.md)

# Linux development environment

The bundled TC32 compiler is a 64-bit Linux executable. A Debian/Ubuntu-style environment, including WSL2 Ubuntu, can run it.

## Install host tools

```bash
sudo apt-get update
sudo apt-get install -y make python3 python3-pip bzip2 wget
python3 -m pip install --user -r requirements.txt
```

## Install the TC32 toolchain

Download the archive over HTTPS:

```bash
wget https://shyboy.oss-cn-shenzhen.aliyuncs.com/readonly/tc32_gcc_v2.0.tar.bz2
echo "33b854be3e3db3dba4b4dacdda2cd4ea1c94dfd4d562864a095956de7991b430  tc32_gcc_v2.0.tar.bz2" | sha256sum -c -
sudo tar -xjf tc32_gcc_v2.0.tar.bz2 -C /opt
export PATH="/opt/tc32/bin:$PATH"
```

Verify the compiler:

```bash
tc32-elf-gcc -v
```

The expected compiler identifies itself as `gcc version 4.5.1.tc32-elf-1.5 (Telink TC32 version 2.0 build)`.

## Build

Build one project:

```bash
cd example/blink
make clean
make
```

Build all 18 discovered projects:

```bash
TC32_TOOLCHAIN_BIN=/opt/tc32/bin bash tools/build_all.sh
```

On WSL2, keep the repository in a path visible to WSL and pass the Linux mount path to `TC32_TOOLCHAIN_BIN` when the toolchain is stored on a Windows drive.
