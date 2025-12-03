#!/bin/bash
set -e

echo "🚀 LOCAL SECOND BRAIN – AUTORUN (ohne Fabric)"

# Use OBSIDIAN_VAULT env var, fallback to ~/Obsidian
export OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-$HOME/Obsidian}"

echo "📁 Using vault: $OBSIDIAN_VAULT"

echo "1️⃣ YAML-Header hinzufügen, falls fehlend"
uv run auto-yaml-header || echo "⚠️ auto-yaml-header fehlgeschlagen, weiter..."

echo "2️⃣ Auto-Tags über einfache Keyword-Regeln"
uv run auto-tags || echo "⚠️ auto-tags fehlgeschlagen, weiter..."

echo "3️⃣ Dateien umbenennen"
uv run organize rename --rules rules/rename.yml || echo "⚠️ organize rename fehlgeschlagen, weiter..."

echo "4️⃣ Dateien verschieben"
uv run organize move --rules rules/categorize.yml || echo "⚠️ organize move fehlgeschlagen, weiter..."

echo "5️⃣ Tags bereinigen"
uv run organize tags --rules rules/tags.yml || echo "⚠️ organize tags fehlgeschlagen, weiter..."

echo "6️⃣ Maps of Content generieren"
uv run moc-builder || echo "⚠️ moc-builder fehlgeschlagen, weiter..."

echo "7️⃣ Semantic Cluster Maps generieren (Tags/Topics)"
uv run cluster-map || echo "⚠️ cluster-map fehlgeschlagen, weiter..."

echo "🎉 Lauf abgeschlossen (lokale Orga ohne Fabric)."
