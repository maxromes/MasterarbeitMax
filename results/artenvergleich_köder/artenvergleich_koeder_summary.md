# Artenvergleich Koeder (cut_47min) - Gesamtuebersicht

Die Koederanalysen wurden getrennt nach Standort gerechnet, da Milimani, Utumbi und Nursery nicht als Replikate behandelt werden.

## Kernergebnisse
| standort   |   n_videos |   n_koeder |   taxa_in_all_koeder | top_koederpaar            |   top_jaccard |   max_koederspezifische_taxa |   composition_p_value_global | composition_significant_0_05   |
|:-----------|-----------:|-----------:|---------------------:|:--------------------------|--------------:|-----------------------------:|-----------------------------:|:-------------------------------|
| milimani   |         17 |          6 |                   31 | control vs ulva_gutweed   |      0.697368 |                            8 |                   0.0241952  | True                           |
| utumbi     |         18 |          6 |                   43 | control vs sargassum      |      0.764045 |                            9 |                   0.00459908 | True                           |
| nursery    |         11 |          4 |                   16 | algae_strings vs algaemix |      0.661765 |                           19 |                   0.00159968 | True                           |

## Kurzinterpretation
- milimani: Globaler Unterschied der Taxa-Zusammensetzung zwischen Koedern signifikant (PERMANOVA p=0.0242).
- utumbi: Globaler Unterschied der Taxa-Zusammensetzung zwischen Koedern signifikant (PERMANOVA p=0.004599).
- nursery: Globaler Unterschied der Taxa-Zusammensetzung zwischen Koedern signifikant (PERMANOVA p=0.0016).
- In den Standorten mit globaler Signifikanz sind nach Holm-Korrektur keine einzelnen Koederpaare signifikant; die Unterschiede zeigen sich primär als Gesamteffekt ueber alle Koeder.

## Zusatzanalyse: Fischkoeder vs Algenkoeder

Fragestellung:
- Unterscheidet sich die Taxa-Zusammensetzung zwischen einer zusammengefassten Fischkoedergruppe (`fischmix` + `mackerel`) und einer zusammengefassten Algenkoedergruppe (`ulva_gutweed` + `sargassum` + `ulva_salad`)?

Methodik:
- PERMANOVA mit Jaccard-Distanzen auf Videoebene (Presence/Absence), analog zur Hauptanalyse.
- Vergleich nur fuer Milimani und Utumbi (in Nursery fehlt `fischmix`).

Ergebnisse:
| standort | n_videos | n_fischkoeder | n_algenkoeder | pseudo_f | p_value | signifikant_0_05 |
|:--|--:|--:|--:|--:|--:|:--|
| milimani | 14 | 4 | 10 | 1.8303 | 0.007998 | True |
| utumbi | 14 | 5 | 9 | 1.7566 | 0.004399 | True |

Interpretation:
- Der gruppierte Vergleich ist in beiden Standorten signifikant.
- Damit zeigt sich, dass sich fischbasierte Koeder und algenbasierte Koeder in der Taxa-Zusammensetzung klar unterscheiden, obwohl einzelne paarweise Koedervergleiche nach Holm nicht signifikant waren.

Exportdatei:
- fishmix_mackerel_vs_algae_permanova.csv

## Berichte pro Standort
- milimani/artenvergleich_koeder_milimani.md
- nursery/artenvergleich_koeder_nursery.md
- utumbi/artenvergleich_koeder_utumbi.md

## Wichtige Exportdateien pro Standort
- <standort>_pairwise_koeder_overlap.csv
- <standort>_taxa_presence_by_koeder.csv
- <standort>_composition_permanova_global.csv
- <standort>_composition_permanova_pairwise.csv
- <standort>_koederspezifische_taxa_long.csv
- <standort>_taxa_lists_by_koeder.csv

## Zusaetzliche standortuebergreifende Exportdatei
- fishmix_mackerel_vs_algae_permanova.csv
