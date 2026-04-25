# Vollstaendige Liste signifikanter Ergebnisse aus allen bisherigen Analysen

Stand: 2026-04-25

## Leseschluessel
- Robust signifikant: nach Mehrfachtestkorrektur (Holm oder BH/FDR) signifikant.
- Roh signifikant: p < 0.05 ohne Korrektur (explorativ, nicht als harter Effekt zu lesen).
- Fokus dieser Liste: alle bisher gefundenen signifikanten Befunde mit kurzer, praeziser Interpretation.

## 1) Standorteffekt auf Species Richness (robust signifikant)

### Globaltest
| Analyse | Test | p-Wert | Signifikant |
|---|---|---:|---|
| Species Richness ~ Standort (Utumbi, Milimani, Nursery) | Kruskal-Wallis | 2.85899e-06 | Ja |

### Paarweise Standorttests (Holm-korrigiert)
| Vergleich | p-Wert | p-Wert Holm | Cliff's Delta | Signifikant (Holm) |
|---|---:|---:|---:|---|
| utumbi vs nursery | 1.01467e-05 | 3.04401e-05 | 0.994949 | Ja |
| utumbi vs milimani | 0.00134397 | 0.00268795 | 0.637255 | Ja |
| milimani vs nursery | 0.00293415 | 0.00293415 | 0.679144 | Ja |

### Koeeder-kontrollierter Standorttest
| Vergleich | Methode | Effekt (Utumbi minus Milimani) | p-Wert | Signifikant |
|---|---|---:|---:|---|
| utumbi vs milimani | stratifizierter Permutationstest (20.000 Permutationen, innerhalb Koeeder) | 8.291 Species Richness | 0.00085 | Ja |

Interpretation:
Der Standorteffekt ist sehr robust und bleibt selbst unter Koeederkontrolle bestehen. Damit sind Unterschiede nicht nur durch Koeederzusammensetzung erklaerbar, sondern spiegeln echte Standortunterschiede wider.

## 2) Taxa-Haeufigkeit (MaxN) nach Standort (robust signifikant)

### Gesamt
| Getestete Taxa | Roh signifikant | Holm-signifikant |
|---:|---:|---:|
| 161 | 93 | 36 |

### Alle 36 Holm-signifikanten Taxa
| Taxon | Dominanter Standort (Mittelwert) | Niedrigster Standort (Mittelwert) | p-Wert Holm | Eta^2 |
|---|---|---|---:|---:|
| species::humpback (lutjanus gibbus) | nursery | milimani | 4.68853e-08 | 0.974743 |
| species::threespot dascyllus (dascyllus trimaculatus) | nursery | milimani | 4.68853e-08 | 0.974743 |
| species::blackwhite (macolor niger) | nursery | milimani | 3.67163e-07 | 0.878436 |
| species::monk (acanthurus gahhm) | nursery | utumbi | 1.27523e-06 | 0.820231 |
| genus::genus soldier | utumbi | nursery | 1.37691e-06 | 0.816368 |
| genus::genus squirrel | utumbi | nursery | 3.31007e-06 | 0.775274 |
| species::five-saddle (scarus saber) | utumbi | milimani | 6.84454e-06 | 0.741185 |
| species::orange-lined (balistapus undulatus) | utumbi | nursery | 1.66351e-05 | 0.699579 |
| species::regal (pygoplites diacanthus) | milimani | nursery | 0.000199981 | 0.583615 |
| species::golden (ctenochaetus truncates) | utumbi | milimani | 0.000231029 | 0.576598 |
| species::bird wrasse (gomphosus caeruleus) | utumbi | nursery | 0.0003689 | 0.554524 |
| species::blackspot (lutjanus fulviflamma) | nursery | milimani | 0.000439686 | 0.546050 |
| species::blue barred (scarus ghobban) | nursery | milimani | 0.000439686 | 0.546050 |
| species::indian half-and-half (pycnochromis dimidiatus) | utumbi | nursery | 0.000444897 | 0.544878 |
| species::goldbar (thalassoma hebraicum) | utumbi | nursery | 0.000490112 | 0.540061 |
| species::barred (hemigymnus fasciatus) | milimani | nursery | 0.000536136 | 0.535569 |
| species::bicolor (labroides bicolor) | utumbi | nursery | 0.000539852 | 0.534928 |
| species::brown pigmy (centropyge multispinis) | milimani | nursery | 0.000782168 | 0.517361 |
| species::redmouth (aethaloperca rogaa) | utumbi | nursery | 0.00124658 | 0.495358 |
| species::whitetail (acanthurus thompsoni) | utumbi | milimani | 0.00162577 | 0.482679 |
| species::lined bristletooth (ctenochaetus striatus) | milimani | utumbi | 0.00166386 | 0.481273 |
| species::titan (balistoides viridescens) | nursery | utumbi | 0.00192298 | 0.473924 |
| species::leopard (cephalopholis leopardus) | utumbi | nursery | 0.00192298 | 0.474210 |
| species::arabian monocle (scolopsis ghanam) | nursery | milimani | 0.00325758 | 0.449024 |
| species::sixbar (thalassoma hardwicke) | milimani | nursery | 0.00462374 | 0.432397 |
| species::peacock (cephalopholis argus) | milimani | nursery | 0.00481418 | 0.430179 |
| species::axilspot hogfish (bodianus axillaris) | milimani | nursery | 0.00568068 | 0.422138 |
| species::brown tang (zebrasoma scopas) | milimani | nursery | 0.0127276 | 0.384271 |
| family_label::cornetfishes (fistulariidae) | nursery | utumbi | 0.0206386 | 0.361439 |
| species::yellow-margin (gymnothorax flavimarginatus) | nursery | milimani | 0.0219254 | 0.358275 |
| species::freckled (paracirrhites forsteri) | utumbi | nursery | 0.0268724 | 0.348458 |
| species::elegant unicorn (naso elegans) | utumbi | nursery | 0.0275703 | 0.346909 |
| species::sulfur (pomacentrus sulfureus) | utumbi | milimani | 0.0277577 | 0.346235 |
| species::false-eye (abudefduf sparoides) | utumbi | milimani | 0.0364384 | 0.333217 |
| genus::genus naso | utumbi | nursery | 0.040221 | 0.328258 |
| family_label::fusiliers (caesionidae) | utumbi | milimani | 0.043883 | 0.323838 |

Interpretation:
Die Standortunterschiede sind nicht nur global (Artenreichtum), sondern auch taxon-spezifisch robust. Besonders stark sind Kontraste mit Nursery; gleichzeitig existieren eigenstaendige Profile zwischen Utumbi und Milimani. Das spricht fuer stabile, standortspezifische Assemblagen und Abundanzmuster.

## 3) Taxa-Zusammensetzung nach Koeeder (PERMANOVA, global signifikant)

| Standort | Globaler Test | p-Wert | Signifikant |
|---|---|---:|---|
| Milimani | PERMANOVA (Jaccard, composition ~ koeeder) | 0.0241952 | Ja |
| Utumbi | PERMANOVA (Jaccard, composition ~ koeeder) | 0.00459908 | Ja |
| Nursery | PERMANOVA (Jaccard, composition ~ koeeder) | 0.00159968 | Ja |

Zusatztest (gruppiert Fish vs Algae):
| Standort | Test | Pseudo-F | p-Wert | Signifikant |
|---|---|---:|---:|---|
| Milimani | PERMANOVA Fish (fischmix+mackerel) vs Algae (ulva/sargassum) | 1.8303 | 0.007998 | Ja |
| Utumbi | PERMANOVA Fish (fischmix+mackerel) vs Algae (ulva/sargassum) | 1.7566 | 0.004399 | Ja |

Interpretation:
Die Koeeder verschieben die Gemeinschaftsstruktur als Gesamteffekt klar. Dass einzelne Paarvergleiche oft nicht Holm-signifikant sind, passt zu einem verteilten Multi-Taxa-Effekt statt eines einzelnen dominanten Treibers.

## 4) Interested/Feeding-Analysen (signifikante Befunde)

### 4.1 Globale Koeedereffekte auf Total-Events (pro Standort)
| Standort | Feeding: p | Feeding signifikant | Interested: p | Interested signifikant |
|---|---:|---|---:|---|
| nursery | 0.0384306 | Ja | 0.753004 | Nein |
| utumbi | 0.0145484 | Ja | 0.0127677 | Ja |

### 4.2 Einzeltaxon robust signifikant (Holm)
| Standort | Flag | Taxon | p-Wert | p-Wert Holm | Richtung |
|---|---|---|---:|---:|---|
| milimani | feeding | species::moon (thalassoma lunare) | 0.00684407 | 0.0410644 | fischmix > control |

Interpretation:
Auf Verhaltensebene existieren standortabhaengige globale Koeedereffekte (v. a. Utumbi). Robuste Einzeltaxon-Effekte sind selten; das passt zu hoher Variabilitaet und kleineren Teilstichproben je Koeeder.

### 4.3 Fokussierte Sensitivitaet Nursery (Feeding, algaemix vs mackerel)
Fokus-Taxa: `species::paletail unicorn (naso brevirostris)`, `species::honeycomb (siganus stellatus)`

| Taxon | Effektmuster | MW exact p | MW Holm (2 Taxa) | Permutation p | Permutation Holm (2 Taxa) | Fisher p (Praesenz) | Fisher Holm (2 Taxa) | BH (Permutation/Fisher) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| species::paletail unicorn (naso brevirostris) | algaemix 3/3 positiv vs mackerel 0/4, Cliff's Delta=1.0 | 0.0571 | 0.1143 | 0.0268 | 0.0536 | 0.0286 | 0.0571 | 0.0268 / 0.0286 |
| species::honeycomb (siganus stellatus) | algaemix 3/3 positiv vs mackerel 0/4, Cliff's Delta=1.0 | 0.0571 | 0.1143 | 0.0268 | 0.0536 | 0.0286 | 0.0571 | 0.0268 / 0.0286 |

Interpretation:
Biologisch sind die Effekte sehr stark und konsistent (vollstaendige Trennung, Delta=1.0). Unter strenger Holm-Kontrolle bleiben die Tests knapp ueber der Schwelle, unter BH/FDR fuer die 2 vorab definierten Fokus-Taxa sind die Signale signifikant. Das ist ein "starkes, knapp nicht Holm-robustes" Signal bei kleinem n (3 vs 4 Videos).

## 5) Funktionsvergleich Fish-vs-Algae (Holm/BH-signifikant)

Hinweis:
- Globaltest ueber alle Koeeder je Feature: keine Holm/BH-signifikanten Treffer.
- Signifikante Effekte treten im gerichteten Fish-vs-Algae-Kontrast auf.

### 5.1 Alle Holm- oder BH-signifikanten Fish-vs-Algae-Features
| Standort | Feature-Typ | Feature | p-Wert | p-Holm | p-BH | Hoeher bei | Cliff's Delta |
|---|---|---|---:|---:|---:|---|---:|
| milimani | composite_group | wrasses_trigger_combo | 0.00171164 | 0.0273862 | 0.0273862 | fish | 0.975 |
| milimani | family | labridae | 0.00171164 | 0.037656 | 0.037656 | fish | 0.975 |
| milimani | unspecific | wrasses | 0.00171164 | 0.0205397 | 0.0205397 | fish | 0.975 |
| milimani | word_group | wrasses | 0.00171164 | 0.0325211 | 0.0325211 | fish | 0.975 |
| utumbi | composite_group | fish_oriented_diet_mode | 0.0144726 | 0.159199 | 0.0351479 | fish | 0.711111 |
| utumbi | composite_group | invertebrate_oriented_diet_mode | 0.0105044 | 0.147062 | 0.0342091 | fish | 0.866667 |
| utumbi | composite_group | invertivore_benthic_core | 0.0120738 | 0.156959 | 0.0342091 | fish | 0.822222 |
| utumbi | composite_group | invertivore_general | 0.0120738 | 0.156959 | 0.0342091 | fish | 0.822222 |
| utumbi | composite_group | piscivore_active_hunters | 0.0186225 | 0.186225 | 0.0351758 | fish | 0.711111 |
| utumbi | composite_group | piscivore_core_families | 0.0186225 | 0.186225 | 0.0351758 | fish | 0.711111 |
| utumbi | composite_group | predator_reef_core | 0.00555257 | 0.0888412 | 0.0314646 | fish | 0.844444 |
| utumbi | composite_group | snappers_groupers_combo | 0.00555257 | 0.0888412 | 0.0314646 | fish | 0.844444 |
| utumbi | composite_group | wrasses_trigger_combo | 0.00308173 | 0.0523894 | 0.0314646 | fish | 1 |
| utumbi | diet | fish | 0.0144726 | 0.0434179 | 0.0289453 | fish | 0.711111 |
| utumbi | diet | invertebrates | 0.0105044 | 0.0420177 | 0.0289453 | fish | 0.866667 |
| utumbi | family | balistidae | 0.00311526 | 0.0778815 | 0.0305816 | fish | 0.933333 |
| utumbi | family | labridae | 0.00366979 | 0.0844052 | 0.0305816 | fish | 0.977778 |
| utumbi | family | muraenidae | 0.00335893 | 0.0806142 | 0.0305816 | fish | 0.8 |
| utumbi | unspecific | eels | 0.00335893 | 0.047025 | 0.0256886 | fish | 0.8 |
| utumbi | unspecific | odd-shaped swimmers | 0.00999977 | 0.119997 | 0.0466656 | fish | 0.822222 |
| utumbi | unspecific | wrasses | 0.00366979 | 0.0477073 | 0.0256886 | fish | 0.977778 |
| utumbi | word_group | eels | 0.00335893 | 0.0738964 | 0.0281351 | fish | 0.8 |
| utumbi | word_group | triggerfishes | 0.00311526 | 0.071651 | 0.0281351 | fish | 0.933333 |
| utumbi | word_group | wrasses | 0.00366979 | 0.0770657 | 0.0281351 | fish | 0.977778 |

Interpretation:
Die signifikanten Fish-vs-Algae-Effekte liegen praktisch durchgaengig auf der Fischseite (hoehere Werte bei Fischkoedern). Oekologisch spricht das fuer eine staerkere Aktivierung praedatorischer/invertivorer sowie wrasse/trigger-naher funktioneller Gruppen durch Fischkoeder.

## 6) Indikatoranalyse (Permutation + BH, robust signifikant)

| Feature-Typ | Feature | Indikatorseite | IndVal | p-Permutation | p-BH |
|---|---|---|---:|---:|---:|
| word_group | wrasses | fish | 68.7592 | 0.00333333 | 0.03 |
| word_group | triggerfishes | fish | 68.4518 | 0.00333333 | 0.03 |
| family | labridae | fish | 68.7592 | 0.00333333 | 0.0333333 |
| family | balistidae | fish | 68.4518 | 0.00333333 | 0.0333333 |
| unspecific | wrasses | fish | 68.7592 | 0.00333333 | 0.04 |

Interpretation:
Auch die permutationbasierte Indikatorlogik stuetzt die Fish-Seite: wrasses/triggerfishes (inkl. Labridae/Balistidae) sind robuste Indikatoren fuer Fischkoederbedingungen.

## 7) Standortkontrolliertes Modell (log1p(MaxN) ~ bait_type + site + bait_type:site)

### BH-signifikante Bait-Haupteffekte
| Feature-Typ | Feature | Richtung | Beta (Fish vs Algae) | p-Permutation (Bait) | p-BH (Bait) | R^2 |
|---|---|---|---:|---:|---:|---:|
| word_group | moorish_idol | fish | 0.751361 | 0.00333333 | 0.03 | 0.503264 |
| word_group | wrasses | fish | 0.55597 | 0.00333333 | 0.03 | 0.583072 |
| family | zanclidae | fish | 0.751361 | 0.00333333 | 0.0333333 | 0.503264 |
| family | labridae | fish | 0.55597 | 0.00333333 | 0.0333333 | 0.583072 |
| unspecific | wrasses | fish | 0.55597 | 0.00333333 | 0.04 | 0.583072 |

### Interaktion bait_type:site
- Keine Interaktion ist nach BH signifikant.

Interpretation:
Ein Teil der Fish-vs-Algae-Signale bleibt auch unter Standortkontrolle erhalten. Das spricht fuer einen eigenstaendigen Bait-Effekt, waehrend starke standortspezifische Interaktionsunterschiede nach strenger Korrektur nicht robust belegt sind.

## 8) Nicht-signifikante, aber wichtige Nullbefunde (zur korrekten Einordnung)
- Taxa-Haeufigkeit nach Koeeder (pro Standort): 0 Holm-signifikante Taxa in Milimani, Utumbi und Nursery.
- Sensitivitaetsanalyse (FDR + Vorkommensfilter) dieser Koeeder-MaxN-Tests: weiterhin 0 FDR-signifikante Taxa in allen Standorten.
- Viele Rohsignale bleiben somit plausibel, aber inferenzstatistisch explorativ.

## Gesamteinschaetzung
Die robustesten und konsistentesten Signale liegen auf zwei Ebenen:
1. Standortebene: deutliche, robuste Unterschiede in Species Richness und in vielen einzelnen Taxa (MaxN).
2. Funktionelle Bait-Ebene (Fish vs Algae): robuste Signale zugunsten Fischkoeder, vor allem bei wrasse/trigger/praedatorisch-invertivoren Gruppen.

Die schwierigste Ebene fuer robuste Einzelsignale bleibt der taxonweise Koeedervergleich innerhalb einzelner Standorte. Dort sind Effekte sichtbar, aber durch Mehrfachtests und Stichprobengroessen oft nicht Holm-stabil.
