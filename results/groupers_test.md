# Groupers-Test (ohne feeding/interested-Filter)

Fragestellung:
Kommt `family_label::groupers (serranidae)` bei den Koedern `mackerel` und `fischmix` haeufiger vor als bei den anderen Koedern?

Datengrundlage:
- Quelle: `results/taxahäufigkeitköder/*/*_taxon_maxn_by_koeder_summary.csv`
- Taxon: `family_label::groupers (serranidae)`
- Vergleichsmetrik: Mean MaxN und Occurrence Rate
- Signifikanz pro Standort: Kruskal-Wallis aus `*_taxa_kruskal_koeder_tests.csv`

## Standortspezifische Ergebnisse

### Milimani
| koeder | n_videos | n_present | occurrence_rate | mean_maxn | median_maxn | max_maxn |
|:--|--:|--:|--:|--:|--:|--:|
| fischmix | 1 | 1 | 1.000 | 3.000 | 3.0 | 3.0 |
| sargassum | 3 | 3 | 1.000 | 1.667 | 2.0 | 2.0 |
| ulva_salad | 4 | 2 | 0.500 | 1.000 | 0.5 | 3.0 |
| mackerel | 3 | 2 | 0.667 | 1.000 | 1.0 | 2.0 |
| control | 3 | 2 | 0.667 | 0.667 | 1.0 | 1.0 |
| ulva_gutweed | 3 | 2 | 0.667 | 0.667 | 1.0 | 1.0 |

Vergleich `mackerel+fischmix` vs andere (video-gewichtet):
- target_mean = 1.500 vs others_mean = 1.000
- target_occ = 0.750 vs others_occ = 0.692

Signifikanz:
- Kruskal p = 0.394305
- Holm p = 1.000000
- Dominanter Koeder (Mean): fischmix
- Niedrigster Koeder (Mean): control

Interpretation:
- Tendenz zu hoeheren Werten bei `mackerel/fischmix`, aber nicht signifikant.
- `fischmix` basiert nur auf einem Video und ist daher vorsichtig zu interpretieren.

### Utumbi
| koeder | n_videos | n_present | occurrence_rate | mean_maxn | median_maxn | max_maxn |
|:--|--:|--:|--:|--:|--:|--:|
| mackerel | 3 | 3 | 1.000 | 2.333 | 2.0 | 3.0 |
| fischmix | 2 | 2 | 1.000 | 2.000 | 2.0 | 3.0 |
| control | 4 | 4 | 1.000 | 1.500 | 1.5 | 2.0 |
| sargassum | 3 | 3 | 1.000 | 1.333 | 1.0 | 2.0 |
| ulva_gutweed | 3 | 3 | 1.000 | 1.333 | 1.0 | 2.0 |
| ulva_salad | 3 | 3 | 1.000 | 1.333 | 1.0 | 2.0 |

Vergleich `mackerel+fischmix` vs andere (video-gewichtet):
- target_mean = 2.200 vs others_mean = 1.385
- target_occ = 1.000 vs others_occ = 1.000

Signifikanz:
- Kruskal p = 0.437712
- Holm p = 1.000000
- Dominanter Koeder (Mean): mackerel
- Niedrigster Koeder (Mean): sargassum

Interpretation:
- Klare Tendenz zu hoeherem Mean MaxN bei `mackerel/fischmix`.
- Auftretensrate ist in allen Koedern gleich hoch (1.0), der Unterschied liegt v. a. in der Hoehe der MaxN-Werte.
- Nicht signifikant.

### Nursery
| koeder | n_videos | n_present | occurrence_rate | mean_maxn | median_maxn | max_maxn |
|:--|--:|--:|--:|--:|--:|--:|
| mackerel | 4 | 2 | 0.500 | 1.000 | 0.5 | 3.0 |
| algaemix | 3 | 2 | 0.667 | 0.667 | 1.0 | 1.0 |
| algae_strings | 3 | 0 | 0.000 | 0.000 | 0.0 | 0.0 |
| control | 1 | 0 | 0.000 | 0.000 | 0.0 | 0.0 |

Vergleich `mackerel+fischmix` vs andere (video-gewichtet):
- target_mean = 1.000 vs others_mean = 0.286
- target_occ = 0.500 vs others_occ = 0.286

Signifikanz:
- Kruskal p = 0.366635
- Holm p = 1.000000
- Dominanter Koeder (Mean): mackerel
- Niedrigster Koeder (Mean): algae_strings

Interpretation:
- Tendenz zugunsten `mackerel`.
- Nicht signifikant.
- `fischmix` ist in Nursery nicht vorhanden.

## Standortuebergreifender Vergleich

Gepoolt (video-gewichtet ueber alle Standorte/Bait-Kombinationen):
- target_mean (`mackerel+fischmix`) = 1.615
- others_mean = 1.000
- target_occ = 0.769
- others_occ = 0.727

Interpretation:
- Standortuebergreifend zeigt sich eine konsistente Tendenz, dass Groupers bei `mackerel/fischmix` haeufiger bzw. mit hoeherem MaxN auftreten.
- Diese Tendenz ist in den standortspezifischen Tests jedoch nicht signifikant.

## Fazit
- Ja, es gibt eine konsistente Tendenz zugunsten `mackerel/fischmix`.
- Nein, die Unterschiede sind (pro Standort) statistisch nicht signifikant.
