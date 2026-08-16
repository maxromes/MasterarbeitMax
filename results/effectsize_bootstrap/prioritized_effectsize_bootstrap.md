# Priorisierte Effektgroessen: Bootstrap-Konfidenzintervalle

Stand: 2026-08-16

## Methode

- Kontraste: a-priori Herbivore-MaxN (site x family) und Herbivore-Feeding-Responsiveness (site).
- Bootstrap: 5000 Resamples je Kontrast (mit Zuruecklegen, gruppenweise).
- Ausgegeben: CIs fuer Mittelwertdifferenz, Mediandifferenz und Cliff's Delta.
- p-Werte: gerichteter Mann-Whitney-Test (algae > fish), Korrektur mit BH/Holm je Analyseblock.

## herbivore_maxn_apriori

| site     | target       |   n_algae |   n_fish |   mean_diff_algae_minus_fish |   ci_mean_diff_low |   ci_mean_diff_high |   median_diff_algae_minus_fish |   ci_median_diff_low |   ci_median_diff_high |   cliffs_delta |   ci_cliffs_delta_low |   ci_cliffs_delta_high |   p_value_mwu_one_sided |   q_holm |
|:---------|:-------------|----------:|---------:|-----------------------------:|-------------------:|--------------------:|-------------------------------:|---------------------:|----------------------:|---------------:|----------------------:|-----------------------:|------------------------:|---------:|
| nursery  | acanthuridae |         6 |        4 |                      17.8333 |            11.6667 |             25.3333 |                        17.5000 |              10.0000 |               27.0000 |         1.0000 |                1.0000 |                 1.0000 |                  0.0070 |   0.0835 |
| nursery  | siganidae    |         6 |        4 |                       2.2500 |            -0.2500 |              4.5000 |                         3.0000 |              -1.0000 |                4.5000 |         0.5000 |               -0.3333 |                 1.0000 |                  0.1124 |   1.0000 |
| utumbi   | scaridae     |         9 |        5 |                       9.9778 |            -1.9556 |             27.9778 |                         4.0000 |              -5.0000 |               11.0000 |         0.3333 |               -0.3333 |                 0.9111 |                  0.1743 |   1.0000 |
| utumbi   | siganidae    |         9 |        5 |                       0.8667 |            -0.5333 |              2.4889 |                         1.0000 |              -1.0000 |                2.0000 |         0.2000 |               -0.4000 |                 0.7333 |                  0.2845 |   1.0000 |
| milimani | blenniidae   |        10 |        4 |                       0.0000 |            -1.4500 |              1.1500 |                         0.5000 |              -2.0000 |                1.5000 |         0.1000 |               -0.6500 |                 0.8000 |                  0.4117 |   1.0000 |
| nursery  | scaridae     |         6 |        4 |                      -0.0833 |            -4.9167 |              4.9187 |                        -1.5000 |              -8.0000 |                7.5000 |         0.0000 |               -0.7083 |                 0.7083 |                  0.5428 |   1.0000 |
| milimani | siganidae    |        10 |        4 |                      -0.1000 |            -1.0000 |              1.0000 |                         0.0000 |              -2.0000 |                2.0000 |        -0.0500 |               -0.5000 |                 0.5000 |                  0.6066 |   1.0000 |
| milimani | scaridae     |        10 |        4 |                       0.1500 |            -6.3000 |              6.7000 |                        -1.0000 |             -11.0000 |                4.5000 |        -0.1500 |               -0.8000 |                 0.5000 |                  0.6910 |   1.0000 |
| utumbi   | acanthuridae |         9 |        5 |                      -2.1111 |            -5.7333 |              0.4000 |                         0.0000 |              -9.0000 |                1.0000 |        -0.3111 |               -0.8444 |                 0.3333 |                  0.8542 |   1.0000 |
| utumbi   | blenniidae   |         9 |        5 |                      -0.5333 |            -1.2444 |              0.2667 |                         0.0000 |              -2.0000 |                1.0000 |        -0.4000 |               -0.8889 |                 0.2667 |                  0.9228 |   1.0000 |
| milimani | acanthuridae |        10 |        4 |                     -23.7500 |           -48.0000 |              0.4025 |                       -17.5000 |             -62.0000 |                2.0000 |        -0.4750 |               -1.0000 |                 0.4506 |                  0.9271 |   1.0000 |
| nursery  | blenniidae   |         6 |        4 |                      -0.7500 |            -1.5000 |              0.0000 |                        -0.5000 |              -2.0000 |                0.0000 |        -0.5000 |               -1.0000 |                 0.0000 |                  0.9760 |   1.0000 |

## herbivore_feeding_responsiveness

| site     | target                      |   n_algae |   n_fish |   mean_diff_algae_minus_fish |   ci_mean_diff_low |   ci_mean_diff_high |   median_diff_algae_minus_fish |   ci_median_diff_low |   ci_median_diff_high |   cliffs_delta |   ci_cliffs_delta_low |   ci_cliffs_delta_high |   p_value_mwu_one_sided |   q_holm |
|:---------|:----------------------------|----------:|---------:|-----------------------------:|-------------------:|--------------------:|-------------------------------:|---------------------:|----------------------:|---------------:|----------------------:|-----------------------:|------------------------:|---------:|
| nursery  | herbivore_core_feeding_rate |         6 |        4 |                       0.2038 |             0.1523 |              0.2575 |                         0.1938 |               0.1318 |                0.2857 |         1.0000 |                1.0000 |                 1.0000 |                  0.0057 |   0.0171 |
| utumbi   | herbivore_core_feeding_rate |         9 |        5 |                       0.0030 |             0.0000 |              0.0090 |                         0.0000 |               0.0000 |                0.0000 |         0.1111 |                0.0000 |                 0.3333 |                  0.2755 |   0.5510 |
| milimani | herbivore_core_feeding_rate |        10 |        4 |                       0.0029 |             0.0000 |              0.0086 |                         0.0000 |               0.0000 |                0.0000 |         0.1000 |                0.0000 |                 0.3000 |                  0.3176 |   0.5510 |

