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

📁 **Annotation_reports/** → BIIGLE Annotation-Dateien  
📁 **data/** → Andere Rohdaten  
📁 **results/** → R-Analyse-Ergebnisse  
📁 **scripts/** → R-Scripts  

---

## Wichtig!

✅ **Immer `git pull` vor `git push` machen!**  
✅ **Aussagekräftige Commit-Nachrichten schreiben**  
✅ **Dateien im Projekt-Ordner speichern, nicht in OneDrive**

---

## Schnell-Referenz

```bash
# Kompletter Workflow in einem:
git pull origin main && \
git add Annotation_reports/DeineDatei.csv && \
git commit -m "Add: DeineDatei" && \
git push origin main
```
