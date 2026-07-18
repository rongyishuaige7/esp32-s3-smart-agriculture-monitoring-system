# Hardware Lab 索引卡片

> 只有独立仓已完成 Description/Topics 回读、`main` 当前 exact SHA 的 Actions 成功、公开范围门禁通过且仓库为 Public 后，才可把下面卡片加入 `rongyishuaige7/hardware-lab`。在线事实未回读前不得提前加入。

## 基于ESP32-S3和Avalonia的智能农业环境监测系统

- **仓库 slug：** `esp32-s3-smart-agriculture-monitoring-system`
- **一句话：** 基于 ESP32-S3、DHT11、BH1750、ACD10、BMP280、OLED 与 Avalonia/.NET 8 示例数据界面的环境监测教学原型。
- **技术：** ESP32-S3 / Arduino / PlatformIO / Avalonia / .NET 8 / DHT11 / BH1750 / ACD10 / BMP280 / SSD1306。
- **公开默认：** 固件不连接 Wi-Fi/TCP，GPIO5/GPIO6/GPIO38 为输入；桌面端使用示例数据（非真机），不含网络 listener、设备控制或下行命令。传感器/OLED 仍可能初始化，不代表无外设 I/O、电气安全或外部负载已关闭。
- **可选实验：** compile-time opt-in 的单向局域网教学遥测和输出保持关闭的执行器分支；没有身份、TLS、认证、ACK、可靠投递或远程控制。
- **未公开素材：** 实物照片、演示视频、原理图、PCB、EDA、Gerber、制造文件。
- **不适用：** 农业自动化、可靠告警、作物/空气质量/安全结论、远程控制、无人值守、生产或工业系统。
- **验证边界：** CI 或本地构建仅表示公开源码门禁和构建，不表示烧录、传感器、OLED、网络、桌面界面、执行器、电气安全或真实环境效果。

- **项目素材：** 已补充项目照片、界面截图和相关资料；范围和版本差异见 [`MEDIA_EVIDENCE.md`](MEDIA_EVIDENCE.md)。
