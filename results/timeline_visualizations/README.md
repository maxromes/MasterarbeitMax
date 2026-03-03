# Timeline Visualisierungen - Übersicht

## Zusammenfassung

Erstellt: **35 Videos** mit kontinuierlichen Zeitmessungen und mindestens 50 Annotations pro Video.  
Gesamte Grafiken: **105 PNG-Dateien** (3 Grafiken pro Video)  
Gesamtgröße: **19 MB**

## Grafik-Typen

Für jedes Video wurden drei verschiedene Visualisierungen erstellt:

### 1. **First Seen Timeline** (`01_first_seen_timeline.png`)
- **Was zeigt es:** Zeitpunkt, an dem eine neue Fischart zum **ersten Mal** im Video auftaucht
- **Format:** Horizontales Streudiagramm  
- **X-Achse:** Video-Zeit (Minuten:Sekunden)
- **Y-Achse:** Fischart-Namen (alphabetisch sortiert)
- **Farben:** Farbcodiert nach Familie für bessere Unterscheidung
- **Nutzen:** Identifiziert die Reihenfolge, in der neue Arten erscheinen

**Beispiel-Interpretation:**
- Punkt bei 5:30 = Diese Art wurde zum ersten Mal 5:30 Minuten ins Video gesichtet
- Sehr frühe Punkte (oben) = Arten, die schnell zu Beginn erscheinen
- Späte Punkte (unten) = Arten, die erst später im Video auftauchen

### 2. **Kumulative Species Entdeckung** (`02_cumulative_species.png`)
- **Was zeigt es:** Wie viele **verschiedene Arten** kumulativ über die Zeit hinweg gesichtet wurden
- **Format:** Liniendiagramm mit Fläche
- **X-Achse:** Video-Zeit (Minuten:Sekunden)
- **Y-Achse:** Anzahl unterschiedlicher Arten (kumulativ)
- **Nutzen:** Zeigt, wie schnell neue Arten entdeckt werden; Sättigungseffekt erkennbar

**Beispiel-Interpretation:**
- Steile Kurve = Viele neue Arten werden schnell entdeckt
- Flache Kurve = Wenige neue Arten werden entdeckt (schon viele bekannt)
- Asymptotisches Verhalten = Keine neuen Arten mehr gegen Ende

### 3. **Annotations-Dichte** (`03_annotation_density.png`)
- **Was zeigt es:** **Anzahl der Annotations pro Minute** über die Zeit
- **Format:** Balkendiagramm
- **X-Achse:** Video-Zeit (Minuten)
- **Y-Achse:** Anzahl Annotations pro 1-Minuten-Fenster
- **Nutzen:** Zeigt, in welchen Videoabschnitten am meisten/wenigsten annotiert wurde

**Beispiel-Interpretation:**
- Hohe Balken = Viel Aktivität (viele Fische in diesem Bereich)
- Niedrige Balken = Wenig Aktivität (leerer Bereich oder schnelle Übergänge)
- Muster = Erkennbar sind Rush-Phasen und ruhige Phasen

## Video-Eigenschaften

### Längste Videos:
1. **20241029-utumbi-ulva_gutweed.csv** - 59:55 Min (375 Annotations, 56 Arten)
2. **20241110-milimani-ulva_salad.csv** - 59:23 Min (326 Annotations, 60 Arten)
3. **20241110-utumbi-ulva_salad.csv** - 59:21 Min (346 Annotations, 62 Arten)

### Reichste Videos (meiste Annotations):
1. **20241025-utumbi-ulva_salad.csv** - 560 Annotations (53:48 Min)
2. **20241025-milimani-mackerel.csv** - 490 Annotations (58:51 Min)
3. **20241210-milimani-fischmix.csv** - 459 Annotations (58:07 Min)

### Artenreichste Videos (meiste verschiedene Arten):
1. **20241209-utumbi-fischmix.csv** - 79 verschiedene Arten (59:02 Min)
2. **20241124-milimani-mackerel.csv** - 79 verschiedene Arten (58:01 Min)
3. **20241110-utumbi-ulva_salad.csv** - 62 verschiedene Arten (59:21 Min)

## Verzeichnisstruktur

```
results/
├── timeline_visualizations/
│   ├── timeline_summary.txt                          (Diese Zusammenfassung)
│   ├── <video_name>_01_first_seen_timeline.png       (35 Dateien)
│   ├── <video_name>_02_cumulative_species.png        (35 Dateien)
│   └── <video_name>_03_annotation_density.png        (35 Dateien)
```

## Dateibenennungsschema

Format: `<DATUMCODE>-<STANDORT>-<KÖDER>_<TYPNUMMER>_<BESCHREIBUNG>.png`

**Beispiele:**
- `20241209-utumbi-fischmix_01_first_seen_timeline.png`
  - Datum: 2024-12-09
  - Standort: Utumbi
  - Köder: Fischmix
  - Typ: 01 (First Seen Timeline)

## Verwendung in der Masterarbeit

Diese Visualisierungen können für folgende Analysen verwendet werden:

1. **Ökologische Muster:** Welche Arten erscheinen in welcher Reihenfolge?
2. **Fütterungsverhalten:** In welchen Zeitfenstern ist die meiste Aktivität?
3. **Biodiversitäts-Sättigung:** Wie schnell stabilisiert sich die Artenanzahl?
4. **Vergleichende Ökologie:** Unterschiede zwischen Standorten (Milimani vs. Utumbi)
5. **Köder-Effekte:** Unterschiede zwischen Köder-Typen (Fischmix, Sargassum, etc.)

## Technische Details

**Erstellungs-Script:** `scripts/generate_timeline_visualizations.py`

**Filter-Kriterien:**
- Nur Videos mit kontinuierlichen Zeitmessungen (Coral Reef, nicht Nursery)
- Mindestens 50 Annotations pro Video
- Maximum 60 Minuten Video-Länge
- Auflösung: 150 DPI (druckfreundlich)

**Datenquellen:**
- `Annotation_reports_coral_reef/*.csv` (insgesamt 35 Videos selektiert von 34+)

## Hinweise

- Die "first seen" Punkte berücksichtigen nur das erste Auftreten einer Art im Video
- Mehrfaches Auftreten der gleichen Art wird nicht visualisiert (nur der erste Punkt)
- Die Kumulativen Kurven zeigen die Sättigung der Art-Entdeckung
- Die Dichte-Plots helfen, "hotspots" von Fischaktivitäten zu identifizieren

---

**Erstellt:** 2026-03-03  
**Generator:** generate_timeline_visualizations.py
