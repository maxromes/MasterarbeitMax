# Interested/Feeding Koedervergleich (cut_47min) - Gesamtuebersicht

## Kernergebnisse
| standort   |   n_videos |   n_koeder |   feeding_taxa_tested |   feeding_raw_sig_taxa |   feeding_holm_sig_taxa |   feeding_total_events_p | feeding_total_events_sig   |   interested_taxa_tested |   interested_raw_sig_taxa |   interested_holm_sig_taxa |   interested_total_events_p | interested_total_events_sig   |
|:-----------|-----------:|-----------:|----------------------:|-----------------------:|------------------------:|-------------------------:|:---------------------------|-------------------------:|--------------------------:|---------------------------:|----------------------------:|:------------------------------|
| milimani   |         17 |          6 |                     6 |                      1 |                       1 |                0.070288  | False                      |                        6 |                         0 |                          0 |                   0.0508942 | False                         |
| nursery    |         11 |          4 |                    16 |                      2 |                       0 |                0.0384306 | True                       |                       13 |                         0 |                          0 |                   0.753004  | False                         |
| utumbi     |         18 |          6 |                    14 |                      4 |                       0 |                0.0145484 | True                       |                       15 |                         2 |                          0 |                   0.0127677 | True                          |

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
- Fuer robuste Aussagen pro Taxon sollten Holm-signifikante Ergebnisse priorisiert werden; Roh-Signale sind als Trends/Hypothesen zu interpretieren.

## Besondere Taxa und Trends
- Pro Standort finden sich detaillierte Listen bait-spezifischer Taxa sowie Top-Taxa-Trends in den jeweiligen Site-Reports.
- Besonders relevant sind Taxa, die (a) bait-spezifisch auftreten und (b) gleichzeitig trendhaft als dominanter Koeder in den MaxN-Event-Tests erscheinen.

## Fokusupdate Nursery: algaemix vs mackerel (feeding)
- Fuer `species::paletail unicorn (naso brevirostris)` und `species::honeycomb (siganus stellatus)` zeigt sich eine vollstaendige Trennung: algaemix 3/3 positive Videos, mackerel 0/4 positive Videos.
- Effektstaerke: `cliffs_delta = 1.0` bei beiden Taxa.
- Exakter Mann-Whitney: p=0.0571 je Taxon; Holm(2 Taxa)=0.1143 (nicht signifikant).
- Permutationstest und Fisher-Exact zeigen p=0.0268 bzw. p=0.0286; Holm(2 Taxa)=0.0536 bzw. 0.0571 (knapp nicht signifikant), BH(2 Taxa) signifikant.
- Interpretation: biologisch sehr starkes Signal, inferenzstatistisch unter Holm-konservativer Lesart knapp nicht robust; unter BH/FDR fuer die vorab definierten 2 Fokus-Taxa signifikant.

Quelle:
- nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md

## Berichte pro Standort
- milimani/interested_feeding_milimani.md
- nursery/interested_feeding_nursery.md
- utumbi/interested_feeding_utumbi.md
