# Koedervergleich: Bisherige Statistik und weitere Ideen

## Bereits durchgefuehrte Statistik und Berechnungen
- Standortvergleich der Taxa-Zusammensetzung ueber alle Standorte (cut_47min).
- Artenvergleich nach Standort mit Ueberlappung, exklusiven Taxa und Praesenzmustern.
- Koedervergleich getrennt nach Standort fuer Milimani, Utumbi und Nursery.
- Taxa-Haeufigkeit je Taxon und Standort mit Kruskal-Wallis-Test auf MaxN-Basis.
- Paarweise Taxa-Haeufigkeitsvergleiche mit Mann-Whitney-U-Tests.
- Holm-Korrektur fuer taxonweise und paarweise Vergleiche.
- Taxa-Zusammensetzung je Standort mit globaler PERMANOVA auf Jaccard-Distanz.
- Paarweise PERMANOVA zwischen Koedern mit Roh-p und Holm-korrigierten p-Werten.
- Jaccard-Ueberlappung und Jaccard-Distanzen zwischen Koederpaaren.
- Anzahl koederspezifischer Taxa pro Koeder.
- Dominanzkennzahlen je Koeder, inklusive Ratio Max/Min >= 3.
- Kombination von dominante Taxa und koederspezifischen Taxa in einer gemeinsamen Grafik.
- Auswertung der Annotationen `feeding` und `interested` pro Koeder und Standort.
- Vergleich der `feeding`- und `interested`-Annotationen gegen `control` ueber Total-Events je Video.
- Paarweise Mann-Whitney-U-Tests fuer `feeding` und `interested` auf Koederbasis.
- Roh- und Holm-Korrektur fuer die Verhaltensanalysen.
- Standortbezogene control-Vergleiche fuer `feeding` und `interested`.
- Funktioneller Koedervergleich fuer Milimani und Utumbi mit mehreren Gruppierungsebenen: `word_group`, `family`, `genus`, `unspecific`, `diet` und `composite_group`.
- Fish-vs-Algae-Vergleiche auf denselben Ebenen mit Holm- und BH-Korrektur.
- Zusammentestung von zusammengesetzten Gruppen wie `wrasses_trigger_combo`, `predator_reef_core`, `snappers_groupers_combo`, `piscivore_active_hunters`, `invertivore_general`, `herbivore_core_families`.
- Spezifische Auswertung von Rabbitfishes und Unicornfishes (`rabbitfishes`/`siganidae`/`siganus`, `naso`, `acanthuridae`, `surgeonfishes`).
- Grafiken fuer die Praesentation: Signifikanzuebersicht Fish-vs-Algae, staerkste Effektgroessen, Rabbitfishes/Unicornfishes nach Koeder.
- Modellbasierte Fish-vs-Algae-Analyse mit Standortfaktor in `results/funktionsvergleich_modell`.
- Indikator-/Permutationstest fuer robuste Koedergruppen in `results/funktionsvergleich_indicator`.
- Sensitivitaetsanalyse mit dominanten Videos und seltenen Features in `results/funktionsvergleich_sensitivity`.

## Zentrale neue Ergebnisse im Koedervergleich
- Global ueber alle Koeder je Feature gab es keine Holm- oder BH-signifikanten Treffer in Milimani oder Utumbi.
- Fish-vs-Algae ergab 24 BH-signifikante Effekte insgesamt, ausschliesslich mit Hoeherauspraegung bei Fischkoedern.
- Milimani war dabei fokussiert auf `wrasses`/`Labridae` und `wrasses_trigger_combo`.
- Utumbi zeigte ein breiteres Muster mit `wrasses`, `triggerfishes`, `eels`, `balistidae`, `muraenidae`, `snappers_groupers_combo`, `predator_reef_core` und weiteren zusammengesetzten Gruppen.
- Keine robusten Algenvorteile nach Holm oder BH; Algennahe Tendenzen bleiben explorativ (`chlorurus` in Utumbi, tendenziell `rabbitfishes`/`siganidae` in Utumbi).
- Das standortkontrollierte Modell ergab keine BH-signifikanten Fish-vs-Algae-Effekte, aber die Rohsignale blieben konsistent mit den explorativen Mustern.
- Die Indikatoranalyse fand BH-signifikante Fischindikatoren wie `wrasses`, `triggerfishes`, `labridae`, `balistidae`, `thalassoma`, `balistapus`, `labroides`, `aethaloperca`, `wrasses_trigger_combo`, `predator_reef_core` und `snappers_groupers_combo`.
- In der Sensitivitaet blieben nach Entfernen dominanter Videos 4 Fish-side Effekte signifikant: `large ovals`, `wrasses`, `herbivore_core_families`, `wrasses_trigger_combo`.

## Welche Rohsignale und Tendenzen wurden beobachtet?
- Milimani: `moorish_idol`, `zanclidae`, `zanclus`, `lutjanidae`, `lutjanus`, `nocturnal_predator_mixture`.
- Utumbi: `wrasses`, `labridae`, `triggerfishes`, `balistidae`, `fusiliers`, `caesionidae`, `planktivore_core`.
- Rabbitfishes in Utumbi tendenziell eher algennah, aber nicht signifikant.
- Unicornfishes (`naso`) und Surgeonfishes/Acanthuridae tendenziell fischnah, aber ebenfalls nicht signifikant.

## Wo gibt es noch Luecken in der statistischen Auswertung?
- Es fehlt noch ein vollstaendiges hierarchisches Modell, das Standort, Koeder und funktionelle Gruppe gemeinsam und mit Abhaengigkeiten abbildet.
- Es fehlen Mixed-Effects-Modelle oder aehnliche Ansätze, die Video- bzw. Standortstruktur explizit mit aufnehmen.
- Es fehlt eine PERMDISP-Pruefung, um reine Streuunterschiede von echten Lageunterschieden zu trennen.
- Es fehlt eine Rarefaction bzw. Sampling-Normalisierung fuer die funktionellen Vergleichsgruppen.
- Es fehlt eine vollstaendige hierarchische Modellierung mit Taxon-, Standort- und Koeder-Ebene gemeinsam.
- Es fehlt eine gezielte Analyse, die seltene Taxa und unbalancierte Gruppengroessen gleichzeitig in einem robusten Rahmen behandelt.

## Bereits durchgefuehrte offene Punkte
- Modell mit Standortfaktor fuer Fish vs Algae.
- Indikator-/Permutationstest fuer robuste Gruppen.
- Sensitivitaetsanalyse mit dominantem Video- und Rare-Feature-Filter.

## Naechste sinnvolle Schritte
- PERMDISP zur Pruefung von Streuunterschieden.
- Rarefaction bzw. Sampling-Normalisierung.
- Hierarchisches Modell mit Taxon-, Standort- und Koeder-Ebene.
- Spezifische Folgeanalyse fuer `chlorurus`, `rabbitfishes` und die dominanten Fischgruppen in Utumbi.

## Weitere Analyseideen
- PERMDISP zur Pruefung von Streuunterschieden.
- IndVal-Analyse fuer Indikatorarten.
- Praesenz/Absenz-Tests pro Taxon mit logistischen Modellen oder Fisher-Exact.
- Artenreichtum pro Video mit GLM oder Negative Binomial.
- Rarefaction bzw. Stichprobennormalisierung.
- Konsistenzanalyse zwischen Standorten.
- Erweiterung der Verhaltensanalyse auf weitere Annotationen oder zeitliche Teilfenster.
- Sensitivitaetsanalysen fuer unbalancierte Stichprobengroessen.
