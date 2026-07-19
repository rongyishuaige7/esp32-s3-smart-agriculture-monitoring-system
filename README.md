# 基于ESP32-S3和Avalonia的智能农业环境监测系统

> 本科阶段完成的软硬件教学原型。项目包含 ESP32-S3 传感器/OLED 固件，以及 Avalonia/.NET 8 本地桌面数据展示与内置示例数据展示代码，用于学习环境数据采集、桌面界面和受控局域网遥测边界。

[![Validate](https://github.com/rongyishuaige7/esp32-s3-smart-agriculture-monitoring-system/actions/workflows/validate.yml/badge.svg)](https://github.com/rongyishuaige7/esp32-s3-smart-agriculture-monitoring-system/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/own%20code-MIT-f97316.svg)](LICENSE)

> [!CAUTION]
> **使用提示：** 本项目用于环境数据采集、桌面界面和局域网遥测学习，不作为农业自动化、告警、远程控制或生产部署方案。

## 项目资料

这里整理了项目照片、界面截图和相关资料；文件处理说明见 [MEDIA_EVIDENCE](docs/MEDIA_EVIDENCE.md)。

![智能农业桌面原型，2026-03-24](assets/photos/historical-prototype.jpg)

## 系统功能

```text
DHT11 / BH1750 / ACD10 / BMP280 / SSD1306
  → ESP32-S3 中的周期性读取与本地 OLED 展示
  → 可选：明确 opt-in 的单向、无认证局域网教学遥测

Avalonia / .NET 8 本地示例数据界面
  → 显示明确标注为“非真机”的环境数据
  → 公开默认不监听网络、不发送命令、不提供设备控制或持久化入口
```

- `ACD10` 代码等待预热；使用前请核对预热、地址、电平、供电与模块行为。
- 公开桌面端使用内置示例数据；它不提供真实设备接收、账号、数据库、持久化、迁移、备份、删除、审计或生产数据能力。
- “本地显示阈值”只影响桌面端展示判断，公开默认不会同步给设备，更不会自动控制任何负载。

## 硬件与电气说明

| 模块 / 信号 | 源码接口 | 当前可确认事实 | 实物仍需确认 |
| :-- | :-- | :-- | :-- |
| ESP32-S3 | `esp32-s3-devkitc-1` 构建环境 | PlatformIO 板型配置 | 真实开发板型号、USB、供电与启动脚 |
| DHT11 | GPIO4 | 温湿度读取入口 | 模块电压、上拉、线长、失效读数 |
| BH1750 | I²C GPIO8 / GPIO9 | 光照读取入口 | 地址、供电、总线质量、标定 |
| ACD10 | I²C 常见 `0x2A` | 本地库读取入口与预热逻辑 | 模块型号、电平、预热、准确性、CO₂ 语义 |
| BMP280 | I²C `0x76` | 气压读取入口 | 地址、模块、电平、准确性 |
| SSD1306 OLED | I²C `0x3C` | 本地显示入口 | 屏幕型号、地址、电压、显示效果 |
| GPIO5 / GPIO6 | 风扇驱动信号候选 | 默认设为输入；opt-in 分支也固定低电平 | 驱动器、极性、电流、保护、共地与真实负载 |
| GPIO38 | WS2812B 数据候选 | 默认设为输入；opt-in 分支输出黑色 | 灯带电源、电平、限流、共地与真实行为 |

[BOM](hardware/BOM.csv)、[接线图](hardware/wiring-diagram.svg)和[硬件说明](HARDWARE.md)列出了项目接口。断电后再接线，确认模块额定电压、电流、电平、供电能力、公共地、驱动与保护；ESP32 GPIO 不得直接驱动风扇、灯带或任何高电流/市电负载。

## 构建与本地教学配置

### 1. 公开门禁（推荐）

```bash
git clone https://github.com/rongyishuaige7/esp32-s3-smart-agriculture-monitoring-system.git
cd esp32-s3-smart-agriculture-monitoring-system
bash scripts/verify.sh
```

### 2. 桌面端示例数据展示

```bash
dotnet restore SmartAgriculture.sln
dotnet build SmartAgriculture.sln --configuration Release
```

桌面端启动后加载内置示例数据（非真机）；它不会连接数据库、监听网络或发送设备命令。

### 3. 固件公开默认构建

```bash
python3 -m pip install 'platformio==6.1.19'
pio run -d hardware/firmware -e esp32-s3-public-default
```

### 4. 受监督局域网/低压台架 opt-in

```bash
cp hardware/firmware/src/config.local.example.h hardware/firmware/src/config.local.h
# 只在隔离、可信局域网和受监督低压台架中，明确填写本机配置。
# 保持两个实验宏为 0，除非自行完成网络、电气和风险复核。
```

`config.local.h` 被 Git 忽略。只有在使用者本机把 `ENABLE_EXPERIMENTAL_WIFI_TCP` 或 `ENABLE_EXPERIMENTAL_ACTUATORS` 设为精确值 `1` 时，相应 compile-time 分支才会存在。网络 opt-in 仅尝试**单向、无认证**的教学遥测；执行器 opt-in 仍固定让已知输出保持低电平/黑色，不提供自动控制或远程命令。它们不构成设备身份、授权、加密、命令确认、可靠通信、物理动作或电气安全保证。

## 项目资料说明

本仓不包含本地 Wi-Fi 配置、私网地址、客户资料或真实环境数据。报告问题时请勿提交 Wi-Fi 凭据、私网 IP/MAC、数据库配置、照片 EXIF/GPS、串口日志或网络抓包。

## 许可与第三方组件

Rongyi 自有的公开整理代码、文档、BOM 和边界图以 [MIT License](LICENSE) 发布。随源码分发的 ACD10 及构建依赖的归属、许可证和后续二进制分发注意事项见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。
