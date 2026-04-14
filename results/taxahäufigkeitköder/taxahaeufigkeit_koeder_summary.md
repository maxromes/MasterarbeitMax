# Taxa-Haeufigkeit Koedervergleich (MaxN, cut_47min) - Gesamtuebersicht

Die Koedervergleiche wurden getrennt je Standort durchgefuehrt.

## Kernergebnisse
| standort   |   n_videos |   n_koeder |   n_taxa_tested |   n_significant_raw_p_lt_0_05 |   n_significant_holm_p_lt_0_05 |
|:-----------|-----------:|-----------:|----------------:|------------------------------:|-------------------------------:|
| milimani   |         17 |          6 |             104 |                             6 |                              0 |
| nursery    |         11 |          4 |              99 |                            11 |                              0 |
| utumbi     |         18 |          6 |             120 |                             8 |                              0 |

## Kurzinterpretation
- milimani: 0 signifikante Taxa (Holm) bei 104 getesteten Taxa im Koedervergleich.
- nursery: 0 signifikante Taxa (Holm) bei 99 getesteten Taxa im Koedervergleich.
- utumbi: 0 signifikante Taxa (Holm) bei 120 getesteten Taxa im Koedervergleich.

## Ausfuehrliche standortuebergreifende Interpretation
Die drei Standorte zeigen konsistent dasselbe statistische Gesamtmuster: einzelne Taxa reagieren im Rohsignal auf Koeder, aber die Effekte sind nach konservativer Mehrfachtest-Korrektur nicht robust genug, um als gesichert zu gelten. Damit ist die wahrscheinlichste Deutung, dass ein grosser Teil der beobachteten Koederunterschiede von wenigen, stark variablen Ereignissen und von der hohen Taxonzahl pro Standort getrieben wird.

Oekologisch bleibt das Muster dennoch informativ. In Milimani treten explorativ vor allem fischbasierte Koeder (fischmix/mackerel) als dominante Bedingungen fuer mehrere Taxa auf. In Utumbi ist das Bild gemischter: fischmix dominiert bei mehreren Top-Taxa, zugleich treten einzelne Maxima bei sargassum oder ulva-basierten Koedern auf. In Nursery verschiebt sich das Signal deutlich in Richtung weniger Koederstufen und geringerer Stichprobe; dort erscheinen mehrere Rohsignale mit grossen Mittelwertdifferenzen, die aber ebenfalls nicht multipeltest-robust sind.

Methodisch spricht dieses Profil fuer ein Szenario mit moderaten bis heterogenen Koedereffekten, die zwischen Taxa und Standorten nicht einheitlich stark genug sind. Fuer die Praxis heisst das: Die Daten stützen eher eine taxon- und standortabhaengige Koederantwort als einen universellen Koedereffekt, aber die Evidenz reicht in der aktuellen Stichprobe nicht fuer harte inferenzstatistische Aussagen pro Taxon.

Explorative Treiber (niedrigste Roh-p je Standort):
- milimani: species::blue-green (chromis viridis), species::moorish idol (zanclus cornutus), species::red (lutjanus bohar)
- utumbi: species::longnose (lethrinus olivaceus), species::orange-lined (balistapus undulatus), species::brown pigmy (centropyge multispinis)
- nursery: family_label::batfishes (ephippidae), family_label::puffers (tetraodontidae), family_label::snappers (lutjanidae)

## Sensitivitaetsanalyse (FDR + Vorkommensfilter)
Zusaetzlich zur Holm-Korrektur wurde eine Sensitivitaetsanalyse gerechnet mit:
- Benjamini-Hochberg (FDR) auf Standortebene
- Filter nach Mindestvorkommen pro Taxon (n_videos_present >= 2 bzw. >= 3)
- Filter nach Vorkommensrate (occ_rate >= 0.20)

### Ergebnis der Sensitivitaetsanalyse
| standort   | filter               |   n_taxa_in_filter |   n_raw_p_lt_0_05_in_filter |   n_fdr_q_lt_0_05_in_filter |
|:-----------|:---------------------|-------------------:|----------------------------:|----------------------------:|
| milimani   | none                 |                104 |                           6 |                           0 |
| milimani   | n_videos_present>=2  |                 89 |                           5 |                           0 |
| milimani   | n_videos_present>=3  |                 71 |                           5 |                           0 |
| milimani   | occ_rate>=0.20       |                 63 |                           4 |                           0 |
| nursery    | none                 |                 99 |                          11 |                           0 |
| nursery    | n_videos_present>=2  |                 69 |                           6 |                           0 |
| nursery    | n_videos_present>=3  |                 55 |                           6 |                           0 |
| nursery    | occ_rate>=0.20       |                 55 |                           6 |                           0 |
| utumbi     | none                 |                120 |                           8 |                           0 |
| utumbi     | n_videos_present>=2  |                100 |                           8 |                           0 |
| utumbi     | n_videos_present>=3  |                 85 |                           7 |                           0 |
| utumbi     | occ_rate>=0.20       |                 76 |                           6 |                           0 |

Interpretation der Sensitivitaet:
- Auch unter FDR-Korrektur (weniger konservativ als Holm) bleibt die Anzahl signifikanter Taxa in allen Standorten bei 0.
- Das Reduzieren auf haeufiger vorkommende Taxa senkt die Zahl der nominalen Treffer etwas, erzeugt aber keine robusten FDR-Signale.
- Das Nullresultat ist daher nicht nur ein Holm-Artefakt, sondern gegenueber diesen gaengigen Sensitivitaetsvarianten stabil.

Zusatzexports der Sensitivitaetsanalyse:
- taxahaeufigkeit_koeder_sensitivity_summary.csv
- <standort>/<standort>_taxa_kruskal_koeder_tests_sensitivity.csv

## Berichte pro Standort
- milimani/taxahaeufigkeit_koeder_milimani.md
- nursery/taxahaeufigkeit_koeder_nursery.md
- utumbi/taxahaeufigkeit_koeder_utumbi.md

## Wichtige Exportdateien pro Standort
- <standort>_taxa_kruskal_koeder_tests.csv
- <standort>_taxon_maxn_by_koeder_summary.csv
- <standort>_taxa_pairwise_mannwhitney_tests.csv
- <standort>_taxa_significant_koeder_differences.csv
- <standort>_taxa_similar_frequency_all_koeder.csv
