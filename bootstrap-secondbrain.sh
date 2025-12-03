#!/bin/bash
set -e

echo "🚀 FABRIC SECOND BRAIN – AUTORUN"

# Use OBSIDIAN_VAULT env var, fallback to ~/Obsidian
export OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-$HOME/Obsidian}"

echo "📁 Using vault: $OBSIDIAN_VAULT"

echo "1️⃣ YAML vereinheitlichen"
fabric apply yaml --add-missing --normalize -r "$OBSIDIAN_VAULT"

echo "2️⃣ Inhalte analysieren"
fabric apply summarize,keywords,tags -r "$OBSIDIAN_VAULT"

echo "3️⃣ Kategorien ableiten"
fabric apply categorize -r "$OBSIDIAN_VAULT" -o rules/categorize.yaml

echo "4️⃣ Projekte extrahieren"
python3 generators/project_extractor.py

echo "5️⃣ Personen extrahieren"
python3 generators/people_extractor.py

echo "6️⃣ Dateien umbenennen"
python3 organize.py rename --rules rules/rename.yaml

echo "7️⃣ Dateien verschieben"
python3 organize.py move --rules rules/categorize.yaml

echo "8️⃣ Tags bereinigen"
python3 organize.py tags --rules rules/tags.yaml

echo "9️⃣ Maps of Content generieren"
python3 generators/moc_builder.py

echo "🔟 Semantic Cluster Maps generieren"
python3 generators/cluster_map.py

echo "🎉 Fertig! Dein Vault wurde vollständig reorganisiert."
