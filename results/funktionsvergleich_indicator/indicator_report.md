# Indikator-/Permutationstest fuer robuste Koedergruppen

Permutation: Bait-Labels innerhalb der Standorte geshuffelt (299 Permutationen).

## Uebersicht
| feature_type    |   n_tested |   n_sig_bh | top_fish_indicator         | top_algae_indicator   |
|:----------------|-----------:|-----------:|:---------------------------|:----------------------|
| diet            |          4 |          0 | invertebrates              | fish                  |
| word_group      |         18 |          2 | surgeonfishes              | goatfishes            |
| family          |         20 |          2 | acanthuridae               | mullidae              |
| genus           |         45 |          4 | zebrasoma                  | chlorurus             |
| unspecific      |         12 |          1 | large ovals                | parrotfishes          |
| composite_group |         16 |          6 | nocturnal_predator_mixture | bioeroder_set         |

## Signifikante Gruppen
| feature_type    | feature                    | best_side   |   indval |     p_perm |      p_bh |   fish_score |   algae_score |   mean_fish |   mean_algae |
|:----------------|:---------------------------|:------------|---------:|-----------:|----------:|-------------:|--------------:|------------:|-------------:|
| composite_group | wrasses_trigger_combo      | fish        |  70.1911 | 0.00333333 | 0.0177778 |      70.1911 |       29.8089 |     6.44444 |     2.73684  |
| composite_group | predator_reef_core         | fish        |  65.598  | 0.00333333 | 0.0177778 |      65.598  |       34.402  |     3.11111 |     1.63158  |
| composite_group | snappers_groupers_combo    | fish        |  65.598  | 0.00333333 | 0.0177778 |      65.598  |       34.402  |     3.11111 |     1.63158  |
| composite_group | piscivore_active_hunters   | fish        |  64.1737 | 0.00666667 | 0.0213333 |      64.1737 |       35.8263 |     3.11111 |     1.73684  |
| composite_group | piscivore_core_families    | fish        |  64.1737 | 0.00666667 | 0.0213333 |      64.1737 |       35.8263 |     3.11111 |     1.73684  |
| composite_group | nocturnal_predator_mixture | fish        |  71.6981 | 0.01       | 0.0266667 |      71.6981 |       22.3436 |     2.66667 |     1.05263  |
| word_group      | wrasses                    | fish        |  71.1853 | 0.00333333 | 0.03      |      71.1853 |       28.8147 |     6.11111 |     2.47368  |
| word_group      | triggerfishes              | fish        |  69.5775 | 0.00333333 | 0.03      |      69.5775 |       30.4225 |     4.33333 |     1.89474  |
| family          | labridae                   | fish        |  71.1853 | 0.00333333 | 0.0333333 |      71.1853 |       28.8147 |     6.11111 |     2.47368  |
| family          | balistidae                 | fish        |  69.5775 | 0.00333333 | 0.0333333 |      69.5775 |       30.4225 |     4.33333 |     1.89474  |
| genus           | balistapus                 | fish        |  69.5775 | 0.00333333 | 0.0375    |      69.5775 |       30.4225 |     4.33333 |     1.89474  |
| genus           | thalassoma                 | fish        |  68.9119 | 0.00333333 | 0.0375    |      68.9119 |       31.0881 |     4.66667 |     2.10526  |
| genus           | aethaloperca               | fish        |  60.9434 | 0.00333333 | 0.0375    |      60.9434 |       39.0566 |     1.88889 |     1.21053  |
| genus           | labroides                  | fish        |  59.5313 | 0.00333333 | 0.0375    |      59.5313 |       11.1125 |     1.88889 |     0.578947 |
| unspecific      | wrasses                    | fish        |  71.1853 | 0.00333333 | 0.04      |      71.1853 |       28.8147 |     6.11111 |     2.47368  |

## Interpretation
- Robuste Indikatorgruppen liegen vor allem auf der Fischseite.
- Algenindikatoren bleiben explorativ und werden durch Permutation und BH-Korrektur nicht robust gestuetzt.