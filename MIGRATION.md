# Vault Migration Guide

## Aktuelle Situation

Dein Vault `/Users/anton.feldmann/lynq/` enthält:

- ✅ PARA-Ordner wurden erstellt (01_Projects, 02_Areas, 03_Resources, 04_Archive)
- 18 Projekt-Ordner im Root-Verzeichnis
- 1 Markdown-Datei: `00-Projects-Index.md`

## Migration-Strategie

### Option 1: Manuelle Migration (empfohlen für Kontrolle)

Verschiebe deine Ordner manuell in die PARA-Struktur:

```bash
cd /Users/anton.feldmann/lynq/

# Aktive Projekte → 01_Projects/
mv airbyte-updater 01_Projects/
mv datalynq 01_Projects/
mv honeytrap 01_Projects/
mv tamagochi 01_Projects/
# ... weitere aktive Projekte

# Verantwortungsbereiche → 02_Areas/
mv acc 02_Areas/
mv github-actions 02_Areas/
# ... weitere Areas

# Referenzmaterial → 03_Resources/
mv "whitepaper-energiezaehler" 03_Resources/
mv "lynqtech projektentscheidungsdokumente" 03_Resources/
# ... weitere Resources

# Abgeschlossene/Inaktive → 04_Archive/
mv aws-batch-jobdef-validator 04_Archive/
# ... weitere Archive
```

### Option 2: Automatische Organisation mit Fabric AI

Nach manueller Verschiebung der Ordner:

```bash
source .venv/bin/activate
export OBSIDIAN_VAULT="/Users/anton.feldmann/lynq"

# Vollständige Organisation
./bootstrap-secondbrain.sh
```

Dies führt aus:

1. YAML Frontmatter normalisieren
2. Inhalte analysieren (Summaries, Keywords, Tags)
3. Auto-Kategorisierung
4. Projekt/Personen-Extraktion
5. Datei-Umbenennung
6. Ordner-Organisation
7. Tag-Bereinigung
8. MOC-Generierung
9. Cluster-Maps

### Option 3: Schrittweise Organisation

```bash
source .venv/bin/activate

# 1. Nur Dateien analysieren
python3 organize.py tags --rules rules/tags.yaml

# 2. Nur umbenennen
python3 organize.py rename --rules rules/rename.yaml

# 3. In PARA-Struktur verschieben
python3 organize.py move --rules rules/categorize.yaml

# 4. MOCs generieren
python3 generators/moc_builder.py
```

## Kategorisierungs-Regeln

Die Datei `rules/categorize.yml` definiert, wie Notizen kategorisiert werden:

```yaml
categories:
  Projects:
    folder: "01_Projects"
    tags: ["project", "todo", "task", "deadline"]

  Areas:
    folder: "02_Areas"
    tags: ["area", "responsibility", "role", "department"]

  Resources:
    folder: "03_Resources"
    tags: ["research", "knowledge", "reference", "info"]

  Archives:
    folder: "04_Archive"
    tags: ["archive", "old", "inactive"]
```

Passe diese Regeln nach deinen Bedürfnissen an!

## Nächste Schritte

1. ✅ PARA-Struktur ist erstellt
2. ⏳ Verschiebe Ordner manuell in passende PARA-Kategorien
3. ⏳ Führe `./bootstrap-secondbrain.sh` aus
4. ⏳ Prüfe die generierten Index-Dateien und Cluster-Maps

## Tipps

- Starte mit wenigen Ordnern zum Testen
- Erstelle Backups vor der ersten Organisation
- Nutze `--dry-run` Flags zum Testen
- Passe `rules/*.yml` an deine Workflows an
