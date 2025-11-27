# 环境与依赖说明

本项目用于编写并批量执行 OpenHarmony XTS 子系统测试脚本。为了确保 `run_all.py`、`xts_batch_runner.py` 以及 `devicetest` 目录中的用例可以直接运行，请按下列要求准备环境。

## 1. 操作系统
- 已在 **Windows 10/11 x64** 上验证，亦可在任意可安装 Python 3.10+ 与 HUAWEI DevEco Device Toolchain 的桌面系统上运行。

## 2. 运行时与工具链
- **Python**：建议 3.10 及以上版本，需保证 `python`/`pip` 命令在 PATH 中。
- **HDC (Huawei Device Connector)**：随 DevEco Device Toolchain 或 OpenHarmony SDK 安装，需在 PATH 中可直接调用 `hdc`。
  - 使用 `hdc list targets` 确认设备连接正常；`devicetest.core._RealDevice` 会依赖该命令获取设备 SN 并下发 `hdc shell`。
- **Git**（可选）：用于获取上游 OpenHarmony XTS/xdevice 代码和版本控制。

## 3. Python 依赖
当前仓库仅使用标准库（`argparse`、`json`、`subprocess`、`glob`、`xml.etree` 等），无需额外安装第三方包。但如果需要将批运行脚本整合进自建平台，可根据需要添加依赖并在此处补充。

## 4. 外部组件
- **xdevice**：`xts_batch_runner.py` 需要可执行的 `xdevice` Python 脚本或模块（例如 `OpenHarmony/test/developtools/xdevice/__main__.py`）。请提前同步官方仓库并在命令行能执行：
  ```powershell
  python path\to\xdevice.py list
  ```
- **XTS 计划/JSON 配置**：`--plan` 参数指向的 JSON 文件需来自 XTS 计划定义（如 Acts、WUKONG 等），请按实际测试范围准备。

## 5. 环境变量建议
```text
PATH=%PATH%;C:\Users\<you>\AppData\Local\Programs\Python\Python310;C:\Program Files\OpenHarmony\tools\hdc
HDC_SERVER_PORT=8710   # 如需自定义设备连接端口
```

## 6. 快速验证
1. 连接一台刷入 OpenHarmony 的设备并执行 `hdc list targets`，保证输出不为 `Empty`。
2. 运行 `python testPrintWorkingDirectory.py`，确认基础控制流程正常。
3. 执行 `python run_all.py`，应生成 `XTS_Report.html`。
4. 如需批量执行官方 XTS 计划，先准备好 `Acts*.json`，再运行示例：
   ```powershell
   python xts_batch_runner.py --xdevice C:\openharmony\xdevice.py --plan C:\plans\ActsExample.json --output-dir out\xts --report-name nightly --junit-pattern "*.xml"
   ```

## 7. 常见问题
- **找不到 hdc**：将 `hdc.exe` 所在目录加入 PATH，或在 `devicetest/core/test_case.py` 中替换为绝对路径。
- **设备 Busy/Offline**：使用 `hdc kill-server && hdc start-server` 重启服务，再插拔 USB。
- **字符编码报错**：所有脚本已使用 `encoding='utf-8'`，如果依旧报错，可手工设置 `PYTHONIOENCODING=utf-8`。

如需在 Linux/macOS 上运行，只需保证可安装 Python、hdc 以及能与设备通信，命令示例可替换为相应 shell 语法。

