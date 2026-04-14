# Interested/Feeding Koedervergleich - Utumbi (cut_47min)

## Datengrundlage
- Standort: utumbi
- Anzahl Videos: 18
- Koeder: control, fischmix, mackerel, sargassum, ulva_gutweed, ulva_salad
- Taxonbildung: species > genus > family/label
- Betrachtete Annotationen: feeding und interested

## Feeding - Signifikanz und Trends
- Getestete Taxa: 14; roh signifikant: 4; Holm-signifikant: 0.
- Globaler Koedereffekt (Total-Events je Video): p=0.01455 (signifikant).

### Koederprofile
| koeder       |   n_videos |   mean_total_events |   median_total_events |   mean_unique_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:-------------|-----------:|--------------------:|----------------------:|-------------------:|-----------------------:|------------------------:|
| control      |          4 |            0.25     |                   0   |           0.25     |                      0 |                       0 |
| fischmix     |          2 |           23.5      |                  23.5 |           8.5      |                      1 |                       3 |
| mackerel     |          3 |           14.6667   |                  17   |           5.66667  |                      2 |                       1 |
| sargassum    |          3 |            4.33333  |                   2   |           2.66667  |                      0 |                       0 |
| ulva_gutweed |          3 |            0.333333 |                   0   |           0.333333 |                      0 |                       0 |
| ulva_salad   |          3 |            2.33333  |                   1   |           2        |                      1 |                       0 |

### Besondere Taxa (bait-spezifisch)
- control (0):
  - Keine
- fischmix (1):
  - species::freckled (paracirrhites forsteri)
- mackerel (2):
  - species::false-eye (abudefduf sparoides)
  - species::undulated (gymnothorax undulatus)
- sargassum (0):
  - Keine
- ulva_gutweed (0):
  - Keine
- ulva_salad (1):
  - family_label::naso feeding

### Top-Taxa-Trends (roh p<0.05)
| taxon_key                                    | dominant_koeder_mean   | lowest_koeder_mean   |    p_value |   p_value_holm |   mean_diff_max_minus_min |   eta_sq |
|:---------------------------------------------|:-----------------------|:---------------------|-----------:|---------------:|--------------------------:|---------:|
| species::orange-lined (balistapus undulatus) | fischmix               | control              | 0.00871379 |       0.121993 |                   8.5     | 0.868262 |
| species::redmouth (aethaloperca rogaa)       | fischmix               | control              | 0.0202522  |       0.263279 |                   1       | 0.696429 |
| species::black-lipped (chaetodon kleinii)    | fischmix               | control              | 0.0362928  |       0.435514 |                   2       | 0.574363 |
| species::green (amblyglyphidodon indicus)    | mackerel               | ulva_gutweed         | 0.0462339  |       0.508573 |                   5.66667 | 0.522723 |

### Paarweise Koederunterschiede (Total-Events)
| site   | flag    | koeder_a     | koeder_b     |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm | significant_0_05   | significant_0_05_holm   | sig_label_raw   | sig_label_holm   |
|:-------|:--------|:-------------|:-------------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|:-------------------|:------------------------|:----------------|:-----------------|
| utumbi | feeding | control      | mackerel     |     4 |     3 |       0.25     |      14.6667   |      0   | 0.0435966 |       0.65395  | True               | False                   | *               | ns               |
| utumbi | feeding | control      | sargassum    |     4 |     3 |       0.25     |       4.33333  |      0.5 | 0.0639689 |       0.895565 | False              | False                   | ns              | ns               |
| utumbi | feeding | mackerel     | ulva_gutweed |     3 |     3 |      14.6667   |       0.333333 |      9   | 0.0765225 |       0.994793 | False              | False                   | ns              | ns               |
| utumbi | feeding | mackerel     | ulva_salad   |     3 |     3 |      14.6667   |       2.33333  |      9   | 0.0765225 |       0.994793 | False              | False                   | ns              | ns               |
| utumbi | feeding | control      | fischmix     |     4 |     2 |       0.25     |      23.5      |      0   | 0.0851524 |       0.994793 | False              | False                   | ns              | ns               |
| utumbi | feeding | control      | ulva_salad   |     4 |     3 |       0.25     |       2.33333  |      1   | 0.0857117 |       0.994793 | False              | False                   | ns              | ns               |
| utumbi | feeding | sargassum    | ulva_gutweed |     3 |     3 |       4.33333  |       0.333333 |      8.5 | 0.115688  |       1        | False              | False                   | ns              | ns               |
| utumbi | feeding | fischmix     | ulva_gutweed |     2 |     3 |      23.5      |       0.333333 |      6   | 0.138641  |       1        | False              | False                   | ns              | ns               |
| utumbi | feeding | fischmix     | ulva_salad   |     2 |     3 |      23.5      |       2.33333  |      6   | 0.138641  |       1        | False              | False                   | ns              | ns               |
| utumbi | feeding | ulva_gutweed | ulva_salad   |     3 |     3 |       0.333333 |       2.33333  |      1   | 0.157299  |       1        | False              | False                   | ns              | ns               |
| utumbi | feeding | fischmix     | sargassum    |     2 |     3 |      23.5      |       4.33333  |      6   | 0.2       |       1        | False              | False                   | ns              | ns               |
| utumbi | feeding | mackerel     | sargassum    |     3 |     3 |      14.6667   |       4.33333  |      8   | 0.2       |       1        | False              | False                   | ns              | ns               |
| utumbi | feeding | sargassum    | ulva_salad   |     3 |     3 |       4.33333  |       2.33333  |      6   | 0.642835  |       1        | False              | False                   | ns              | ns               |
| utumbi | feeding | fischmix     | mackerel     |     2 |     3 |      23.5      |      14.6667   |      4   | 0.8       |       1        | False              | False                   | ns              | ns               |
| utumbi | feeding | control      | ulva_gutweed |     4 |     3 |       0.25     |       0.333333 |      5.5 | 1         |       1        | False              | False                   | ns              | ns               |

### Uebersicht: Taxa mit Flag je Koeder (inkl. MaxN dieser Taxa)
#### control
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus) |                   1 |                    1 |           2 |             2 |          3 |                      1 |

#### fischmix
| taxon_key                                      |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:-----------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::orange-lined (balistapus undulatus)   |                  17 |                    2 |         7.5 |           7.5 |         10 |                    1   |
| species::green (amblyglyphidodon indicus)      |                  10 |                    2 |        10.5 |          10.5 |         12 |                    1   |
| species::moon (thalassoma lunare)              |                   7 |                    2 |         7.5 |           7.5 |          8 |                    1   |
| species::black-lipped (chaetodon kleinii)      |                   4 |                    2 |         2   |           2   |          2 |                    1   |
| species::red (lutjanus bohar)                  |                   2 |                    2 |         1.5 |           1.5 |          2 |                    1   |
| species::redmouth (aethaloperca rogaa)         |                   2 |                    2 |         2   |           2   |          2 |                    1   |
| family_label::groupers feeding                 |                   1 |                    1 |         0.5 |           0.5 |          1 |                    0.5 |
| species::blacktip (epinephelus fasciatus)      |                   1 |                    1 |         0.5 |           0.5 |          1 |                    0.5 |
| species::freckled (paracirrhites forsteri)     |                   1 |                    1 |         2   |           2   |          2 |                    1   |
| species::goldbar (thalassoma hebraicum)        |                   1 |                    1 |         1.5 |           1.5 |          2 |                    1   |
| species::longfin banner (heniochus acuminatus) |                   1 |                    1 |         1   |           1   |          1 |                    1   |

#### mackerel
| taxon_key                                      |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:-----------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus)      |                  17 |                    2 |    8.33333  |             6 |         18 |               1        |
| species::orange-lined (balistapus undulatus)   |                   9 |                    3 |    5.33333  |             5 |          6 |               1        |
| family_label::groupers feeding                 |                   3 |                    1 |    0.666667 |             0 |          2 |               0.333333 |
| species::moon (thalassoma lunare)              |                   3 |                    1 |    2.33333  |             3 |          3 |               1        |
| species::blacktip (epinephelus fasciatus)      |                   2 |                    2 |    1.33333  |             2 |          2 |               0.666667 |
| species::red (lutjanus bohar)                  |                   2 |                    2 |    2.33333  |             3 |          3 |               1        |
| species::redmouth (aethaloperca rogaa)         |                   2 |                    2 |    2        |             2 |          2 |               1        |
| species::goldbar (thalassoma hebraicum)        |                   2 |                    1 |    3.33333  |             2 |          6 |               1        |
| species::longfin banner (heniochus acuminatus) |                   2 |                    1 |    0.666667 |             0 |          2 |               0.333333 |
| species::false-eye (abudefduf sparoides)       |                   1 |                    1 |    3.33333  |             2 |          8 |               0.666667 |
| species::undulated (gymnothorax undulatus)     |                   1 |                    1 |    0.666667 |             0 |          2 |               0.333333 |

#### sargassum
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::goldbar (thalassoma hebraicum)   |                   5 |                    2 |     2.66667 |             3 |          3 |               1        |
| species::green (amblyglyphidodon indicus) |                   3 |                    3 |     4       |             4 |          5 |               1        |
| species::black-lipped (chaetodon kleinii) |                   3 |                    1 |     1.33333 |             2 |          2 |               0.666667 |
| species::moon (thalassoma lunare)         |                   1 |                    1 |     1.66667 |             2 |          2 |               1        |
| species::red (lutjanus bohar)             |                   1 |                    1 |     1.66667 |             2 |          2 |               1        |

#### ulva_gutweed
| taxon_key                               |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:----------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::goldbar (thalassoma hebraicum) |                   1 |                    1 |     1.66667 |             2 |          2 |                      1 |

#### ulva_salad
| taxon_key                                    |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:---------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::goldbar (thalassoma hebraicum)      |                   2 |                    2 |    2        |             2 |          3 |               1        |
| species::moon (thalassoma lunare)            |                   2 |                    1 |    3        |             3 |          5 |               1        |
| family_label::naso feeding                   |                   1 |                    1 |    0.333333 |             0 |          1 |               0.333333 |
| species::orange-lined (balistapus undulatus) |                   1 |                    1 |    2        |             2 |          2 |               1        |
| species::red (lutjanus bohar)                |                   1 |                    1 |    0.666667 |             1 |          1 |               0.666667 |

### Interpretation
- Es gibt 4 trendhafte Taxa-Unterschiede (roh p<0.05), aber keine Holm-robusten Einzeleffekte.
- Paarweise Total-Event-Kontraste: roh signifikant 1, Holm-signifikant 0.
- Taxa mit hoher bait-spezifischer Anzahl und gleichzeitig trendhaftem Dominanzprofil sind prioritaere Kandidaten fuer koederabhaengiges Verhalten.

## Interested - Signifikanz und Trends
- Getestete Taxa: 15; roh signifikant: 2; Holm-signifikant: 0.
- Globaler Koedereffekt (Total-Events je Video): p=0.01277 (signifikant).

### Koederprofile
| koeder       |   n_videos |   mean_total_events |   median_total_events |   mean_unique_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:-------------|-----------:|--------------------:|----------------------:|-------------------:|-----------------------:|------------------------:|
| control      |          4 |            0.25     |                     0 |           0.25     |                      0 |                       0 |
| fischmix     |          2 |           18        |                    18 |           5.5      |                      3 |                       1 |
| mackerel     |          3 |           15        |                     8 |           5.66667  |                      4 |                       1 |
| sargassum    |          3 |            2.33333  |                     2 |           2        |                      0 |                       0 |
| ulva_gutweed |          3 |            0.666667 |                     1 |           0.666667 |                      0 |                       0 |
| ulva_salad   |          3 |            2.66667  |                     3 |           2.33333  |                      0 |                       0 |

### Besondere Taxa (bait-spezifisch)
- control (0):
  - Keine
- fischmix (3):
  - species::black-lipped (chaetodon kleinii)
  - species::freckled (paracirrhites forsteri)
  - species::undulated (gymnothorax undulatus)
- mackerel (4):
  - family_label::wrasses interested
  - species::blacktip (epinephelus fasciatus)
  - species::false-eye (abudefduf sparoides)
  - species::leopard (cephalopholis leopardus)
- sargassum (0):
  - Keine
- ulva_gutweed (0):
  - Keine
- ulva_salad (0):
  - Keine

### Top-Taxa-Trends (roh p<0.05)
| taxon_key                                 | dominant_koeder_mean   | lowest_koeder_mean   |    p_value |   p_value_holm |   mean_diff_max_minus_min |   eta_sq |
|:------------------------------------------|:-----------------------|:---------------------|-----------:|---------------:|--------------------------:|---------:|
| species::black-lipped (chaetodon kleinii) | fischmix               | control              | 0.00461272 |      0.0691908 |                   2.5     | 0.995098 |
| species::goldbar (thalassoma hebraicum)   | mackerel               | control              | 0.0383465  |      0.536851  |                   1.33333 | 0.562678 |

### Paarweise Koederunterschiede (Total-Events)
| site   | flag       | koeder_a     | koeder_b     |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm | significant_0_05   | significant_0_05_holm   | sig_label_raw   | sig_label_holm   |
|:-------|:-----------|:-------------|:-------------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|:-------------------|:------------------------|:----------------|:-----------------|
| utumbi | interested | control      | mackerel     |     4 |     3 |       0.25     |      15        |      0   | 0.0435966 |       0.65395  | True               | False                   | *               | ns               |
| utumbi | interested | control      | sargassum    |     4 |     3 |       0.25     |       2.33333  |      0.5 | 0.0639689 |       0.895565 | False              | False                   | ns              | ns               |
| utumbi | interested | control      | ulva_salad   |     4 |     3 |       0.25     |       2.66667  |      0.5 | 0.0639689 |       0.895565 | False              | False                   | ns              | ns               |
| utumbi | interested | mackerel     | ulva_gutweed |     3 |     3 |      15        |       0.666667 |      9   | 0.0765225 |       0.91827  | False              | False                   | ns              | ns               |
| utumbi | interested | control      | fischmix     |     4 |     2 |       0.25     |      18        |      0   | 0.0851524 |       0.936676 | False              | False                   | ns              | ns               |
| utumbi | interested | mackerel     | sargassum    |     3 |     3 |      15        |       2.33333  |      9   | 0.1       |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | mackerel     | ulva_salad   |     3 |     3 |      15        |       2.66667  |      9   | 0.1       |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | fischmix     | ulva_gutweed |     2 |     3 |      18        |       0.666667 |      6   | 0.138641  |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | ulva_gutweed | ulva_salad   |     3 |     3 |       0.666667 |       2.66667  |      1   | 0.16416   |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | sargassum    | ulva_gutweed |     3 |     3 |       2.33333  |       0.666667 |      8   | 0.16416   |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | fischmix     | sargassum    |     2 |     3 |      18        |       2.33333  |      6   | 0.2       |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | fischmix     | ulva_salad   |     2 |     3 |      18        |       2.66667  |      6   | 0.2       |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | control      | ulva_gutweed |     4 |     3 |       0.25     |       0.666667 |      3.5 | 0.414216  |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | fischmix     | mackerel     |     2 |     3 |      18        |      15        |      4   | 0.8       |       1        | False              | False                   | ns              | ns               |
| utumbi | interested | sargassum    | ulva_salad   |     3 |     3 |       2.33333  |       2.66667  |      4   | 1         |       1        | False              | False                   | ns              | ns               |

### Uebersicht: Taxa mit Flag je Koeder (inkl. MaxN dieser Taxa)
#### control
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus) |                   1 |                    1 |           2 |             2 |          3 |                      1 |

#### fischmix
| taxon_key                                    |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:---------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus)    |                  15 |                    2 |        10.5 |          10.5 |         12 |                    1   |
| species::orange-lined (balistapus undulatus) |                   9 |                    2 |         7.5 |           7.5 |         10 |                    1   |
| species::black-lipped (chaetodon kleinii)    |                   5 |                    2 |         2   |           2   |          2 |                    1   |
| species::moon (thalassoma lunare)            |                   2 |                    1 |         7.5 |           7.5 |          8 |                    1   |
| species::sulfur (pomacentrus sulfureus)      |                   2 |                    1 |         1   |           1   |          2 |                    0.5 |
| family_label::groupers interested            |                   1 |                    1 |         0.5 |           0.5 |          1 |                    0.5 |
| species::freckled (paracirrhites forsteri)   |                   1 |                    1 |         2   |           2   |          2 |                    1   |
| species::undulated (gymnothorax undulatus)   |                   1 |                    1 |         0.5 |           0.5 |          1 |                    0.5 |

#### mackerel
| taxon_key                                    |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:---------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::green (amblyglyphidodon indicus)    |                  15 |                    2 |    8.33333  |             6 |         18 |               1        |
| species::orange-lined (balistapus undulatus) |                   9 |                    1 |    5.33333  |             5 |          6 |               1        |
| species::goldbar (thalassoma hebraicum)      |                   4 |                    3 |    3.33333  |             2 |          6 |               1        |
| species::false-eye (abudefduf sparoides)     |                   4 |                    1 |    3.33333  |             2 |          8 |               0.666667 |
| family_label::groupers interested            |                   3 |                    1 |    0.666667 |             0 |          2 |               0.333333 |
| species::red (lutjanus bohar)                |                   2 |                    2 |    2.33333  |             3 |          3 |               1        |
| species::redmouth (aethaloperca rogaa)       |                   2 |                    2 |    2        |             2 |          2 |               1        |
| species::moon (thalassoma lunare)            |                   2 |                    1 |    2.33333  |             3 |          3 |               1        |
| family_label::wrasses interested             |                   1 |                    1 |    0.333333 |             0 |          1 |               0.333333 |
| species::blacktip (epinephelus fasciatus)    |                   1 |                    1 |    1.33333  |             2 |          2 |               0.666667 |
| species::leopard (cephalopholis leopardus)   |                   1 |                    1 |    1.33333  |             2 |          2 |               0.666667 |
| species::sulfur (pomacentrus sulfureus)      |                   1 |                    1 |    1.33333  |             1 |          2 |               1        |

#### sargassum
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::goldbar (thalassoma hebraicum)   |                   2 |                    2 |     2.66667 |             3 |          3 |                      1 |
| species::red (lutjanus bohar)             |                   2 |                    2 |     1.66667 |             2 |          2 |                      1 |
| species::green (amblyglyphidodon indicus) |                   2 |                    1 |     4       |             4 |          5 |                      1 |
| species::redmouth (aethaloperca rogaa)    |                   1 |                    1 |     1.33333 |             1 |          2 |                      1 |

#### ulva_gutweed
| taxon_key                                    |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:---------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::orange-lined (balistapus undulatus) |                   2 |                    2 |           2 |             2 |          2 |                      1 |

#### ulva_salad
| taxon_key                                    |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:---------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::orange-lined (balistapus undulatus) |                   3 |                    2 |    2        |             2 |          2 |               1        |
| species::red (lutjanus bohar)                |                   2 |                    2 |    0.666667 |             1 |          1 |               0.666667 |
| species::goldbar (thalassoma hebraicum)      |                   1 |                    1 |    2        |             2 |          3 |               1        |
| species::green (amblyglyphidodon indicus)    |                   1 |                    1 |    2        |             2 |          4 |               0.666667 |
| species::moon (thalassoma lunare)            |                   1 |                    1 |    3        |             3 |          5 |               1        |

### Interpretation
- Es gibt 2 trendhafte Taxa-Unterschiede (roh p<0.05), aber keine Holm-robusten Einzeleffekte.
- Paarweise Total-Event-Kontraste: roh signifikant 1, Holm-signifikant 0.
- Taxa mit hoher bait-spezifischer Anzahl und gleichzeitig trendhaftem Dominanzprofil sind prioritaere Kandidaten fuer koederabhaengiges Verhalten.

