# First Seen vs. MaxN Visualisierung

## Video analysiert
**20241029-utumbi-ulva_gutweed.csv** (59:55 Min)

## Grafiken

### 1. First Seen Timeline
**Datei:** `20241029-utumbi-ulva_gutweed_first_seen.png`

Zeigt **wann jede Art zum ersten Mal** im Video erscheint.
- X-Achse: Video-Zeit (Minuten:Sekunden)  
- Y-Achse: Arten/Taxa (sortiert nach Erscheinungszeitpunkt)
- Punktfarbe: Familie
- **Interpretation:** Kolonisations-Reihenfolge, ökologische Hierarchie

### 2. MaxN Timeline
**Datei:** `20241029-utumbi-ulva_gutweed_maxn.png`

Zeigt **wann die maximale Anzahl einer Art** erreicht wird.
- X-Achse: Video-Zeit (Minuten:Sekunden)
- Y-Achse: Arten/Taxa mit MaxN-Anzahl (z.B. "Indian Half-and-Half (n=56)")
- Punktgröße: Proportional zur MaxN-Anzahl
- Punktfarbe: Familie
- **Interpretation:** Wann erreichen Schwärme ihre maximale Größe?

## Wichtigste Erkenntnisse

### First Seen
- **Median:** 7:55 Min → Hälfte aller Arten erscheint in den ersten 8 Minuten
- **Nach 40 Min:** Nur noch 5 neue Arten (90% bereits gesehen)

### MaxN  
- **Median:** 13:49 Min → Hälfte der MaxN-Werte wird in den ersten 14 Minuten erreicht
- **Nach 40 Min:** Nur noch 7 MaxN-Ereignisse
- **Zeit bis MaxN:** Durchschnittlich 5:13 Min von First Seen bis MaxN

### Top 3 MaxN-Arten
1. **Indian Half-and-Half:** MaxN = 56 Individuen (bei 12:54 Min)
2. **Ternate Chromis:** MaxN = 55 Individuen (bei 10:13 Min)
3. **Blue-green Chromis:** MaxN = 17 Individuen (bei 11:11 Min)

## Interpretation

**Ab welcher Minute kommen wenig neue Arten dazu?**
- Nach **Minute 20:** < 25% neue Arten (nur 13 von 56)
- Nach **Minute 40:** < 10% neue Arten (nur 5 von 56)

**Ab welcher Minute werden wenig neue MaxN erreicht?**
- Nach **Minute 20:** 61% der MaxN-Werte bereits erreicht  
- Nach **Minute 40:** 87% der MaxN-Werte bereits erreicht

---

**Erstellt:** 2026-03-03  
**Generator:** generate_first_seen_vs_maxn.py  
**Zusammenfassung:** first_seen_vs_maxn_summary.txt
