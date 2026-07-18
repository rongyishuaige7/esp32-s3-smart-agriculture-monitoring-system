# 第三方组件、派生来源与许可证提示

本文件只记录当前可识别的直接依赖、已随源码分发的派生文件和已知传递依赖线索，不构成完整 SBOM、法律意见或二进制再分发清单。仓库不提交 NuGet 缓存、PlatformIO 缓存、固件二进制或桌面发布包；构建、修改或分发二进制前，使用者须按实际解析版本、传递依赖、NOTICE、链接方式和许可证条件自行复核。

## 本项目许可范围

根目录 [LICENSE](LICENSE) 仅适用于 Rongyi 自有的公开整理代码、文档、BOM 和源码推导接线边界图。它不把第三方组件、商标、SDK、构建产物或保留归属的派生文件概括为“全仓 MIT”。

## 随源码分发的 ACD10

| 文件/组件 | 来源与版本 | 许可处理 |
| :-- | :-- | :-- |
| `hardware/firmware/lib/ACD10/ACD10.h`、`ACD10.cpp` | 基于 Rob Tillaart 的 [ACD10 v0.2.3](https://github.com/RobTillaart/ACD10/tree/f5864ec03e4662098c84731bc470f8835b15cc91) 整理的派生副本，文件头标注 v0.2.3（2023-09-25）；不是上游字节级镜像 | MIT；保留原作者/来源标记，并在 [LICENSES/ACD10-MIT.txt](LICENSES/ACD10-MIT.txt) 保留完整许可证文本。 |

## ESP32 / PlatformIO 直接依赖

| 组件 | 公开构建约束 | 许可线索 | 上游 |
| :-- | :-- | :-- | :-- |
| PlatformIO Core | 6.1.19（CI/构建环境） | Apache-2.0 | https://github.com/platformio/platformio-core |
| Espressif32 Platform | 6.13.0 | Apache-2.0 | https://github.com/platformio/platform-espressif32 |
| Arduino-ESP32 framework | 由 PlatformIO 解析（实际解析版本须由隔离构建记录） | LGPL-2.1-or-later（以实际解析上游为准） | https://github.com/espressif/arduino-esp32 |
| DHT sensor library / Adafruit Unified Sensor | 1.4.6 / 1.1.14 | MIT / Apache-2.0 | https://github.com/adafruit/DHT-sensor-library |
| BH1750 | 1.3.0 | MIT | https://registry.platformio.org/libraries/claws/BH1750 |
| Adafruit SSD1306 / GFX | 2.5.9 / 1.11.9 | BSD-3-Clause / BSD-2-Clause | https://github.com/adafruit/Adafruit_SSD1306 |
| Adafruit BMP280 | 2.6.8 | 源码头为 BSD 许可线索；二进制分发前须保留上游头部与复核实际版本 | https://github.com/adafruit/Adafruit_BMP280 |
| Adafruit BusIO（传递依赖） | 由 PlatformIO 解析（实际解析版本须由隔离构建记录） | MIT | https://github.com/adafruit/Adafruit_BusIO |
| FastLED | 3.6.0 | MIT | https://github.com/FastLED/FastLED |

Arduino-ESP32 含 LGPL 许可线索。当前仓仅公开源代码、不分发预构建 firmware 或桌面二进制；若后续分发二进制、商业产品或静态链接产物，必须另行完成源码、重新链接、NOTICE 与实际依赖版本审查。

## .NET 直接依赖

| 组件 | 版本 | 许可线索 | 上游 |
| :-- | :-- | :-- | :-- |
| Avalonia / Avalonia.Desktop / Fluent | 11.2.2 | MIT | https://github.com/AvaloniaUI/Avalonia |
| Avalonia.Controls.DataGrid | 11.2.0 | MIT | https://github.com/AvaloniaUI/Avalonia |
| CommunityToolkit.Mvvm | 8.3.2 | MIT | https://github.com/CommunityToolkit/dotnet |

桌面项目使用内置示例数据。NuGet、.NET SDK、PlatformIO 和 ESP32 依赖不随本仓再分发。
