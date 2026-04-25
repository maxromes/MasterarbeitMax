# Feeding-only Koedervergleich - Nursery (cut_47min)

## Beschreibung
- Es wurden ausschliesslich feeding-Annotationen ausgewertet.
- Taxonschluessel: species > genus > family/label.
- Standort: nursery; Videos: 11; Koeder: algae_strings, algaemix, control, mackerel.
- Tests: Kruskal-Wallis (global), Mann-Whitney U (paarweise), Holm und BH fuer multiple Tests.

## Zusammenfassung der Ergebnisse
- Getestete Taxa: 4
- Roh signifikante Taxa (p<0.05): 2
- Holm-signifikante Taxa: 0
- Globaler Koedereffekt auf totale feeding Events je Video: p=0.03843 (signifikant)

## Kernaussagen
- Es gibt trendhafte Taxa-Unterschiede zwischen Koedern (roh signifikant), aber keine Holm-robusten Effekte.
- Die stärksten Hinweise liegen bei Taxa mit hoher Mitteldifferenz zwischen dominantem und schwächstem Koeder.
- Bait-spezifische Taxa liefern zusaetzlich biologische Plausibilitaet fuer koederabhaengige feeding-Muster.

## Koederprofile
| koeder        |   n_videos |   mean_total_feeding_events |   median_total_feeding_events |   mean_unique_feeding_taxa |   n_bait_specific_taxa |   n_trend_taxa_dominant |
|:--------------|-----------:|----------------------------:|------------------------------:|---------------------------:|-----------------------:|------------------------:|
| algae_strings |          3 |                     13.6667 |                          13   |                    5       |                      5 |                       1 |
| algaemix      |          3 |                     33.6667 |                          31   |                    3.66667 |                      2 |                       1 |
| control       |          1 |                      0      |                           0   |                    0       |                      0 |                       0 |
| mackerel      |          4 |                      5.75   |                           4.5 |                    2.25    |                      5 |                       0 |

## Top-Taxa (global, nach p-Wert)
| taxon_key                                     | dominant_koeder_mean   | weakest_koeder_mean   |   p_value |   p_value_holm |   p_value_bh |   mean_diff_max_minus_min |    eta_sq |
|:----------------------------------------------|:-----------------------|:----------------------|----------:|---------------:|-------------:|--------------------------:|----------:|
| species::paletail unicorn (naso brevirostris) | algaemix               | control               | 0.0218055 |      0.087222  |    0.0660583 |                  30.3333  | 0.949749  |
| species::honeycomb (siganus stellatus)        | algae_strings          | control               | 0.0330292 |      0.0990875 |    0.0660583 |                   2       | 0.819292  |
| species::humpback (lutjanus gibbus)           | mackerel               | algae_strings         | 0.160271  |      0.320541  |    0.213694  |                   3       | 0.308943  |
| family_label::parrotfishes feeding            | algae_strings          | control               | 0.339648  |      0.339648  |    0.339648  |                   1.33333 | 0.0511464 |

## Paarweise Koedervergleiche (Total feeding Events je Video)
| koeder_a      | koeder_b   |   n_a |   n_b |   mean_total_a |   mean_total_b |   u_stat |   p_value |   p_value_holm |   p_value_bh | significant_holm   | significant_bh   | sig_label_raw   | sig_label_holm   |
|:--------------|:-----------|------:|------:|---------------:|---------------:|---------:|----------:|---------------:|-------------:|:-------------------|:-----------------|:----------------|:-----------------|
| algaemix      | mackerel   |     3 |     4 |        33.6667 |         5.75   |     12   | 0.0571429 |       0.342857 |     0.223385 | False              | False            | ns              | ns               |
| algae_strings | mackerel   |     3 |     4 |        13.6667 |         5.75   |     11.5 | 0.0744618 |       0.372309 |     0.223385 | False              | False            | ns              | ns               |
| algae_strings | algaemix   |     3 |     3 |        13.6667 |        33.6667 |      1   | 0.2       |       0.8      |     0.4      | False              | False            | ns              | ns               |
| control       | mackerel   |     1 |     4 |         0      |         5.75   |      0   | 0.4       |       1        |     0.5      | False              | False            | ns              | ns               |
| algaemix      | control    |     3 |     1 |        33.6667 |         0      |      3   | 0.5       |       1        |     0.5      | False              | False            | ns              | ns               |
| algae_strings | control    |     3 |     1 |        13.6667 |         0      |      3   | 0.5       |       1        |     0.5      | False              | False            | ns              | ns               |

## Bait-spezifische Taxa
- algae_strings (5):
  - family_label::siganus feeding
  - species::blue barred (scarus ghobban)
  - species::longbarbel (parupeneus macronemus)
  - species::monk (acanthurus gahhm)
  - species::red-breasted (cheilinus fasciatus)
- algaemix (2):
  - species::threadfin (chaetodon auriga)
  - species::yellow-margin (gymnothorax flavimarginatus)
- control (0):
  - Keine
- mackerel (5):
  - family_label::groupers feeding
  - species::black-lipped (chaetodon kleinii)
  - species::longfin banner (heniochus acuminatus)
  - species::longnose (lethrinus olivaceus)
  - species::red (lutjanus bohar)

## Fokus Nursery: Algaemix vs Mackerel
- Total feeding Events: p=0.05714, Holm=0.3429, BH=0.2234.
- Signifikant (roh/Holm/BH): False/False/False
- Taxa mit signifikantem algaemix-vs-mackerel Unterschied: roh=2, Holm=0, BH=0.

Top Taxa fuer algaemix vs mackerel:
| taxon_key                                     |    mean_a |   mean_b |   p_value |   p_value_holm_within_taxon |   p_value_bh_within_taxon |
|:----------------------------------------------|----------:|---------:|----------:|----------------------------:|--------------------------:|
| species::honeycomb (siganus stellatus)        |  1.33333  |        0 | 0.0300653 |                    0.180392 |                 0.0957336 |
| species::paletail unicorn (naso brevirostris) | 30.3333   |        0 | 0.0319112 |                    0.180392 |                 0.0957336 |
| family_label::parrotfishes feeding            |  0.666667 |        0 | 0.117525  |                    0.705149 |                 0.705149  |
| species::humpback (lutjanus gibbus)           |  0.666667 |        3 | 0.19909   |                    0.995449 |                 0.59727   |

## Interpretation
- Der globale Test ist signifikant: die Gesamthaefigkeit von feeding-Ereignissen unterscheidet sich zwischen Koedern am Standort.
- Taxon-spezifische Signifikanz (insb. nach Holm/BH) ist der robusteste Nachweis fuer echte koederabhaengige Unterschiede auf Arten/Gattungs/Familienebene.
- Roh-signifikante Effekte ohne Korrektur sind als Trends zu lesen und sollten mit groesserer Stichprobe oder fokussierten Hypothesentests validiert werden.
