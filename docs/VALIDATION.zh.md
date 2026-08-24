[![English](https://img.shields.io/badge/English-Docs-green)](VALIDATION.md)

# 构建与验证证据

## 可复现固件构建

全仓构建脚本会发现 `example/` 与 `study/` 下的 18 个 Make 工程，并逐个执行干净构建：

```bash
TC32_TOOLCHAIN_BIN=/opt/tc32/bin bash tools/build_all.sh
```

已验证工具链压缩包 `tc32_gcc_v2.0.tar.bz2` 的 SHA-256 为：

```text
33b854be3e3db3dba4b4dacdda2cd4ea1c94dfd4d562864a095956de7991b430
```

脚本为每个工程输出 `PASS` 或 `FAIL`、编译警告数、ELF/BIN 大小、ELF 入口地址以及 BIN SHA-256；任何工程失败都会返回非零状态。OTA 构建身份来自已配置的 SDK、固件和 AT 版本宏，不再使用编译器墙上时钟宏，因此相同源码和工具链输入会生成相同固件字节。

## 主机侧验证

```bash
python -m pip install -r requirements.txt
python tools/validate_repository.py
python -m unittest discover -s tests -v
```

单元测试使用模拟串口，覆盖非法 Flash 范围、读取超时与响应、设备改变前的固件大小检查、分块写入、密钥脱敏和 CRC 帧，不会打开串口或修改硬件。

## CI 范围

工作流在 Ubuntu 22.04 执行仓库结构/文档检查、Python 严格编译、主机测试以及全部固件构建。工具链通过 HTTPS 下载，校验值不匹配会立即失败。

## 仍存在的警告与限制

旧版 TC32 编译器仍会在部分历史工程报告缺少函数原型、指针符号、未使用变量以及旧键盘表类型等警告。构建成功与警告数量分开记录，不会把警告伪装成零或静默忽略。

CI 不执行烧录、开发板启动、BLE 互操作、RF、时序/功耗或 OTA 故障注入；这些项目需要受控硬件测试。仓库中的预编译库也无法进行源码级审查。
