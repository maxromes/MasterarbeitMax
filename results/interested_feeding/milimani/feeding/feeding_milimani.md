# Feeding-only Koedervergleich - Milimani (cut_47min)

## Beschreibung
- Es wurden ausschliesslich feeding-Annotationen ausgewertet.
- Taxonschluessel: species > genus > family/label.
- Standort: milimani; Videos: 17; Koeder: control, fischmix, mackerel, sargassum, ulva_gutweed, ulva_salad.
- Tests: Kruskal-Wallis (global), Mann-Whitney U (paarweise), Holm und BH fuer multiple Tests.

## Zusammenfassung der Ergebnisse
- Getestete Taxa: 4
- Roh signifikante Taxa (p<0.05): 0
- Holm-signifikante Taxa: 0
- Globaler Koedereffekt auf totale feeding Events je Video: p=0.07029 (nicht signifikant)

## Kernaussagen
- Es zeigen sich keine klaren Taxa-Unterschiede zwischen den Koedern.
- Die stärksten Hinweise liegen bei Taxa mit hoher Mitteldifferenz zwischen dominantem und schwächstem Koeder.
- Bait-spezifische Taxa liefern zusaetzlich biologische Plausibilitaet fuer koederabhaengige feeding-Muster.

## Koederprofile
| koeder       |   n_videos |   mean_total_feeding_events |   median_total_feeding_events |   mean_unique_feeding_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:-------------|-----------:|----------------------------:|------------------------------:|---------------------------:|-----------------------:|------------------------:|
| control      |          3 |                     0       |                             0 |                    0       |                      0 |                       0 |
| fischmix     |          1 |                    12       |                            12 |                    5       |                      1 |                       0 |
| mackerel     |          3 |                     4.33333 |                             0 |                    1.33333 |                      0 |                       0 |
| sargassum    |          3 |                     2       |                             2 |                    1.33333 |                      1 |                       0 |
| ulva_gutweed |          3 |                     0       |                             0 |                    0       |                      0 |                       0 |
| ulva_salad   |          4 |                     0.25    |                             0 |                    0.25    |                      0 |                       0 |

## Top-Taxa (global, nach p-Wert)
| taxon_key                                 | dominant_koeder_mean   | weakest_koeder_mean   |   p_value |   p_value_holm |   p_value_bh |   mean_diff_max_minus_min |   eta_sq |
|:------------------------------------------|:-----------------------|:----------------------|----------:|---------------:|-------------:|--------------------------:|---------:|
| species::red (lutjanus bohar)             | fischmix               | control               | 0.0584045 |       0.233618 |    0.0994985 |                         3 | 0.515152 |
| family_label::groupers feeding            | fischmix               | control               | 0.0584045 |       0.233618 |    0.0994985 |                         2 | 0.515152 |
| species::green (amblyglyphidodon indicus) | fischmix               | control               | 0.0809956 |       0.233618 |    0.0994985 |                         5 | 0.43669  |
| species::goldbar (thalassoma hebraicum)   | fischmix               | control               | 0.0994985 |       0.233618 |    0.0994985 |                         1 | 0.386364 |

## Paarweise Koedervergleiche (Total feeding Events je Video)
| koeder_a     | koeder_b     |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm |   p_value_bh | significant_holm   | significant_bh   | sig_label_raw   | sig_label_holm   |
|:-------------|:-------------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|-------------:|:-------------------|:-----------------|:----------------|:-----------------|
| sargassum    | ulva_salad   |     3 |     4 |        2       |        0.25    |     12   | 0.0356983 |       0.535475 |     0.234271 | False              | False            | *               | ns               |
| control      | sargassum    |     3 |     3 |        0       |        2       |      0   | 0.0468542 |       0.655958 |     0.234271 | False              | False            | *               | ns               |
| sargassum    | ulva_gutweed |     3 |     3 |        2       |        0       |      9   | 0.0468542 |       0.655958 |     0.234271 | False              | False            | *               | ns               |
| fischmix     | ulva_salad   |     1 |     4 |       12       |        0.25    |      4   | 0.23568   |       1        |     0.531885 | False              | False            | ns              | ns               |
| fischmix     | sargassum    |     1 |     3 |       12       |        2       |      3   | 0.248213  |       1        |     0.531885 | False              | False            | ns              | ns               |
| control      | fischmix     |     3 |     1 |        0       |       12       |      0   | 0.248213  |       1        |     0.531885 | False              | False            | ns              | ns               |
| fischmix     | ulva_gutweed |     1 |     3 |       12       |        0       |      3   | 0.248213  |       1        |     0.531885 | False              | False            | ns              | ns               |
| control      | mackerel     |     3 |     3 |        0       |        4.33333 |      3   | 0.504985  |       1        |     0.768686 | False              | False            | ns              | ns               |
| mackerel     | ulva_gutweed |     3 |     3 |        4.33333 |        0       |      6   | 0.504985  |       1        |     0.768686 | False              | False            | ns              | ns               |
| ulva_gutweed | ulva_salad   |     3 |     4 |        0       |        0.25    |      4.5 | 0.563703  |       1        |     0.768686 | False              | False            | ns              | ns               |
| control      | ulva_salad   |     3 |     4 |        0       |        0.25    |      4.5 | 0.563703  |       1        |     0.768686 | False              | False            | ns              | ns               |
| mackerel     | sargassum    |     3 |     3 |        4.33333 |        2       |      3   | 0.637352  |       1        |     0.79669  | False              | False            | ns              | ns               |
| mackerel     | ulva_salad   |     3 |     4 |        4.33333 |        0.25    |      7   | 0.825498  |       1        |     0.952498 | False              | False            | ns              | ns               |
| control      | ulva_gutweed |     3 |     3 |        0       |        0       |      4.5 | 1         |       1        |     1        | False              | False            | ns              | ns               |
| fischmix     | mackerel     |     1 |     3 |       12       |        4.33333 |      2   | 1         |       1        |     1        | False              | False            | ns              | ns               |

## Bait-spezifische Taxa
- control (0):
  - Keine
- fischmix (1):
  - species::moon (thalassoma lunare)
- mackerel (0):
  - Keine
- sargassum (1):
  - species::lined bristletooth (ctenochaetus striatus)
- ulva_gutweed (0):
  - Keine
- ulva_salad (0):
  - Keine

## Interpretation
- Der globale Test ist nicht signifikant: auf Ebene der totalen feeding-Ereignisse zeigt sich kein robuster Koedereffekt am Standort.
- Taxon-spezifische Signifikanz (insb. nach Holm/BH) ist der robusteste Nachweis fuer echte koederabhaengige Unterschiede auf Arten/Gattungs/Familienebene.
- Roh-signifikante Effekte ohne Korrektur sind als Trends zu lesen und sollten mit groesserer Stichprobe oder fokussierten Hypothesentests validiert werden.
