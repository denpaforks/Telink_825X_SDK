[![English](https://img.shields.io/badge/English-Docs-green)](ARCHITECTURE.md)

# 架构说明

## 分层

| 层级 | 源码位置 | 职责 |
| --- | --- | --- |
| 启动/链接 | `components/boot/8258/`、`make/*.link` | 复位向量、运行时启动、RAM/Flash 布局 |
| 芯片支持 | `components/drivers/8258/`、`components/vendor/8258/` | GPIO、时钟、DMA、UART、RF、Flash、电源管理 |
| BLE 接口 | `components/stack/ble/` | 控制器/主机接口、UUID、事件和属性定义 |
| 二进制协议栈 | `components/stack/ble/lib/` | 裸机及 FreeRTOS 的预编译 BLE 实现 |
| 服务/辅助 | `components/application/`、`components/tinyFlash/`、`components/freertos/` | 打印、键盘/音频/UI、持久化设置、RTOS 支持 |
| 应用 | `example/`、`study/` | 产品示例与学习固件 |
| 主机工具 | `make/*.py`、`tools/`、`tests/` | 构建规则、串口监视、烧录与验证 |

## 内存模型

主链接脚本将向量/RAM 代码放在 `0x0`，应用代码放在 Flash 偏移 `0x4000`，数据与 BSS 放入 TLSR8258 RAM 区域。安信可 UART Bootloader 将应用前 16 KiB 存在 Flash 偏移 `0x2C000`，以便启动应用前恢复 RAM 代码。

AT/OTA 工程通过 tinyFlash 预留持久化区域。修改分区前，必须同时核对工程源码、Bootloader 和固件布局。

## 构建变体

18 个 Make 工程都定义 `CHIP_TYPE=CHIP_TYPE_8258`。FreeRTOS 示例额外定义 `USE_FREE_RTOS=1` 并链接 RTOS BLE 库。AT 与 OTA 使用 32 KiB retention 配置。每个工程通过 `project.mk` 管理源文件，并在自己的 `out/` 目录产生 ELF/BIN。

## 审查边界

仓库包含预编译的 `liblt_8258.a`、`liblt_8258_rtos.a` 和 `libfirmware_encrypt.a`。`blt_sdk_main_loop`、`blc_ll_*`、`bls_*` 等符号进入这些二进制库。源码审查和 CI 编译只能验证集成，不能证明库内部正确性、安全性或许可条款。

RF 性能、极限电压温度时序、睡眠功耗、Flash 寿命、UART 电气特性、OTA 断电恢复和启动选择等硬件行为也不属于 CI 验证范围。
