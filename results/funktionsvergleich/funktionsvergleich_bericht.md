# Funktionsvergleich: Koederunterschiede in Milimani und Utumbi

Datengrundlage: normalized_reports/cut_47min/Annotation_reports_coral_reef

Verwendete Korrekturen fuer multiples Testen: Holm und Benjamini-Hochberg (FDR/BH).

## Getestete Zusammenfassungen und Kombinationen
Die folgenden Gruppen wurden explizit als zusammengesetzte Features getestet:
| composite_group                      | beschreibung                                                                                                         |
|:-------------------------------------|:---------------------------------------------------------------------------------------------------------------------|
| algae_oriented_diet_mode             | Alle Taxa mit Algenbezug gemaess Word-Diet-Mapping                                                                   |
| bioeroder_set                        | Bioeroder/Hard-substrate feeder: Scaridae + Balistidae                                                               |
| fish_oriented_diet_mode              | Alle Taxa mit Fischbezug gemaess Word-Diet-Mapping                                                                   |
| herbivore_core_families              | Kern-Herbivore (Familien): Siganidae, Acanthuridae, Scaridae, Blenniidae                                             |
| herbivore_extended_with_damselfishes | Erweiterte Herbivore: rabbitfishes/surgeonfishes/parrotfishes/blennies + small_ovals_damselfishes                    |
| invertebrate_oriented_diet_mode      | Alle Taxa mit Wirbellosenbezug gemaess Word-Diet-Mapping                                                             |
| invertivore_benthic_core             | Benthos-Invertivore: Mullidae, Haemulidae, Balistidae, Diodontidae, Nemipteridae, Lethrinidae                        |
| invertivore_general                  | Breite Invertivore (Word): goatfishes, sweetlips, triggerfishes, porcupinefishes, coral_breams, emperors, hawkfishes |
| nocturnal_predator_mixture           | Nachtaktive Jaeger-Mischung: eels, snappers, bigeyes, soldier_squirrelfishes                                         |
| omnivore_box_puffer_file             | Omnivore/Tendenz-gemischt: Ostraciidae, Tetraodontidae, Monacanthidae                                                |
| piscivore_active_hunters             | Aktive/ambush Fischjaeger: groupers_large, eels, snappers, barracudas, trumpetfishes, cornetfishes, jacks_trevallies |
| piscivore_core_families              | Kern-Piscivore (Familien): Serranidae, Lutjanidae, Muraenidae, Sphyraenidae, Aulostomidae, Fistulariidae             |
| planktivore_core                     | Planktivore Kernfamilien: Apogonidae, Caesionidae, Pempheridae (+ Anthias als Word-Gruppe)                           |
| plankton_oriented_diet_mode          | Alle Taxa mit Planktonbezug gemaess Word-Diet-Mapping                                                                |
| predator_reef_core                   | Riff-Praedatoren (familienbasiert): Lutjanidae, Serranidae, Muraenidae, Sphyraenidae, Synanceiidae, Antennariidae    |
| snappers_groupers_combo              | Kombination Lutjanidae + Serranidae (Snappers + Groupers)                                                            |
| wrasses_trigger_combo                | Kombination Labridae + Balistidae (Wrasses + Triggerfishes)                                                          |

Zusatzebenen (ebenfalls getestet): diet, word_group, family, genus, unspecific.

## Signifikanz-Uebersicht
Globaltest ueber Koeder:
| site     | feature_type    |   n_tested |   n_sig_holm |   n_sig_bh |
|:---------|:----------------|-----------:|-------------:|-----------:|
| milimani | composite_group |         16 |            0 |          0 |
| milimani | diet            |          4 |            0 |          0 |
| milimani | family          |         22 |            0 |          0 |
| milimani | genus           |         47 |            0 |          0 |
| milimani | unspecific      |         12 |            0 |          0 |
| milimani | word_group      |         19 |            0 |          0 |
| utumbi   | composite_group |         17 |            0 |          0 |
| utumbi   | diet            |          4 |            0 |          0 |
| utumbi   | family          |         25 |            0 |          0 |
| utumbi   | genus           |         54 |            0 |          0 |
| utumbi   | unspecific      |         14 |            0 |          0 |
| utumbi   | word_group      |         23 |            0 |          0 |

Fish-vs-Algae-Test:
| site     | feature_type    |   n_tested |   n_sig_holm |   n_sig_bh |
|:---------|:----------------|-----------:|-------------:|-----------:|
| milimani | composite_group |         16 |            1 |          1 |
| milimani | diet            |          4 |            0 |          0 |
| milimani | family          |         22 |            1 |          1 |
| milimani | genus           |         47 |            0 |          0 |
| milimani | unspecific      |         12 |            1 |          1 |
| milimani | word_group      |         19 |            1 |          1 |
| utumbi   | composite_group |         17 |            0 |          9 |
| utumbi   | diet            |          4 |            2 |          2 |
| utumbi   | family          |         25 |            0 |          3 |
| utumbi   | genus           |         54 |            0 |          0 |
| utumbi   | unspecific      |         14 |            2 |          3 |
| utumbi   | word_group      |         23 |            0 |          3 |

## Signifikante Gruppen (Globaltest ueber Koeder)
Keine Gruppe erreicht Signifikanz nach Holm/BH.

Top explorative Signale (roh p):
| site     | feature_type    | feature                     |   p_value |   p_value_holm |   p_value_bh | dominant_bait   |   mean_diff_max_minus_min |
|:---------|:----------------|:----------------------------|----------:|---------------:|-------------:|:----------------|--------------------------:|
| utumbi   | composite_group | wrasses_trigger_combo       | 0.0136261 |       0.231643 |     0.119947 | fischmix        |                   6.16667 |
| milimani | word_group      | moorish_idol                | 0.0145643 |       0.276722 |     0.197844 | mackerel        |                   2.33333 |
| milimani | family          | zanclidae                   | 0.0145643 |       0.320415 |     0.229082 | mackerel        |                   2.33333 |
| milimani | genus           | zanclus                     | 0.0145643 |       0.684524 |     0.42723  | mackerel        |                   2.33333 |
| utumbi   | word_group      | wrasses                     | 0.0191135 |       0.439611 |     0.127545 | fischmix        |                   5.5     |
| utumbi   | family          | labridae                    | 0.0191135 |       0.477838 |     0.138636 | fischmix        |                   5.5     |
| utumbi   | unspecific      | wrasses                     | 0.0191135 |       0.267589 |     0.129394 | fischmix        |                   5.5     |
| milimani | word_group      | snappers                    | 0.0208257 |       0.374862 |     0.197844 | fischmix        |                   7.75    |
| milimani | family          | lutjanidae                  | 0.0208257 |       0.437339 |     0.229082 | fischmix        |                   7.75    |
| milimani | genus           | lutjanus                    | 0.0208257 |       0.957981 |     0.42723  | fischmix        |                   7.75    |
| milimani | composite_group | nocturnal_predator_mixture  | 0.0208257 |       0.333211 |     0.290541 | fischmix        |                   7.75    |
| utumbi   | word_group      | triggerfishes               | 0.0214871 |       0.472717 |     0.127545 | fischmix        |                   6       |
| utumbi   | family          | balistidae                  | 0.0214871 |       0.515691 |     0.138636 | fischmix        |                   6       |
| utumbi   | genus           | balistapus                  | 0.0214871 |       1        |     0.422475 | fischmix        |                   6       |
| utumbi   | genus           | centropyge                  | 0.0222947 |       1        |     0.422475 | ulva_gutweed    |                   1.66667 |
| utumbi   | genus           | thalassoma                  | 0.0237071 |       1        |     0.422475 | fischmix        |                   5.83333 |
| utumbi   | word_group      | fusiliers                   | 0.0251106 |       0.527323 |     0.127545 | ulva_salad      |                  74.3333  |
| utumbi   | family          | caesionidae                 | 0.0251106 |       0.577545 |     0.138636 | ulva_salad      |                  74.3333  |
| utumbi   | unspecific      | slender schoolers/colourful | 0.0251106 |       0.326438 |     0.129394 | ulva_salad      |                  74.3333  |
| utumbi   | composite_group | planktivore_core            | 0.0251106 |       0.40177  |     0.119947 | ulva_salad      |                  74.3333  |

## Signifikante paarweise Koederunterschiede
Keine paarweisen Vergleiche signifikant nach Holm/BH (innerhalb Feature).

## Signifikante Fish-vs-Algae-Unterschiede
| site     | feature_type    | feature                         |    p_value |   p_value_holm |   p_value_bh | higher_side   |   cliffs_delta_fish_minus_algae |
|:---------|:----------------|:--------------------------------|-----------:|---------------:|-------------:|:--------------|--------------------------------:|
| milimani | unspecific      | wrasses                         | 0.00171164 |      0.0205397 |    0.0205397 | fish          |                        0.975    |
| utumbi   | unspecific      | eels                            | 0.00335893 |      0.047025  |    0.0256886 | fish          |                        0.8      |
| utumbi   | unspecific      | wrasses                         | 0.00366979 |      0.0477073 |    0.0256886 | fish          |                        0.977778 |
| milimani | composite_group | wrasses_trigger_combo           | 0.00171164 |      0.0273862 |    0.0273862 | fish          |                        0.975    |
| utumbi   | word_group      | triggerfishes                   | 0.00311526 |      0.071651  |    0.0281351 | fish          |                        0.933333 |
| utumbi   | word_group      | eels                            | 0.00335893 |      0.0738964 |    0.0281351 | fish          |                        0.8      |
| utumbi   | word_group      | wrasses                         | 0.00366979 |      0.0770657 |    0.0281351 | fish          |                        0.977778 |
| utumbi   | diet            | invertebrates                   | 0.0105044  |      0.0420177 |    0.0289453 | fish          |                        0.866667 |
| utumbi   | diet            | fish                            | 0.0144726  |      0.0434179 |    0.0289453 | fish          |                        0.711111 |
| utumbi   | family          | balistidae                      | 0.00311526 |      0.0778815 |    0.0305816 | fish          |                        0.933333 |
| utumbi   | family          | muraenidae                      | 0.00335893 |      0.0806142 |    0.0305816 | fish          |                        0.8      |
| utumbi   | family          | labridae                        | 0.00366979 |      0.0844052 |    0.0305816 | fish          |                        0.977778 |
| utumbi   | composite_group | wrasses_trigger_combo           | 0.00308173 |      0.0523894 |    0.0314646 | fish          |                        1        |
| utumbi   | composite_group | snappers_groupers_combo         | 0.00555257 |      0.0888412 |    0.0314646 | fish          |                        0.844444 |
| utumbi   | composite_group | predator_reef_core              | 0.00555257 |      0.0888412 |    0.0314646 | fish          |                        0.844444 |
| milimani | word_group      | wrasses                         | 0.00171164 |      0.0325211 |    0.0325211 | fish          |                        0.975    |
| utumbi   | composite_group | invertebrate_oriented_diet_mode | 0.0105044  |      0.147062  |    0.0342091 | fish          |                        0.866667 |
| utumbi   | composite_group | invertivore_general             | 0.0120738  |      0.156959  |    0.0342091 | fish          |                        0.822222 |
| utumbi   | composite_group | invertivore_benthic_core        | 0.0120738  |      0.156959  |    0.0342091 | fish          |                        0.822222 |
| utumbi   | composite_group | fish_oriented_diet_mode         | 0.0144726  |      0.159199  |    0.0351479 | fish          |                        0.711111 |
| utumbi   | composite_group | piscivore_active_hunters        | 0.0186225  |      0.186225  |    0.0351758 | fish          |                        0.711111 |
| utumbi   | composite_group | piscivore_core_families         | 0.0186225  |      0.186225  |    0.0351758 | fish          |                        0.711111 |
| milimani | family          | labridae                        | 0.00171164 |      0.037656  |    0.037656  | fish          |                        0.975    |
| utumbi   | unspecific      | odd-shaped swimmers             | 0.00999977 |      0.119997  |    0.0466656 | fish          |                        0.822222 |

## Zusatztest: Gruppen mit Algenvorteil

Fragestellung: Gibt es Gruppen/Familien/Genera/Komposita, die bei algenbasierten Koedern signifikant haeufiger sind als bei fischbasierten Koedern?

Getestete Basis:
- Alle Fish-vs-Algae-Tests aus Milimani und Utumbi ueber die Ebenen `diet`, `word_group`, `family`, `genus`, `unspecific` und `composite_group`.
- Gesamtzahl Tests: 257
- Davon mit `higher_side = algae`: 115

Signifikanz (korrigiert):
- Holm-signifikant (`p_value_holm < 0.05`) mit Algenvorteil: 0
- BH/FDR-signifikant (`p_value_bh < 0.05`) mit Algenvorteil: 0

Explorative (unkorrigierte) Algen-Signale, nicht signifikant nach Korrektur:

| site   | feature_type   | feature      | p_value | p_value_holm | p_value_bh | cliffs_delta_fish_minus_algae |
|:-------|:---------------|:-------------|--------:|-------------:|-----------:|-------------------------------:|
| utumbi | genus          | chlorurus    | 0.0065  | 0.3403       | 0.1178     | -0.8889 |
| utumbi | word_group     | moorish_idol | 0.0514  | 0.9764       | 0.2364     | -0.5778 |
| utumbi | family         | zanclidae    | 0.0514  | 1.0000       | 0.2570     | -0.5778 |
| utumbi | genus          | zanclus      | 0.0514  | 1.0000       | 0.3158     | -0.5778 |

Interpretation:
- Unter strenger Mehrfachtest-Kontrolle zeigen sich in diesem Datensatz keine robusten Gruppen mit klarer Algen-Praeferenz.
- Der stabile Signaturblock liegt weiterhin auf der Fisch-Seite (mehrere wrasses/trigger/eels-nahe Gruppen in Utumbi und Wrasses in Milimani).
- Algen-nahe Hinweise sind momentan nur explorativ (vor allem auf Genus-Ebene wie `chlorurus`) und sollten als Hypothesen fuer gezielte Folgeanalysen verstanden werden, nicht als gesicherte Effekte.
- Fuer die Thesis bedeutet das: Signifikante Unterschiede sind vorhanden, aber vor allem als Fischkoeder-Effekte; ein gleich starkes, korrigiert-signifikantes Algenkoeder-Profil wurde hier nicht gefunden.

## Restliche Ergebnisse und Gesamtinterpretation

### 1) Standortmuster (korrigierte Signifikanz)

- Insgesamt wurden 24 BH-signifikante Fish-vs-Algae-Effekte gefunden; alle mit Vorteil fuer fischbasierte Koeder.
- Milimani: 4 BH-signifikante Effekte (1x composite_group, 1x family, 1x word_group, 1x unspecific), jeweils rund um Wrasses/Labridae.
- Utumbi: 20 BH-signifikante Effekte (9x composite_group, 2x diet, 3x family, 3x word_group, 3x unspecific), mit breiterem funktionellem Signal.

Interpretation:
- Milimani zeigt ein fokussiertes Muster (hauptsaechlich Wrasses-basiert).
- Utumbi zeigt ein diverseres trophisches Antwortmuster auf fischbasierte Koeder (Wrasses, Triggerfishes, Eels sowie mehrere zusammengesetzte Praedatoren-/Invertivoren-Gruppen).

### 2) Restliche globale Ergebnisse ueber alle Koeder (explorativ)

- Trotz vieler Tests gab es global (Kruskal ueber alle Koeder je Feature) keine Holm/BH-signifikanten Treffer.
- Wiederkehrende Roh-p-Signale:
	- Milimani: moorish_idol/zanclidae/zanclus sowie snappers/lutjanidae/lutjanus und nocturnal_predator_mixture.
	- Utumbi: wrasses/labridae, triggerfishes/balistidae sowie planktivore_core/fusiliers/caesionidae.

Interpretation:
- Die Unterschiede sind eher als gerichtete Fish-vs-Algae-Kontraste sichtbar als als robuste Mehrgruppen-Unterschiede ueber alle Koeder gleichzeitig.
- Das spricht fuer klare Achsen in der Koederwirkung (fischbasiert vs algenbasiert), aber weniger fuer durchgehend stabile Rangfolgen zwischen allen einzelnen Koedern.

### 3) Effektstaerken (Cliff's Delta) der robusten Signale

- Sehr starke Effekte (|delta| nahe 1):
  - utumbi / wrasses_trigger_combo: delta = 1.00 (fish > algae)
  - utumbi / wrasses (family/word_group/unspecific): delta ca. 0.98
  - milimani / wrasses (family/word_group/unspecific): delta = 0.975
- Weitere starke Effekte in Utumbi:
  - triggerfishes/balistidae: delta ca. 0.93
  - snappers_groupers_combo und predator_reef_core: delta ca. 0.84
  - eels/muraenidae: delta = 0.80

Interpretation:
- Die signifikanten Fish-vs-Algae-Effekte sind nicht nur statistisch, sondern auch biologisch deutlich (grosse Effektstaerken).
- Die Ergebnisse sind damit inhaltlich konsistent mit einem staerkeren Anlocken raeuberischer bzw. opportunistisch-karnivorer Gruppen durch fischbasierte Koeder.

### 4) Paarweise Koedervergleiche innerhalb Features

- Nach Holm/BH gab es keine signifikanten paarweisen Koedervergleiche innerhalb einzelner Features.

Interpretation:
- Die Daten reichen aus, um den breiten Kontrast fish vs algae zu zeigen, aber nicht fuer fein aufgeloeste, mehrfachkorrigierte Unterschiede zwischen einzelnen Koederpaaren.
- Fuer die Praxis ist daher der aggregierte Fish-vs-Algae-Vergleich derzeit die robusteste Aussageebene.

### 5) Einordnung fuer die Thesis

- Hauptbefund: Der funktionelle Unterschied liegt klar auf der Fischseite; robuste Algenvorteile fehlen nach Korrektur.
- Robusteste Markergruppen:
  - Wrasses/Labridae (beide Standorte)
  - Triggerfishes/Balistidae (v. a. Utumbi)
  - Eels/Muraenidae (Utumbi)
  - Zusammengesetzte Praedatoren-Gruppen (Utumbi)
- Konsequenz fuer die Darstellung:
  - Globaltest: keine korrigierten Treffer ueber alle Koeder.
  - Fish-vs-Algae: mehrere robuste, biologisch starke Effekte zugunsten fischbasierter Koeder.
  - Algenvorteile: nur explorative Hinweise, keine robusten Nachweise.

### 6) Spezifisch: Rabbitfishes und Unicornfishes

Rabbitfishes wurden ueber `rabbitfishes` (word_group), `siganidae` (family) und `siganus` (genus) betrachtet.
Unicornfishes wurden primär ueber `naso` (genus) und ergaenzend ueber `surgeonfishes` bzw. `acanthuridae` betrachtet.

Fish-vs-Algae (Milimani):
- Rabbitfishes (`rabbitfishes` / `siganidae`): mean fish = 1.5, mean algae = 1.4, p = 0.9282, p_holm = 1.0000, p_bh = 0.9943.
- Unicornfishes (`naso`): mean fish = 2.5, mean algae = 1.3, p = 0.2076, p_holm = 1.0000, p_bh = 0.4879.
- Surgeonfishes/Acanthuridae (als breiter Unicorn-Kontext): mean fish = 28.75, mean algae = 5.00, p = 0.1904, p_holm = 1.0000, p_bh = 0.5169.

Fish-vs-Algae (Utumbi):
- Rabbitfishes (`rabbitfishes` / `siganidae`): mean fish = 0.8, mean algae = 1.6667, p = 0.5690, p_holm = 1.0000, p_bh = 0.7698.
- Unicornfishes (`naso`): mean fish = 3.2, mean algae = 1.2222, p = 0.5336, p_holm = 1.0000, p_bh = 0.8004.
- Surgeonfishes/Acanthuridae (als breiter Unicorn-Kontext): mean fish = 5.00, mean algae = 2.8889, p = 0.3607, p_holm = 1.0000, p_bh = 0.5185.

Globaltest ueber alle Koeder (Kruskal, explorativ):
- Rabbitfishes/Siganidae: Milimani p = 0.6183, Utumbi p = 0.0999 (beides nicht signifikant nach Holm/BH).
- Unicornfishes (`naso`): Milimani p = 0.1018, Utumbi p = 0.4052 (nicht signifikant).
- Surgeonfishes/Acanthuridae: Milimani p = 0.0837, Utumbi p = 0.6091 (nicht signifikant).

Interpretation:
- Fuer Rabbitfishes gibt es in beiden Standorten keinen robusten, korrigiert-signifikanten Koedereffekt.
- Fuer Unicornfishes (`naso`) ebenfalls keinen robusten, korrigiert-signifikanten Koedereffekt.
- Die beobachteten Richtungen sind nur tendenziell: Rabbitfishes in Utumbi leicht algennah, Unicorn-/Surgeonfishes eher fischnah.
- Diese Signale sollten als Hypothesen fuer gezielte Folgeanalysen interpretiert werden (z. B. groessere Stichprobe oder standortspezifische Submodelle), nicht als gesicherte Effekte.