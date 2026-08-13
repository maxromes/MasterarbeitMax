# Einheitliches Bait x Standort-Interaktionsmodell (Kern-Endpunkte)

Modell: log1p(y) ~ bait_type + site + bait_type:site
Permutation: Bait-Labels innerhalb der Standorte permutiert
Permutationen je Endpunkt: 10000

## Ergebnisuebersicht

| endpoint                    |   n_videos | direction   |   beta_bait_fish_vs_algae |   p_perm_bait |   p_bh_bait |   p_perm_interaction |   p_bh_interaction | sig_bait_bh_0_05   | sig_interaction_bh_0_05   |       r2 |
|:----------------------------|-----------:|:------------|--------------------------:|--------------:|------------:|---------------------:|-------------------:|:-------------------|:--------------------------|---------:|
| herbivore_acanthuridae_maxn |         38 | fish        |                 1.08007   |    0.00019998 |  0.00089991 |           0.00019998 |         0.00089991 | True               | True                      | 0.648916 |
| total_feeding_events        |         38 | fish        |                 0.902103  |    9.999e-05  |  0.00089991 |           9.999e-05  |         0.00089991 | True               | True                      | 0.690156 |
| herbivore_core_total_maxn   |         38 | fish        |                 0.772628  |    0.00289971 |  0.00869913 |           0.00089991 |         0.00269973 | True               | True                      | 0.346863 |
| total_interested_events     |         38 | fish        |                 0.686866  |    0.0237976  |  0.0535446  |           0.0956904  |         0.215303   | False              | False                     | 0.292284 |
| herbivore_siganidae_maxn    |         38 | fish        |                 0.0549306 |    0.250275   |  0.406159   |           0.30447    |         0.456704   | False              | False                     | 0.233517 |
| herbivore_blenniidae_maxn   |         38 | algae       |                -0.0869822 |    0.270773   |  0.406159   |           0.357864   |         0.460111   | False              | False                     | 0.238654 |
| maxn_video_peak             |         38 | fish        |                 0.240756  |    0.471953   |  0.606796   |           0.29887    |         0.456704   | False              | False                     | 0.408066 |
| herbivore_scaridae_maxn     |         38 | fish        |                 0.0711838 |    0.642636   |  0.673233   |           0.50435    |         0.50435    | False              | False                     | 0.151623 |
| species_richness            |         38 | fish        |                 0.0624066 |    0.673233   |  0.673233   |           0.49925    |         0.50435    | False              | False                     | 0.623812 |

## Kurzfazit

- BH-signifikante Bait-Effekte: 3 von 9 Endpunkten.
- BH-signifikante Bait x Standort-Interaktionen: 3 von 9 Endpunkten.
- Die Richtung ist als fish/algae fuer den Bait-Haupteffekt kodiert (positiv = fish > algae auf log1p-Skala).