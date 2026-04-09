# One-Pager: Species Richness (cut_47min, 46 Videos)

## Kurzfazit
- Insgesamt wurden 46 Videos aus cut_47min ausgewertet.
- Species Richness wurde pro Video als Anzahl eindeutiger Taxon-Einheiten berechnet:
  1. species, wenn vorhanden
  2. sonst genus
  3. sonst naechste Hierarchiestufe (family bzw. label_name, z.B. Parrotfishes)
- Labels mit feeding=TRUE und interested=TRUE wurden ignoriert.
- Das kuerzere Sondervideo 20240108-nursery-control.csv ist in den Ergebnissen explizit markiert.

## Signifikanz (alpha = 0.05)
- Kruskal-Wallis Standort: p = 2.859e-06 -> signifikant
- Kruskal-Wallis Koeder: p = 0.1291 -> nicht signifikant
- Paarweise Standorttests (Mann-Whitney U, Holm-korrigiert):
  - nursery vs utumbi: p_holm = 3.044e-05 (signifikant)
  - milimani vs utumbi: p_holm = 0.002688 (signifikant)
  - milimani vs nursery: p_holm = 0.002934 (signifikant)

## Top 10 Videos nach Species Richness
| Rang | Video | Standort | Koeder | Richness |
|---:|---|---|---|---:|
| 1 | 20241209-utumbi-fischmix.csv | utumbi | fischmix | 63 |
| 2 | 20240516-utumbi-mackerel.csv | utumbi | mackerel | 62 |
| 3 | 20241128-utumbi-sargassum.csv | utumbi | sargassum | 61 |
| 4 | 20241124-milimani-mackerel.csv | milimani | mackerel | 59 |
| 5 | 20241110-milimani-ulva_salad.csv | milimani | ulva_salad | 57 |
| 6 | 20241129-utumbi-sargassum.csv | utumbi | sargassum | 56 |
| 7 | 20241027-utumbi-ulva_salad.csv | utumbi | ulva_salad | 55 |
| 8 | 20241112-utumbi-ulva_gutweed.csv | utumbi | ulva_gutweed | 55 |
| 9 | 20241030-utumbi-ulva_gutweed.csv | utumbi | ulva_gutweed | 54 |
| 10 | 20241115-utumbi-control.csv | utumbi | control | 54 |

## Visualisierungen
- Ranking aller 46 Videos:
  - [species_richness_ranking_all_videos.png](figures/species_richness_ranking_all_videos.png)
- Boxplot nach Standort (mit globalem p-Wert):
  - [species_richness_by_standort_boxplot.png](figures/species_richness_by_standort_boxplot.png)
- Boxplot nach Koeder (mit globalem p-Wert):
  - [species_richness_by_koeder_boxplot.png](figures/species_richness_by_koeder_boxplot.png)
- Mittelwerte je Standort x Koeder:
  - [species_richness_mean_by_standort_koeder.png](figures/species_richness_mean_by_standort_koeder.png)

## Detaildateien
- Vollstaendige Markdown-Auswertung: [species richness.md](species%20richness.md)
- Komplette CSV-Auswertung: [species_richness_complete_results.csv](species_richness_complete_results.csv)
- Alle Videos (Ranking + Metadaten): [species_richness_all_46_videos.csv](species_richness_all_46_videos.csv)
