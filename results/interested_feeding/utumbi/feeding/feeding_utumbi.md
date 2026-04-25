# Feeding-only Koedervergleich - Utumbi (cut_47min)

## Beschreibung
- Es wurden ausschliesslich feeding-Annotationen ausgewertet.
- Taxonschluessel: species > genus > family/label.
- Standort: utumbi; Videos: 18; Koeder: control, fischmix, mackerel, sargassum, ulva_gutweed, ulva_salad.
- Tests: Kruskal-Wallis (global), Mann-Whitney U (paarweise), Holm und BH fuer multiple Tests.

## Zusammenfassung der Ergebnisse
- Getestete Taxa: 10
- Roh signifikante Taxa (p<0.05): 4
- Holm-signifikante Taxa: 0
- Globaler Koedereffekt auf totale feeding Events je Video: p=0.01455 (signifikant)

## Kernaussagen
- Es gibt trendhafte Taxa-Unterschiede zwischen Koedern (roh signifikant), aber keine Holm-robusten Effekte.
- Die stärksten Hinweise liegen bei Taxa mit hoher Mitteldifferenz zwischen dominantem und schwächstem Koeder.
- Bait-spezifische Taxa liefern zusaetzlich biologische Plausibilitaet fuer koederabhaengige feeding-Muster.

## Koederprofile
| koeder       |   n_videos |   mean_total_feeding_events |   median_total_feeding_events |   mean_unique_feeding_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:-------------|-----------:|----------------------------:|------------------------------:|---------------------------:|-----------------------:|------------------------:|
| control      |          4 |                    0.25     |                           0   |                   0.25     |                      0 |                       0 |
| fischmix     |          2 |                   23.5      |                          23.5 |                   8.5      |                      1 |                       3 |
| mackerel     |          3 |                   14.6667   |                          17   |                   5.66667  |                      2 |                       1 |
| sargassum    |          3 |                    4.33333  |                           2   |                   2.66667  |                      0 |                       0 |
| ulva_gutweed |          3 |                    0.333333 |                           0   |                   0.333333 |                      0 |                       0 |
| ulva_salad   |          3 |                    2.33333  |                           1   |                   2        |                      1 |                       0 |

## Top-Taxa (global, nach p-Wert)
| taxon_key                                      | dominant_koeder_mean   | weakest_koeder_mean   |    p_value |   p_value_holm |   p_value_bh |   mean_diff_max_minus_min |    eta_sq |
|:-----------------------------------------------|:-----------------------|:----------------------|-----------:|---------------:|-------------:|--------------------------:|----------:|
| species::orange-lined (balistapus undulatus)   | fischmix               | control               | 0.00871379 |      0.0871379 |    0.0871379 |                  8.5      | 0.868262  |
| species::redmouth (aethaloperca rogaa)         | fischmix               | control               | 0.0202522  |      0.18227   |    0.101261  |                  1        | 0.696429  |
| species::black-lipped (chaetodon kleinii)      | fischmix               | control               | 0.0362928  |      0.290343  |    0.115585  |                  2        | 0.574363  |
| species::green (amblyglyphidodon indicus)      | mackerel               | ulva_gutweed          | 0.0462339  |      0.323637  |    0.115585  |                  5.66667  | 0.522723  |
| species::blacktip (epinephelus fasciatus)      | mackerel               | control               | 0.106434   |      0.638606  |    0.186783  |                  0.666667 | 0.338889  |
| species::moon (thalassoma lunare)              | fischmix               | control               | 0.129759   |      0.648794  |    0.186783  |                  3.5      | 0.293426  |
| species::red (lutjanus bohar)                  | fischmix               | control               | 0.130748   |      0.648794  |    0.186783  |                  1        | 0.291667  |
| family_label::groupers feeding                 | mackerel               | control               | 0.339499   |      1         |    0.377221  |                  1        | 0.0559641 |
| species::longfin banner (heniochus acuminatus) | mackerel               | control               | 0.339499   |      1         |    0.377221  |                  0.666667 | 0.0559641 |
| species::goldbar (thalassoma hebraicum)        | sargassum              | control               | 0.509426   |      1         |    0.509426  |                  1.66667  | 0         |

## Paarweise Koedervergleiche (Total feeding Events je Video)
| koeder_a     | koeder_b     |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm |   p_value_bh | significant_holm   | significant_bh   | sig_label_raw   | sig_label_holm   |
|:-------------|:-------------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|-------------:|:-------------------|:-----------------|:----------------|:-----------------|
| control      | mackerel     |     4 |     3 |       0.25     |      14.6667   |      0   | 0.0435966 |       0.65395  |     0.214279 | False              | False            | *               | ns               |
| control      | sargassum    |     4 |     3 |       0.25     |       4.33333  |      0.5 | 0.0639689 |       0.895565 |     0.214279 | False              | False            | ns              | ns               |
| mackerel     | ulva_gutweed |     3 |     3 |      14.6667   |       0.333333 |      9   | 0.0765225 |       0.994793 |     0.214279 | False              | False            | ns              | ns               |
| mackerel     | ulva_salad   |     3 |     3 |      14.6667   |       2.33333  |      9   | 0.0765225 |       0.994793 |     0.214279 | False              | False            | ns              | ns               |
| control      | fischmix     |     4 |     2 |       0.25     |      23.5      |      0   | 0.0851524 |       0.994793 |     0.214279 | False              | False            | ns              | ns               |
| control      | ulva_salad   |     4 |     3 |       0.25     |       2.33333  |      1   | 0.0857117 |       0.994793 |     0.214279 | False              | False            | ns              | ns               |
| sargassum    | ulva_gutweed |     3 |     3 |       4.33333  |       0.333333 |      8.5 | 0.115688  |       1        |     0.231068 | False              | False            | ns              | ns               |
| fischmix     | ulva_gutweed |     2 |     3 |      23.5      |       0.333333 |      6   | 0.138641  |       1        |     0.231068 | False              | False            | ns              | ns               |
| fischmix     | ulva_salad   |     2 |     3 |      23.5      |       2.33333  |      6   | 0.138641  |       1        |     0.231068 | False              | False            | ns              | ns               |
| ulva_gutweed | ulva_salad   |     3 |     3 |       0.333333 |       2.33333  |      1   | 0.157299  |       1        |     0.235949 | False              | False            | ns              | ns               |
| fischmix     | sargassum    |     2 |     3 |      23.5      |       4.33333  |      6   | 0.2       |       1        |     0.25     | False              | False            | ns              | ns               |
| mackerel     | sargassum    |     3 |     3 |      14.6667   |       4.33333  |      8   | 0.2       |       1        |     0.25     | False              | False            | ns              | ns               |
| sargassum    | ulva_salad   |     3 |     3 |       4.33333  |       2.33333  |      6   | 0.642835  |       1        |     0.741732 | False              | False            | ns              | ns               |
| fischmix     | mackerel     |     2 |     3 |      23.5      |      14.6667   |      4   | 0.8       |       1        |     0.857143 | False              | False            | ns              | ns               |
| control      | ulva_gutweed |     4 |     3 |       0.25     |       0.333333 |      5.5 | 1         |       1        |     1        | False              | False            | ns              | ns               |

## Bait-spezifische Taxa
- control (0):
  - Keine
- fischmix (1):
  - species::freckled (paracirrhites forsteri)
- mackerel (2):
  - species::false-eye (abudefduf sparoides)
  - species::undulated (gymnothorax undulatus)
- sargassum (0):
  - Keine
- ulva_gutweed (0):
  - Keine
- ulva_salad (1):
  - family_label::naso feeding

## Interpretation
- Der globale Test ist signifikant: die Gesamthaefigkeit von feeding-Ereignissen unterscheidet sich zwischen Koedern am Standort.
- Taxon-spezifische Signifikanz (insb. nach Holm/BH) ist der robusteste Nachweis fuer echte koederabhaengige Unterschiede auf Arten/Gattungs/Familienebene.
- Roh-signifikante Effekte ohne Korrektur sind als Trends zu lesen und sollten mit groesserer Stichprobe oder fokussierten Hypothesentests validiert werden.
