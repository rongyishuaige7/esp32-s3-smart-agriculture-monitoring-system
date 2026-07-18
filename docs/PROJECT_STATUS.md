# 项目状态与证据边界

**项目：** 基于ESP32-S3和Avalonia的智能农业环境监测系统
**更新时间：** 2026-07-18（文档生成日期，不代表硬件测试日期）

GitHub 仓库可见性、默认分支、当前 HEAD、Description/Topics 与 Actions exact-SHA 结果必须由 GitHub 页面/API 实时回读；本文件不以候选目录、旧构建物或历史工程替代这些在线事实。

| 范围 | 已确认事实 | 不可据此推出 |
| :-- | :-- | :-- |
| 公开净化 | 候选只从显式 allowlist 单向复制，排除原 `App.config`、ZIP、IDE 状态和构建产物 | 原工程全量安全、历史安全或真实配置安全 |
| 桌面默认 | 无 TCP listener、无下行命令、无设备控制页；加载内置示例数据（非真机） | 网络安全、真实数据、持久化、实际 UI/设备联调 |
| 固件默认 | 不连接 Wi-Fi/TCP；GPIO5、GPIO6、GPIO38 为输入 | 无外设 I/O、外部负载物理关闭、传感器准确或电气安全 |
| 可选分支 | 网络与执行器均为显式 compile-time opt-in；网络仅单向遥测，执行器分支固定已知输出为低 | 身份、授权、可靠通信、实体动作或安全控制 |
| 构建 | 需由 `scripts/verify.sh` 的本地隔离构建和当前 `main` exact-SHA Actions 分别提供证据 | 烧录、真机、Wi-Fi、TCP、传感器、OLED、执行器或电气安全已验证 |
| 真机复测 | **未执行**当前公开 commit 的日期化复测 | 任何“当前硬件已验证”“已联调”“可部署”结论 |
| 媒体/EDA | **未提供**实物照片、视频、原理图、PCB、Gerber、制造文件 | 外观、焊接、实际接线、生产能力或产品化状态 |

只有公开仓 `main` 当前 exact SHA 已取得 completed / success 的 Actions 结果，并已回读仓库元数据后，Hardware Lab 与 Profile 才能引用该提交；不能预填成功或真机结论。
