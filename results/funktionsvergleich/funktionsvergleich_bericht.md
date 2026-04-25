# Funktionsvergleich: Koederunterschiede in Milimani, Utumbi und Nursery

Datengrundlage: normalized_reports/cut_47min/Annotation_reports_coral_reef und normalized_reports/cut_47min/Annotation_reports_Nursery

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
| nursery  | composite_group |         17 |            0 |          0 |
| nursery  | diet            |          4 |            0 |          0 |
| nursery  | family          |         24 |            0 |          0 |
| nursery  | genus           |         36 |            0 |          0 |
| nursery  | unspecific      |         13 |            0 |          0 |
| nursery  | word_group      |         23 |            0 |          0 |
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
| nursery  | composite_group |         17 |            0 |          0 |
| nursery  | diet            |          4 |            0 |          0 |
| nursery  | family          |         24 |            0 |          0 |
| nursery  | genus           |         36 |            0 |          0 |
| nursery  | unspecific      |         13 |            0 |          0 |
| nursery  | word_group      |         23 |            0 |          0 |
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
| nursery  | genus           | chlorurus                   | 0.0216228 |       0.778422 |     0.355742 | algae_strings   |                   2       |
| utumbi   | genus           | centropyge                  | 0.0222947 |       1        |     0.422475 | ulva_gutweed    |                   1.66667 |
| utumbi   | genus           | thalassoma                  | 0.0237071 |       1        |     0.422475 | fischmix        |                   5.83333 |
| utumbi   | word_group      | fusiliers                   | 0.0251106 |       0.527323 |     0.127545 | ulva_salad      |                  74.3333  |
| utumbi   | family          | caesionidae                 | 0.0251106 |       0.577545 |     0.138636 | ulva_salad      |                  74.3333  |
| utumbi   | unspecific      | slender schoolers/colourful | 0.0251106 |       0.326438 |     0.129394 | ulva_salad      |                  74.3333  |

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