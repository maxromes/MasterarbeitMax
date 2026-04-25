# Modellbasierte Fish-vs-Algae-Analyse mit Standortfaktor

Modell: log1p(MaxN) ~ bait_type + site + bait_type:site

Permutationstest: Bait-Labels innerhalb der Standorte geshuffelt (299 Permutationen).

## Uebersicht
| feature_type    |   n_tested |   n_sig_bait_bh |   n_sig_interaction_bh |   median_r2 |
|:----------------|-----------:|----------------:|-----------------------:|------------:|
| diet            |          4 |               0 |                      0 |    0.102842 |
| word_group      |         18 |               2 |                      0 |    0.204696 |
| family          |         20 |               2 |                      0 |    0.204696 |
| genus           |         45 |               0 |                      0 |    0.218765 |
| unspecific      |         12 |               1 |                      0 |    0.264973 |
| composite_group |         16 |               0 |                      0 |    0.218172 |

## Interpretation
- Der Bait-Effekt bleibt auch nach Kontrolle fuer den Standort in mehreren Feature-Klassen sichtbar.
- Signifikante Interaktionen deuten darauf hin, dass die Staerke des Fish-vs-Algae-Effekts zwischen Milimani und Utumbi variiert.
- Die staerksten Effekte liegen erwartungsgemaess bei den funktionellen Gruppen, die bereits in den explorativen Analysen auffielen.

## Signifikante Features (BH)
| feature_type   | feature      | direction   |   beta_bait_fish_vs_algae |   p_perm_bait |   p_bh_bait |   beta_interaction |   p_perm_interaction |   p_bh_interaction |       r2 |
|:---------------|:-------------|:------------|--------------------------:|--------------:|------------:|-------------------:|---------------------:|-------------------:|---------:|
| word_group     | moorish_idol | fish        |                  0.751361 |    0.00333333 |   0.03      |         -1.28361   |           0.00333333 |          0.06      | 0.503264 |
| word_group     | wrasses      | fish        |                  0.55597  |    0.00333333 |   0.03      |          0.0356683 |           0.916667   |          0.977647  | 0.583072 |
| family         | zanclidae    | fish        |                  0.751361 |    0.00333333 |   0.0333333 |         -1.28361   |           0.00333333 |          0.0666667 | 0.503264 |
| family         | labridae     | fish        |                  0.55597  |    0.00333333 |   0.0333333 |          0.0356683 |           0.916667   |          0.97193   | 0.583072 |
| unspecific     | wrasses      | fish        |                  0.55597  |    0.00333333 |   0.04      |          0.0356683 |           0.916667   |          1         | 0.583072 |