#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════╗
║         TikTok Video Downloader                ║
║   Cross-platform · Powered by yt-dlp           ║
╚════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import platform
import subprocess
from pathlib import Path
from datetime import datetime

# ── Dependency check ──────────────────────────────────────────────────────────
def check_and_install_deps():
    missing = []
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        missing.append("yt-dlp")
    try:
        import rich  # noqa: F401
    except ImportError:
        missing.append("rich")

    if missing:
        print(f"\n[INFO] Installing missing packages: {', '.join(missing)} ...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + missing
        )
        print("[INFO] Packages installed successfully.\n")

check_and_install_deps()

# ── Imports (after install) ───────────────────────────────────────────────────
import yt_dlp
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import (
    Progress, SpinnerColumn, BarColumn,
    TextColumn, TimeElapsedColumn, DownloadColumn
)
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich import box
from rich.align import Align
from rich.padding import Padding
from rich.style import Style
from rich.live import Live
from rich.columns import Columns
from rich.markup import escape

console = Console()

# ── Constants ─────────────────────────────────────────────────────────────────
APP_VERSION   = "1.0.0"
CONFIG_FILE   = Path.home() / ".tiktok_downloader_config.json"
DEFAULT_DIR   = Path.home() / "TikTok Downloads"
TIKTOK_BASE   = "https://www.tiktok.com/@"

# Browser-like headers to prevent TikTok from redirecting to /foryou
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.tiktok.com/",
}

# ── Config helpers ────────────────────────────────────────────────────────────
def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(cfg: dict):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

# ── UI helpers ────────────────────────────────────────────────────────────────
def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def print_banner():
    banner = """
[bold magenta]  ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗[/bold magenta]
[bold magenta]     ██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝[/bold magenta]
[bold magenta]     ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝ [/bold magenta]
[bold magenta]     ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗ [/bold magenta]
[bold magenta]     ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗[/bold magenta]
[bold magenta]     ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝[/bold magenta]
[dim]              Video Downloader  v{ver}  ·  Powered by yt-dlp[/dim]""".format(ver=APP_VERSION)

    console.print(banner)
    console.print()

def print_header(title: str):
    console.print()
    console.print(Rule(f"[bold cyan] {title} [/bold cyan]", style="cyan"))
    console.print()

def success(msg: str):
    console.print(f"  [bold green]✔[/bold green]  {msg}")

def warn(msg: str):
    console.print(f"  [bold yellow]⚠[/bold yellow]  {msg}")

def error(msg: str):
    console.print(f"  [bold red]✘[/bold red]  {msg}")

def info(msg: str):
    console.print(f"  [bold blue]ℹ[/bold blue]  {msg}")

# ── Permission / Disclaimer screen ───────────────────────────────────────────
def show_disclaimer(cfg: dict) -> bool:
    """
    Show legal disclaimer. Returns True if user agrees.
    Saves acceptance to config so it's only shown once.
    """
    if cfg.get("disclaimer_accepted"):
        return True

    clear()
    console.print()

    disclaimer_text = (
        "[bold white]Before using this tool, please read and acknowledge the following:[/bold white]\n\n"
        "[yellow]1. CREATOR PERMISSION[/yellow]\n"
        "   You [bold]MUST[/bold] have explicit permission from the TikTok content creator\n"
        "   before downloading their videos. Downloading without permission may\n"
        "   violate the creator's intellectual property rights.\n\n"
        "[yellow]2. TIKTOK TERMS OF SERVICE[/yellow]\n"
        "   Downloading TikTok videos may violate TikTok's Terms of Service.\n"
        "   Use this tool only for content you are authorised to download\n"
        "   (e.g., your own videos, or videos where the creator has given consent).\n\n"
        "[yellow]3. PERSONAL USE ONLY[/yellow]\n"
        "   Downloaded content should be used for personal, non-commercial purposes\n"
        "   unless you hold the appropriate rights or licences.\n\n"
        "[yellow]4. NO LIABILITY[/yellow]\n"
        "   The developers of this tool accept no responsibility for how you use\n"
        "   the downloaded content. You are solely responsible for ensuring your\n"
        "   use is lawful.\n\n"
        "[yellow]5. RESPECT PRIVACY[/yellow]\n"
        "   Do not download or distribute content that violates anyone's privacy\n"
        "   or that was intended for a restricted audience."
    )

    console.print(
        Panel(
            disclaimer_text,
            title="[bold red]⚠  IMPORTANT — Legal Disclaimer & Permission Notice  ⚠[/bold red]",
            border_style="red",
            padding=(1, 3),
            expand=True,
        )
    )

    console.print()
    console.print(
        Padding(
            "[bold white]To continue, you must confirm that:[/bold white]\n"
            "  [cyan]•[/cyan] You have permission from the creator to download their content.\n"
            "  [cyan]•[/cyan] You will use the downloaded content responsibly and lawfully.\n"
            "  [cyan]•[/cyan] You understand the risks associated with using this tool.",
            (0, 3)
        )
    )
    console.print()

    response = Prompt.ask(
        "  [bold yellow]Type [bold white]AGREE[/bold white] to accept and continue, or press Enter to exit[/bold yellow]",
        default=""
    )

    if response.strip().upper() == "AGREE":
        cfg["disclaimer_accepted"] = True
        cfg["accepted_at"] = datetime.now().isoformat()
        save_config(cfg)
        success("Thank you. You have agreed to the terms.")
        time.sleep(1)
        return True
    else:
        console.print()
        warn("You did not agree to the terms. Exiting.")
        console.print()
        sys.exit(0)

# ── Output directory chooser ──────────────────────────────────────────────────
def choose_output_dir(cfg: dict) -> Path:
    last = cfg.get("last_output_dir", str(DEFAULT_DIR))
    console.print()
    console.print(f"  [dim]Default output folder:[/dim] [bold cyan]{last}[/bold cyan]")
    custom = Prompt.ask(
        "  [bold]Output folder[/bold] [dim](press Enter to use default)[/dim]",
        default=last
    )
    out = Path(custom).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    cfg["last_output_dir"] = str(out)
    save_config(cfg)
    return out

# ── yt-dlp progress hook ──────────────────────────────────────────────────────
class YTDLPProgress:
    """Wraps yt-dlp progress hooks to feed a Rich progress bar."""

    def __init__(self, task_id, progress: Progress):
        self.task_id  = task_id
        self.progress = progress
        self._total   = None

    def hook(self, d: dict):
        status = d.get("status")
        if status == "downloading":
            total   = d.get("total_bytes") or d.get("total_bytes_estimate")
            current = d.get("downloaded_bytes", 0)
            if total and self._total != total:
                self._total = total
                self.progress.update(self.task_id, total=total)
            self.progress.update(self.task_id, completed=current)
        elif status == "finished":
            if self._total:
                self.progress.update(self.task_id, completed=self._total)

# ── Single video download ─────────────────────────────────────────────────────
def download_single_video(cfg: dict):
    print_header("Download Single Video")

    url = Prompt.ask("  [bold]TikTok video URL[/bold]").strip()
    if not url:
        error("No URL entered.")
        return

    # Validate (rough check)
    if "tiktok.com" not in url and "vm.tiktok.com" not in url:
        warn("URL doesn't look like a TikTok link. Attempting anyway...")

    out_dir = choose_output_dir(cfg)
    watermark = Confirm.ask(
        "\n  [bold]Download with TikTok watermark?[/bold]", default=False
    )
    console.print()

    ydl_opts = _build_ydl_opts(out_dir, watermark=watermark)

    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold magenta"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40, style="magenta", complete_style="bold green"),
        DownloadColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("Downloading…", total=None)
        hook_obj = YTDLPProgress(task, progress)
        ydl_opts["progress_hooks"] = [hook_obj.hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename  = ydl.prepare_filename(info_dict)
        except yt_dlp.utils.DownloadError as e:
            console.print()
            error(f"Download failed: {escape(str(e))}")
            _print_troubleshoot()
            return
        except Exception as e:
            console.print()
            error(f"Unexpected error: {escape(str(e))}")
            return

    console.print()
    success(f"Video saved to [bold cyan]{out_dir}[/bold cyan]")
    _show_open_folder_hint(out_dir)

# ── Bulk account download ─────────────────────────────────────────────────────
def _get_cookie_opts(cfg: dict) -> dict:
    """
    Ask the user if they want to supply browser cookies (helps bypass TikTok
    bot detection). Returns extra yt-dlp opts dict.
    """
    browser_map = {
        "1": "chrome",
        "2": "firefox",
        "3": "edge",
        "4": "safari",
        "5": None,   # skip
    }
    console.print()
    console.print(
        Panel(
            "[yellow]TikTok may block automated requests.\n"
            "Providing your browser cookies greatly improves reliability.[/yellow]\n\n"
            "  [cyan]1[/cyan]  Chrome\n"
            "  [cyan]2[/cyan]  Firefox\n"
            "  [cyan]3[/cyan]  Edge\n"
            "  [cyan]4[/cyan]  Safari\n"
            "  [cyan]5[/cyan]  Skip (no cookies — may fail on some accounts)",
            title="[bold]🍪 Cookie Source[/bold]",
            border_style="cyan",
            padding=(1, 3),
        )
    )
    choice = Prompt.ask(
        "  [bold]Select browser to extract cookies from[/bold]",
        choices=["1", "2", "3", "4", "5"],
        default="5",
    )
    browser = browser_map[choice]
    if browser:
        info(f"Will extract cookies from [bold cyan]{browser.title()}[/bold cyan]")
        return {"cookiesfrombrowser": (browser, None, None, None)}
    return {}


def download_account_videos(cfg: dict):
    print_header("Download All Videos from Account")

    console.print(
        Padding(
            "[dim]This will download ALL publicly available videos from a TikTok account.\n"
            "Make sure you have the creator's permission before proceeding.[/dim]",
            (0, 2)
        )
    )
    console.print()

    username = Prompt.ask("  [bold]TikTok username[/bold] [dim](without @)[/dim]").strip().lstrip("@")
    if not username:
        error("No username entered.")
        return

    # Use @username (not @username/video) — the /video suffix causes TikTok
    # to redirect to /foryou when no session is present.
    account_url = f"{TIKTOK_BASE}{username}"
    info(f"Target: [bold cyan]{account_url}[/bold cyan]")

    out_dir    = choose_output_dir(cfg)
    watermark  = Confirm.ask("\n  [bold]Download with TikTok watermark?[/bold]", default=False)
    skip_exist = Confirm.ask(
        "  [bold]Skip already downloaded videos?[/bold]", default=True
    )

    # Ask for cookie source — significantly improves TikTok reliability
    cookie_opts = _get_cookie_opts(cfg)
    console.print()

    # ── Fetch video list ──────────────────────────────────────────────────────
    console.print("  [dim]Fetching video list (this may take a moment)…[/dim]")

    flat_opts: dict = {
        "quiet":         True,
        "no_warnings":   True,
        "extract_flat":  "in_playlist",
        "skip_download": True,
        "ignoreerrors":  True,
        "http_headers":  BROWSER_HEADERS,
        "extractor_args": {
            "tiktok": {"webpage_download": ["1"]},
        },
    }
    flat_opts.update(cookie_opts)

    video_urls: list[str] = []
    try:
        with yt_dlp.YoutubeDL(flat_opts) as ydl:
            info_dict = ydl.extract_info(account_url, download=False)

            # Guard against /foryou redirect (TikTok bot detection)
            if info_dict:
                page_url = info_dict.get("webpage_url", "") or info_dict.get("url", "")
                if "foryou" in page_url or info_dict.get("id") == "foryou":
                    console.print()
                    error("TikTok redirected to the 'For You' page — bot detection triggered.")
                    console.print(
                        Panel(
                            "[yellow]TikTok blocked the request.[/yellow]\n\n"
                            "To fix this, re-run and choose a [bold]browser cookie source[/bold]\n"
                            "when prompted. This lets TikFetch use your logged-in session.\n\n"
                            "Other options:\n"
                            "  • Make sure you are [bold]logged in to TikTok[/bold] in that browser first\n"
                            "  • Try a different browser\n"
                            "  • Use a VPN and try again\n"
                            "  • Update yt-dlp: [bold cyan]pip install -U yt-dlp[/bold cyan]",
                            title="[bold red]⚠ Bot Detection[/bold red]",
                            border_style="red",
                            padding=(1, 3),
                        )
                    )
                    return

            if info_dict and "entries" in info_dict:
                for e in info_dict["entries"]:
                    if not e:
                        continue
                    vid_id  = e.get("id", "")
                    vid_url = e.get("url") or e.get("webpage_url") or ""
                    # Rebuild a proper watch URL if only an ID or short path came back
                    if not vid_url.startswith("http"):
                        vid_url = f"https://www.tiktok.com/@{username}/video/{vid_id}"
                    video_urls.append(vid_url)

    except Exception as e:
        console.print()
        error(f"Could not fetch video list: {escape(str(e))}")
        _print_troubleshoot()
        return

    if not video_urls:
        console.print()
        warn("No public videos found for this account.")
        warn("The account may be private, empty, or the username may be incorrect.")
        warn("Try running again and selecting a browser cookie source when prompted.")
        return

    console.print()
    success(f"Found [bold]{len(video_urls)}[/bold] video(s) for [bold cyan]@{username}[/bold cyan]")
    console.print()

    if not Confirm.ask(f"  [bold]Proceed with downloading {len(video_urls)} video(s)?[/bold]", default=True):
        info("Download cancelled.")
        return

    console.print()

    # User-specific subfolder
    user_dir = out_dir / f"@{username}"
    user_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = _build_ydl_opts(user_dir, watermark=watermark, skip_existing=skip_exist)
    ydl_opts.update(cookie_opts)

    downloaded = 0
    skipped    = 0
    failed     = 0

    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold magenta"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=35, style="magenta", complete_style="bold green"),
        TextColumn("[dim]{task.completed}/{task.total}[/dim]"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        overall = progress.add_task(
            f"[bold]@{username}[/bold] — overall", total=len(video_urls)
        )
        dl_task = progress.add_task("Current video…", total=None)
        hook_obj = YTDLPProgress(dl_task, progress)

        def _hook(d: dict):
            status = d.get("status")
            if status in ("downloading", "finished"):
                hook_obj.hook(d)

        ydl_opts["progress_hooks"] = [_hook]

        for idx, vid_url in enumerate(video_urls, 1):
            progress.update(dl_task, description=f"Video {idx}/{len(video_urls)}…", completed=0, total=None)
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([vid_url])
                downloaded += 1
            except yt_dlp.utils.DownloadError as e:
                msg = str(e)
                if "has already been downloaded" in msg or "already been downloaded" in msg:
                    skipped += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
            finally:
                progress.advance(overall)

    console.print()
    _print_summary_table(username, len(video_urls), downloaded, skipped, failed, user_dir)
    _show_open_folder_hint(user_dir)

# ── yt-dlp options builder ────────────────────────────────────────────────────
def _build_ydl_opts(out_dir: Path, watermark: bool = False, skip_existing: bool = True) -> dict:
    template = str(out_dir / "%(uploader)s - %(title).80s [%(id)s].%(ext)s")

    opts: dict = {
        "outtmpl":        template,
        "quiet":          True,
        "no_warnings":    True,
        "ignoreerrors":   True,
        "retries":        5,
        "fragment_retries": 5,
        "concurrent_fragment_downloads": 4,
        "nooverwrites":   skip_existing,
        "continuedl":     True,
        "merge_output_format": "mp4",
        "http_headers":   BROWSER_HEADERS,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
        "extractor_args": {
            "tiktok": {"webpage_download": ["1"]},
        },
    }

    if watermark:
        # Download the watermarked version (TikTok's default direct stream)
        opts["format"] = "download_addr-0"
    else:
        # Prefer the highest quality without watermark
        opts["format"] = "best[ext=mp4]/best"

    return opts

# ── Helpers ───────────────────────────────────────────────────────────────────
def _print_summary_table(username, total, downloaded, skipped, failed, out_dir: Path):
    table = Table(
        title=f"  Download Summary — @{username}",
        box=box.ROUNDED,
        border_style="cyan",
        show_header=True,
        header_style="bold magenta",
        padding=(0, 2),
    )
    table.add_column("Metric",    style="bold white")
    table.add_column("Count",     justify="right", style="bold cyan")

    table.add_row("Total videos found", str(total))
    table.add_row("[bold green]Downloaded[/bold green]", f"[bold green]{downloaded}[/bold green]")
    table.add_row("[bold yellow]Skipped (exists)[/bold yellow]", f"[bold yellow]{skipped}[/bold yellow]")
    table.add_row("[bold red]Failed[/bold red]",        f"[bold red]{failed}[/bold red]")
    table.add_row("Output folder",      f"[dim]{out_dir}[/dim]")

    console.print(table)

def _show_open_folder_hint(folder: Path):
    console.print()
    if platform.system() == "Windows":
        hint = f'  Run [bold cyan]explorer "{folder}"[/bold cyan] to open the folder.'
    elif platform.system() == "Darwin":
        hint = f'  Run [bold cyan]open "{folder}"[/bold cyan] to open the folder.'
    else:
        hint = f'  Run [bold cyan]xdg-open "{folder}"[/bold cyan] to open the folder.'
    info(hint)

def _print_troubleshoot():
    console.print()
    console.print(
        Panel(
            "[yellow]Troubleshooting tips:[/yellow]\n"
            "  • Make sure the video/account is [bold]public[/bold].\n"
            "  • Run again and select a [bold]browser cookie source[/bold] when prompted.\n"
            "  • Make sure you are logged in to TikTok in that browser first.\n"
            "  • Try updating yt-dlp: [bold cyan]pip install -U yt-dlp[/bold cyan]\n"
            "  • Some regions block TikTok — try using a VPN.\n"
            "  • TikTok may have changed its API. Check yt-dlp GitHub for updates.",
            border_style="yellow",
            padding=(1, 3),
        )
    )

# ── Settings menu ─────────────────────────────────────────────────────────────
def settings_menu(cfg: dict):
    print_header("Settings")

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("Key",   style="bold cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Default download folder", cfg.get("last_output_dir", str(DEFAULT_DIR)))
    table.add_row("Disclaimer accepted",     "✔ Yes" if cfg.get("disclaimer_accepted") else "✘ No")
    accepted_at = cfg.get("accepted_at", "—")
    table.add_row("Accepted at",             accepted_at)
    table.add_row("Config file",             str(CONFIG_FILE))

    console.print(table)
    console.print()

    options = [
        "1. Change default download folder",
        "2. Reset disclaimer (will ask again on next run)",
        "3. Update yt-dlp to latest version",
        "4. Back to main menu",
    ]
    for o in options:
        console.print(f"  [cyan]{o}[/cyan]")

    console.print()
    choice = Prompt.ask("  [bold]Choose[/bold]", choices=["1", "2", "3", "4"], default="4")

    if choice == "1":
        new_dir = Prompt.ask("  [bold]New download folder[/bold]", default=cfg.get("last_output_dir", str(DEFAULT_DIR)))
        p = Path(new_dir).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        cfg["last_output_dir"] = str(p)
        save_config(cfg)
        success(f"Default folder updated to [bold cyan]{p}[/bold cyan]")

    elif choice == "2":
        cfg.pop("disclaimer_accepted", None)
        cfg.pop("accepted_at", None)
        save_config(cfg)
        success("Disclaimer reset. It will show again on next run.")

    elif choice == "3":
        console.print()
        info("Updating yt-dlp…")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                success("yt-dlp updated successfully!")
            else:
                error(f"Update failed:\n{result.stderr}")
        except Exception as e:
            error(str(e))

    time.sleep(1)

# ── Main menu ─────────────────────────────────────────────────────────────────
def main_menu(cfg: dict):
    while True:
        clear()
        print_banner()

        # Status bar
        out_dir = cfg.get("last_output_dir", str(DEFAULT_DIR))
        console.print(
            Panel(
                f"[dim]Output folder:[/dim] [bold cyan]{out_dir}[/bold cyan]   "
                f"[dim]OS:[/dim] [bold]{platform.system()} {platform.release()}[/bold]",
                border_style="dim",
                padding=(0, 2),
            )
        )
        console.print()

        options_table = Table(
            box=box.ROUNDED, border_style="magenta",
            show_header=False, padding=(0, 3), expand=False
        )
        options_table.add_column("Opt",   style="bold magenta", no_wrap=True, width=5)
        options_table.add_column("Label", style="bold white")
        options_table.add_column("Desc",  style="dim")

        options_table.add_row("1", "📥  Download Single Video",  "Download one video by URL")
        options_table.add_row("2", "📦  Download Account Videos", "Download ALL videos from a username")
        options_table.add_row("3", "⚙   Settings",               "Change output folder · update yt-dlp")
        options_table.add_row("4", "🚪  Exit",                   "Quit the program")

        console.print(Align.center(options_table))
        console.print()

        choice = Prompt.ask(
            "  [bold yellow]Select an option[/bold yellow]",
            choices=["1", "2", "3", "4"],
            default="1"
        )

        if choice == "1":
            download_single_video(cfg)
            console.print()
            Prompt.ask("  [dim]Press Enter to return to the menu…[/dim]", default="")

        elif choice == "2":
            download_account_videos(cfg)
            console.print()
            Prompt.ask("  [dim]Press Enter to return to the menu…[/dim]", default="")

        elif choice == "3":
            settings_menu(cfg)

        elif choice == "4":
            clear()
            console.print()
            console.print(Align.center("[bold magenta]Thanks for using TikTok Downloader! Goodbye 👋[/bold magenta]"))
            console.print()
            sys.exit(0)

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = load_config()

    # Always show disclaimer if not yet accepted
    show_disclaimer(cfg)

    main_menu(cfg)
