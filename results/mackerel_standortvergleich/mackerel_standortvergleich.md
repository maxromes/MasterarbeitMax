# Mackerel-Standortvergleich (cut_47min)

## Species-Richness-Grafiken
- Boxplot + Einzelpunkte: [figures/species_richness_mackerel_boxstrip.png](figures/species_richness_mackerel_boxstrip.png)
- Mittelwert + 95%-Bootstrap-CI: [figures/species_richness_mackerel_mean_ci.png](figures/species_richness_mackerel_mean_ci.png)
- Paarweise Differenzen + 95%-Bootstrap-CI: [figures/species_richness_mackerel_pairwise_diff.png](figures/species_richness_mackerel_pairwise_diff.png)

## Taxa-Komposition (Species/Family)
- Globale PERMANOVA (Bray-Curtis, relative MaxN-Profile):
	- Species: p=0.0015, Holm=0.0015, BH=0.0015 (signifikant)
	- Family: p=0.0007, Holm=0.0014, BH=0.0014 (signifikant)
- Paarweise PERMANOVA:
	- Milimani vs Utumbi: nicht signifikant
	- Milimani vs Nursery: roh signifikant, BH signifikant, Holm nicht signifikant
	- Utumbi vs Nursery: roh signifikant, BH signifikant, Holm nicht signifikant
- Details: [taxa_composition/mackerel_taxa_composition_summary.md](taxa_composition/mackerel_taxa_composition_summary.md)
- Globale Tabelle: [taxa_composition/mackerel_taxa_permanova_global.csv](taxa_composition/mackerel_taxa_permanova_global.csv)
- Paarweise Tabelle: [taxa_composition/mackerel_taxa_permanova_pairwise.csv](taxa_composition/mackerel_taxa_permanova_pairwise.csv)
- Ordinationsplots:
	- [taxa_composition/mackerel_species_composition_pcoa.png](taxa_composition/mackerel_species_composition_pcoa.png)
	- [taxa_composition/mackerel_family_composition_pcoa.png](taxa_composition/mackerel_family_composition_pcoa.png)

## Datengrundlage
- Koeder: mackerel (nur mackerel-Videos)
- Quelle: normalized_reports/cut_47min
- Signifikanzniveau: alpha=0.05
- Multiple-Testing-Korrektur: Holm und Benjamini-Hochberg (BH/FDR)

### Stichprobe je Standort
| standort   |   n_videos |
|:-----------|-----------:|
| milimani   |          3 |
| nursery    |          4 |
| utumbi     |          3 |

## 1) Videoebene (Species Richness, MaxN, First Seen, Interested/Feeding, weitere)
| metric                         | test           |   h_stat |   p_value |   p_value_holm |   p_value_bh | sig_raw   | sig_holm   | sig_bh   |
|:-------------------------------|:---------------|---------:|----------:|---------------:|-------------:|:----------|:-----------|:---------|
| peak_family_maxn               | Kruskal-Wallis | 7.43636  | 0.0242781 |       0.485561 |     0.213093 | *         | ns         | ns       |
| sum_family_maxn                | Kruskal-Wallis | 6.60137  | 0.0368579 |       0.7003   |     0.213093 | *         | ns         | ns       |
| duration_sec_non_behavior      | Kruskal-Wallis | 6.56364  | 0.0375599 |       0.7003   |     0.213093 | *         | ns         | ns       |
| species_richness               | Kruskal-Wallis | 5.57273  | 0.061645  |       1        |     0.213093 | ns        | ns         | ns       |
| peak_species_maxn              | Kruskal-Wallis | 5.57273  | 0.061645  |       1        |     0.213093 | ns        | ns         | ns       |
| sum_species_maxn               | Kruskal-Wallis | 5.5      | 0.0639279 |       1        |     0.213093 | ns        | ns         | ns       |
| total_non_behavior_annotations | Kruskal-Wallis | 4.84545  | 0.0886794 |       1        |     0.252289 | ns        | ns         | ns       |
| median_first_seen_species_sec  | Kruskal-Wallis | 4.56364  | 0.102098  |       1        |     0.252289 | ns        | ns         | ns       |
| general_richness               | Kruskal-Wallis | 4.35137  | 0.11353   |       1        |     0.252289 | ns        | ns         | ns       |
| median_first_seen_family_sec   | Kruskal-Wallis | 2.3      | 0.316637  |       1        |     0.633274 | ns        | ns         | ns       |
| total_feeding_events           | Kruskal-Wallis | 1.5      | 0.472367  |       1        |     0.674809 | ns        | ns         | ns       |
| feeding_unique_species         | Kruskal-Wallis | 1.5      | 0.472367  |       1        |     0.674809 | ns        | ns         | ns       |
| feeding_unique_family          | Kruskal-Wallis | 1.5      | 0.472367  |       1        |     0.674809 | ns        | ns         | ns       |
| feeding_ratio_total            | Kruskal-Wallis | 1.5      | 0.472367  |       1        |     0.674809 | ns        | ns         | ns       |
| family_richness                | Kruskal-Wallis | 1.19811  | 0.54933   |       1        |     0.73244  | ns        | ns         | ns       |
| shannon_species                | Kruskal-Wallis | 0.336364 | 0.8452    |       1        |     1        | ns        | ns         | ns       |
| total_interested_events        | Kruskal-Wallis | 0        | 1         |       1        |     1        | ns        | ns         | ns       |
| interested_unique_species      | Kruskal-Wallis | 0        | 1         |       1        |     1        | ns        | ns         | ns       |
| interested_unique_family       | Kruskal-Wallis | 0        | 1         |       1        |     1        | ns        | ns         | ns       |
| interested_ratio_total         | Kruskal-Wallis | 0        | 1         |       1        |     1        | ns        | ns         | ns       |

### Paarweise Standortvergleiche je Metrik
| metric                         | site_a   | site_b   |   p_value |   p_value_holm_within_metric | sig_raw   | sig_holm_within_metric   |
|:-------------------------------|:---------|:---------|----------:|-----------------------------:|:----------|:-------------------------|
| duration_sec_non_behavior      | milimani | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| duration_sec_non_behavior      | utumbi   | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| duration_sec_non_behavior      | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| family_richness                | utumbi   | nursery  | 0.4       |                     1        | ns        | ns                       |
| family_richness                | milimani | nursery  | 0.628571  |                     1        | ns        | ns                       |
| family_richness                | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| feeding_ratio_total            | milimani | nursery  | 0.857143  |                     1        | ns        | ns                       |
| feeding_ratio_total            | utumbi   | nursery  | 0.857143  |                     1        | ns        | ns                       |
| feeding_ratio_total            | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| feeding_unique_family          | milimani | nursery  | 0.857143  |                     1        | ns        | ns                       |
| feeding_unique_family          | utumbi   | nursery  | 0.857143  |                     1        | ns        | ns                       |
| feeding_unique_family          | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| feeding_unique_species         | milimani | nursery  | 0.857143  |                     1        | ns        | ns                       |
| feeding_unique_species         | utumbi   | nursery  | 0.857143  |                     1        | ns        | ns                       |
| feeding_unique_species         | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| general_richness               | utumbi   | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| general_richness               | milimani | nursery  | 0.4       |                     0.8      | ns        | ns                       |
| general_richness               | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| interested_ratio_total         | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| interested_ratio_total         | milimani | nursery  | 1         |                     1        | ns        | ns                       |
| interested_ratio_total         | utumbi   | nursery  | 1         |                     1        | ns        | ns                       |
| interested_unique_family       | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| interested_unique_family       | milimani | nursery  | 1         |                     1        | ns        | ns                       |
| interested_unique_family       | utumbi   | nursery  | 1         |                     1        | ns        | ns                       |
| interested_unique_species      | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| interested_unique_species      | milimani | nursery  | 1         |                     1        | ns        | ns                       |
| interested_unique_species      | utumbi   | nursery  | 1         |                     1        | ns        | ns                       |
| median_first_seen_family_sec   | milimani | nursery  | 0.114286  |                     0.342857 | ns        | ns                       |
| median_first_seen_family_sec   | milimani | utumbi   | 0.7       |                     1        | ns        | ns                       |
| median_first_seen_family_sec   | utumbi   | nursery  | 1         |                     1        | ns        | ns                       |
| median_first_seen_species_sec  | milimani | nursery  | 0.114286  |                     0.342857 | ns        | ns                       |
| median_first_seen_species_sec  | utumbi   | nursery  | 0.114286  |                     0.342857 | ns        | ns                       |
| median_first_seen_species_sec  | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| peak_family_maxn               | milimani | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| peak_family_maxn               | utumbi   | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| peak_family_maxn               | milimani | utumbi   | 0.2       |                     0.2      | ns        | ns                       |
| peak_species_maxn              | milimani | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| peak_species_maxn              | utumbi   | nursery  | 0.114286  |                     0.228571 | ns        | ns                       |
| peak_species_maxn              | milimani | utumbi   | 0.7       |                     0.7      | ns        | ns                       |
| shannon_species                | milimani | utumbi   | 0.7       |                     1        | ns        | ns                       |
| shannon_species                | utumbi   | nursery  | 0.857143  |                     1        | ns        | ns                       |
| shannon_species                | milimani | nursery  | 1         |                     1        | ns        | ns                       |
| species_richness               | utumbi   | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| species_richness               | milimani | nursery  | 0.114286  |                     0.228571 | ns        | ns                       |
| species_richness               | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| sum_family_maxn                | utumbi   | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| sum_family_maxn                | milimani | nursery  | 0.114286  |                     0.228571 | ns        | ns                       |
| sum_family_maxn                | milimani | utumbi   | 0.4       |                     0.4      | ns        | ns                       |
| sum_species_maxn               | milimani | nursery  | 0.0571429 |                     0.171429 | ns        | ns                       |
| sum_species_maxn               | utumbi   | nursery  | 0.114286  |                     0.228571 | ns        | ns                       |
| sum_species_maxn               | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| total_feeding_events           | milimani | nursery  | 0.857143  |                     1        | ns        | ns                       |
| total_feeding_events           | utumbi   | nursery  | 0.857143  |                     1        | ns        | ns                       |
| total_feeding_events           | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| total_interested_events        | milimani | utumbi   | 1         |                     1        | ns        | ns                       |
| total_interested_events        | milimani | nursery  | 1         |                     1        | ns        | ns                       |
| total_interested_events        | utumbi   | nursery  | 1         |                     1        | ns        | ns                       |
| total_non_behavior_annotations | utumbi   | nursery  | 0.114286  |                     0.342857 | ns        | ns                       |
| total_non_behavior_annotations | milimani | utumbi   | 0.2       |                     0.4      | ns        | ns                       |
| total_non_behavior_annotations | milimani | nursery  | 0.228571  |                     0.4      | ns        | ns                       |

## 2) Taxon-Ebene: MaxN
### Species
| taxon                                          |   p_value |   p_value_holm |   p_value_bh | sig_raw   | sig_holm   | sig_bh   |
|:-----------------------------------------------|----------:|---------------:|-------------:|:----------|:-----------|:---------|
| blackwhite (macolor niger)                     | 0.011109  |              1 |     0.187824 | *         | ns         | ns       |
| checkerboard (halichoeres hortulanus)          | 0.011109  |              1 |     0.187824 | *         | ns         | ns       |
| golden (ctenochaetus truncates)                | 0.011109  |              1 |     0.187824 | *         | ns         | ns       |
| orange-lined (balistapus undulatus)            | 0.0121552 |              1 |     0.187824 | *         | ns         | ns       |
| bicolor (labroides bicolor)                    | 0.0125881 |              1 |     0.187824 | *         | ns         | ns       |
| sulfur (pomacentrus sulfureus)                 | 0.0125881 |              1 |     0.187824 | *         | ns         | ns       |
| threespot dascyllus (dascyllus trimaculatus)   | 0.0157039 |              1 |     0.187824 | *         | ns         | ns       |
| humpback (lutjanus gibbus)                     | 0.0157039 |              1 |     0.187824 | *         | ns         | ns       |
| barred (hemigymnus fasciatus)                  | 0.0165727 |              1 |     0.187824 | *         | ns         | ns       |
| brown tang (zebrasoma scopas)                  | 0.0188636 |              1 |     0.192409 | *         | ns         | ns       |
| regal (pygoplites diacanthus)                  | 0.0231605 |              1 |     0.194814 | *         | ns         | ns       |
| redmouth (aethaloperca rogaa)                  | 0.0253834 |              1 |     0.194814 | *         | ns         | ns       |
| goldbar (thalassoma hebraicum)                 | 0.0255898 |              1 |     0.194814 | *         | ns         | ns       |
| indian half-and-half (pycnochromis dimidiatus) | 0.0281286 |              1 |     0.194814 | *         | ns         | ns       |
| bird wrasse (gomphosus caeruleus)              | 0.0286491 |              1 |     0.194814 | *         | ns         | ns       |
| blackeye (hemigymnus melapterus)               | 0.0360726 |              1 |     0.229963 | *         | ns         | ns       |
| peacock (cephalopholis argus)                  | 0.0387742 |              1 |     0.232645 | *         | ns         | ns       |

### Family
| taxon         |   p_value |   p_value_holm |   p_value_bh | sig_raw   | sig_holm   | sig_bh   |
|:--------------|----------:|---------------:|-------------:|:----------|:-----------|:---------|
| holocentridae | 0.0131037 |       0.353799 |     0.218503 | *         | ns         | ns       |
| balistidae    | 0.0227523 |       0.59156  |     0.218503 | *         | ns         | ns       |
| pomacentridae | 0.0242781 |       0.606952 |     0.218503 | *         | ns         | ns       |
| lutjanidae    | 0.0329587 |       0.791009 |     0.222471 | *         | ns         | ns       |

## 3) Interested/Feeding nach Standort
### Feeding (Species)
Keine Daten.

### Feeding (Family)
Keine Daten.

### Interested (Species)
Keine Daten.

### Interested (Family)
Keine Daten.

## Fazit
- Videoebene: Holm-signifikant 0, BH-signifikant 0.
- Species-MaxN: Holm-signifikant 0.
- Family-MaxN: Holm-signifikant 0.
- Robust signifikant gelten nur Befunde nach Holm/BH.
