# Kompositions-Robustheit: offene Zusatztests (PERMDISP + Rarefaction)

Stand: 2026-08-16

## Ziel

- Offener Punkt 1: PERMDISP als Streuungspruefung ergaenzend zur PERMANOVA.
- Offener Punkt 2: Rarefaction/Sampling-Normalisierung fuer ungleiche Videozahlen je Koeder.

## Methode

- Datengrundlage: normalized_reports/cut_47min, getrennt nach Standorten.
- Taxa-Komposition: Presence/Absence je Video mit Jaccard-Distanzen.
- PERMDISP: Distanz jedes Videos zum Koeder-Zentrum im PCoA-Raum; Signifikanz per Permutationstest (5000).
- Rarefaction: Monte-Carlo-Subsampling je Koeder auf k = minimale Videozahl je Standort (4000 Wiederholungen).

## PERMDISP pro Standort

| standort   |   n_videos |   n_koeder |   f_stat |    p_value |   q_value_bh |   p_value_holm | significant_0_05   | significant_bh_0_05   |
|:-----------|-----------:|-----------:|---------:|-----------:|-------------:|---------------:|:-------------------|:----------------------|
| milimani   |         17 |          6 | 18.4544  | 0.00419916 |   0.00629874 |     0.00839832 | True               | True                  |
| nursery    |         11 |          4 | 17.7449  | 0.00179964 |   0.00539892 |     0.00539892 | True               | True                  |
| utumbi     |         18 |          6 |  4.69268 | 0.0175965  |   0.0175965  |     0.0175965  | True               | True                  |

## Rarefied Richness pro Koeder (alle Koeder inkl. control)

| standort   | koeder        |   n_videos |   k_standardized_videos |   rarefied_union_richness_mean |   rarefied_union_richness_ci95_low |   rarefied_union_richness_ci95_high |   observed_union_richness |
|:-----------|:--------------|-----------:|------------------------:|-------------------------------:|-----------------------------------:|------------------------------------:|--------------------------:|
| milimani   | mackerel      |          3 |                       1 |                        48.0365 |                            34.0000 |                             57.0000 |                        74 |
| milimani   | sargassum     |          3 |                       1 |                        45.0123 |                            43.0000 |                             46.0000 |                        63 |
| milimani   | fischmix      |          1 |                       1 |                        45.0000 |                            45.0000 |                             45.0000 |                        45 |
| milimani   | ulva_gutweed  |          3 |                       1 |                        44.7013 |                            39.0000 |                             49.0000 |                        66 |
| milimani   | ulva_salad    |          4 |                       1 |                        42.8670 |                            31.0000 |                             57.0000 |                        71 |
| milimani   | control       |          3 |                       1 |                        42.3368 |                            36.0000 |                             46.0000 |                        63 |
| nursery    | algaemix      |          3 |                       1 |                        39.0755 |                            33.0000 |                             43.0000 |                        58 |
| nursery    | algae_strings |          3 |                       1 |                        35.6722 |                            34.0000 |                             38.0000 |                        51 |
| nursery    | mackerel      |          4 |                       1 |                        34.8670 |                            29.0000 |                             41.0000 |                        67 |
| nursery    | control       |          1 |                       1 |                        29.0000 |                            29.0000 |                             29.0000 |                        29 |
| utumbi     | sargassum     |          3 |                       2 |                        72.0005 |                            70.0000 |                             74.0000 |                        80 |
| utumbi     | mackerel      |          3 |                       2 |                        71.7500 |                            67.0000 |                             75.0000 |                        81 |
| utumbi     | fischmix      |          2 |                       2 |                        68.0000 |                            68.0000 |                             68.0000 |                        68 |
| utumbi     | ulva_salad    |          3 |                       2 |                        67.6975 |                            64.0000 |                             70.0000 |                        76 |
| utumbi     | ulva_gutweed  |          3 |                       2 |                        66.3020 |                            65.0000 |                             69.0000 |                        74 |
| utumbi     | control       |          4 |                       2 |                        63.1848 |                            60.0000 |                             66.0000 |                        77 |

## Rarefied Richness pro Koeder (Sensitivitaet ohne control)

| standort   | koeder        |   n_videos |   k_standardized_videos |   rarefied_union_richness_mean |   rarefied_union_richness_ci95_low |   rarefied_union_richness_ci95_high |   observed_union_richness |
|:-----------|:--------------|-----------:|------------------------:|-------------------------------:|-----------------------------------:|------------------------------------:|--------------------------:|
| milimani   | mackerel      |          3 |                       1 |                        48.0060 |                            34.0000 |                             57.0000 |                        74 |
| milimani   | fischmix      |          1 |                       1 |                        45.0000 |                            45.0000 |                             45.0000 |                        45 |
| milimani   | sargassum     |          3 |                       1 |                        44.9440 |                            43.0000 |                             46.0000 |                        63 |
| milimani   | ulva_gutweed  |          3 |                       1 |                        44.7220 |                            39.0000 |                             49.0000 |                        66 |
| milimani   | ulva_salad    |          4 |                       1 |                        42.7253 |                            31.0000 |                             57.0000 |                        71 |
| nursery    | mackerel      |          4 |                       3 |                        60.1257 |                            56.0000 |                             65.0000 |                        67 |
| nursery    | algaemix      |          3 |                       3 |                        58.0000 |                            58.0000 |                             58.0000 |                        58 |
| nursery    | algae_strings |          3 |                       3 |                        51.0000 |                            51.0000 |                             51.0000 |                        51 |
| utumbi     | sargassum     |          3 |                       2 |                        72.0135 |                            70.0000 |                             74.0000 |                        80 |
| utumbi     | mackerel      |          3 |                       2 |                        71.6380 |                            67.0000 |                             75.0000 |                        81 |
| utumbi     | fischmix      |          2 |                       2 |                        68.0000 |                            68.0000 |                             68.0000 |                        68 |
| utumbi     | ulva_salad    |          3 |                       2 |                        67.6325 |                            64.0000 |                             70.0000 |                        76 |
| utumbi     | ulva_gutweed  |          3 |                       2 |                        66.3380 |                            65.0000 |                             69.0000 |                        74 |

## Rarefied Richness fish vs algae (bait-type Ebene)

| standort   | bait_type   |   n_videos |   k_standardized_videos |   rarefied_union_richness_mean |   rarefied_union_richness_ci95_low |   rarefied_union_richness_ci95_high |   observed_union_richness |
|:-----------|:------------|-----------:|------------------------:|-------------------------------:|-----------------------------------:|------------------------------------:|--------------------------:|
| milimani   | algae       |         10 |                       4 |                        71.8787 |                            63.0000 |                             81.0000 |                        89 |
| milimani   | fish        |          4 |                       4 |                        77.0000 |                            77.0000 |                             77.0000 |                        77 |
| nursery    | algae       |          6 |                       4 |                        58.3020 |                            54.0000 |                             63.0000 |                        65 |
| nursery    | fish        |          4 |                       4 |                        67.0000 |                            67.0000 |                             67.0000 |                        67 |
| utumbi     | algae       |          9 |                       5 |                        89.2765 |                            85.0000 |                             94.0000 |                       101 |
| utumbi     | fish        |          5 |                       5 |                        92.0000 |                            92.0000 |                             92.0000 |                        92 |

## Kurzinterpretation

- Mindestens ein Standort zeigt signifikante Streuungsunterschiede zwischen Koedern (PERMDISP, BH-korrigiert).
- Rarefaction reduziert den Einfluss ungleicher Stichprobengroessen und zeigt, welche Koeder auch bei gleicher Videozahl die hoehere Taxa-Abdeckung behalten.
- Die Sensitivitaet ohne control ist informativer, wenn control nur mit n=1 vorliegt (sonst wird k auf 1 gedrueckt).
- Diese Zusatztests trennen besser zwischen Lageeffekt (PERMANOVA) und Streuung/Sampling-Effekt.
