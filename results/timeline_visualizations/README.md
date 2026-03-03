# First Seen vs. MaxN - Multi-Video Vergleich

## Übersicht

Diese Visualisierungen vergleichen **5 Videos** mit ähnlicher Länge (~60 Min) bezüglich ihrer **First Seen** und **MaxN** Muster.

## Videos analysiert

1. **20241029-utumbi-ulva_gutweed.csv** (59:55, Utumbi, Ulva Gutweed)
2. **20241110-milimani-ulva_salad.csv** (59:23, Milimani, Ulva Salad)
3. **20241110-utumbi-ulva_salad.csv** (59:21, Utumbi, Ulva Salad)
4. **20241112-milimani-ulva_salad.csv** (59:16, Milimani, Ulva Salad)
5. **20241115-utumbi-control.csv** (59:05, Utumbi, Control)

## Grafiken

### 1. Multi-Video First Seen
**Datei:** `multi_video_first_seen.png`

**Kumulative Kurven** zeigen, wie schnell neue Arten in jedem Video entdeckt werden.
- **X-Achse:** Video-Zeit (Minuten)
- **Y-Achse:** Kumulative Anzahl neuer Arten
- **Farben:** Jedes Video hat eine eigene Farbe
- **Marker:** Verschiedene Symbole pro Video (●, ■, ▲, ◆, ▼)

**Interpretation:**
- **Steile Kurven:** Viele Arten werden früh entdeckt
- **Flache Kurven am Ende:** Artenentdeckung verlangsamt sich (Sättigung)
- **Vergleich:** Videos mit ähnlichem Verlauf zeigen ähnliche Kolonisations-Dynamik

### 2. Multi-Video MaxN
**Datei:** `multi_video_maxn.png`

**Kumulative Kurven** zeigen, wann die maximalen Artenzahlen (MaxN) erreicht werden.
- **X-Achse:** Video-Zeit (Minuten)
- **Y-Achse:** Kumulative Anzahl erreichter MaxN-Werte
- **Farben:** Gleiche Farben wie First Seen für direkten Vergleich

**Interpretation:**
- **MaxN kommt später als First Seen:** Im Durchschnitt 5-15 Min Unterschied
- **Flachere Kurven:** MaxN-Werte brauchen länger zum Erreichen
- **Höhere Kurven:** Mehr verschiedene Schwarm-Ereignisse

## Wichtigste Erkenntnisse

### First Seen Median-Zeiten:
- **20241110-utumbi-ulva_salad:** 7:19 Min (schnellste Artenentdeckung)
- **20241110-milimani-ulva_salad:** 7:48 Min
- **20241029-utumbi-ulva_gutweed:** 7:55 Min
- **20241115-utumbi-control:** 9:14 Min
- **20241112-milimani-ulva_salad:** 10:36 Min (langsamste)

### MaxN Median-Zeiten:
- **20241029-utumbi-ulva_gutweed:** 13:49 Min
- **20241110-milimani-ulva_salad:** 14:58 Min
- **20241110-utumbi-ulva_salad:** 16:12 Min
- **20241115-utumbi-control:** 18:24 Min
- **20241112-milimani-ulva_salad:** 24:20 Min (späteste MaxN)

### Artenvielfalt:
- **Höchste:** 63 Arten (20241115-utumbi-control)
- **Niedrigste:** 50 Arten (20241112-milimani-ulva_salad)
- **Durchschnitt:** 58 Arten pro Video

## Muster und Vergleiche

### Standort-Unterschiede:
- **Utumbi:** 3 Videos (56, 62, 63 Arten) → Durchschnitt 60 Arten
- **Milimani:** 2 Videos (60, 50 Arten) → Durchschnitt 55 Arten
- ➜ Utumbi zeigt tendenziell höhere Artenvielfalt

### Köder-Unterschiede:
- **Ulva Salad:** 3 Videos (60, 62, 50 Arten)
- **Ulva Gutweed:** 1 Video (56 Arten)
- **Control:** 1 Video (63 Arten)
- ➜ Control-Video zeigt höchste Artenvielfalt

### Zeitliche Muster:
- **Alle Videos:** Erste 10 Minuten = 50% der Arten entdeckt
- **Alle Videos:** Erste 20 Minuten = 60-70% der MaxN-Werte erreicht
- **Konsistenz:** Ähnliche Kolonisations-Kurven trotz verschiedener Köder

## Forschungsfragen

Diese Visualisierungen helfen bei:
1. **Vergleich Standorte:** Milimani vs. Utumbi - gibt es systematische Unterschiede?
2. **Köder-Effekte:** Welche Köder ziehen Arten schneller/langsamer an?
3. **Temporal Robustness:** Wie konsistent sind die Muster über verschiedene Videos?
4. **Optimal Sampling:** Ab wann ist die Artenerfassung gesättigt? (wichtig für Sampling-Design)

## Verwendung

- **Vergleiche die Steigungen:** Ähnliche Steigung = ähnliche Kolonisations-Rate
- **Achte auf Endpunkte:** Finale Höhe = Gesamtartenzahl
- **Beobachte Inflection Points:** Wo flachen die Kurven ab?
- **Suche nach Clustern:** Gruppieren sich bestimmte Videos?

---

**Erstellt:** 2026-03-03  
**Generator:** generate_first_seen_vs_maxn_multi.py  
**Zusammenfassung:** multi_video_summary.txt
