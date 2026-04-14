# Interested/Feeding Koedervergleich (cut_47min) - Gesamtuebersicht

## Kernergebnisse
| standort   |   n_videos |   n_koeder |   feeding_taxa_tested |   feeding_raw_sig_taxa |   feeding_holm_sig_taxa |   feeding_total_events_p | feeding_total_events_sig   |   interested_taxa_tested |   interested_raw_sig_taxa |   interested_holm_sig_taxa |   interested_total_events_p | interested_total_events_sig   |
|:-----------|-----------:|-----------:|----------------------:|-----------------------:|------------------------:|-------------------------:|:---------------------------|-------------------------:|--------------------------:|---------------------------:|----------------------------:|:------------------------------|
| milimani   |         17 |          6 |                     6 |                      1 |                       1 |                0.070288  | False                      |                        6 |                         0 |                          0 |                   0.0508942 | False                         |
| nursery    |         11 |          4 |                    16 |                      2 |                       0 |                0.0384306 | True                       |                       13 |                         0 |                          0 |                   0.753004  | False                         |
| utumbi     |         18 |          6 |                    14 |                      4 |                       0 |                0.0145484 | True                       |                       15 |                         2 |                          0 |                   0.0127677 | True                          |

## Aehnlichkeit zwischen feeding und interested
### Standortebene
| standort   |   taxa_feeding |   taxa_interested |   shared_taxa |   taxa_jaccard |   spearman_video_totals |   pearson_video_totals |   both_in_same_video |   feed_only_videos |   interested_only_videos |   neither_videos |
|:-----------|---------------:|------------------:|--------------:|---------------:|-----------------------:|----------------------:|--------------------:|------------------:|------------------------:|----------------:|
| milimani   |              6 |                 6 |             5 |          0.714 |                  0.872 |                 0.913 |               0.294 |             0.059 |                   0.059 |           0.588 |
| nursery    |             16 |                13 |             8 |          0.381 |                  0.435 |                 0.773 |               0.545 |             0.364 |                   0     |           0.091 |
| utumbi     |             14 |                15 |            11 |          0.611 |                  0.923 |                 0.810 |               0.722 |             0     |                   0.056 |           0.222 |

### Gesamt
| taxa_feeding | taxa_interested | shared_taxa | taxa_jaccard | spearman_video_totals | pearson_video_totals | both_in_same_video | feed_only_videos | interested_only_videos | neither_videos |
|-------------:|----------------:|------------:|-------------:|----------------------:|--------------------:|-------------------:|----------------:|-----------------------:|---------------:|
|           27 |              25 |          18 |        0.529 |                 0.720 |               0.692 |              0.522 |            0.109 |                  0.043 |          0.326 |

## Ausfuehrliche Interpretation
### milimani
- Feeding: 1 Roh-Signale, 1 Holm-signifikant; Globaltest Total-Events p=0.07029.
- Interested: 0 Roh-Signale, 0 Holm-signifikant; Globaltest Total-Events p=0.05089.
- Ein gemeinsames Muster aus trendhaften Einzeltaxa + bait-spezifischen Taxa spricht fuer koederabhaengige Verhaltensschwerpunkte, auch wenn konservative Korrekturen einzelne Signale abschwaechen koennen.

### nursery
- Feeding: 2 Roh-Signale, 0 Holm-signifikant; Globaltest Total-Events p=0.03843.
- Interested: 0 Roh-Signale, 0 Holm-signifikant; Globaltest Total-Events p=0.753.
- Ein gemeinsames Muster aus trendhaften Einzeltaxa + bait-spezifischen Taxa spricht fuer koederabhaengige Verhaltensschwerpunkte, auch wenn konservative Korrekturen einzelne Signale abschwaechen koennen.

### utumbi
- Feeding: 4 Roh-Signale, 0 Holm-signifikant; Globaltest Total-Events p=0.01455.
- Interested: 2 Roh-Signale, 0 Holm-signifikant; Globaltest Total-Events p=0.01277.
- Ein gemeinsames Muster aus trendhaften Einzeltaxa + bait-spezifischen Taxa spricht fuer koederabhaengige Verhaltensschwerpunkte, auch wenn konservative Korrekturen einzelne Signale abschwaechen koennen.

## Standortuebergreifende Tendenzen
- Global signifikante Koedereffekte auf Total-Events: Feeding in 2/3 Standorten, Interested in 1/3 Standorten.
- Roh-signifikante Taxa summiert ueber Standorte: Feeding 7, Interested 2.
- `feeding` und `interested` sind insgesamt deutlich verwandt, aber nicht identisch: Die Video-Korrelation ist moderat bis hoch, und ueber die Haelfte der Videos enthalten beide Annotationen gleichzeitig.
- Milimani zeigt die hoechste Aehnlichkeit zwischen beiden Flags, Nursery die geringste.
- Fuer robuste Aussagen pro Taxon sollten Holm-signifikante Ergebnisse priorisiert werden; Roh-Signale sind als Trends/Hypothesen zu interpretieren.

## Besondere Taxa und Trends
- Pro Standort finden sich detaillierte Listen bait-spezifischer Taxa sowie Top-Taxa-Trends in den jeweiligen Site-Reports.
- Besonders relevant sind Taxa, die (a) bait-spezifisch auftreten und (b) gleichzeitig trendhaft als dominanter Koeder in den MaxN-Event-Tests erscheinen.

## Berichte pro Standort
- milimani/interested_feeding_milimani.md
- nursery/interested_feeding_nursery.md
- utumbi/interested_feeding_utumbi.md
