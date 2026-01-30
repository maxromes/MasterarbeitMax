# Anleitung: Neue Annotation-Dateien auf GitHub synchronisieren

## 1. Datei in RStudio speichern

### Option A: Aus OneDrive importieren
```r
# Lade die CSV-Datei von OneDrive
MeineDaten <- read.csv("C:/Users/romes/OneDrive/Dokumente/Mafia/Masterarbeit/Annotation_reports/DeineDatei.csv")

# Speichere sie im Projekt-Ordner
write.csv(MeineDaten, "Annotation_reports/DeineDatei.csv", row.names = FALSE)
```

### Option B: Manuell kopieren
1. Kopiere die CSV-Datei aus OneDrive
2. Füge sie ein in: `C:\Users\romes\Documents\MasterarbeitMax\Annotation_reports\`

---

## 2. Mit GitHub synchronisieren

Öffne das **RStudio Terminal** (unten im Fenster) und gib diese Befehle ein:

```bash
# Hole neueste Änderungen von GitHub
git pull origin main

# Füge die neue Datei hinzu
git add Annotation_reports/DeineDatei.csv

# Committe mit Nachricht
git commit -m "Add annotation report: DeineDatei"

# Pushe auf GitHub
git push origin main
```

---

## Ordnerstruktur

📁 **Annotation_reports/** → BIIGLE Annotation-Dateien (Originale)  
📁 **data/** → Verarbeitete Daten & Analysen  
  - `*_cleaned.csv` = Dateien mit Spalten 12 (points) und 16 (attributes) gelöscht  
📁 **results/** → R-Analyse-Ergebnisse  
📁 **scripts/** → R-Scripts  

---

## 3. Dateien verarbeiten und in data/ speichern

### Spalten entfernen und speichern:
```bash
python3 << 'EOF'
import csv
import os

# Lese Original-Datei
with open('Annotation_reports/DeineDatei.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    rows = list(reader)

# Lösche Spalten 12 und 16 (Index 11 und 15)
processed_rows = []
for row in rows:
    new_row = [val for i, val in enumerate(row) if i not in [11, 15]]
    processed_rows.append(new_row)

# Speichere als _cleaned Datei
with open('data/DeineDatei_cleaned.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows(processed_rows)

print("✓ Datei verarbeitet: data/DeineDatei_cleaned.csv")
EOF
```

---

## 4. Dateien löschen und synchronisieren

### Im RStudio Files-Panel:
1. Wähle die Datei aus
2. Klick auf "Delete"

### Oder im RStudio Terminal:
```bash
git rm Annotation_reports/AleDatei.csv
```

### Löschung synchronisieren:
```bash
git pull origin main
git add -A
git commit -m "Remove: AleDatei"
git push origin main
```

**`git add -A`** registriert alle Änderungen inklusive Löschungen!

---

## Wichtig!

✅ **Immer `git pull` vor `git push` machen!**  
✅ **Aussagekräftige Commit-Nachrichten schreiben**  
✅ **Dateien im Projekt-Ordner speichern, nicht in OneDrive**  
✅ **Aufräumen und Löschen in RStudio machen, nicht in Codespaces**

---

## Schnell-Referenz

```bash
# Datei hinzufügen:
git pull origin main && \
git add Annotation_reports/DeineDatei.csv && \
git commit -m "Add: DeineDatei" && \
git push origin main

# Verarbeitete Datei pushen:
git pull origin main && \
git add data/DeineDatei_cleaned.csv && \
git commit -m "Add: processed data DeineDatei_cleaned" && \
git push origin main

# Datei löschen:
git pull origin main && \
git add -A && \
git commit -m "Remove: AleDatei" && \
git push origin main

# Alle Änderungen synchronisieren:
git pull origin main && \
git add -A && \
git commit -m "Update: Beschreibung" && \
git push origin main
```

## Verarbeitete Dateien (aktuell)

✅ `data/22375-2510milimani-c10-makarel-formatiert_cleaned.csv` (119 KB)  
✅ `data/22375-2510milimani-c10-makarel-ganz_cleaned.csv` (187 KB)  
✅ `data/TestKopie_cleaned.csv` (197 KB)  

**Gelöschte Spalten:** 12 (points), 16 (attributes)
