# Mackerel-Taxa-Komposition nach Standort

Test: PERMANOVA auf Bray-Curtis-Distanzen, basierend auf relativen Taxon-MaxN-Profilen pro Video.

## Globaler Test
| level   | test                    |   f_stat |   p_value |   permutations |   n_videos |   p_value_holm |   p_value_bh | significant_raw   | significant_holm   | significant_bh   |
|:--------|:------------------------|---------:|----------:|---------------:|-----------:|---------------:|-------------:|:------------------|:-------------------|:-----------------|
| species | PERMANOVA (Bray-Curtis) |  3.97997 |    0.0015 |           9999 |         10 |         0.0015 |       0.0015 | True              | True               | True             |
| family  | PERMANOVA (Bray-Curtis) |  6.57796 |    0.0007 |           9999 |         10 |         0.0014 |       0.0014 | True              | True               | True             |

## Paarweise Tests
| level   | site_a   | site_b   |   f_stat |   p_value |   n_a |   n_b |   p_value_holm |   p_value_bh | significant_raw   | significant_holm   | significant_bh   |
|:--------|:---------|:---------|---------:|----------:|------:|------:|---------------:|-------------:|:------------------|:-------------------|:-----------------|
| species | milimani | utumbi   |  1.07049 |    0.2998 |     3 |     3 |         0.2998 |       0.2998 | False             | False              | False            |
| species | milimani | nursery  |  4.50101 |    0.0288 |     3 |     4 |         0.0819 |       0.0432 | True              | False              | True             |
| species | utumbi   | nursery  |  6.10746 |    0.0273 |     3 |     4 |         0.0819 |       0.0432 | True              | False              | True             |
| family  | milimani | utumbi   |  3.19807 |    0.1989 |     3 |     3 |         0.1989 |       0.1989 | False             | False              | False            |
| family  | milimani | nursery  |  5.8559  |    0.0288 |     3 |     4 |         0.0819 |       0.0432 | True              | False              | True             |
| family  | utumbi   | nursery  |  9.26385 |    0.0273 |     3 |     4 |         0.0819 |       0.0432 | True              | False              | True             |
