# Standortvergleich (cut_47min)

## Kurzfazit
Standorte **nicht** als direkte Replikate behandeln (signifikante Standorteffekte vorhanden).

## Datengrundlage
- Anzahl Videos gesamt: 46
- Standorte: Utumbi, Milimani, Nursery
- Basis: normalized_reports/cut_47min
- Metrik pro Video: Species Richness (unique Taxa; feeding/interested ausgeschlossen)

## Schwerpunktvergleiche
- utumbi vs milimani: p=0.001338, Holm-p=0.002675, signifikant(Holm)=True, Delta=0.637
- utumbi vs nursery: p=1.02e-05, Holm-p=3.059e-05, signifikant(Holm)=True, Delta=0.995
- milimani vs nursery: p=0.001848, Holm-p=0.002675, signifikant(Holm)=True, Delta=0.711

## Köder-kontrollierter Test (Utumbi vs Milimani)
- Stratifizierter Permutationstest (Utumbi vs Milimani | by koeder): p=0.0008, signifikant=True, Mittelwertdifferenz (Utumbi-Milimani)=8.196
- Gemeinsame Köder: control, fischmix, mackerel, sargassum, ulva_gutweed, ulva_salad

## Statistik-Tabellen
### Deskriptive Statistik je Standort
| standort   |   n |    mean |   median |     std |   min |   max |
|:-----------|----:|--------:|---------:|--------:|------:|------:|
| milimani   |  17 | 44.4706 |       45 | 7.22078 |    31 |    57 |
| nursery    |  11 | 35.6364 |       35 | 4.71747 |    29 |    43 |
| utumbi     |  18 | 52.6667 |       53 | 5.12204 |    43 |    61 |

### Globaltest über alle 3 Standorte
| test                                         | groups                    |   h_stat |    p_value | significant_0_05   | sig_label   |
|:---------------------------------------------|:--------------------------|---------:|-----------:|:-------------------|:------------|
| Kruskal-Wallis (species_richness ~ standort) | utumbi, milimani, nursery |  25.9593 | 2.3068e-06 | True               | ***         |

### Paarweise Standorttests
| site_a   | site_b   |   n_a |   n_b |   median_a |   median_b |   mean_a |   mean_b |   mean_diff_a_minus_b |   u_stat |    p_value |   cliffs_delta |   p_value_holm | significant_0_05   | significant_0_05_holm   | sig_label_raw   | sig_label_holm   |
|:---------|:---------|------:|------:|-----------:|-----------:|---------:|---------:|----------------------:|---------:|-----------:|---------------:|---------------:|:-------------------|:------------------------|:----------------|:-----------------|
| utumbi   | nursery  |    18 |    11 |         53 |         35 |  52.6667 |  35.6364 |              17.0303  |    197.5 | 1.0198e-05 |       0.994949 |     3.0594e-05 | True               | True                    | ***             | ***              |
| utumbi   | milimani |    18 |    17 |         53 |         45 |  52.6667 |  44.4706 |               8.19608 |    250.5 | 0.00133767 |       0.637255 |     0.00267534 | True               | True                    | **              | **               |
| milimani | nursery  |    17 |    11 |         45 |         35 |  44.4706 |  35.6364 |               8.83422 |    160   | 0.00184804 |       0.71123  |     0.00267534 | True               | True                    | **              | **               |

### Artenpool-Überlappung
| site_a   | site_b   |   n_taxa_a |   n_taxa_b |   intersection_taxa |   union_taxa |   jaccard_similarity |   jaccard_distance |   unique_a |   unique_b |
|:---------|:---------|-----------:|-----------:|--------------------:|-------------:|---------------------:|-------------------:|-----------:|-----------:|
| utumbi   | milimani |        116 |        102 |                  86 |          132 |             0.651515 |           0.348485 |         30 |         16 |
| utumbi   | nursery  |        116 |         95 |                  61 |          150 |             0.406667 |           0.593333 |         55 |         34 |
| milimani | nursery  |        102 |         95 |                  62 |          135 |             0.459259 |           0.540741 |         40 |         33 |

## Grafiken
- figures/species_richness_by_site_boxplot.png
- figures/site_pool_jaccard_heatmap.png
- figures/site_overlap_pcoa_jaccard.png
- figures/shared_unique_taxa_pairwise.png
- figures/site_distance_dendrogram.png

## Interpretation zur Replikat-Frage
- Wenn global oder paarweise (Holm-korrigiert) signifikant: Standorteffekt spricht gegen Replikatannahme.
- Wenn nicht signifikant, aber Überlappung gering (niedriger Jaccard) oder klare Cluster in PCoA: ebenfalls Vorsicht bei Replikatannahme.
