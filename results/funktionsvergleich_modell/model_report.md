# Modellbasierte Fish-vs-Algae-Analyse mit Standortfaktor

Modell: log1p(MaxN) ~ bait_type + site + bait_type:site

Permutationstest: Bait-Labels innerhalb der Standorte geshuffelt (299 Permutationen).

## Uebersicht
| feature_type    |   n_tested |   n_sig_bait_bh |   n_sig_interaction_bh |   median_r2 |
|:----------------|-----------:|----------------:|-----------------------:|------------:|
| diet            |          4 |               0 |                      0 |    0.121227 |
| word_group      |         18 |               0 |                      0 |    0.214226 |
| family          |         20 |               0 |                      0 |    0.214226 |
| genus           |         45 |               0 |                      0 |    0.227072 |
| unspecific      |         12 |               0 |                      0 |    0.261554 |
| composite_group |         16 |               0 |                      0 |    0.226899 |

## Interpretation
- Nach Standortkontrolle gibt es in diesem Modell keine BH-signifikanten Fish-vs-Algae-Effekte und keine BH-signifikanten Interaktionen.
- Die Rohsignale folgen aber weitgehend dem explorativen Bild aus den vorherigen Analysen: `moorish_idol`, `zanclidae`, `zanclus`, `wrasses`, `labridae` und `wrasses_trigger_combo` liegen vorn.
- Das Modell ist damit ein konservativer Test und bestaetigt vor allem, dass die robustesten Signale nicht aus einer einfachen Standort-Kontrollierung heraus als neue harte Effekte auftauchen.

## Rohsignale
| feature_type    | feature                | direction   |   p_perm_bait |   p_bh_bait |   beta_bait_fish_vs_algae |   p_perm_interaction |   p_bh_interaction |
|:----------------|:-----------------------|:------------|--------------:|------------:|--------------------------:|---------------------:|-------------------:|
| word_group      | moorish_idol           | fish        |        0.0033 |        0.06 |                    0.7514 |               0.0033 |              0.06  |
| family          | zanclidae              | fish        |        0.0033 |        0.0667 |                  0.7514 |               0.0033 |              0.0667 |
| genus           | zanclus                | fish        |        0.0033 |        0.15 |                    0.7514 |               0.0033 |              0.15  |
| family          | labridae               | fish        |        0.0067 |        0.0667 |                  0.5560 |               0.4667 |              0.8462 |
| word_group      | wrasses                | fish        |        0.0067 |        0.06 |                    0.5560 |               0.4667 |              0.9   |
| composite_group | wrasses_trigger_combo  | fish        |        0.0067 |        0.1067 |                  0.5560 |               0.6067 |              0.8492 |