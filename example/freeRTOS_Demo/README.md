[![中文](https://img.shields.io/badge/中文-文档-blue)](README.zh.md)

# FreeRTOS example

This TB-02 Kit example demonstrates task creation and scheduling with three tasks: RGB LED control, warm/cool LED control, and UART output.

At runtime, the RGB LED blinks quickly, the warm/cool LED blinks slowly, and UART prints `Hello FreeRTOS!` once per second. Pressing `K_D2` toggles the RGB task's blinking state.

The project `makefile` must select the RTOS library:

```make
USE_FREE_RTOS = 1
```

`main()` creates the tasks and calls `vTaskStartScheduler()`. This project links `liblt_8258_rtos.a`; the library's internal implementation is not present as source.
