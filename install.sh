#!/bin/bash
set -e

echo "📦 Installing Fabric Second Brain environment..."

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 1. Python venv
if [ ! -d ".venv" ]; then
  echo "🐍 Creating virtual environment (.venv)..."
  python3 -m venv .venv
else
  echo "✅ Virtual environment .venv already exists."
fi

# 2. Activate venv
echo "⚙️  Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

# 3. Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# 4. Install requirements
echo "📥 Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# 5. Make scripts executable
echo "🔐 Marking scripts as executable..."
chmod +x bootstrap-secondbrain.sh
chmod +x organize.py
chmod +x generators/*.py || true

echo ""
echo "✅ Installation complete."

echo ""
echo "🔧 Usage:"
echo "  1) Set your vault path (optional, default is ~/Obsidian):"
echo "       export OBSIDIAN_VAULT=\"/path/to/your/vault\""
echo "  2) Run:"
echo "       source .venv/bin/activate"
echo "       ./bootstrap-secondbrain.sh"
