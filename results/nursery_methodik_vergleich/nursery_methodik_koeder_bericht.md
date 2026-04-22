# Nursery-Methodik: Koedervergleich (cut_47min)

## Datengrundlage
- Standort: nursery
- Anzahl Videos gesamt: 11
- Hauptvergleich: algae_strings (n=3), algaemix (n=3), mackerel (n=4)
- Kontrollvideo: control (n=1), kuerzeres Einzelvideo -> separat als explorativer Kontext
- Signifikanzniveau: alpha=0.05
- Korrekturen fuer multiples Testen: Holm (FWER) und Benjamini-Hochberg/FDR
- Robuste Zusatzpruefung fuer 2-Gruppen-Metriken: exakter/perm-basierter Mittelwert-Differenztest

## Taxa-Komposition (PERMANOVA, Bray-Curtis)
- Datengrundlage: relative Taxon-MaxN-Profile pro Video
- Inferenz: nur algae_strings, algaemix, mackerel (control n=1 nur explorativ)

| comparison      | level   | p_value | p_value_holm | p_value_bh | sig_raw | sig_holm | sig_bh |
|:----------------|:--------|--------:|-------------:|-----------:|:--------|:---------|:-------|
| strings_vs_mix  | species | 0.1011  | 0.2344       | 0.1213     | no      | no       | no     |
| strings_vs_mix  | family  | 0.2020  | 0.2344       | 0.2020     | no      | no       | no     |
| mix_vs_mackerel | species | 0.0586  | 0.2344       | 0.0879     | no      | no       | no     |
| mix_vs_mackerel | family  | 0.0586  | 0.2344       | 0.0879     | no      | no       | no     |
| three_baits     | species | 0.0196  | 0.1176       | 0.0639     | yes     | no       | no     |
| three_baits     | family  | 0.0213  | 0.1176       | 0.0639     | yes     | no       | no     |

Interpretation: Nach multipler Korrektur (Holm/BH) kein robuster signifikanter Unterschied in der Taxa-Komposition.

Details und Grafiken:
- [taxa_composition/nursery_taxa_composition_summary.md](taxa_composition/nursery_taxa_composition_summary.md)
- [taxa_composition/nursery_taxa_permanova.csv](taxa_composition/nursery_taxa_permanova.csv)
- [taxa_composition/nursery_three_baits_species_pcoa.png](taxa_composition/nursery_three_baits_species_pcoa.png)
- [taxa_composition/nursery_three_baits_family_pcoa.png](taxa_composition/nursery_three_baits_family_pcoa.png)

### Videoanzahl je Koeder
| koeder        |   n_videos |   median_duration_s |
|:--------------|-----------:|--------------------:|
| algae_strings |          3 |            2629.13  |
| algaemix      |          3 |            2554.88  |
| control       |          1 |             531.381 |
| mackerel      |          4 |             530.197 |

## Vergleich 1: algae_strings vs algaemix
- Gruppen: algae_strings, algaemix

### 1) Videoebene: Species Richness, MaxN, First Seen, Interested/Feeding und weitere Kennzahlen
| metric                         | test           |   p_value |   p_value_holm |   p_value_bh | sig_raw   | sig_holm   | sig_bh   | effect_name   |   effect_size |   perm_p_value_mean_diff |
|:-------------------------------|:---------------|----------:|---------------:|-------------:|:----------|:-----------|:---------|:--------------|--------------:|-------------------------:|
| shannon_species                | Mann-Whitney U |       0.1 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      1        |                      0.1 |
| sum_species_maxn               | Mann-Whitney U |       0.2 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.777778 |                      0.2 |
| sum_family_maxn                | Mann-Whitney U |       0.2 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.777778 |                      0.2 |
| total_non_behavior_annotations | Mann-Whitney U |       0.4 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.555556 |                      0.3 |
| peak_species_maxn              | Mann-Whitney U |       0.4 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.555556 |                      0.3 |
| median_first_seen_family_sec   | Mann-Whitney U |       0.4 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0.555556 |                      0.5 |
| peak_family_maxn               | Mann-Whitney U |       0.4 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.555556 |                      0.3 |
| species_richness               | Mann-Whitney U |       0.7 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.333333 |                      0.7 |
| family_richness                | Mann-Whitney U |       0.7 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.444444 |                      0.5 |
| q25_first_seen_species_sec     | Mann-Whitney U |       0.7 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.333333 |                      1   |
| general_richness               | Mann-Whitney U |       0.7 |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.444444 |                      0.6 |
| duration_sec_non_behavior      | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |     -0.111111 |                      0.9 |
| median_first_seen_species_sec  | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0.111111 |                      0.8 |
| total_feeding_events           | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0        |                      1   |
| total_interested_events        | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0        |                      1   |
| feeding_unique_species         | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0        |                      1   |
| feeding_unique_family          | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0        |                      1   |
| interested_unique_species      | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0        |                      1   |
| interested_unique_family       | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0        |                      1   |
| feeding_ratio_total            | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0        |                      1   |
| interested_ratio_total         | Mann-Whitney U |       1   |              1 |            1 | ns        | ns         | ns       | cliffs_delta  |      0        |                      1   |

Top signifikante Video-Metriken:
Keine Daten.

### 2) Artenebene (Species): Unterschiede in MaxN
Keine Daten.

### 3) Familienebene (Family): Unterschiede in MaxN
Keine Daten.

### 4) Interested vs Feeding: Artenebene
**Feeding (Species) signifikante Taxa**
Keine Daten.

**Interested (Species) signifikante Taxa**
Keine Daten.

### 5) Interested vs Feeding: Familienebene
**Feeding (Family) signifikante Taxa/Familien**
Keine Daten.

**Interested (Family) signifikante Taxa/Familien**
Keine Daten.

### Kurzinterpretation
- Videoebene: Holm-signifikant 0, BH-signifikant 0 Kennzahlen.
- Artenebene (MaxN): Holm-signifikant 0, BH-signifikant 0.
- Familienebene (MaxN): Holm-signifikant 0, BH-signifikant 0.
- Interested/Feeding ist oben getrennt nach Arten und Familien ausgewiesen.

## Vergleich 2: algaemix vs mackerel
- Gruppen: algaemix, mackerel

### 1) Videoebene: Species Richness, MaxN, First Seen, Interested/Feeding und weitere Kennzahlen
| metric                         | test           |   p_value |   p_value_holm |   p_value_bh | sig_raw   | sig_holm   | sig_bh   | effect_name   |   effect_size |   perm_p_value_mean_diff |
|:-------------------------------|:---------------|----------:|---------------:|-------------:|:----------|:-----------|:---------|:--------------|--------------:|-------------------------:|
| duration_sec_non_behavior      | Mann-Whitney U | 0.0571429 |              1 |     0.3      | ns        | ns         | ns       | cliffs_delta  |      1        |                0.0285714 |
| shannon_species                | Mann-Whitney U | 0.0571429 |              1 |     0.3      | ns        | ns         | ns       | cliffs_delta  |     -1        |                0.0571429 |
| median_first_seen_species_sec  | Mann-Whitney U | 0.0571429 |              1 |     0.3      | ns        | ns         | ns       | cliffs_delta  |      1        |                0.0571429 |
| family_richness                | Mann-Whitney U | 0.114286  |              1 |     0.3      | ns        | ns         | ns       | cliffs_delta  |      0.833333 |                0.0857143 |
| peak_family_maxn               | Mann-Whitney U | 0.114286  |              1 |     0.3      | ns        | ns         | ns       | cliffs_delta  |      0.833333 |                0.114286  |
| peak_species_maxn              | Mann-Whitney U | 0.114286  |              1 |     0.3      | ns        | ns         | ns       | cliffs_delta  |      0.833333 |                0.114286  |
| sum_family_maxn                | Mann-Whitney U | 0.114286  |              1 |     0.3      | ns        | ns         | ns       | cliffs_delta  |      0.833333 |                0.0857143 |
| sum_species_maxn               | Mann-Whitney U | 0.114286  |              1 |     0.3      | ns        | ns         | ns       | cliffs_delta  |      0.833333 |                0.142857  |
| median_first_seen_family_sec   | Mann-Whitney U | 0.4       |              1 |     0.763636 | ns        | ns         | ns       | cliffs_delta  |      0.5      |                0.228571  |
| total_non_behavior_annotations | Mann-Whitney U | 0.4       |              1 |     0.763636 | ns        | ns         | ns       | cliffs_delta  |      0.5      |                0.314286  |
| general_richness               | Mann-Whitney U | 0.4       |              1 |     0.763636 | ns        | ns         | ns       | cliffs_delta  |      0.583333 |                0.257143  |
| species_richness               | Mann-Whitney U | 0.857143  |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |      0.25     |                0.657143  |
| feeding_unique_species         | Mann-Whitney U | 0.857143  |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |     -0.25     |                1         |
| total_feeding_events           | Mann-Whitney U | 0.857143  |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |     -0.25     |                1         |
| feeding_ratio_total            | Mann-Whitney U | 0.857143  |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |     -0.25     |                1         |
| feeding_unique_family          | Mann-Whitney U | 0.857143  |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |     -0.25     |                1         |
| total_interested_events        | Mann-Whitney U | 1         |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |      0        |                1         |
| q25_first_seen_species_sec     | Mann-Whitney U | 1         |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |      0        |                0.914286  |
| interested_unique_species      | Mann-Whitney U | 1         |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |      0        |                1         |
| interested_unique_family       | Mann-Whitney U | 1         |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |      0        |                1         |
| interested_ratio_total         | Mann-Whitney U | 1         |              1 |     1        | ns        | ns         | ns       | cliffs_delta  |      0        |                1         |

Top signifikante Video-Metriken:
Keine Daten.

### 2) Artenebene (Species): Unterschiede in MaxN
Keine Daten.

### 3) Familienebene (Family): Unterschiede in MaxN
Keine Daten.

### 4) Interested vs Feeding: Artenebene
**Feeding (Species) signifikante Taxa**
Keine Daten.

**Interested (Species) signifikante Taxa**
Keine Daten.

### 5) Interested vs Feeding: Familienebene
**Feeding (Family) signifikante Taxa/Familien**
Keine Daten.

**Interested (Family) signifikante Taxa/Familien**
Keine Daten.

### Kurzinterpretation
- Videoebene: Holm-signifikant 0, BH-signifikant 0 Kennzahlen.
- Artenebene (MaxN): Holm-signifikant 0, BH-signifikant 0.
- Familienebene (MaxN): Holm-signifikant 0, BH-signifikant 0.
- Interested/Feeding ist oben getrennt nach Arten und Familien ausgewiesen.

## Vergleich 3: algae_strings vs algaemix vs mackerel
- Gruppen: algae_strings, algaemix, mackerel

### 1) Videoebene: Species Richness, MaxN, First Seen, Interested/Feeding und weitere Kennzahlen
| metric                         | test           |   p_value |   p_value_holm |   p_value_bh | sig_raw   | sig_holm   | sig_bh   | effect_name     |   effect_size |   perm_p_value_mean_diff |
|:-------------------------------|:---------------|----------:|---------------:|-------------:|:----------|:-----------|:---------|:----------------|--------------:|-------------------------:|
| duration_sec_non_behavior      | Kruskal-Wallis | 0.0375599 |       0.788758 |     0.38689  | *         | ns         | ns       | epsilon_squared |      0.651948 |                      nan |
| shannon_species                | Kruskal-Wallis | 0.0502417 |       1        |     0.38689  | ns        | ns         | ns       | epsilon_squared |      0.568831 |                      nan |
| median_first_seen_species_sec  | Kruskal-Wallis | 0.0639279 |       1        |     0.38689  | ns        | ns         | ns       | epsilon_squared |      0.5      |                      nan |
| family_richness                | Kruskal-Wallis | 0.0736933 |       1        |     0.38689  | ns        | ns         | ns       | epsilon_squared |      0.459384 |                      nan |
| sum_family_maxn                | Kruskal-Wallis | 0.111815  |       1        |     0.391353 | ns        | ns         | ns       | epsilon_squared |      0.34026  |                      nan |
| sum_species_maxn               | Kruskal-Wallis | 0.111815  |       1        |     0.391353 | ns        | ns         | ns       | epsilon_squared |      0.34026  |                      nan |
| median_first_seen_family_sec   | Kruskal-Wallis | 0.149569  |       1        |     0.423799 | ns        | ns         | ns       | epsilon_squared |      0.257143 |                      nan |
| peak_species_maxn              | Kruskal-Wallis | 0.181628  |       1        |     0.423799 | ns        | ns         | ns       | epsilon_squared |      0.201655 |                      nan |
| peak_family_maxn               | Kruskal-Wallis | 0.181628  |       1        |     0.423799 | ns        | ns         | ns       | epsilon_squared |      0.201655 |                      nan |
| general_richness               | Kruskal-Wallis | 0.394852  |       1        |     0.661313 | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| total_non_behavior_annotations | Kruskal-Wallis | 0.445263  |       1        |     0.661313 | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| total_feeding_events           | Kruskal-Wallis | 0.472367  |       1        |     0.661313 | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| feeding_unique_species         | Kruskal-Wallis | 0.472367  |       1        |     0.661313 | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| feeding_unique_family          | Kruskal-Wallis | 0.472367  |       1        |     0.661313 | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| feeding_ratio_total            | Kruskal-Wallis | 0.472367  |       1        |     0.661313 | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| species_richness               | Kruskal-Wallis | 0.773741  |       1        |     1        | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| q25_first_seen_species_sec     | Kruskal-Wallis | 0.8452    |       1        |     1        | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| total_interested_events        | Kruskal-Wallis | 1         |       1        |     1        | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| interested_unique_species      | Kruskal-Wallis | 1         |       1        |     1        | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| interested_unique_family       | Kruskal-Wallis | 1         |       1        |     1        | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |
| interested_ratio_total         | Kruskal-Wallis | 1         |       1        |     1        | ns        | ns         | ns       | epsilon_squared |      0        |                      nan |

Top signifikante Video-Metriken:
| metric                    |   p_value |   p_value_holm |   p_value_bh | sig_holm   | sig_bh   |
|:--------------------------|----------:|---------------:|-------------:|:-----------|:---------|
| duration_sec_non_behavior | 0.0375599 |       0.788758 |      0.38689 | ns         | ns       |

### 2) Artenebene (Species): Unterschiede in MaxN
| taxon                                |   p_value |   p_value_holm |   p_value_bh | sig_holm   | sig_bh   |
|:-------------------------------------|----------:|---------------:|-------------:|:-----------|:---------|
| bullethead (chlorurus sordidus)      | 0.0125881 |       0.893758 |     0.314382 | ns         | ns       |
| arabian monocle (scolopsis ghanam)   | 0.0197239 |       1        |     0.314382 | ns         | ns       |
| blue barred (scarus ghobban)         | 0.0223549 |       1        |     0.314382 | ns         | ns       |
| sailfin tang (zebrasoma desjardinii) | 0.0281286 |       1        |     0.314382 | ns         | ns       |
| weber's puller (chromis weberi)      | 0.0291621 |       1        |     0.314382 | ns         | ns       |
| paletail unicorn (naso brevirostris) | 0.0295598 |       1        |     0.314382 | ns         | ns       |

### 3) Familienebene (Family): Unterschiede in MaxN
| taxon        |   p_value |   p_value_holm |   p_value_bh | sig_holm   | sig_bh   |
|:-------------|----------:|---------------:|-------------:|:-----------|:---------|
| nemipteridae | 0.0197239 |       0.473373 |     0.344575 | ns         | ns       |
| acanthuridae | 0.0295598 |       0.679874 |     0.344575 | ns         | ns       |
| balistidae   | 0.0430718 |       0.94758  |     0.344575 | ns         | ns       |

### 4) Interested vs Feeding: Artenebene
**Feeding (Species) signifikante Taxa**
Keine Daten.

**Interested (Species) signifikante Taxa**
Keine Daten.

### 5) Interested vs Feeding: Familienebene
**Feeding (Family) signifikante Taxa/Familien**
Keine Daten.

**Interested (Family) signifikante Taxa/Familien**
Keine Daten.

### Kurzinterpretation
- Videoebene: Holm-signifikant 0, BH-signifikant 0 Kennzahlen.
- Artenebene (MaxN): Holm-signifikant 0, BH-signifikant 0.
- Familienebene (MaxN): Holm-signifikant 0, BH-signifikant 0.
- Interested/Feeding ist oben getrennt nach Arten und Familien ausgewiesen.

## Kontrollvideo (explorativ, getrennt)
Hinweis: Das Kontrollvideo hat n=1 und kuerzere Laufzeit. Aussagen sind daher rein deskriptiv und nicht als gleichwertige Signifikanztests zu interpretieren.

| metric                        |   control_value | control_file                 |   algae_strings_mean |   algae_strings_median |   algaemix_mean |   algaemix_median |   mackerel_mean |   mackerel_median |
|:------------------------------|----------------:|:-----------------------------|---------------------:|-----------------------:|----------------:|------------------:|----------------:|------------------:|
| duration_sec_non_behavior     |         531.381 | 20240108-nursery-control.csv |            2495.05   |               2629.13  |       2522.93   |          2554.88  |         560.871 |           530.197 |
| species_richness              |          20     | 20240108-nursery-control.csv |              29.6667 |                 29     |         31      |            32     |          29.25  |            28.5   |
| family_richness               |          17     | 20240108-nursery-control.csv |              17.6667 |                 18     |         18.6667 |            19     |          16     |            16     |
| sum_species_maxn              |          36     | 20240108-nursery-control.csv |             105      |                104     |        146.333  |           158     |          93.5   |            80.5   |
| sum_family_maxn               |          34     | 20240108-nursery-control.csv |              96.3333 |                 94     |        133.333  |           146     |          74.75  |            69     |
| total_feeding_events          |           0     | 20240108-nursery-control.csv |               0      |                  0     |          0      |             0     |           1     |             0     |
| total_interested_events       |           0     | 20240108-nursery-control.csv |               0      |                  0     |          0      |             0     |           0     |             0     |
| median_first_seen_species_sec |         185.844 | 20240108-nursery-control.csv |             274.609  |                252.475 |        258.488  |           216.704 |         148.052 |           132.111 |

## Gesamtfazit
Die drei Hauptkoeder wurden auf Videoebene sowie auf Arten-/Familienebene fuer MaxN und Interested/Feeding verglichen. Signifikanzen sind immer roh, Holm-korrigiert und BH-korrigiert angegeben; dadurch ist transparent, welche Befunde robust gegen multiples Testen bleiben.
