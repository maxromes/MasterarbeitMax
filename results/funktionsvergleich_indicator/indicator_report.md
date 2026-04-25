# Indikator-/Permutationstest fuer robuste Koedergruppen

Permutation: Bait-Labels innerhalb der Standorte geshuffelt (299 Permutationen).

## Uebersicht
| feature_type    |   n_tested |   n_sig_bh | top_fish_indicator    | top_algae_indicator   |
|:----------------|-----------:|-----------:|:----------------------|:----------------------|
| diet            |          4 |          0 | invertebrates         | fish                  |
| word_group      |         18 |          2 | surgeonfishes         | goatfishes            |
| family          |         20 |          2 | acanthuridae          | mullidae              |
| genus           |         45 |          0 | zebrasoma             | chlorurus             |
| unspecific      |         12 |          1 | large ovals           | parrotfishes          |
| composite_group |         16 |          0 | wrasses_trigger_combo | bioeroder_set         |

## Signifikante Gruppen
| feature_type   | feature       | best_side   |   indval |     p_perm |      p_bh |   fish_score |   algae_score |   mean_fish |   mean_algae |
|:---------------|:--------------|:------------|---------:|-----------:|----------:|-------------:|--------------:|------------:|-------------:|
| word_group     | wrasses       | fish        |  68.7592 | 0.00333333 | 0.03      |      68.7592 |       31.2408 |     5.44444 |      2.47368 |
| word_group     | triggerfishes | fish        |  68.4518 | 0.00333333 | 0.03      |      68.4518 |       31.5482 |     4.11111 |      1.89474 |
| family         | labridae      | fish        |  68.7592 | 0.00333333 | 0.0333333 |      68.7592 |       31.2408 |     5.44444 |      2.47368 |
| family         | balistidae    | fish        |  68.4518 | 0.00333333 | 0.0333333 |      68.4518 |       31.5482 |     4.11111 |      1.89474 |
| unspecific     | wrasses       | fish        |  68.7592 | 0.00333333 | 0.04      |      68.7592 |       31.2408 |     5.44444 |      2.47368 |

## Interpretation
- Robuste Indikatorgruppen liegen vor allem auf der Fischseite.
- Algenindikatoren bleiben explorativ und werden durch Permutation und BH-Korrektur nicht robust gestuetzt.