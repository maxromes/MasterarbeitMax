# Nursery taxa composition by bait method

Data basis: results/nursery_methodik_vergleich/data/nursery_video_metrics.csv

Inference excludes control (n=1); control is reported exploratively only.

## PERMANOVA results (Bray-Curtis)
| comparison      | level   | test                    |   f_stat |   p_value |   n_videos | groups                          |   p_value_holm |   p_value_bh | significant_raw   | significant_holm   | significant_bh   |
|:----------------|:--------|:------------------------|---------:|----------:|-----------:|:--------------------------------|---------------:|-------------:|:------------------|:-------------------|:-----------------|
| strings_vs_mix  | species | PERMANOVA (Bray-Curtis) |  1.68994 |    0.1011 |          6 | algae_strings|algaemix          |         0.2344 |      0.12132 | False             | False              | False            |
| strings_vs_mix  | family  | PERMANOVA (Bray-Curtis) |  1.65362 |    0.202  |          6 | algae_strings|algaemix          |         0.2344 |      0.202   | False             | False              | False            |
| mix_vs_mackerel | species | PERMANOVA (Bray-Curtis) |  3.37076 |    0.0586 |          7 | algaemix|mackerel               |         0.2344 |      0.0879  | False             | False              | False            |
| mix_vs_mackerel | family  | PERMANOVA (Bray-Curtis) |  3.51559 |    0.0586 |          7 | algaemix|mackerel               |         0.2344 |      0.0879  | False             | False              | False            |
| three_baits     | species | PERMANOVA (Bray-Curtis) |  3.02508 |    0.0196 |         10 | algae_strings|algaemix|mackerel |         0.1176 |      0.0639  | True              | False              | False            |
| three_baits     | family  | PERMANOVA (Bray-Curtis) |  2.72947 |    0.0213 |         10 | algae_strings|algaemix|mackerel |         0.1176 |      0.0639  | True              | False              | False            |
