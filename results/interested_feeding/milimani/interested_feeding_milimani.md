# Interested/Feeding Koedervergleich - Milimani (cut_47min)

## Datengrundlage
- Standort: milimani
- Anzahl Videos: 17
- Koeder: control, fischmix, mackerel, sargassum, ulva_gutweed, ulva_salad
- Taxonbildung: species > genus > family/label
- Betrachtete Annotationen: feeding und interested

## Feeding - Signifikanz und Trends
- Getestete Taxa: 6; roh signifikant: 1; Holm-signifikant: 1.
- Globaler Koedereffekt (Total-Events je Video): p=0.07029 (nicht signifikant).

### Koederprofile
| koeder       |   n_videos |   mean_total_events |   median_total_events |   mean_unique_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:-------------|-----------:|--------------------:|----------------------:|-------------------:|-----------------------:|------------------------:|
| control      |          3 |             0       |                     0 |            0       |                      0 |                       0 |
| fischmix     |          1 |            12       |                    12 |            5       |                      1 |                       1 |
| mackerel     |          3 |             4.33333 |                     0 |            1.33333 |                      0 |                       0 |
| sargassum    |          3 |             2       |                     2 |            1.33333 |                      1 |                       0 |
| ulva_gutweed |          3 |             0       |                     0 |            0       |                      0 |                       0 |
| ulva_salad   |          4 |             0.25    |                     0 |            0.25    |                      0 |                       0 |

### Besondere Taxa (bait-spezifisch)
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

### Top-Taxa-Trends (roh p<0.05)
| taxon_key                         | dominant_koeder_mean   | lowest_koeder_mean   |    p_value |   p_value_holm |   mean_diff_max_minus_min |   eta_sq |
|:----------------------------------|:-----------------------|:---------------------|-----------:|---------------:|--------------------------:|---------:|
| species::moon (thalassoma lunare) | fischmix               | control              | 0.00684407 |      0.0410644 |                         1 |        1 |

### Paarweise Koederunterschiede (Total-Events)
| site     | flag    | koeder_a     | koeder_b     |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm | significant_0_05   | significant_0_05_holm   | sig_label_raw   | sig_label_holm   |
|:---------|:--------|:-------------|:-------------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|:-------------------|:------------------------|:----------------|:-----------------|
| milimani | feeding | sargassum    | ulva_salad   |     3 |     4 |        2       |        0.25    |     12   | 0.0356983 |       0.535475 | True               | False                   | *               | ns               |
| milimani | feeding | control      | sargassum    |     3 |     3 |        0       |        2       |      0   | 0.0468542 |       0.655958 | True               | False                   | *               | ns               |
| milimani | feeding | sargassum    | ulva_gutweed |     3 |     3 |        2       |        0       |      9   | 0.0468542 |       0.655958 | True               | False                   | *               | ns               |
| milimani | feeding | fischmix     | ulva_salad   |     1 |     4 |       12       |        0.25    |      4   | 0.23568   |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | fischmix     | sargassum    |     1 |     3 |       12       |        2       |      3   | 0.248213  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | control      | fischmix     |     3 |     1 |        0       |       12       |      0   | 0.248213  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | fischmix     | ulva_gutweed |     1 |     3 |       12       |        0       |      3   | 0.248213  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | control      | mackerel     |     3 |     3 |        0       |        4.33333 |      3   | 0.504985  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | mackerel     | ulva_gutweed |     3 |     3 |        4.33333 |        0       |      6   | 0.504985  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | ulva_gutweed | ulva_salad   |     3 |     4 |        0       |        0.25    |      4.5 | 0.563703  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | control      | ulva_salad   |     3 |     4 |        0       |        0.25    |      4.5 | 0.563703  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | mackerel     | sargassum    |     3 |     3 |        4.33333 |        2       |      3   | 0.637352  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | mackerel     | ulva_salad   |     3 |     4 |        4.33333 |        0.25    |      7   | 0.825498  |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | control      | ulva_gutweed |     3 |     3 |        0       |        0       |      4.5 | 1         |       1        | False              | False                   | ns              | ns               |
| milimani | feeding | fischmix     | mackerel     |     1 |     3 |       12       |        4.33333 |      2   | 1         |       1        | False              | False                   | ns              | ns               |

### Uebersicht: Taxa mit Flag je Koeder (inkl. MaxN dieser Taxa)
#### control
Keine Taxa mit diesem Flag bei diesem Koeder.

#### fischmix
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus) |                   5 |                    1 |          16 |            16 |         16 |                      1 |
| species::red (lutjanus bohar)             |                   3 |                    1 |           8 |             8 |          8 |                      1 |
| family_label::groupers feeding            |                   2 |                    1 |           2 |             2 |          2 |                      1 |
| species::goldbar (thalassoma hebraicum)   |                   1 |                    1 |           3 |             3 |          3 |                      1 |
| species::moon (thalassoma lunare)         |                   1 |                    1 |           3 |             3 |          3 |                      1 |

#### mackerel
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus) |                   9 |                    1 |    4        |             3 |          8 |               1        |
| species::goldbar (thalassoma hebraicum)   |                   2 |                    1 |    2        |             2 |          3 |               1        |
| family_label::groupers feeding            |                   1 |                    1 |    0.333333 |             0 |          1 |               0.333333 |
| species::red (lutjanus bohar)             |                   1 |                    1 |    2        |             2 |          3 |               1        |

#### sargassum
| taxon_key                                           |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:----------------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus)           |                   5 |                    3 |     6.33333 |             6 |          9 |                      1 |
| species::lined bristletooth (ctenochaetus striatus) |                   1 |                    1 |     4.33333 |             5 |          5 |                      1 |

#### ulva_gutweed
Keine Taxa mit diesem Flag bei diesem Koeder.

#### ulva_salad
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus) |                   1 |                    1 |           1 |             1 |          1 |                      1 |

### Interpretation
- Es gibt robuste (Holm-korrigierte) Unterschiede zwischen Koedern fuer 1 Taxa im Flag feeding.
- Paarweise Total-Event-Kontraste: roh signifikant 3, Holm-signifikant 0.
- Taxa mit hoher bait-spezifischer Anzahl und gleichzeitig trendhaftem Dominanzprofil sind prioritaere Kandidaten fuer koederabhaengiges Verhalten.

## Interested - Signifikanz und Trends
- Getestete Taxa: 6; roh signifikant: 0; Holm-signifikant: 0.
- Globaler Koedereffekt (Total-Events je Video): p=0.05089 (nicht signifikant).

### Koederprofile
| koeder       |   n_videos |   mean_total_events |   median_total_events |   mean_unique_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:-------------|-----------:|--------------------:|----------------------:|-------------------:|-----------------------:|------------------------:|
| control      |          3 |            0        |                     0 |           0        |                      0 |                       0 |
| fischmix     |          1 |           18        |                    18 |           5        |                      0 |                       0 |
| mackerel     |          3 |            4.33333  |                     0 |           1.66667  |                      0 |                       0 |
| sargassum    |          3 |            6.66667  |                     7 |           2.66667  |                      1 |                       0 |
| ulva_gutweed |          3 |            0.666667 |                     0 |           0.333333 |                      0 |                       0 |
| ulva_salad   |          4 |            0        |                     0 |           0        |                      0 |                       0 |

### Besondere Taxa (bait-spezifisch)
- control (0):
  - Keine
- fischmix (0):
  - Keine
- mackerel (0):
  - Keine
- sargassum (1):
  - species::lined bristletooth (ctenochaetus striatus)
- ulva_gutweed (0):
  - Keine
- ulva_salad (0):
  - Keine

### Top-Taxa-Trends (roh p<0.05)
Keine Daten.

### Paarweise Koederunterschiede (Total-Events)
| site     | flag       | koeder_a     | koeder_b     |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm | significant_0_05   | significant_0_05_holm   | sig_label_raw   | sig_label_holm   |
|:---------|:-----------|:-------------|:-------------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|:-------------------|:------------------------|:----------------|:-----------------|
| milimani | interested | sargassum    | ulva_salad   |     3 |     4 |       6.66667  |       0        |       12 | 0.0319112 |       0.478668 | True               | False                   | *               | ns               |
| milimani | interested | control      | sargassum    |     3 |     3 |       0        |       6.66667  |        0 | 0.0636026 |       0.890436 | False              | False                   | ns              | ns               |
| milimani | interested | sargassum    | ulva_gutweed |     3 |     3 |       6.66667  |       0.666667 |        9 | 0.0765225 |       0.994793 | False              | False                   | ns              | ns               |
| milimani | interested | fischmix     | ulva_salad   |     1 |     4 |      18        |       0        |        4 | 0.133614  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | control      | fischmix     |     3 |     1 |       0        |      18        |        0 | 0.248213  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | fischmix     | ulva_gutweed |     1 |     3 |      18        |       0.666667 |        3 | 0.345779  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | fischmix     | mackerel     |     1 |     3 |      18        |       4.33333  |        3 | 0.345779  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | mackerel     | ulva_salad   |     3 |     4 |       4.33333  |       0        |        8 | 0.386476  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | ulva_gutweed | ulva_salad   |     3 |     4 |       0.666667 |       0        |        8 | 0.386476  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | fischmix     | sargassum    |     1 |     3 |      18        |       6.66667  |        3 | 0.5       |       1        | False              | False                   | ns              | ns               |
| milimani | interested | control      | mackerel     |     3 |     3 |       0        |       4.33333  |        3 | 0.504985  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | control      | ulva_gutweed |     3 |     3 |       0        |       0.666667 |        3 | 0.504985  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | mackerel     | sargassum    |     3 |     3 |       4.33333  |       6.66667  |        3 | 0.657905  |       1        | False              | False                   | ns              | ns               |
| milimani | interested | control      | ulva_salad   |     3 |     4 |       0        |       0        |        6 | 1         |       1        | False              | False                   | ns              | ns               |
| milimani | interested | mackerel     | ulva_gutweed |     3 |     3 |       4.33333  |       0.666667 |        5 | 1         |       1        | False              | False                   | ns              | ns               |

### Uebersicht: Taxa mit Flag je Koeder (inkl. MaxN dieser Taxa)
#### control
Keine Taxa mit diesem Flag bei diesem Koeder.

#### fischmix
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus) |                   8 |                    1 |          16 |            16 |         16 |                      1 |
| species::red (lutjanus bohar)             |                   5 |                    1 |           8 |             8 |          8 |                      1 |
| family_label::groupers interested         |                   3 |                    1 |           2 |             2 |          2 |                      1 |
| species::goldbar (thalassoma hebraicum)   |                   1 |                    1 |           3 |             3 |          3 |                      1 |
| species::moon (thalassoma lunare)         |                   1 |                    1 |           3 |             3 |          3 |                      1 |

#### mackerel
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus) |                   7 |                    1 |    4        |             3 |          8 |               1        |
| family_label::groupers interested         |                   2 |                    1 |    0.666667 |             0 |          2 |               0.333333 |
| species::goldbar (thalassoma hebraicum)   |                   2 |                    1 |    2        |             2 |          3 |               1        |
| species::moon (thalassoma lunare)         |                   1 |                    1 |    2.33333  |             3 |          3 |               1        |
| species::red (lutjanus bohar)             |                   1 |                    1 |    2        |             2 |          3 |               1        |

#### sargassum
| taxon_key                                           |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:----------------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus)           |                  13 |                    3 |    6.33333  |             6 |          9 |               1        |
| species::red (lutjanus bohar)                       |                   3 |                    2 |    2        |             2 |          2 |               1        |
| species::lined bristletooth (ctenochaetus striatus) |                   2 |                    1 |    4.33333  |             5 |          5 |               1        |
| family_label::groupers interested                   |                   1 |                    1 |    0.333333 |             0 |          1 |               0.333333 |
| species::goldbar (thalassoma hebraicum)             |                   1 |                    1 |    1.66667  |             2 |          2 |               1        |

#### ulva_gutweed
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus) |                   2 |                    1 |           4 |             3 |          7 |                      1 |

#### ulva_salad
Keine Taxa mit diesem Flag bei diesem Koeder.

### Interpretation
- Es zeigen sich keine klaren Taxa-Unterschiede zwischen Koedern in diesem Flag.
- Paarweise Total-Event-Kontraste: roh signifikant 1, Holm-signifikant 0.
- Taxa mit hoher bait-spezifischer Anzahl und gleichzeitig trendhaftem Dominanzprofil sind prioritaere Kandidaten fuer koederabhaengiges Verhalten.

