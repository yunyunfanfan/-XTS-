# 开源鸿蒙 XTS 子系统测试用例开发与优化

> 仓库地址：[yunyunfanfan/-XTS-](https://github.com/yunyunfanfan/-XTS-.git)  
> Issue 追踪：[gitcode.com/openharmony/xts_acts/issues/22871](https://gitcode.com/openharmony/xts_acts/issues/22871)

本项目聚焦 OpenHarmony XTS（OpenHarmony Test Suite）子系统测试的设计、实现与自动化执行，旨在帮助参赛者和社区开发者快速理解 XTS 框架、构造有效测试用例并生成可复现的测试报告。

---

## 1. 仓库结构

| 路径 | 说明 |
| --- | --- |
| `devicetest/` | 测试基类与设备抽象，`core/test_case.py` 封装真实设备访问并通过 `hdc shell` 下发命令。 |
| `test*.py` | 11 个自定义 XTS Python 用例，覆盖 init 配置校验、系统目录、Bundle Manager、命令行工具等场景，全部继承自 `devicetest.core.TestCase`。 |
| `ActsPCSPyTest.json` | 示例计划配置，列出需要执行的 Python 用例，方便与本地批量脚本或 xdevice 对接。 |
| `run_all.py` | 本地自动执行器，遍历 `test*.py`、捕获日志并生成交互式 `XTS_Report.html`。 |
| `xts_batch_runner.py` | 面向官方 xdevice 的批量执行脚本，支持多计划、Junit 解析以及 JSON/Markdown 汇总。 |
| `XTS_Report.html` | `run_all.py` 样例输出，展示单次批量执行的通过率、耗时及逐脚本日志。 |
| `ENVIRONMENT.md` | 环境依赖说明，涵盖 OS、Python、HDC、xdevice、环境变量及快速验证步骤。 |
| `requirements.txt` | Python 依赖清单，包含 `setuptools==50.0.0`，需通过 `pip install -r requirements.txt` 安装。 |
| `xts_测试用例.docx` / `xts_测试用例.pdf` | 完整的测试用例设计文档，详细记录用例设计思路、子系统分析、执行结果与测试结论。 |
| `错误报告.md` | 对 PCS Python 用例缺陷的扫描与复现说明，已整理成可用于 issue 的正式报告。 |

---

## 2. 环境准备

1. **操作系统**：Windows 10/11 x64（或任意可安装 Python 3.10+ 与 HDC 的桌面系统）。
2. **Python**：3.10 及以上版本，确保 `python`、`pip` 在 `PATH` 中。
3. **安装依赖**：执行 `pip install -r requirements.txt` 安装所需包（当前包含 `setuptools==50.0.0`）。
4. **HDC**：随 OpenHarmony SDK/DevEco 安装，`hdc list targets` 需能识别设备。
5. **xdevice**：同步官方 `test/developtools/xdevice`，确保 `python path\to\xdevice.py list` 可执行。
6. 详细步骤与常见问题见 `ENVIRONMENT.md`。

---

## 3. 快速上手

1. 连接一台刷入 OpenHarmony 的设备，执行 `hdc list targets` 确保在线。
2. **单用例验证**：`python testPrintWorkingDirectory.py`。
3. **本地批量执行**：
   ```powershell
   python run_all.py
   ```
   完成后在 `XTS_Report.html` 查看通过率、耗时及日志。
4. **与 xdevice 集成**（示例）：
   ```powershell
   python xts_batch_runner.py ^
     --xdevice C:\openharmony\test\developtools\xdevice\__main__.py ^
     --plan ActsPCSPyTest.json ^
     --output-dir out\xts ^
     --report-name nightly ^
     --junit-pattern "junit-*.xml"
   ```
   输出目录包含 JSON 与 Markdown 报告，可直接用于赛题提交或 CI。

---

## 4. 赛题目标覆盖说明

| 赛题要求 | 仓库落实 |
| --- | --- |
| 理解并说明 XTS 框架结构与运行机制 | `ENVIRONMENT.md` + `devicetest/core/test_case.py` 详细描述 HDC 设备交互、测试基类及执行链路；README 的“环境准备”和“快速上手”章节进一步解释流程。 |
| 编写 ≥5 个有效 XTS 测试用例 | 仓库包含 11 个 `test*.py` 用例，覆盖系统目录、init 配置、Bundle 管理、权限校验等多个子系统，可针对单系统或多系统执行。 |
| 输出设计/执行分析文档 | `xts_测试用例.docx`/`xts_测试用例.pdf` 提供完整的测试用例设计文档，详细记录设计思路、子系统分析、复杂场景设计、执行结果与测试结论；`XTS_Report.html` 提供可视化结果；`错误报告.md` 以正式格式列出缺陷及修复优先级。 |
| 自动化脚本、批量执行与报告 | `run_all.py` 与 `xts_batch_runner.py` 支持自动化执行、日志捕获、HTML/JSON/Markdown 报告，并可对接 xdevice 与官方 XTS 计划。 |
| 发现并复现场内 XTS 用例缺陷 | `错误报告.md` 针对 PCS 用例列出 12 项问题、复现步骤与修复建议，并已同步至 [Issue 22871](https://gitcode.com/openharmony/xts_acts/issues/22871)。 |
| XTS 与 Google GTest/Android CTS 机制对比（挑战项） | 对比分析收录在 `xts_测试用例.docx`/`xts_测试用例.pdf`，详细阐述 XTS 在分布式与系统服务场景的优势。 |
| 代码开源、可运行 | 全部脚本和文档已托管在 GitHub，满足提交要求并便于社区复现。 |

---

## 5. Issue 追踪与质量改进

- `错误报告.md` 的缺陷列表已关联到 [openharmony/xts_acts#22871](https://gitcode.com/openharmony/xts_acts/issues/22871)，可以作为 PR 或修复建议的附件。
- `run_all.py`、`xts_batch_runner.py` 会输出详细日志与报告，可直接上传至 issue 记录平台。
- 后续计划包括根据 issue 反馈扩展 `ActsPCSPyTest.json`、将复杂场景脚本化、以及将 `xts_batch_runner.py` 接入 CI/Nightly。

---

## 6. 贡献方式

1. Fork [主仓库](https://github.com/yunyunfanfan/-XTS-.git)，创建特性分支。
2. 根据 `ENVIRONMENT.md` 安装/校验依赖（包括执行 `pip install -r requirements.txt`），编写或更新测试脚本。
3. 运行 `run_all.py` 或 `xts_batch_runner.py` 验证结果，附上 `XTS_Report.html` 或 Markdown 报告。
4. 参考 `xts_测试用例.docx`/`xts_测试用例.pdf` 的格式更新设计文档。
5. 在 PR 或 issue 中引用 [Issue 22871](https://gitcode.com/openharmony/xts_acts/issues/22871) 以便协调修复。

欢迎提交新的系统能力用例、自动化工具或框架改进，一起提升 OpenHarmony XTS 的测试覆盖率和稳定性。

