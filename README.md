# -Sei-Chan

<div align="center">

Minecraft ↔ Discord 整合管理工具

一款輕量化的 Minecraft 伺服器 Discord 管理應用程式

</div>

⸻

📖 簡介

Sei-Chan 是一款專為 Minecraft Java Edition 伺服器設計的 Discord 整合工具。

透過 Discord Bot、RCON 與伺服器 Log 監控，實現 Minecraft 與 Discord 之間的雙向資訊傳遞。

目前支援：

* Minecraft 伺服器狀態查詢
* BlueMap 地圖展示
* 玩家登入 / 離開通知
* 遊戲聊天同步
* 成就通知
* Discord 訊息傳送至 Minecraft

v2.0.0 開始提供 macOS App 與 DMG 安裝包，無需手動配置 Python 環境即可使用。

⸻

✨ 功能特色

🎮 Minecraft 狀態監控

透過 Discord 指令查看伺服器目前狀態。

包含：

* 伺服器版本
* 在線玩家數量
* 玩家列表
* 伺服器延遲
* 伺服器資訊

指令：

/status

⸻

🗺️ BlueMap 地圖展示

自動從 BlueMap 取得世界地圖資料並生成圖片。

功能：

* 自動拼接地圖 Tile
* Discord Embed 顯示
* 連結 BlueMap 網頁地圖

指令：

/map

⸻

🟢 Minecraft → Discord

自動監控 Minecraft Log，將重要事件傳送至 Discord。

支援：

* 玩家加入伺服器
* 玩家離開伺服器
* 遊戲內聊天
* Advancement 成就完成

範例：

🛬 帝國領域 入國記錄
【入國者】 Player

⸻

💬 Discord → Minecraft

透過 RCON 將 Discord 訊息同步至 Minecraft 遊戲內。

支援：

* Discord 名稱顯示
* 身份組顏色
* Hover 顯示 Discord 資訊

⸻

📦 安裝方式

macOS App（推薦）

前往 Releases 下載最新版本：

Sei-Chan.dmg

安裝後直接啟動即可。

首次啟動時會要求輸入：

* Discord Bot Token
* RCON 密碼
* 伺服器外網 IP
* Minecraft Log 路徑
* Discord 頻道 ID

設定完成後會自動建立：

config.json

⸻

Python 版本

需求：

* Python 3.10+
* Minecraft Java Edition Server
* 已啟用 RCON
* Discord Bot

安裝套件：

pip install -r requirements.txt

啟動：

python main.py

⸻

🏗️ 程式架構

Sei-Chan
main.py
│
├── status.py
│      Minecraft 狀態查詢
│
├── map.py
│      BlueMap 地圖生成
│
├── m2d.py
│      Minecraft → Discord
│
├── d2m.py
│      Discord → Minecraft
│
└── secret.py
       設定管理

⸻

🧩 使用技術

* Python
* discord.py
* mcstatus
* mcrcon
* Pillow

⸻

⚙️ 系統需求

Minecraft

* Minecraft Java Edition Server
* 啟用 RCON
* Minecraft Log 可讀取

Discord

* Discord Bot Token
* Message Content Intent

地圖

* BlueMap（選用）

⸻

🖼️ 截圖

待補

建議放置：

* /status 狀態資訊
* /map 地圖展示
* Minecraft ↔ Discord 聊天同步

⸻

📜 開發資訊

Sei-Chan 是一個個人開發的 Minecraft 伺服器管理工具。

目標是提供簡單、輕量且容易部署的 Minecraft 與 Discord 整合方案。

⸻

📄 License

MIT License