# Offene Punkte 1-3: kompakte Uebersicht

## 1) Modell mit Standortfaktor
| feature_type    |   n_tested |   n_sig_bait_bh |   n_sig_interaction_bh |   median_r2 |
|:----------------|-----------:|----------------:|-----------------------:|------------:|
| diet            |          4 |               0 |                      0 |    0.102842 |
| word_group      |         18 |               2 |                      0 |    0.204696 |
| family          |         20 |               2 |                      0 |    0.204696 |
| genus           |         45 |               0 |                      0 |    0.218765 |
| unspecific      |         12 |               1 |                      0 |    0.264973 |
| composite_group |         16 |               0 |                      0 |    0.218172 |

## 2) Indikator-/Permutationstest
| feature_type    |   n_tested |   n_sig_bh | top_fish_indicator    | top_algae_indicator   |
|:----------------|-----------:|-----------:|:----------------------|:----------------------|
| diet            |          4 |          0 | invertebrates         | fish                  |
| word_group      |         18 |          2 | surgeonfishes         | goatfishes            |
| family          |         20 |          2 | acanthuridae          | mullidae              |
| genus           |         45 |          0 | zebrasoma             | chlorurus             |
| unspecific      |         12 |          1 | large ovals           | parrotfishes          |
| composite_group |         16 |          0 | wrasses_trigger_combo | bioeroder_set         |

## 3) Sensitivitaetsanalyse
| scenario                |   n_videos |   n_sig_bait_bh |   n_sig_interaction_bh |   n_tested |
|:------------------------|-----------:|----------------:|-----------------------:|-----------:|
| baseline                |         28 |               5 |                      0 |        115 |
| no_dominant_videos      |         24 |               4 |                      0 |        114 |
| no_rare_features        |         28 |               5 |                      0 |        115 |
| no_dominant_and_no_rare |         24 |               4 |                      0 |        114 |