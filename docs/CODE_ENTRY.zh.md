[![English](https://img.shields.io/badge/English-Docs-green)](CODE_ENTRY.md)

# 代码入口

## 复位入口

`components/boot/8258/cstartup_8258.S` 定义了 `__start` 和复位向量路径。链接脚本 `make/boot_16k_retn_8251_8253_8258.link` 声明 `ENTRY(__start)`，将向量与 RAM 代码放在地址 `0x0`，将驻留 Flash 的应用代码从 `0x4000` 开始放置。

启动代码完成运行时初始化后调用应用工程提供的 `main()`。

## 裸机应用

大多数工程采用以下路径：

```text
__start -> 复位/启动 -> main
        -> CPU/RF/GPIO/时钟初始化
        -> user_init_normal 或 user_init_deepRetn
        -> irq_enable
        -> 持续执行 main_loop
```

初始化路径取决于芯片是否从深度保持睡眠唤醒。循环通常通过 `blt_sdk_main_loop()` 调用预编译 BLE 协议栈，再处理工程自己的 UART、UI、定时器或协议任务。

## 重点工程入口

| 工程 | 入口行为 |
| --- | --- |
| `example/blink` | 初始化 GPIO，并在循环中翻转 LED |
| `example/at` | 初始化 tinyFlash、UART、BLE 角色和 AT 状态，再处理 BLE 与 UART |
| `example/ota` | 在 AT 风格入口上增加 OTA 服务与设置 |
| `example/freeRTOS_Demo` | 创建冷暖灯、RGB、UART 任务，然后调用 `vTaskStartScheduler()` |
| `example/bootloader` | 根据 SWS 启动选择进入 UART 下载循环或跳转到应用 |

## 追踪一个工程的方法

1. 查看工程的 `makefile` 与 `project.mk`，确认源文件、宏、链接脚本和输出名。
2. 在工程目录定位 `main()`。
3. 继续跟踪 `user_init_normal()`、`user_init_deepRetn()` 和 `main_loop()`。
4. 跟踪初始化期间注册的回调函数。
5. 对仅存在于预编译库中的调用明确标注审查边界。
