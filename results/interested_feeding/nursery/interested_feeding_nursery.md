# Interested/Feeding Koedervergleich - Nursery (cut_47min)

## Datengrundlage
- Standort: nursery
- Anzahl Videos: 11
- Koeder: algae_strings, algaemix, control, mackerel
- Taxonbildung: species > genus > family/label
- Betrachtete Annotationen: feeding und interested

## Feeding - Signifikanz und Trends
- Getestete Taxa: 16; roh signifikant: 2; Holm-signifikant: 0.
- Globaler Koedereffekt (Total-Events je Video): p=0.03843 (signifikant).

### Koederprofile
| koeder        |   n_videos |   mean_total_events |   median_total_events |   mean_unique_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:--------------|-----------:|--------------------:|----------------------:|-------------------:|-----------------------:|------------------------:|
| algae_strings |          3 |             13.6667 |                  13   |            5       |                      5 |                       1 |
| algaemix      |          3 |             33.6667 |                  31   |            3.66667 |                      2 |                       1 |
| control       |          1 |              0      |                   0   |            0       |                      0 |                       0 |
| mackerel      |          4 |              5.75   |                   4.5 |            2.25    |                      5 |                       0 |

### Besondere Taxa (bait-spezifisch)
- algae_strings (5):
  - family_label::siganus feeding
  - species::blue barred (scarus ghobban)
  - species::longbarbel (parupeneus macronemus)
  - species::monk (acanthurus gahhm)
  - species::red-breasted (cheilinus fasciatus)
- algaemix (2):
  - species::threadfin (chaetodon auriga)
  - species::yellow-margin (gymnothorax flavimarginatus)
- control (0):
  - Keine
- mackerel (5):
  - family_label::groupers feeding
  - species::black-lipped (chaetodon kleinii)
  - species::longfin banner (heniochus acuminatus)
  - species::longnose (lethrinus olivaceus)
  - species::red (lutjanus bohar)

### Top-Taxa-Trends (roh p<0.05)
| taxon_key                                     | dominant_koeder_mean   | lowest_koeder_mean   |   p_value |   p_value_holm |   mean_diff_max_minus_min |   eta_sq |
|:----------------------------------------------|:-----------------------|:---------------------|----------:|---------------:|--------------------------:|---------:|
| species::paletail unicorn (naso brevirostris) | algaemix               | control              | 0.0218055 |       0.348888 |                   30.3333 | 0.949749 |
| species::honeycomb (siganus stellatus)        | algae_strings          | control              | 0.0330292 |       0.495437 |                    2      | 0.819292 |

### Paarweise Koederunterschiede (Total-Events)
| site    | flag    | koeder_a      | koeder_b   |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm | significant_0_05   | significant_0_05_holm   | sig_label_raw   | sig_label_holm   |
|:--------|:--------|:--------------|:-----------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|:-------------------|:------------------------|:----------------|:-----------------|
| nursery | feeding | algaemix      | mackerel   |     3 |     4 |        33.6667 |         5.75   |     12   | 0.0571429 |       0.342857 | False              | False                   | ns              | ns               |
| nursery | feeding | algae_strings | mackerel   |     3 |     4 |        13.6667 |         5.75   |     11.5 | 0.0744618 |       0.372309 | False              | False                   | ns              | ns               |
| nursery | feeding | algae_strings | algaemix   |     3 |     3 |        13.6667 |        33.6667 |      1   | 0.2       |       0.8      | False              | False                   | ns              | ns               |
| nursery | feeding | control       | mackerel   |     1 |     4 |         0      |         5.75   |      0   | 0.4       |       1        | False              | False                   | ns              | ns               |
| nursery | feeding | algaemix      | control    |     3 |     1 |        33.6667 |         0      |      3   | 0.5       |       1        | False              | False                   | ns              | ns               |
| nursery | feeding | algae_strings | control    |     3 |     1 |        13.6667 |         0      |      3   | 0.5       |       1        | False              | False                   | ns              | ns               |

### Uebersicht: Taxa mit Flag je Koeder (inkl. MaxN dieser Taxa)
#### algae_strings
| taxon_key                                     |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:----------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::paletail unicorn (naso brevirostris) |                  20 |                    3 |    20       |            23 |         23 |               1        |
| species::honeycomb (siganus stellatus)        |                   6 |                    3 |     3.33333 |             4 |          4 |               1        |
| family_label::siganus feeding                 |                   4 |                    2 |     1       |             1 |          2 |               0.666667 |
| family_label::parrotfishes feeding            |                   4 |                    1 |     1.33333 |             0 |          4 |               0.333333 |
| species::longbarbel (parupeneus macronemus)   |                   2 |                    2 |     5.66667 |             5 |          7 |               1        |
| species::monk (acanthurus gahhm)              |                   2 |                    2 |     2.66667 |             2 |          4 |               1        |
| species::blue barred (scarus ghobban)         |                   2 |                    1 |     4       |             4 |          5 |               1        |
| species::red-breasted (cheilinus fasciatus)   |                   1 |                    1 |     1.33333 |             1 |          2 |               1        |

#### algaemix
| taxon_key                                            |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:-----------------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::paletail unicorn (naso brevirostris)        |                  91 |                    3 |   31        |            32 |         40 |               1        |
| species::honeycomb (siganus stellatus)               |                   4 |                    3 |    4        |             4 |          4 |               1        |
| family_label::parrotfishes feeding                   |                   2 |                    2 |    0.666667 |             1 |          1 |               0.666667 |
| species::humpback (lutjanus gibbus)                  |                   2 |                    1 |   36        |            43 |         45 |               1        |
| species::threadfin (chaetodon auriga)                |                   1 |                    1 |    2.66667  |             3 |          4 |               1        |
| species::yellow-margin (gymnothorax flavimarginatus) |                   1 |                    1 |    1        |             1 |          2 |               0.666667 |

#### control
Keine Taxa mit diesem Flag bei diesem Koeder.

#### mackerel
| taxon_key                                      |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:-----------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::humpback (lutjanus gibbus)            |                  12 |                    3 |       14.75 |          12   |         30 |                   1    |
| family_label::groupers feeding                 |                   3 |                    1 |        0.5  |           0   |          2 |                   0.25 |
| species::longfin banner (heniochus acuminatus) |                   3 |                    1 |        0.75 |           0.5 |          2 |                   0.5  |
| species::red (lutjanus bohar)                  |                   2 |                    2 |        1.25 |           1.5 |          2 |                   0.75 |
| species::black-lipped (chaetodon kleinii)      |                   2 |                    1 |        1.75 |           1   |          5 |                   0.75 |
| species::longnose (lethrinus olivaceus)        |                   1 |                    1 |        0.5  |           0   |          2 |                   0.25 |

### Interpretation
- Es gibt 2 trendhafte Taxa-Unterschiede (roh p<0.05), aber keine Holm-robusten Einzeleffekte.
- Paarweise Total-Event-Kontraste: roh signifikant 0, Holm-signifikant 0.
- Taxa mit hoher bait-spezifischer Anzahl und gleichzeitig trendhaftem Dominanzprofil sind prioritaere Kandidaten fuer koederabhaengiges Verhalten.

## Interested - Signifikanz und Trends
- Getestete Taxa: 13; roh signifikant: 0; Holm-signifikant: 0.
- Globaler Koedereffekt (Total-Events je Video): p=0.753 (nicht signifikant).

### Koederprofile
| koeder        |   n_videos |   mean_total_events |   median_total_events |   mean_unique_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:--------------|-----------:|--------------------:|----------------------:|-------------------:|-----------------------:|------------------------:|
| algae_strings |          3 |             2.66667 |                     1 |            1.33333 |                      2 |                       0 |
| algaemix      |          3 |            10       |                     4 |            2.33333 |                      6 |                       0 |
| control       |          1 |             0       |                     0 |            0       |                      0 |                       0 |
| mackerel      |          4 |             3.5     |                     3 |            1.25    |                      4 |                       0 |

### Besondere Taxa (bait-spezifisch)
- algae_strings (2):
  - family_label::wrasses interested
  - species::longbarbel (parupeneus macronemus)
- algaemix (6):
  - species::honeycomb (siganus stellatus)
  - species::indian longnose (hipposcarus harid)
  - species::paletail unicorn (naso brevirostris)
  - species::sailfin tang (zebrasoma desjardinii)
  - species::threadfin (chaetodon auriga)
  - species::titan (balistoides viridescens)
- control (0):
  - Keine
- mackerel (4):
  - species::black-lipped (chaetodon kleinii)
  - species::green (amblyglyphidodon indicus)
  - species::humpback (lutjanus gibbus)
  - species::red (lutjanus bohar)

### Top-Taxa-Trends (roh p<0.05)
Keine Daten.

### Paarweise Koederunterschiede (Total-Events)
| site    | flag       | koeder_a      | koeder_b   |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm | significant_0_05   | significant_0_05_holm   | sig_label_raw   | sig_label_holm   |
|:--------|:-----------|:--------------|:-----------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|:-------------------|:------------------------|:----------------|:-----------------|
| nursery | interested | algae_strings | control    |     3 |     1 |        2.66667 |            0   |      2.5 |  0.637352 |              1 | False              | False                   | ns              | ns               |
| nursery | interested | algaemix      | control    |     3 |     1 |       10       |            0   |      2.5 |  0.637352 |              1 | False              | False                   | ns              | ns               |
| nursery | interested | control       | mackerel   |     1 |     4 |        0       |            3.5 |      1   |  0.692633 |              1 | False              | False                   | ns              | ns               |
| nursery | interested | algae_strings | algaemix   |     3 |     3 |        2.66667 |           10   |      3.5 |  0.824778 |              1 | False              | False                   | ns              | ns               |
| nursery | interested | algaemix      | mackerel   |     3 |     4 |       10       |            3.5 |      7   |  0.854445 |              1 | False              | False                   | ns              | ns               |
| nursery | interested | algae_strings | mackerel   |     3 |     4 |        2.66667 |            3.5 |      6   |  1        |              1 | False              | False                   | ns              | ns               |

### Uebersicht: Taxa mit Flag je Koeder (inkl. MaxN dieser Taxa)
#### algae_strings
| taxon_key                                   |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:--------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::longbarbel (parupeneus macronemus) |                   6 |                    2 |    5.66667  |             5 |          7 |               1        |
| family_label::wrasses interested            |                   1 |                    1 |    0.333333 |             0 |          1 |               0.333333 |
| species::red-breasted (cheilinus fasciatus) |                   1 |                    1 |    1.33333  |             1 |          2 |               1        |

#### algaemix
| taxon_key                                     |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:----------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::paletail unicorn (naso brevirostris) |                  23 |                    1 |   31        |            32 |         40 |               1        |
| species::sailfin tang (zebrasoma desjardinii) |                   2 |                    1 |    2.33333  |             2 |          3 |               1        |
| species::honeycomb (siganus stellatus)        |                   1 |                    1 |    4        |             4 |          4 |               1        |
| species::indian longnose (hipposcarus harid)  |                   1 |                    1 |    1        |             0 |          3 |               0.333333 |
| species::red-breasted (cheilinus fasciatus)   |                   1 |                    1 |    0.666667 |             1 |          1 |               0.666667 |
| species::threadfin (chaetodon auriga)         |                   1 |                    1 |    2.66667  |             3 |          4 |               1        |
| species::titan (balistoides viridescens)      |                   1 |                    1 |    1.66667  |             1 |          4 |               0.666667 |

#### control
Keine Taxa mit diesem Flag bei diesem Koeder.

#### mackerel
| taxon_key                                 |   total_flag_events |   n_videos_with_flag |   mean_maxn |   median_maxn |   max_maxn |   maxn_occurrence_rate |
|:------------------------------------------|--------------------:|---------------------:|------------:|--------------:|-----------:|-----------------------:|
| species::humpback (lutjanus gibbus)       |                   9 |                    2 |       14.75 |          12   |         30 |                   1    |
| species::green (amblyglyphidodon indicus) |                   3 |                    1 |        3    |           3   |          6 |                   0.75 |
| species::black-lipped (chaetodon kleinii) |                   1 |                    1 |        1.75 |           1   |          5 |                   0.75 |
| species::red (lutjanus bohar)             |                   1 |                    1 |        1.25 |           1.5 |          2 |                   0.75 |

### Interpretation
- Es zeigen sich keine klaren Taxa-Unterschiede zwischen Koedern in diesem Flag.
- Paarweise Total-Event-Kontraste: roh signifikant 0, Holm-signifikant 0.
- Taxa mit hoher bait-spezifischer Anzahl und gleichzeitig trendhaftem Dominanzprofil sind prioritaere Kandidaten fuer koederabhaengiges Verhalten.

