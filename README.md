<div align="center">

# 🎬 TikFetch

**A powerful, user-friendly TikTok video downloader for the terminal.**

Download any TikTok video — or every video from an entire account — in seconds.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-red?logo=youtube)](https://github.com/yt-dlp/yt-dlp)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)](#)
[![License](https://img.shields.io/badge/License-GPLv3-orange)](#license)

</div>

---

## ⚠️ Legal Notice

> **You must have explicit permission from the TikTok content creator before downloading their videos.**  
> TikFetch is intended for **personal, authorised use only**. Downloading content without permission may violate the creator's intellectual property rights and TikTok's Terms of Service.  
> The developers accept **no responsibility** for misuse.

The tool displays a full legal disclaimer on **first run** — you must type `AGREE` before anything happens.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Legal disclaimer** | Full consent screen required on first launch |
| **Single video download** | Paste any TikTok video URL |
| **Bulk account download** | Enter a username → downloads **all** public videos |
| **No-watermark option** | Download the clean version (where available) |
| **Resume support** | Automatically skips already-downloaded files |
| **Live progress bars** | Real-time speed, ETA, and download count |
| **Pretty terminal UI** | Powered by `rich` — colours, panels, and tables |
| **In-app updater** | Update `yt-dlp` from the Settings menu |
| **Cross-platform** | Linux, macOS, and Windows |

---

## 🚀 Quick Start

### Linux / macOS

```bash
git clone https://github.com/pdev-labs/tikfetch.git
cd tikfetch
chmod +x run.sh
./run.sh
```

### Windows

```
git clone https://github.com/pdev-labs/tikfetch.git
cd tikfetch
run.bat
```
Or simply **double-click `run.bat`**.

> The launchers automatically create a Python virtual environment and install all dependencies. No manual `pip install` needed.

---

## 📋 Requirements

| Requirement | Notes |
|---|---|
| **Python 3.8+** | [Download](https://www.python.org/downloads/) — check "Add to PATH" on Windows |
| **ffmpeg** | [Download](https://ffmpeg.org/download.html) — needed for best quality |
| yt-dlp | Auto-installed by launcher |
| rich | Auto-installed by launcher |

### Installing ffmpeg

| OS | Command |
|---|---|
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| Fedora | `sudo dnf install ffmpeg` |
| Arch Linux | `sudo pacman -S ffmpeg` |
| macOS | `brew install ffmpeg` |
| Windows | `winget install ffmpeg` |

---

## 🖥️ Screenshots

### Main Menu
```
  ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
     ██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
     ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝
     ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗
     ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
     ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
              Video Downloader  v1.0.0  ·  Powered by yt-dlp

 ╭──────────────────────────────────────────────────╮
 │  1  │  📥 Download Single Video                  │
 │  2  │  📦 Download Account Videos                │
 │  3  │  ⚙  Settings                               │
 │  4  │  🚪 Exit                                   │
 ╰──────────────────────────────────────────────────╯
```

---

## 📁 Output Structure

```
~/TikTok Downloads/
├── @username/                             ← Bulk account downloads
│   ├── username - Video Title [abc123].mp4
│   └── ...
└── username - Another Video [xyz789].mp4  ← Single video downloads
```

---

## 🔧 Manual Usage (without launcher)

```bash
pip install yt-dlp rich
python tikfetch.py
```

---

## 🛠 Troubleshooting

| Problem | Solution |
|---|---|
| No videos found | Account may be private or username incorrect |
| Download fails | Update yt-dlp via Settings menu or `pip install -U yt-dlp` |
| Watermark always appears | Some videos only provide the watermarked stream |
| Slow / rate limited | Try again later or use a VPN |

---

## 🌍 Bypassing ISP Blocks (e.g., in India)

TikTok is banned in several countries (like India), meaning ISPs block access to `tiktok.com`. If you try to run TikFetch from these regions, the connection will time out. 

To use TikFetch in these countries, you have two options:

### Option 1: Use a Free System-Wide VPN (Recommended & Easiest)
Turn on a VPN on your computer before running the script.
- **Cloudflare WARP (1.1.1.1):** Completely free and very fast. [Download here](https://1.1.1.1/).
- **ProtonVPN:** Has a generous free tier.

*Just turn the VPN on, run `./run.sh`, and TikFetch will work normally!*

### Option 2: Use Proxy settings directly
You can configure a proxy environment variable before running the script in your terminal:

```bash
# For Linux / macOS
export HTTP_PROXY="http://your.proxy.ip:port"
export HTTPS_PROXY="http://your.proxy.ip:port"
./run.sh

# For Windows (Command Prompt)
set HTTP_PROXY=http://your.proxy.ip:port
set HTTPS_PROXY=http://your.proxy.ip:port
run.bat
```

### Option 3: Use a Free Cloud RDP (No VPN required)
If you don't want to install a VPN or mess with proxies locally, you can create a completely free remote Windows desktop hosted on GitHub's USA servers. 

Check out this repository: **[Free-Github-Actions-RDP-for-App-Testing](https://github.com/pdev-labs/Free-Github-Actions-RDP-for-App-Testing)**

By following the instructions there, you'll get a free Windows RDP instance. Since it's hosted in the US, TikTok is unblocked natively! You can just download TikFetch on that remote desktop and run it effortlessly.

---

## 📄 License

TikFetch is released under the **GNU General Public License v3.0 (GPLv3)**.  
See the [LICENSE](LICENSE) file for more details.

Please note that this tool is provided for educational and personal use only.  
Always respect creators' rights and TikTok's Terms of Service.
