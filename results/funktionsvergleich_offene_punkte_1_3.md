# Offene Punkte 1-3: kompakte Uebersicht

## 1) Modell mit Standortfaktor
| feature_type    |   n_tested |   n_sig_bait_bh |   n_sig_interaction_bh |   median_r2 |
|:----------------|-----------:|----------------:|-----------------------:|------------:|
| diet            |          4 |               0 |                      0 |    0.121227 |
| word_group      |         18 |               0 |                      0 |    0.214226 |
| family          |         20 |               0 |                      0 |    0.214226 |
| genus           |         45 |               0 |                      0 |    0.227072 |
| unspecific      |         12 |               0 |                      0 |    0.261554 |
| composite_group |         16 |               0 |                      0 |    0.226899 |

## 2) Indikator-/Permutationstest
| feature_type    |   n_tested |   n_sig_bh | top_fish_indicator         | top_algae_indicator   |
|:----------------|-----------:|-----------:|:---------------------------|:----------------------|
| diet            |          4 |          0 | invertebrates              | fish                  |
| word_group      |         18 |          2 | surgeonfishes              | goatfishes            |
| family          |         20 |          2 | acanthuridae               | mullidae              |
| genus           |         45 |          4 | zebrasoma                  | chlorurus             |
| unspecific      |         12 |          1 | large ovals                | parrotfishes          |
| composite_group |         16 |          6 | nocturnal_predator_mixture | bioeroder_set         |

## 3) Sensitivitaetsanalyse
| scenario                |   n_videos |   n_sig_bait_bh |   n_sig_interaction_bh |   n_tested |
|:------------------------|-----------:|----------------:|-----------------------:|-----------:|
| baseline                |         28 |               0 |                      0 |        115 |
| no_dominant_videos      |         24 |               4 |                      0 |        114 |
| no_rare_features        |         28 |               0 |                      0 |        115 |
| no_dominant_and_no_rare |         24 |               4 |                      0 |        114 |