#!/bin/bash
set -e

echo "🚀 LOCAL SECOND BRAIN – AUTORUN (ohne Fabric)"

# Use OBSIDIAN_VAULT env var, fallback to ~/Obsidian
export OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-$HOME/Obsidian}"

echo "📁 Using vault: $OBSIDIAN_VAULT"

echo "1️⃣ YAML-Header hinzufügen, falls fehlend"
python3 auto_yaml_header.py || echo "⚠️ auto_yaml_header.py fehlgeschlagen, weiter..."

echo "2️⃣ Auto-Tags über einfache Keyword-Regeln"
python3 auto_tags.py || echo "⚠️ auto_tags.py fehlgeschlagen, weiter..."

echo "3️⃣ Dateien umbenennen"
python3 organize.py rename --rules rules/rename.yml || echo "⚠️ organize.py rename fehlgeschlagen, weiter..."

echo "4️⃣ Dateien verschieben"
python3 organize.py move --rules rules/categorize.yml || echo "⚠️ organize.py move fehlgeschlagen, weiter..."

echo "5️⃣ Tags bereinigen"
python3 organize.py tags --rules rules/tags.yml || echo "⚠️ organize.py tags fehlgeschlagen, weiter..."

echo "6️⃣ Maps of Content generieren"
python3 generators/moc_builder.py || echo "⚠️ moc_builder.py fehlgeschlagen, weiter..."

echo "7️⃣ Semantic Cluster Maps generieren (Tags/Topics)"
python3 generators/cluster_map.py || echo "⚠️ cluster_map.py fehlgeschlagen, weiter..."

echo "🎉 Lauf abgeschlossen (lokale Orga ohne Fabric)."
