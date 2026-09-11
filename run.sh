#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════
#  TikFetch — Linux / macOS Launcher
# ══════════════════════════════════════════════════════════
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
MAIN_SCRIPT="$SCRIPT_DIR/tikfetch.py"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

# ── Colours ───────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}[INFO]${RESET} $*"; }
success() { echo -e "${GREEN}[OK]${RESET}   $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET} $*"; }
die()     { echo -e "${RED}[ERROR]${RESET} $*" >&2; exit 1; }

# ── Check Python ──────────────────────────────────────────
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        VER=$("$cmd" --version 2>&1 | awk '{print $2}')
        MAJOR=$(echo "$VER" | cut -d. -f1)
        MINOR=$(echo "$VER" | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    die "Python 3.8+ is required but not found.\n  Install it from: https://www.python.org/downloads/"
fi

success "Found Python: $($PYTHON --version)"

# ── Create virtualenv ─────────────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment at $VENV_DIR …"
    "$PYTHON" -m venv "$VENV_DIR"
    success "Virtual environment created."
fi

# ── Activate venv ─────────────────────────────────────────
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
PYTHON="$VENV_DIR/bin/python"

# ── Install / update dependencies ─────────────────────────
if [ -f "$REQ_FILE" ]; then
    info "Checking dependencies…"
    "$PYTHON" -m pip install --quiet --upgrade pip
    "$PYTHON" -m pip install --quiet -r "$REQ_FILE"
    success "Dependencies ready."
else
    warn "requirements.txt not found — installing core deps directly."
    "$PYTHON" -m pip install --quiet --upgrade yt-dlp rich playwright
fi

info "Installing browser binaries for Playwright..."
"$PYTHON" -m playwright install --with-deps chromium

# ── Also check ffmpeg ─────────────────────────────────────
if ! command -v ffmpeg &>/dev/null; then
    echo ""
    warn "ffmpeg is not installed. Video merging may not work correctly."
    warn "Install it with:"
    warn "  Ubuntu/Debian : sudo apt install ffmpeg"
    warn "  Fedora        : sudo dnf install ffmpeg"
    warn "  Arch          : sudo pacman -S ffmpeg"
    warn "  macOS (brew)  : brew install ffmpeg"
    echo ""
    read -rp "Press Enter to continue anyway, or Ctrl+C to abort..."
fi

# ── Launch ────────────────────────────────────────────────
echo ""
exec "$PYTHON" "$MAIN_SCRIPT" "$@"
