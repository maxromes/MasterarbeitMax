# Koedervergleich: Uebersicht der Ergebnisse

## Taxa-Ebene: Standort- und Koedervergleich
- Standortvergleich der Taxa-Zusammensetzung: [results/Standortvergleich/standortvergleich.md](../Standortvergleich/standortvergleich.md)
- Artenvergleich nach Standort inklusive Ueberlappung, exklusiven Taxa und Praesenzmustern: [results/Artenvergleich_standort/artenvergleich_standort.md](../Artenvergleich_standort/artenvergleich_standort.md)
- Koedervergleich getrennt nach Standort: [results/artenvergleich_köder/artenvergleich_koeder_summary.md](../artenvergleich_köder/artenvergleich_koeder_summary.md)
- Standortberichte mit Koederprofilen und Grafiken:
  - [Milimani](../artenvergleich_köder/milimani/artenvergleich_koeder_milimani.md)
  - [Utumbi](../artenvergleich_köder/utumbi/artenvergleich_koeder_utumbi.md)
  - [Nursery](../artenvergleich_köder/nursery/artenvergleich_koeder_nursery.md)

### Wichtige Taxa-Ergebnisse
- Milimani: hoechste Koeder-Ueberlappung bei `control` vs `ulva_gutweed` (Jaccard 0.697).
- Utumbi: hoechste Koeder-Ueberlappung bei `control` vs `sargassum` (Jaccard 0.764).
- Taxa in allen Koedern: Milimani 31, Utumbi 43.
- In beiden Standorten sind klar koederspezifische Taxa vorhanden.

### Groesster Abstand zu `control`
#### Taxa-Vorkommen (Jaccard-Distanz)
| standort | koeder mit groesstem Abstand zu control | Jaccard-Distanz |
|:--|:--|--:|
| milimani | fischmix | 0.493 |
| utumbi | fischmix | 0.426 |
| nursery | algaemix | 0.778 |

#### Taxa-MaxN (Anzahl dominanter Taxa)
| standort | koeder mit groesstem Abstand zu control | dominante Taxa | control | Differenz |
|:--|:--|--:|--:|--:|
| milimani | fischmix | 32 | 15 | +17 |
| utumbi | mackerel | 36 | 12 | +24 |
| nursery | mackerel | 31 | 14 | +17 |

## Taxa-Haeufigkeit: MaxN-basierte Tests
- Kruskal-Wallis-Test je Taxon und Standort.
- Paarweise Mann-Whitney-U-Tests zwischen Koedern.
- Holm-Korrektur fuer taxonweise und paarweise Vergleiche.
- Dominanzkennzahlen je Koeder (dominante Taxa, starke Dominanz mit Ratio >= 3).

### Wichtige MaxN-Ergebnisse
- Milimani: 6 roh-signifikante Taxa, 0 Holm-signifikante Taxa; 13 roh-signifikante paarweise Kontraste, 0 Holm-signifikante.
- Utumbi: 8 roh-signifikante Taxa, 0 Holm-signifikante Taxa; 16 roh-signifikante paarweise Kontraste, 0 Holm-signifikante.
- Nursery: 11 roh-signifikante Taxa, 0 Holm-signifikante Taxa; 11 roh-signifikante paarweise Kontraste, 0 Holm-signifikante.

## Verhaltensebene: `feeding` und `interested`
- Analyse der Total-Events je Video pro Koeder.
- Paarweise Koederunterschiede mit Mann-Whitney-U-Tests.
- Roh- und Holm-Korrektur fuer Taxa- und Paarvergleiche.
- Analyse pro Standort: Milimani, Utumbi, Nursery.

### Milimani
- Feeding: 1 roh-signifikantes Taxon, 1 Holm-signifikantes Taxon; globaler Koedereffekt auf Total-Events nicht signifikant.
- Interested: 0 roh-signifikante Taxa, 0 Holm-signifikante Taxa; globaler Koedereffekt auf Total-Events nicht signifikant.

### Utumbi
- Feeding: 4 roh-signifikante Taxa, 0 Holm-signifikante Taxa; globaler Koedereffekt auf Total-Events signifikant.
- Interested: 2 roh-signifikante Taxa, 0 Holm-signifikante Taxa; globaler Koedereffekt auf Total-Events signifikant.

### Nursery
- Feeding: 2 roh-signifikante Taxa, 0 Holm-signifikante Taxa; globaler Koedereffekt auf Total-Events signifikant.
- Interested: 0 roh-signifikante Taxa, 0 Holm-signifikante Taxa; globaler Koedereffekt auf Total-Events nicht signifikant.

### Control-Vergleich fuer `feeding` und `interested`
#### Milimani
- groesster control-Abstand bei feeding: `fischmix`
- groesster control-Abstand bei interested: `fischmix`

#### Utumbi
- groesster control-Abstand bei feeding: `fischmix`
- groesster control-Abstand bei interested: `fischmix`

#### Nursery
- groesster control-Abstand bei feeding: `algaemix`
- groesster control-Abstand bei interested: `algaemix`

### Signifikanzbewertung
- Milimani: eher trendhafte Signale, insgesamt nicht robust signifikant.
- Utumbi: globale Total-Event-Unterschiede signifikant, aber keine Holm-robusten Paarvergleiche.
- Nursery: global fuer feeding signifikant, fuer interested nicht.

## Berechnete Hilfsmaße und Visualisierungen
- Jaccard-Ueberlappung und Jaccard-Distanz zwischen Koedern.
- Anzahl koederspezifischer Taxa pro Koeder.
- Koederprofile je Standort mit dominanten Taxa und starker Dominanz.
- Kombinierte Grafik fuer dominante Taxa und koederspezifische Taxa.
- Balken- und Distanzgrafiken fuer den control-Vergleich.

## Weitere Analyseideen
- PERMDISP zur Pruefung der Streuungsunterschiede.
- IndVal-Analyse fuer Indikatorarten.
- Praesenz/Absenz-Tests pro Taxon mit logistischer Modellierung oder Fisher-Exact.
- Artenreichtum pro Video mit GLM oder Negative Binomial.
- Rarefaction bzw. Stichprobennormalisierung.
- Konsistenzanalyse zwischen Standorten.
