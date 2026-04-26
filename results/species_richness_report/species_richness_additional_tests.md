# Species Richness Zusatztests (BH + Permutation)

- Permutationen pro Test: 5000

## Globaltests
| factor   | groups                                                                                    |   n_total |   n_groups |   h_stat |   p_value_kw |   p_value_perm |   eta_squared |   epsilon_squared | significant_kw_0_05   | significant_perm_0_05   |   n_permutations |
|:---------|:------------------------------------------------------------------------------------------|----------:|-----------:|---------:|-------------:|---------------:|--------------:|------------------:|:----------------------|:------------------------|-----------------:|
| standort | milimani, nursery, utumbi                                                                 |        46 |          3 |  25.9593 |   2.3068e-06 |     0.00019996 |      0.557193 |         0.509772  | True                  | True                    |             5000 |
| koeder   | algae_strings, algaemix, control, fischmix, mackerel, sargassum, ulva_gutweed, ulva_salad |        46 |          8 |  11.2522 |   0.127989   |     0.111778   |      0.111901 |         0.0904728 | False                 | False                   |             5000 |

## Anzahl signifikanter paarweiser Vergleiche (p<0.05)
| Faktor | raw | Holm | BH/FDR | Permutation |
|:--|--:|--:|--:|--:|
| standort | 3 | 3 | 3 | 3 |
| koeder | 3 | 0 | 0 | 3 |

## Top paarweise Standortvergleiche (nach BH)
| factor   | group_a   | group_b   |   n_a |   n_b |   u_stat |   p_value_raw |   p_value_perm_mean_diff |   cliffs_delta |   mean_a |   mean_b |   mean_diff_a_minus_b |   n_permutations |   p_value_holm |   p_value_bh | sig_raw_0_05   | sig_holm_0_05   | sig_bh_0_05   | sig_perm_0_05   |
|:---------|:----------|:----------|------:|------:|---------:|--------------:|-------------------------:|---------------:|---------:|---------:|----------------------:|-----------------:|---------------:|-------------:|:---------------|:----------------|:--------------|:----------------|
| standort | nursery   | utumbi    |    11 |    18 |      0.5 |    1.0198e-05 |               0.00019996 |      -0.994949 |  35.6364 |  52.6667 |             -17.0303  |             5000 |     3.0594e-05 |   3.0594e-05 | True           | True            | True          | True            |
| standort | milimani  | utumbi    |    17 |    18 |     55.5 |    0.00133767 |               0.00079984 |      -0.637255 |  44.4706 |  52.6667 |              -8.19608 |             5000 |     0.00267534 |   0.00184804 | True           | True            | True          | True            |
| standort | milimani  | nursery   |    17 |    11 |    160   |    0.00184804 |               0.00159968 |       0.71123  |  44.4706 |  35.6364 |               8.83422 |             5000 |     0.00267534 |   0.00184804 | True           | True            | True          | True            |

## Top paarweise Ködervergleiche (nach BH)
| factor   | group_a       | group_b      |   n_a |   n_b |   u_stat |   p_value_raw |   p_value_perm_mean_diff |   cliffs_delta |   mean_a |   mean_b |   mean_diff_a_minus_b |   n_permutations |   p_value_holm |   p_value_bh | sig_raw_0_05   | sig_holm_0_05   | sig_bh_0_05   | sig_perm_0_05   |
|:---------|:--------------|:-------------|------:|------:|---------:|--------------:|-------------------------:|---------------:|---------:|---------:|----------------------:|-----------------:|---------------:|-------------:|:---------------|:----------------|:--------------|:----------------|
| koeder   | algae_strings | ulva_gutweed |     3 |     6 |      0   |     0.0238095 |                0.0129974 |      -1        |  35.6667 |  48.8333 |             -13.1667  |             5000 |       0.666667 |     0.347659 | True           | False           | False         | True            |
| koeder   | algae_strings | sargassum    |     3 |     6 |      0   |     0.0275319 |                0.0255949 |      -1        |  35.6667 |  51      |             -15.3333  |             5000 |       0.743361 |     0.347659 | True           | False           | False         | True            |
| koeder   | algaemix      | sargassum    |     3 |     6 |      0.5 |     0.0372492 |                0.0305939 |      -0.944444 |  39      |  51      |             -12       |             5000 |       0.968478 |     0.347659 | True           | False           | False         | True            |
| koeder   | algaemix      | ulva_gutweed |     3 |     6 |      2   |     0.0952381 |                0.064787  |      -0.777778 |  39      |  48.8333 |              -9.83333 |             5000 |       1        |     0.392548 | False          | False           | False         | False           |
| koeder   | algae_strings | fischmix     |     3 |     3 |      0   |     0.1       |                0.107179  |      -1        |  35.6667 |  52.3333 |             -16.6667  |             5000 |       1        |     0.392548 | False          | False           | False         | False           |
| koeder   | algaemix      | fischmix     |     3 |     3 |      0   |     0.1       |                0.0993801 |      -1        |  39      |  52.3333 |             -13.3333  |             5000 |       1        |     0.392548 | False          | False           | False         | False           |
| koeder   | control       | sargassum    |     8 |     6 |     11   |     0.104271  |                0.0829834 |      -0.541667 |  43.375  |  51      |              -7.625   |             5000 |       1        |     0.392548 | False          | False           | False         | False           |
| koeder   | algae_strings | ulva_salad   |     3 |     7 |      3   |     0.116667  |                0.0945811 |      -0.714286 |  35.6667 |  46.5714 |             -10.9048  |             5000 |       1        |     0.392548 | False          | False           | False         | False           |
| koeder   | algae_strings | control      |     3 |     8 |      4   |     0.133333  |                0.138372  |      -0.666667 |  35.6667 |  43.375  |              -7.70833 |             5000 |       1        |     0.392548 | False          | False           | False         | False           |
| koeder   | control       | fischmix     |     8 |     3 |      4.5 |     0.152107  |                0.130374  |      -0.625    |  43.375  |  52.3333 |              -8.95833 |             5000 |       1        |     0.392548 | False          | False           | False         | False           |
