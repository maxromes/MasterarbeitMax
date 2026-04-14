# Integrierter Koedervergleich: Taxavorkommen + Taxahaeufigkeit (MaxN)

Diese Auswertung verbindet den Artenvergleich nach Koeder (Taxa-Zusammensetzung, Vorkommen) mit der Taxa-Haeufigkeitsanalyse (MaxN je Taxon, Kruskal/Mann-Whitney).

## Ziel
Bestimmt wird, bei welchem Koeder sich Unterschiede zu anderen Koedern zeigen, sowohl in der Taxa-Zusammensetzung als auch in der Taxa-Haeufigkeit.

## Signifikanzstatus (integriert)
| standort | Taxa-Haeufigkeit: Roh-signifikante Taxa | Taxa-Haeufigkeit: Holm-signifikante Taxa | Pairwise MaxN Roh | Pairwise MaxN Holm | Komposition global p | Komposition global signifikant |
|:--|--:|--:|--:|--:|--:|:--|
| milimani | 6 | 0 | 13 | 0 | 0.0242 | True |
| utumbi | 8 | 0 | 16 | 0 | 0.0046 | True |
| nursery | 11 | 0 | 11 | 0 | 0.0016 | True |

Interpretation:
- Milimani und Utumbi zeigen signifikante globale Unterschiede in der Taxa-Zusammensetzung zwischen Koedern.
- Gleichzeitig gibt es in allen Standorten keine Holm-signifikanten taxonweisen MaxN-Effekte; die Haeufigkeitssignale bleiben trendbasiert.
- Das Muster spricht fuer breit verteilte, eher moderate Koedereffekte statt einzelner, sehr robuster Taxon-Einzeleffekte.

## Standort milimani

### Gesamtbild
- Kompositionsunterschiede ueber alle Koeder: p=0.0242 (signifikant).
- Taxa-Haeufigkeit: 6 Roh-Signale, 0 Holm-signifikante Taxa.
- Paarweise MaxN-Tests: 13 Roh-signifikante Kontraste, 0 nach Holm.

### Koederprofil je Koeder
| koeder | dominante Taxa (MaxN) | Roh-Tendenzen unter dominanten Taxa | starke Dominanz (Ratio >= 3) | koederspezifische Taxa (Vorkommen) | mittlere Jaccard-Distanz |
|:--|--:|--:|--:|--:|--:|
| control | 15 | 0 | 15 | 1 | 0.374 |
| fischmix | 32 | 3 | 27 | 1 | 0.495 |
| mackerel | 23 | 3 | 21 | 8 | 0.408 |
| sargassum | 17 | 0 | 15 | 5 | 0.401 |
| ulva_gutweed | 10 | 0 | 8 | 2 | 0.396 |
| ulva_salad | 7 | 0 | 7 | 2 | 0.377 |

### Besonderheiten je Koeder
- milimani/control: Profil moderat; koederspezifische Taxa (Vorkommen): 1; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.374; dominante Taxa nach MaxN: 15; davon Roh-Signal (p<0.05): 0; starke Dominanz (Max/Min >= 3): 15; mittleres dominantes MaxN-Niveau: 5.07
- milimani/fischmix: Profil ausgepraegt; koederspezifische Taxa (Vorkommen): 1; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.495; dominante Taxa nach MaxN: 32; davon Roh-Signal (p<0.05): 3; starke Dominanz (Max/Min >= 3): 27; mittleres dominantes MaxN-Niveau: 3.25
- milimani/mackerel: Profil ausgepraegt; koederspezifische Taxa (Vorkommen): 8; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.408; dominante Taxa nach MaxN: 23; davon Roh-Signal (p<0.05): 3; starke Dominanz (Max/Min >= 3): 21; mittleres dominantes MaxN-Niveau: 4.70
- milimani/sargassum: Profil moderat; koederspezifische Taxa (Vorkommen): 5; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.401; dominante Taxa nach MaxN: 17; davon Roh-Signal (p<0.05): 0; starke Dominanz (Max/Min >= 3): 15; mittleres dominantes MaxN-Niveau: 9.00
- milimani/ulva_gutweed: Profil schwach; koederspezifische Taxa (Vorkommen): 2; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.396; dominante Taxa nach MaxN: 10; davon Roh-Signal (p<0.05): 0; starke Dominanz (Max/Min >= 3): 8; mittleres dominantes MaxN-Niveau: 1.33
- milimani/ulva_salad: Profil schwach; koederspezifische Taxa (Vorkommen): 2; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.377; dominante Taxa nach MaxN: 7; davon Roh-Signal (p<0.05): 0; starke Dominanz (Max/Min >= 3): 7; mittleres dominantes MaxN-Niveau: 1.29

### Wichtigste Taxa-Tendenzen (roh p<0.05, nicht Holm-korrigiert)
| taxon_key | dominanter koeder | p_value | p_value_holm | ratio max/min | mean_maxn dominant | mean_maxn niedrigster koeder |
|:--|:--|--:|--:|--:|--:|--:|
| species::blue-green (chromis viridis) | fischmix | 0.0068 | 0.7118 | inf | 14.00 | 0.00 |
| species::moorish idol (zanclus cornutus) | mackerel | 0.0146 | 1.0000 | inf | 2.33 | 0.00 |
| species::red (lutjanus bohar) | fischmix | 0.0208 | 1.0000 | 32.00 | 8.00 | 0.25 |
| species::green (amblyglyphidodon indicus) | fischmix | 0.0273 | 1.0000 | 16.00 | 16.00 | 1.00 |
| species::black-backed (chaetodon melannotus) | mackerel | 0.0297 | 1.0000 | inf | 2.00 | 0.00 |
| species::ternate (chromis ternatensis) | mackerel | 0.0481 | 1.0000 | inf | 40.67 | 0.00 |

### Staerkster Vorkommenskontrast (Jaccard-Distanz)
- fischmix vs ulva_gutweed: Distanz=0.532, unique_a=11, unique_b=30.

## Standort utumbi

### Gesamtbild
- Kompositionsunterschiede ueber alle Koeder: p=0.0046 (signifikant).
- Taxa-Haeufigkeit: 8 Roh-Signale, 0 Holm-signifikante Taxa.
- Paarweise MaxN-Tests: 16 Roh-signifikante Kontraste, 0 nach Holm.

### Koederprofil je Koeder
| koeder | dominante Taxa (MaxN) | Roh-Tendenzen unter dominanten Taxa | starke Dominanz (Ratio >= 3) | koederspezifische Taxa (Vorkommen) | mittlere Jaccard-Distanz |
|:--|--:|--:|--:|--:|--:|
| control | 12 | 0 | 11 | 2 | 0.331 |
| fischmix | 29 | 5 | 26 | 3 | 0.404 |
| mackerel | 36 | 0 | 31 | 9 | 0.395 |
| sargassum | 16 | 1 | 14 | 2 | 0.336 |
| ulva_gutweed | 11 | 1 | 9 | 3 | 0.360 |
| ulva_salad | 16 | 1 | 15 | 4 | 0.354 |

### Besonderheiten je Koeder
- utumbi/control: Profil moderat; koederspezifische Taxa (Vorkommen): 2; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.331; dominante Taxa nach MaxN: 12; davon Roh-Signal (p<0.05): 0; starke Dominanz (Max/Min >= 3): 11; mittleres dominantes MaxN-Niveau: 1.65
- utumbi/fischmix: Profil ausgepraegt; koederspezifische Taxa (Vorkommen): 3; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.404; dominante Taxa nach MaxN: 29; davon Roh-Signal (p<0.05): 5; starke Dominanz (Max/Min >= 3): 26; mittleres dominantes MaxN-Niveau: 2.16
- utumbi/mackerel: Profil ausgepraegt; koederspezifische Taxa (Vorkommen): 9; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.395; dominante Taxa nach MaxN: 36; davon Roh-Signal (p<0.05): 0; starke Dominanz (Max/Min >= 3): 31; mittleres dominantes MaxN-Niveau: 6.61
- utumbi/sargassum: Profil moderat; koederspezifische Taxa (Vorkommen): 2; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.336; dominante Taxa nach MaxN: 16; davon Roh-Signal (p<0.05): 1; starke Dominanz (Max/Min >= 3): 14; mittleres dominantes MaxN-Niveau: 1.52
- utumbi/ulva_gutweed: Profil moderat; koederspezifische Taxa (Vorkommen): 3; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.360; dominante Taxa nach MaxN: 11; davon Roh-Signal (p<0.05): 1; starke Dominanz (Max/Min >= 3): 9; mittleres dominantes MaxN-Niveau: 1.42
- utumbi/ulva_salad: Profil moderat; koederspezifische Taxa (Vorkommen): 4; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.354; dominante Taxa nach MaxN: 16; davon Roh-Signal (p<0.05): 1; starke Dominanz (Max/Min >= 3): 15; mittleres dominantes MaxN-Niveau: 9.69

### Wichtigste Taxa-Tendenzen (roh p<0.05, nicht Holm-korrigiert)
| taxon_key | dominanter koeder | p_value | p_value_holm | ratio max/min | mean_maxn dominant | mean_maxn niedrigster koeder |
|:--|:--|--:|--:|--:|--:|--:|
| species::longnose (lethrinus olivaceus) | fischmix | 0.0046 | 0.5535 | inf | 1.50 | 0.00 |
| species::orange-lined (balistapus undulatus) | fischmix | 0.0215 | 1.0000 | 5.00 | 7.50 | 1.50 |
| species::brown pigmy (centropyge multispinis) | ulva_gutweed | 0.0223 | 1.0000 | 2.67 | 2.67 | 1.00 |
| species::bullethead (chlorurus sordidus) | sargassum | 0.0319 | 1.0000 | 5.00 | 5.00 | 1.00 |
| species::claudia (halichoeres claudia) | fischmix | 0.0326 | 1.0000 | inf | 2.00 | 0.00 |
| species::redmouth (aethaloperca rogaa) | fischmix | 0.0391 | 1.0000 | 2.00 | 2.00 | 1.00 |
| family_label::morays (muraenidae) | fischmix | 0.0432 | 1.0000 | inf | 1.00 | 0.00 |
| family_label::fusiliers (caesionidae) | ulva_salad | 0.0446 | 1.0000 | inf | 71.33 | 0.00 |

### Staerkster Vorkommenskontrast (Jaccard-Distanz)
- fischmix vs ulva_gutweed: Distanz=0.441, unique_a=19, unique_b=22.

## Standort nursery

### Gesamtbild
- Kompositionsunterschiede ueber alle Koeder: p=0.0016 (signifikant).
- Taxa-Haeufigkeit: 11 Roh-Signale, 0 Holm-signifikante Taxa.
- Paarweise MaxN-Tests: 11 Roh-signifikante Kontraste, 0 nach Holm.

### Koederprofil je Koeder
| koeder | dominante Taxa (MaxN) | Roh-Tendenzen unter dominanten Taxa | starke Dominanz (Ratio >= 3) | koederspezifische Taxa (Vorkommen) | mittlere Jaccard-Distanz |
|:--|--:|--:|--:|--:|--:|
| algae_strings | 26 | 3 | 24 | 6 | 0.548 |
| algaemix | 28 | 2 | 26 | 9 | 0.552 |
| control | 14 | 6 | 14 | 5 | 0.736 |
| mackerel | 31 | 0 | 31 | 19 | 0.598 |

### Besonderheiten je Koeder
- nursery/algae_strings: Profil ausgepraegt; koederspezifische Taxa (Vorkommen): 6; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.548; dominante Taxa nach MaxN: 26; davon Roh-Signal (p<0.05): 3; starke Dominanz (Max/Min >= 3): 24; mittleres dominantes MaxN-Niveau: 1.97
- nursery/algaemix: Profil ausgepraegt; koederspezifische Taxa (Vorkommen): 9; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.552; dominante Taxa nach MaxN: 28; davon Roh-Signal (p<0.05): 2; starke Dominanz (Max/Min >= 3): 26; mittleres dominantes MaxN-Niveau: 4.23
- nursery/control: Profil ausgepraegt; koederspezifische Taxa (Vorkommen): 5; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.736; dominante Taxa nach MaxN: 14; davon Roh-Signal (p<0.05): 6; starke Dominanz (Max/Min >= 3): 14; mittleres dominantes MaxN-Niveau: 2.43
- nursery/mackerel: Profil ausgepraegt; koederspezifische Taxa (Vorkommen): 19; mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: 0.598; dominante Taxa nach MaxN: 31; davon Roh-Signal (p<0.05): 0; starke Dominanz (Max/Min >= 3): 31; mittleres dominantes MaxN-Niveau: 1.84

### Wichtigste Taxa-Tendenzen (roh p<0.05, nicht Holm-korrigiert)
| taxon_key | dominanter koeder | p_value | p_value_holm | ratio max/min | mean_maxn dominant | mean_maxn niedrigster koeder |
|:--|:--|--:|--:|--:|--:|--:|
| family_label::batfishes (ephippidae) | control | 0.0186 | 1.0000 | inf | 1.00 | 0.00 |
| family_label::puffers (tetraodontidae) | control | 0.0186 | 1.0000 | inf | 2.00 | 0.00 |
| family_label::snappers (lutjanidae) | control | 0.0186 | 1.0000 | inf | 1.00 | 0.00 |
| label::stomatapoda | control | 0.0186 | 1.0000 | inf | 1.00 | 0.00 |
| species::wirenet (cantherhines pardalis) | control | 0.0186 | 1.0000 | inf | 1.00 | 0.00 |
| species::bullethead (chlorurus sordidus) | algae_strings | 0.0216 | 1.0000 | inf | 2.00 | 0.00 |
| species::blue barred (scarus ghobban) | algae_strings | 0.0349 | 1.0000 | inf | 4.00 | 0.00 |
| species::arabian monocle (scolopsis ghanam) | algaemix | 0.0353 | 1.0000 | 14.00 | 14.00 | 1.00 |

### Staerkster Vorkommenskontrast (Jaccard-Distanz)
- algaemix vs control: Distanz=0.778, unique_a=43, unique_b=13.

## Uebergreifende Einordnung (ausfuehrlich)
Die kombinierte Evidenz aus Vorkommen (Artenvergleich) und Haeufigkeit (MaxN) zeigt ein konsistentes Muster mit zwei Ebenen:
- Ebene 1, Gemeinschaft: In Milimani und Utumbi sind die globalen Kompositionsunterschiede zwischen Koedern signifikant. Das bedeutet, dass sich die Taxa-Gemeinschaft als Ganzes je nach Koeder verschiebt.
- Ebene 2, Einzeltaxa: Gleichzeitig fehlen Holm-signifikante Einzeltaxon-Effekte in der MaxN-Analyse. Das spricht gegen wenige, extrem robuste Treibertaxa und eher fuer verteilte, moderate Effekte ueber viele Taxa.

Standortuebergreifende Tendenzen:
- In allen drei Standorten gibt es Roh-Signale (p<0.05), aber keine Holm-signifikanten Taxa. Die Richtung ist damit standortuebergreifend stabil, die inferenzstatistische Sicherheit jedoch begrenzt.
- In allen Standorten treten viele Taxa mit starker Dominanz auf (Ratio Max/Min >= 3). Das zeigt klare Haeufigkeitskontraste zwischen Koedern, auch wenn diese wegen Mehrfachtests nicht als robust signifikant klassifiziert werden.
- Fischkoeder (vor allem fischmix/mackerel) tragen in Milimani und Utumbi viele dominante Taxa und viele Roh-Tendenzen; Algenkoeder liefern parallel starke Kontraste, aber oft mit weniger Roh-signifikanten dominanten Taxa.
- Nursery zeigt ebenfalls deutliche Roh-Tendenzen, aber wegen kleinerer und unausgewogener Stichproben ist die Unsicherheit hoeher; dort ist die Interpretation staerker explorativ.

## Interpretation Algenkoeder vs Fischkoeder
Zur Einordnung wurden Koeder in Gruppen zusammengefasst:
- Fischkoeder: fischmix, mackerel
- Algenkoeder: sargassum, ulva_gutweed, ulva_salad, algae_strings, algaemix

Zusammengefasste Tendenzen ueber alle Standorte:
- Dominante Taxa (MaxN): Fischkoeder 151, Algenkoeder 131. Beide Koedertypen zeigen breite taxonomische Wirkung, mit leichter Tendenz zugunsten Fischkoeder.
- Roh-Tendenzen unter dominanten Taxa: Fischkoeder 11, Algenkoeder 8. Roh-Signale sind etwas haeufiger bei Fischkoedern.
- Starke Dominanzkontraste (Ratio >= 3): Fischkoeder 136, Algenkoeder 118. Beide Koedertypen erzeugen starke Kontraste, Fischkoeder etwas ausgepraegter.

Standortspezifische Lesart des Algen-vs-Fisch-Vergleichs:
- Milimani: Fischkoeder zeigen mehr Roh-Tendenzen als Algenkoeder, bei aehnlichem mittleren Dominanzniveau. Mackerel ist zudem ein klar differenzierender Koeder in der Vorkommensebene.
- Utumbi: Fischkoeder zeigen ebenfalls mehr Roh-Tendenzen. Gleichzeitig hat ein Algenkoeder (ulva_salad) ein sehr hohes mittleres Dominanzniveau. Das spricht fuer gemischte Koederantwort.
- Nursery: Algenkoeder tragen mehrere Roh-Tendenzen, waehrend mackerel in den dominanten Taxa kaum Roh-Signale zeigt. Wegen kleiner Stichprobe ist dies als Hinweis zu lesen.

Praktische Folgerung:
- Ein einfacher Satz "Fisch ist besser als Algen" wird durch die Daten nicht getragen.
- Plausibler ist ein differenziertes Modell: Fischkoeder erzeugen haeufiger trendhafte Einzeltaxon-Reaktionen, waehrend Algenkoeder in einzelnen Kontexten sehr hohe lokale MaxN-Spitzen und klare Gemeinschaftsverschiebungen tragen.
- Fuer belastbare Aussagen pro Taxon sind mehr Replikate je Koeder notwendig, besonders um Standort*Koeder-Interaktionen robust zu testen.

## Exportdateien in diesem Ordner
- integrierte_standort_summary.csv
- integrierte_koederprofile.csv
- integrierte_overlap_paare.csv
- <standort>_top_tendenzen_taxa.csv
