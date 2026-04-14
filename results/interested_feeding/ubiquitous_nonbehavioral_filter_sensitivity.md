# Sensitivitaetsanalyse: ubiquitaere, nicht-verhaltensbezogene Taxa entfernen (erweiterte Filterstufen)

Ziel: pruefen, ob Koederunterschiede deutlicher werden, wenn mehr ubiquitaere Hintergrundtaxa entfernt werden, die:
- in fast allen Videos vorkommen (occurrence rate >= Schwellwert)
- und nie als feeding/interested annotiert wurden

Datengrundlage:
- Taxa-Haeufigkeit: results/taxahäufigkeitköder/*/*_taxa_kruskal_koeder_tests.csv
- Videoebene MaxN: results/taxahäufigkeitköder/taxon_maxn_video_level.csv
- Verhaltensannotation: results/interested_feeding/interested_feeding_taxon_event_long.csv

Neue Schwellen: 0.5, 0.6, 0.7, 0.8, 0.9

## Ergebnisuebersicht
| standort   |   threshold_occ_rate |   n_taxa_before |   n_taxa_excluded |   n_taxa_after |   raw_sig_before |   holm_sig_before |   raw_sig_after |   holm_sig_after_refit |   share_removed |
|:-----------|---------------------:|----------------:|------------------:|---------------:|-----------------:|------------------:|----------------:|-----------------------:|----------------:|
| milimani   |                  0.5 |             104 |                35 |             69 |                6 |                 0 |               5 |                      0 |       0.336538  |
| milimani   |                  0.6 |             104 |                28 |             76 |                6 |                 0 |               5 |                      0 |       0.269231  |
| milimani   |                  0.7 |             104 |                24 |             80 |                6 |                 0 |               6 |                      0 |       0.230769  |
| milimani   |                  0.8 |             104 |                18 |             86 |                6 |                 0 |               6 |                      0 |       0.173077  |
| milimani   |                  0.9 |             104 |                11 |             93 |                6 |                 0 |               6 |                      0 |       0.105769  |
| nursery    |                  0.5 |              99 |                18 |             81 |               11 |                 0 |              10 |                      0 |       0.181818  |
| nursery    |                  0.6 |              99 |                16 |             83 |               11 |                 0 |              10 |                      0 |       0.161616  |
| nursery    |                  0.7 |              99 |                12 |             87 |               11 |                 0 |              10 |                      0 |       0.121212  |
| nursery    |                  0.8 |              99 |                 7 |             92 |               11 |                 0 |              10 |                      0 |       0.0707071 |
| nursery    |                  0.9 |              99 |                 4 |             95 |               11 |                 0 |              11 |                      0 |       0.040404  |
| utumbi     |                  0.5 |             120 |                41 |             79 |                8 |                 0 |               5 |                      0 |       0.341667  |
| utumbi     |                  0.6 |             120 |                35 |             85 |                8 |                 0 |               6 |                      0 |       0.291667  |
| utumbi     |                  0.7 |             120 |                27 |             93 |                8 |                 0 |               6 |                      0 |       0.225     |
| utumbi     |                  0.8 |             120 |                19 |            101 |                8 |                 0 |               6 |                      0 |       0.158333  |
| utumbi     |                  0.9 |             120 |                11 |            109 |                8 |                 0 |               6 |                      0 |       0.0916667 |

## milimani
### Schwelle occ_rate >= 0.5
- Ausgeschlossen: 35 von 104 Taxa (33.7%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=control)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=sargassum)
  - species::sixbar (thalassoma hardwicke) (occ=1.000, dominant=fischmix)
  - species::brown tang (zebrasoma scopas) (occ=1.000, dominant=mackerel)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=ulva_gutweed)
  - species::orange-lined (balistapus undulatus) (occ=1.000, dominant=fischmix)
  - species::redmouth (aethaloperca rogaa) (occ=1.000, dominant=fischmix)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=fischmix)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.6
- Ausgeschlossen: 28 von 104 Taxa (26.9%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=control)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=sargassum)
  - species::sixbar (thalassoma hardwicke) (occ=1.000, dominant=fischmix)
  - species::brown tang (zebrasoma scopas) (occ=1.000, dominant=mackerel)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=ulva_gutweed)
  - species::orange-lined (balistapus undulatus) (occ=1.000, dominant=fischmix)
  - species::redmouth (aethaloperca rogaa) (occ=1.000, dominant=fischmix)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=fischmix)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.7
- Ausgeschlossen: 24 von 104 Taxa (23.1%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=control)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=sargassum)
  - species::sixbar (thalassoma hardwicke) (occ=1.000, dominant=fischmix)
  - species::brown tang (zebrasoma scopas) (occ=1.000, dominant=mackerel)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=ulva_gutweed)
  - species::orange-lined (balistapus undulatus) (occ=1.000, dominant=fischmix)
  - species::redmouth (aethaloperca rogaa) (occ=1.000, dominant=fischmix)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=fischmix)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.8
- Ausgeschlossen: 18 von 104 Taxa (17.3%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=control)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=sargassum)
  - species::sixbar (thalassoma hardwicke) (occ=1.000, dominant=fischmix)
  - species::brown tang (zebrasoma scopas) (occ=1.000, dominant=mackerel)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=ulva_gutweed)
  - species::orange-lined (balistapus undulatus) (occ=1.000, dominant=fischmix)
  - species::redmouth (aethaloperca rogaa) (occ=1.000, dominant=fischmix)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=fischmix)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.9
- Ausgeschlossen: 11 von 104 Taxa (10.6%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=control)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=sargassum)
  - species::sixbar (thalassoma hardwicke) (occ=1.000, dominant=fischmix)
  - species::brown tang (zebrasoma scopas) (occ=1.000, dominant=mackerel)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=ulva_gutweed)
  - species::orange-lined (balistapus undulatus) (occ=1.000, dominant=fischmix)
  - species::redmouth (aethaloperca rogaa) (occ=1.000, dominant=fischmix)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=fischmix)
- Keine neuen Holm-signifikanten Taxa nach Refit.

## utumbi
### Schwelle occ_rate >= 0.5
- Ausgeschlossen: 41 von 120 Taxa (34.2%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=mackerel)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=ulva_salad)
  - species::bullethead (chlorurus sordidus) (occ=1.000, dominant=sargassum)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=sargassum)
  - genus::genus soldier (occ=1.000, dominant=mackerel)
  - species::brown pigmy (centropyge multispinis) (occ=1.000, dominant=ulva_gutweed)
  - family_label::groupers (serranidae) (occ=1.000, dominant=mackerel)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=mackerel)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.6
- Ausgeschlossen: 35 von 120 Taxa (29.2%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=mackerel)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=ulva_salad)
  - species::bullethead (chlorurus sordidus) (occ=1.000, dominant=sargassum)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=sargassum)
  - genus::genus soldier (occ=1.000, dominant=mackerel)
  - species::brown pigmy (centropyge multispinis) (occ=1.000, dominant=ulva_gutweed)
  - family_label::groupers (serranidae) (occ=1.000, dominant=mackerel)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=mackerel)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.7
- Ausgeschlossen: 27 von 120 Taxa (22.5%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=mackerel)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=ulva_salad)
  - species::bullethead (chlorurus sordidus) (occ=1.000, dominant=sargassum)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=sargassum)
  - genus::genus soldier (occ=1.000, dominant=mackerel)
  - species::brown pigmy (centropyge multispinis) (occ=1.000, dominant=ulva_gutweed)
  - family_label::groupers (serranidae) (occ=1.000, dominant=mackerel)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=mackerel)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.8
- Ausgeschlossen: 19 von 120 Taxa (15.8%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=mackerel)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=ulva_salad)
  - species::bullethead (chlorurus sordidus) (occ=1.000, dominant=sargassum)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=sargassum)
  - genus::genus soldier (occ=1.000, dominant=mackerel)
  - species::brown pigmy (centropyge multispinis) (occ=1.000, dominant=ulva_gutweed)
  - family_label::groupers (serranidae) (occ=1.000, dominant=mackerel)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=mackerel)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.9
- Ausgeschlossen: 11 von 120 Taxa (9.2%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - species::indian half-and-half (pycnochromis dimidiatus) (occ=1.000, dominant=mackerel)
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=ulva_salad)
  - species::bullethead (chlorurus sordidus) (occ=1.000, dominant=sargassum)
  - species::longbarbel (parupeneus macronemus) (occ=1.000, dominant=sargassum)
  - genus::genus soldier (occ=1.000, dominant=mackerel)
  - species::brown pigmy (centropyge multispinis) (occ=1.000, dominant=ulva_gutweed)
  - family_label::groupers (serranidae) (occ=1.000, dominant=mackerel)
  - species::bird wrasse (gomphosus caeruleus) (occ=1.000, dominant=mackerel)
- Keine neuen Holm-signifikanten Taxa nach Refit.

## nursery
### Schwelle occ_rate >= 0.5
- Ausgeschlossen: 18 von 99 Taxa (18.2%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=algae_strings)
  - species::threespot dascyllus (dascyllus trimaculatus) (occ=1.000, dominant=mackerel)
  - species::moon (thalassoma lunare) (occ=0.909, dominant=mackerel)
  - species::blackwhite (macolor niger) (occ=0.909, dominant=algae_strings)
  - species::arabian monocle (scolopsis ghanam) (occ=0.818, dominant=algaemix)
  - family_label::fusiliers (caesionidae) (occ=0.818, dominant=algae_strings)
  - species::black-backed (chaetodon melannotus) (occ=0.818, dominant=algae_strings)
  - family_label::jacks/trevallyes (carangidae) (occ=0.727, dominant=control)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.6
- Ausgeschlossen: 16 von 99 Taxa (16.2%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=algae_strings)
  - species::threespot dascyllus (dascyllus trimaculatus) (occ=1.000, dominant=mackerel)
  - species::moon (thalassoma lunare) (occ=0.909, dominant=mackerel)
  - species::blackwhite (macolor niger) (occ=0.909, dominant=algae_strings)
  - species::arabian monocle (scolopsis ghanam) (occ=0.818, dominant=algaemix)
  - family_label::fusiliers (caesionidae) (occ=0.818, dominant=algae_strings)
  - species::black-backed (chaetodon melannotus) (occ=0.818, dominant=algae_strings)
  - family_label::jacks/trevallyes (carangidae) (occ=0.727, dominant=control)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.7
- Ausgeschlossen: 12 von 99 Taxa (12.1%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=algae_strings)
  - species::threespot dascyllus (dascyllus trimaculatus) (occ=1.000, dominant=mackerel)
  - species::moon (thalassoma lunare) (occ=0.909, dominant=mackerel)
  - species::blackwhite (macolor niger) (occ=0.909, dominant=algae_strings)
  - species::arabian monocle (scolopsis ghanam) (occ=0.818, dominant=algaemix)
  - family_label::fusiliers (caesionidae) (occ=0.818, dominant=algae_strings)
  - species::black-backed (chaetodon melannotus) (occ=0.818, dominant=algae_strings)
  - family_label::jacks/trevallyes (carangidae) (occ=0.727, dominant=control)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.8
- Ausgeschlossen: 7 von 99 Taxa (7.1%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=algae_strings)
  - species::threespot dascyllus (dascyllus trimaculatus) (occ=1.000, dominant=mackerel)
  - species::moon (thalassoma lunare) (occ=0.909, dominant=mackerel)
  - species::blackwhite (macolor niger) (occ=0.909, dominant=algae_strings)
  - species::arabian monocle (scolopsis ghanam) (occ=0.818, dominant=algaemix)
  - family_label::fusiliers (caesionidae) (occ=0.818, dominant=algae_strings)
  - species::black-backed (chaetodon melannotus) (occ=0.818, dominant=algae_strings)
- Keine neuen Holm-signifikanten Taxa nach Refit.

### Schwelle occ_rate >= 0.9
- Ausgeschlossen: 4 von 99 Taxa (4.0%).
- Holm-signifikante Taxa vorher/nachher: 0 -> 0.
- Beispiele ausgeschlossener Taxa:
  - family_label::parrotfishes (scaridae) (occ=1.000, dominant=algae_strings)
  - species::threespot dascyllus (dascyllus trimaculatus) (occ=1.000, dominant=mackerel)
  - species::moon (thalassoma lunare) (occ=0.909, dominant=mackerel)
  - species::blackwhite (macolor niger) (occ=0.909, dominant=algae_strings)
- Keine neuen Holm-signifikanten Taxa nach Refit.

## Interpretation
- Der staerkere Filter entfernt deutlich mehr Hintergrundtaxa (je nach Standort bis rund die Haelfte der Taxa bei Schwelle 0.5).
- Trotz staerkerer Filterung entstehen weiterhin keine neuen Holm-signifikanten Taxa.
- In diesem Datensatz ist die Null-Erkenntnis gegenueber aggressiverer Entfernung ubiquitaerer, nicht-verhaltensbezogener Taxa stabil.
- Das staerkt die Aussage, dass die fehlende Holm-Signifikanz nicht primaer durch allgegenwaertige Riffarten verursacht wird.
