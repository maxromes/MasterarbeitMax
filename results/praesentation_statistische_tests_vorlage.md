# Statistische Gesamtauswertung: Standort, Koeder, Verhalten und funktionelle Reaktionen

Stand: 2026-08-11

Diese Datei ist eine fachliche Gesamtdarstellung der wichtigsten statistischen Befunde.
Der Schwerpunkt liegt auf:
- robusten, multipeltest-korrigierten Ergebnissen
- klarer Trennung zwischen signifikanter Evidenz, belastbaren Trends und explorativen Mustern
- biologisch interpretierbaren Aussagen zur Frage, welche Taxa mehr von welchem Koeder essen

Zentrale Leitfrage dieser Fassung:
- Gibt es Taxa oder Gruppen, die Algenkoeder signifikant stärker nutzen als Fischkoeder?
- Wo ist diese Hypothese bestätigt, wo nur bedingt, und wo bleibt die Aussage unklar?

---

## Inhaltsverzeichnis

1. Datengrundlage und methodische Leitlinien
2. Robust signifikante Hauptergebnisse
3. Konkrete Beispiele fuer signifikante Effekte
4. Konkrete Beispiele fuer Tendenzen und unklare Befunde
5. Fish-vs-Algae: robuster Standard-Funktionsvergleich
6. Herbivore-Fokus: a priori Tests und Feeding-Filter
7. Sichtweite (Visibility): bivariates Signal vs. adjustierte Modelle
8. Gesamtinterpretation entlang der Leitfrage
9. Methodische Grenzen und offene Punkte
10. Quellenverzeichnis

---

## 1. Datengrundlage und methodische Leitlinien

Datengrundlage:
- 46 Videos aus `cut_47min`
- Standorte: Milimani, Utumbi, Nursery
- Zielgroessen: Taxa-Haeufigkeit (MaxN), Taxa-Zusammensetzung, Verhaltensereignisse (feeding, interested), Sichtweite

Methodischer Rahmen:
- Taxonweise Gruppenvergleiche: Kruskal-Wallis (global), Mann-Whitney U (paarweise)
- Multiple Tests: primaer Holm; in Sensitivitaeten zusaetzlich BH/FDR
- Kompositionsanalyse: PERMANOVA auf Jaccard-Distanzen
- Bait × Standort-Interaktion: lineares Permutationsmodell auf log1p(MaxN) mit `bait_type + site + bait_type:site`, wobei Bait-Labels innerhalb der Standorte permutiert werden
- Sichtanalyse: bivariate Korrelationen sowie adjustierte Modelle mit Standort- und Koederkontrolle

Interpretationsregel:
- Robust = nach Korrektur signifikant
- Bedingt = klare Richtung oder starker Effekt, aber knapp oder nur in Sensitivitaet signifikant
- Explorativ = roh auffaellig, aber nicht korrigiert signifikant

Wichtig fuer die Leitfrage:
- Ein Taxon kann im globalen Funktionsvergleich schon enthalten sein, ohne dort als Algae-responding sichtbar zu werden.
- Die spaeteren Herbivore- und Feeding-Filter-Analysen testen dieselbe biologische Frage in engeren, a priori motivierten Teilmengen.
- Dadurch kann ein Effekt in einem strengen globalen Modell unauffaellig bleiben, in einer biologisch begruendeten Teilanalyse aber klar sichtbar werden.

---

## 2. Robust signifikante Hauptergebnisse

### 2.1 Standorteffekte auf Taxa-Haeufigkeit (MaxN)

Quelle: [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

Zentrale Kennzahlen:
- Getestete Taxa: 161
- Roh signifikant: 93
- Holm-signifikant: 36
- Anteil Holm-signifikant: 22.36%

Einordnung:
- Das ist der robusteste Befund ueber alle Analysen.
- Standort ist ein starker strukturierender Faktor fuer Haeufigkeiten.
- Fuer die Leitfrage heisst das: Zunaechst bestimmt der Standort sehr stark, welche Taxa wo ueberhaupt haeufig genug vorkommen, um Koedereffekte sichtbar werden zu lassen.

### 2.2 Koederunterschiede in der Zusammensetzung (global)

Quelle: [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

PERMANOVA (global je Standort):
- Milimani: p = 0.0242 (signifikant)
- Utumbi: p = 0.0046 (signifikant)
- Nursery: p = 0.0016 (signifikant)

Einordnung:
- Koeder verschieben die Zusammensetzung der beobachteten Gemeinschaft in allen Standorten.
- Der robuste Effekt liegt auf globaler Ebene, nicht zwingend in einzelnen Paarvergleichen.
- Diese Analyse sagt aber noch nicht, ob Algenkoeder speziell Algenfresser bevorzugen. Sie zeigt nur, dass sich die Gemeinschaften zwischen Koedern unterscheiden.

### 2.3 Fish-vs-Algae im Standard-Funktionsvergleich

Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

Robuste Richtung:
- Signifikante Fish-vs-Algae-Befunde zeigen ueberwiegend higher_side = fish.
- Besonders deutlich in Utumbi mit mehreren BH-signifikanten Funktionsgruppen.

Einordnung:
- Der Standard-Funktionsvergleich findet vor allem Gruppen, die bei Fischkoedern haeufiger sind.
- Die Gegenhypothese "Algenfresser reagieren staerker auf Algen" wird dort nur sehr begrenzt unterstuetzt.
- Genau deshalb wurde zusaetzlich ein a priori Herbivore-Fokus gerechnet.

### 2.4 Visibility (adjustiert)

Quellen:
- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

Robuster Schluss:
- Bivariat sind Zusammenhaenge mit MaxN und Richness sichtbar.
- Nach Kontrolle fuer Standort + Koeder bleibt kein robuster, unabhaengiger Sicht-Effekt.

---

## 3. Konkrete Beispiele fuer signifikante Effekte

### 3.1 Standortvergleich (taxonweise, Holm-korrigiert signifikant)

Quelle: [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

Beispiel A:
- Taxon: species::humpback (lutjanus gibbus)
- Kruskal-Wallis: p = 2.91e-10, Holm p = 4.69e-08
- Mittelwerte: Milimani 0.00, Utumbi 0.00, Nursery 20.18
- Interpretation: sehr starker standortspezifischer Schwerpunkt in Nursery

Beispiel B:
- Taxon: species::threespot dascyllus (dascyllus trimaculatus)
- Kruskal-Wallis: p = 2.91e-10, Holm p = 4.69e-08
- Mittelwerte: Milimani 0.00, Utumbi 0.00, Nursery 8.00
- Interpretation: klarer Standortkontrast mit Konzentration in Nursery

Beispiel C:
- Taxon: genus::genus soldier
- Kruskal-Wallis: p = 8.77e-09, Holm p = 1.38e-06
- Mittelwerte: Milimani 0.29, Utumbi 3.17, Nursery 0.00
- Interpretation: deutliches Utumbi-Signal

Beispiel D:
- Taxon: species::arabian monocle (scolopsis ghanam)
- Kruskal-Wallis: p = 2.36e-05, Holm p = 0.00326
- Mittelwerte: Milimani 0.12, Utumbi 0.44, Nursery 7.00
- Interpretation: starker Nursery-Schwerpunkt

### 3.2 Kompositionsvergleich nach Koeder (global signifikant)

Quelle: [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

Beispiel A:
- Standort: Utumbi
- PERMANOVA global: p = 0.0046
- Top-Overlap-Paar: control vs sargassum (Jaccard 0.764)
- Interpretation: trotz teils hoher Ueberlappung bleibt die Gesamtstruktur zwischen Koedern signifikant verschieden

Beispiel B:
- Standort: Nursery
- PERMANOVA global: p = 0.0016
- Top-Overlap-Paar: algae_strings vs algaemix (Jaccard 0.662)
- Interpretation: Koedereffekt auf Zusammensetzung ist auch in Nursery robust

### 3.3 Fish-vs-Algae (BH-signifikante Einzelfeatures)

Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

Beispiel A (Milimani):
- Feature: wrasses (unspecific)
- p = 0.00171, Holm p = 0.02054, BH p = 0.02054
- Richtung: fish > algae
- Effektgroesse: Cliff's Delta = 0.975

Beispiel B (Utumbi):
- Feature: eels (unspecific)
- p = 0.00336, Holm p = 0.04703, BH p = 0.02569
- Richtung: fish > algae
- Effektgroesse: Cliff's Delta = 0.800

Beispiel C (Utumbi):
- Feature: wrasses (word_group)
- p = 0.00367, BH p = 0.02814
- Richtung: fish > algae
- Effektgroesse: Cliff's Delta = 0.978

Beispiel D (Utumbi):
- Feature: invertebrates (diet)
- p = 0.01050, Holm p = 0.04202, BH p = 0.02895
- Richtung: fish > algae
- Effektgroesse: Cliff's Delta = 0.867

### 3.4 Visibility: konkrete bivariate Signifikanz

Quelle: [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)

Beispiel A:
- visibility_mean vs species_richness
- Spearman rho = 0.563, p = 4.61e-05, BH q = 1.38e-04
- Interpretation: starker positiver Rohzusammenhang

Beispiel B:
- visibility_mean vs maxn_video_peak
- Spearman rho = 0.467, p = 0.00108, BH q = 0.00161
- Interpretation: moderater positiver Rohzusammenhang

### 3.5 Species-Richness-Standortvergleich als zusaetzlicher robuster Standortanker

Quelle: [Standortvergleich/standortvergleich.md](Standortvergleich/standortvergleich.md)

Globaltest:
- Kruskal-Wallis species_richness ~ standort: H = 25.96, p = 2.31e-06

Paarweise (Holm-korrigiert, alle signifikant):
- Utumbi vs Nursery: p_Holm = 3.06e-05, Cliff's Delta = 0.995
- Utumbi vs Milimani: p_Holm = 0.00268, Cliff's Delta = 0.637
- Milimani vs Nursery: p_Holm = 0.00268, Cliff's Delta = 0.711

Koeder-kontrollierter Zusatztest:
- Stratifizierter Permutationstest (Utumbi vs Milimani | by bait): p = 0.0008

Interpretation:
- Die Standortstruktur bleibt auch bei koeder-kontrollierter Pruefung klar bestehen.
- Das stuetzt die Kernaussage, dass Standort der dominierende Treiber ist, nochmals unabhaengig von den taxonweisen MaxN-Tests.

---

## 4. Konkrete Beispiele fuer Tendenzen und unklare Befunde

### 4.1 Koeder-Haeufigkeit je Standort: Rohsignal ohne Holm-Robustheit

Quelle: [taxahaeufigkeitkoeder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)

Gesamtmuster:
- Milimani: 6 Rohsignale, 0 Holm-signifikant
- Nursery: 11 Rohsignale, 0 Holm-signifikant
- Utumbi: 8 Rohsignale, 0 Holm-signifikant

Konkrete Tendenzbeispiele aus den Top-Rohsignalen:
- Milimani: species::blue-green (chromis viridis)
- Milimani: species::moorish idol (zanclus cornutus)
- Utumbi: species::longnose (lethrinus olivaceus)
- Utumbi: species::orange-lined (balistapus undulatus)
- Nursery: family_label::puffers (tetraodontidae)

Interpretation:
- Es gibt wiederholt gerichtete Koederhinweise, aber keine ausreichende Robustheit nach strenger Korrektur.

### 4.2 Globaltest ohne robuste paarweise Signifikanz

Quelle: [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

Muster:
- Globale PERMANOVA je Standort signifikant.
- Paarweise Koedervergleiche nach Holm meist nicht signifikant.

Interpretation:
- Effekt ist verteilt ueber mehrere Koederbeziehungen.
- Kein einzelnes Paar traegt die komplette Evidenz.

### 4.3 Visibility: bivariates Signal verschwindet nach Adjustierung

Quelle: [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)

Konkrete Beispiele:
- species_richness: Beta = 0.004, p(HC3) = 0.734, q = 0.739
- maxn_video_peak: Beta = 0.030, p(HC3) = 0.483, q = 0.739
- first_seen_median_sec: Beta = -0.017, p(HC3) = 0.739, q = 0.739

Interpretation:
- Konfundierung durch Standort/Koeder ist plausibel.
- Rohzusammenhang ist nicht gleich unabhaengiger Treibereffekt.

### 4.4 Algae-Responsiveness (Reverse-Focus): nur begrenzt robust

Quelle: [algae_responsiveness/algae_responsiveness_summary.md](algae_responsiveness/algae_responsiveness_summary.md)

Muster:
- Milimani: 14 Taxa mit Algen-Vorteil, 0 Holm-signifikant, 0 BH-signifikant
- Utumbi: 14 Taxa mit Algen-Vorteil, 1 Holm-/BH-signifikantes Taxon
- Nursery: 29 Taxa mit Algen-Vorteil, 0 Holm-signifikant, 0 BH-signifikant

Ein robustes Einzelbeispiel (Utumbi):
- species::bullethead (chlorurus sordidus): Cliff's Delta = 0.889, p = 0.0458, Algae-Median 3.0 vs Fish-Median 1.0

Interpretation:
- Es existieren klare Algen-Tendenzen in mehreren Taxa, aber nur sehr begrenzte korrigierte Robustheit.
- Damit passt der Reverse-Focus zur Gesamtinterpretation: Die staerkste Algen-Unterstuetzung entsteht im gezielten Herbivore-/Feeding-Fokus, nicht im breiten All-Taxa-Screen.

### 2.5 Species-Richness-Zusatzauswertung

Quelle: [species_richness_report/species_richness_additional_tests.md](species_richness_report/species_richness_additional_tests.md)

Ergebnisbild:
- Der Standort ist fuer Species Richness robust signifikant, sowohl im Kruskal-Wallis-Test als auch in der Permutation.
- Der Koeder-Faktor ist dagegen global nicht signifikant.
- Auch paarweise bleibt der Standortkontrast deutlich, waehrend fuer Koeder nach Korrektur keine robusten Unterschiede mehr uebrig bleiben.

Einordnung:

---

## 5. Weitere Tests, die die Ergebnisse weiter festigen koennen

Die bisherigen Ergebnisse sind bereits klar in ihrer Richtung, aber es gibt mehrere sinnvolle Zusatzanalysen, die die Evidenz weiter absichern oder die Interpretation differenzieren.

### 5.1 Effektgroessen und Konfidenzintervalle statt nur p-Werte

Warum wichtig:
- p-Werte allein sagen nichts darueber, wie gross oder praktisch relevant ein Effekt ist.
- Bei vielen biologischen Vergleichsanalysen ist die Richtung und Starke der Differenz oft wichtiger als die rein formale Signifikanz.

Sinnvolle Erweiterung:
- Cliff's Delta fuer robuste, distributionsfreie Effektgroessen
- Bootstrap-Konfidenzintervalle fuer mean differences
- eta^2 oder epsilon^2 als groessere Effektmasse in Kruskal-Wallis-Analysen

Interpretation:
- Wenn ein Effekt sowohl signifikant als auch gross ist, wird die biologische Aussage deutlich tragfaehiger.
- Wenn ein Effekt klein bleibt, trotz niedrigem p-Wert, ist die Evidenz eher vorsichtig zu bewerten.

### 5.2 Permutationsbasierte Sensitivitaetsanalysen fuer die wichtigsten Hypothesen

Warum wichtig:
- Besonders bei kleinen Gruppengrössen (z.B. wenige Videos pro Koeder) ist die Verteilung von p-Werten empfindlich.
- Permutationstests helfen, die Robustheit der Schlussfolgerung gegen kleine Abweichungen in der Verteilung zu prüfen.

Sinnvolle Erweiterung:
- Permutations-Tests fuer Mittelwertdifferenzen zwischen den wichtigsten Koederpaaren
- Permutationstests fuer den globalen Bait-Effekt mit direkten und standortspezifischen Interaktionen
- Permutations-Tests mit stratifizierter Permutation innerhalb von Standorten

Interpretation:
- Wenn ein Effekt sowohl nach Parametern als auch nach Permutation robust bleibt, ist er deutlich belastbarer.
- Wenn der Effekt nur im klassischen Test erscheint, aber in Permutation verschwindet, ist Vorsicht geboten.

### 5.3 Standort-stratifizierte Analysen statt rein globaler Vergleiche

Warum wichtig:
- Der Standort ist der dominante Strukturtreiber in den Daten.
- Viele Koeder- und Sicht-Effekte koennen nur deshalb sichtbar werden, weil sie mit Standortkontexten zusammenfallen.

Sinnvolle Erweiterung:
- Analyse pro Standort mit Bait-Effekt getrennt
- Vergleich innerhalb identischer Standort-Koeder-Kombinationen
- Interaktionsmodell `bait_type * site` mit Permutation und Effektgrössen

Interpretation:
- Ein Effekt, der nur in einem Standort auftritt, ist biologisch interessant, aber nicht global generalisierbar.
- Ein globaler Effekt mit konsistenter Richtung in mehreren Standorten ist stark belastbarer.

### 5.4 Multivariat- und Dispersionstests zur Unterscheidung von Gruppenverschiebung vs. Streuung

Warum wichtig:
- PERMANOVA zeigt Unterschiede in der Gemeinschaftsstruktur, kann aber nicht sauber zwischen verschobenen Mittelwerten und unterschiedlicher Streuung unterscheiden.

Sinnvolle Erweiterung:
- PERMDISP (tests of multivariate dispersion)
- Ordinationsplots (nMDS, PCoA) mit ellipses per Koeder oder Standort
- Distanz zu Gruppenzentren als Zusatzmaass fuer Stabilitaet/Variabilitaet

Interpretation:
- Wenn die Gruppenvariablen nicht nur verschoben, sondern auch ungleich streuend sind, muss die biologische Interpretation genauer differenziert werden.
- Das ist besonders wichtig bei der Interpretation von Koedereffekten auf die Komposition.

### 5.5 Prevalence- und Occupancy-Sensitivitaet

Warum wichtig:
- Viele Taxa sind selten; ihre Signale koennen durch wenige extreme Videos entstehen.
- Die Beurteilung sollte zwischen seltenen, doch stark reagierenden Taxa und frequenten, stabilen Taxa unterscheiden.

Sinnvolle Erweiterung:
- Anteil der Videos mit Nachweis je Taxon und Standort
- Prevalence-gesteuerte Filter (z.B. nur Taxa mit Mindestnachweis in einem Anteil der Videos)
- Vergleich von durchschnittlicher Haeufigkeit vs. prevalenter Nachweis

Interpretation:
- Ein Taxon mit hoher MaxN, aber niedriger Praevalenz kann biologisch anders interpretiert werden als ein Taxon, das in vielen Videos konsistent vorkommt.
- So lassen sich "hotspot"-Effekte von robusten Community-Mustern trennen.

### 5.6 Leave-one-out-Sensitivitaet und Resampling

Warum wichtig:
- Einzelne Videos oder kurze Zeitfenster koennen einen Effekt stark beeinflussen.
- Ein Gutachter will wissen, ob das Ergebnis stabil ist oder an wenigen Ausreissern haengt.

Sinnvolle Erweiterung:
- Systematische Leave-one-video-out-Analysen fuer die wichtigsten Signale
- Vergleich der Effektstaerke unter Entfernung eines einzelnen Videos
- Fokus auf die biologisch zentralen Befunde: Nursery-Herbivore und Fish-vs-Algae-Hauptsignale

Interpretation:
- Wenn der Effekt bei jedem einzelnen Videoremoval in der gleichen Richtung bleibt, ist die Schlussfolgerung deutlich robuster.
- Wenn er stark schwankt, sollte die Aussage entsprechend nuancierter formuliert werden.

Quelle: [leave_one_video_out_sensitivity/leave_one_video_out_sensitivity.md](leave_one_video_out_sensitivity/leave_one_video_out_sensitivity.md)

Ergebnis der systematischen LOO-Sensitivitaet:
- Nursery-Acanthuridae bleibt auch bei jedem einzelnen Video-Remove signifikant (LOO-p-Werte: 0.0079 bis 0.0138).
- Die koerperlich zentralen Fish-vs-Algae-Familien im Coral-Reef-Datensatz (Labridae, Balistidae, Muraenidae) bleiben ebenfalls unter jedem einzelnen Videoremoval durchgehend signifikant.
- Damit ist der robuste Kern der Schlussfolgerungen nicht durch einzelne extreme Videos getrieben.
- Der wichtigste Befund bleibt damit stabil: Die Haupteffekte sind real, aber standortabhaengig und nicht durch einen einzigen Ausreisser zu erklären.

### 5.7 Präsenz-/Absenz-Modell als komplementärer Robustheitscheck

Warum wichtig:
- MaxN-Analysen zeigen vor allem, wie stark eine Gruppe in einem Video vertreten ist.
- Ein echter Effekt kann aber auch als veraenderte Nachweiswahrscheinlichkeit interpretiert werden: ein Taxon ist auf Algenvideos häufiger überhaupt vorhanden, nicht nur intensiver.
- Gerade bei Herbivoren und Fisch-vs-Algae-Mustern ist diese Unterscheidung wichtig, weil hohe MaxN-Werte auch durch wenige, sehr dichte Videos entstehen koennen.

Methode:
- Videoebene: jedes Taxon/Familie wird je Video als vorhanden/abwesend kodiert.
- Vergleich zwischen Algen- und Fischvideos mit Fisher-Exact-Test, gerichtete Alternative entsprechend der biologischen Hypothese.
- Fokus auf die wichtigsten biologischen Signale: Nursery-Acanthuridae, Coral-Reef-Labridae, Balistidae und Muraenidae.

Ergebnis:
- Nursery-Acanthuridae: kein robuster Prävalenzunterschied; beide Koedergruppen zeigen in praktisch allen Videos Vorhandensein. Das spricht dafür, dass hier der Kern des Effekts auf einer Dichte- oder Aktivitätsdifferenz beruht, nicht auf reiner Praesenz.
- Coral-Reef-Muraenidae: klarstes Presence/Absence-Signal; auf Algenvideos war die Familie in keinem der 19 Videos vorhanden, auf Fischvideos in 5 von 9 Videos. Fisher-Exact p = 0.00128, BH-q = 0.00769.
- Coral-Reef-Labridae und Balistidae: no robust prevalence effect; beide Familien waren in nahezu allen Algen- und Fischvideos präsent. Das deutet darauf hin, dass hier die Differenz nicht durch Vorkommen, sondern durch Groessen-/Dichteunterschiede oder Verhaltensunterschiede entsteht.
- Coral-Reef-Siganidae und Scaridae: ebenfalls kein relevanter Präsenzunterschied, was die Interpretation stützt, dass die breitesten Fish-vs-Algae-Muster im MaxN-Raum stärker greifen als im binären Occurrence-Raum.

Interpretation:
- Das Präsenz-/Absenz-Modell ergänzt die MaxN- und LOO-Analysen, statt sie zu ersetzen.
- Der robusteste Kern der biologischen Aussage liegt in der Kombination aus: (i) Konsistenz im MaxN-Bereich, (ii) Stabilitaet nach Videoremoval, und (iii) nur teilweise klarer Prevalence-Differenz bei einzelnen Familien.
- Deshalb bleibt die sauberste Formulierung: Die wichtigsten Effekte sind real, aber biologisch vor allem als Dichte- und Intensitaetsmuster zu lesen, nicht als generelle Unterschiede im bloßen Vorkommen.

### 5.8 Ranking von Evidenzstufen statt bloßer Signifikanzlabels

Warum wichtig:
- In biologischen Daten ist die Frage nicht nur, ob etwas signifikant ist, sondern wie stark und wie konsistent die Evidenz ist.

Sinnvolle Erweiterung:
- Robust = signifikant nach Holm, konsistent ueber Sensitivitaetsanalysen, kompatibel mit Effektgroessen
- Bedingt = Richtung stabil, aber nur in Teilanalysen oder nach BH signifikant
- Explorativ = nur roh signifikant oder nur in einer Teilmenge sichtbar

Interpretation:
- Diese Einordnung verhindert, dass eine einzelne p-Wert-Grenze zu stark und zu simplifiziert interpretiert wird.
- Gerade fuer die Leitfrage "Algenkoeder vs. Fischkoeder" ist dies sehr hilfreich.

### 5.9 Hurdle-Modell: Trennung von Praesenz- und Intensitaetseffekten

Quelle: [hurdle_model/hurdle_model_focal_signals.md](hurdle_model/hurdle_model_focal_signals.md)

Warum wichtig:
- Das Praesenz-/Absenz-Modell und MaxN-Modelle beantworten unterschiedliche biologische Fragen.
- Ein Hurdle-Ansatz trennt explizit: (i) kommt ein Taxon ueberhaupt vor und (ii) wie stark ist es, wenn es vorkommt.
- Damit wird direkt sichtbar, ob Koedereffekte eher occurrence-getrieben oder dichte-/aktivitaetsgetrieben sind.

Modellaufbau:
- Stufe 1 (Praesenz): logistische Regression (bzw. Fisher-Fallback bei Separation) fuer Nachweis ja/nein.
- Stufe 2 (Intensitaet): OLS auf log1p(MaxN) nur fuer Videos mit MaxN > 0 (HC3-robuste Standardfehler).
- Korrektur: BH/FDR getrennt fuer Praesenz- und Intensitaetsteil ueber alle fokussierten Signale.

Kernaussagen aus dem Ergebnis:
- Nursery Acanthuridae: kein Praesenzsignal (beide Koedergruppen praktisch immer praesent), aber sehr starkes Intensitaetssignal zugunsten Algenkoeder (q_BH < 1e-4).
- Coral Labridae und Balistidae: kein Praesenzsignal, aber robustes Intensitaetssignal in Richtung fish > algae.
- Coral Muraenidae: robustes Praesenzsignal (Fisher-Fallback, q_BH = 0.00769), Intensitaetsteil wegen fehlender positiver Algen-Beobachtungen nicht stabil schaetzbar.
- Coral Siganidae und Scaridae: weder im Praesenz- noch im Intensitaetsteil robust signifikant.

Interpretation:
- Der Zusatztest bestaetigt die bisherige Hauptlesart: Die staerksten Effekte liegen meist auf der Intensitaetsebene (MaxN bei Praesenz), nicht in einer pauschal veraenderten Nachweiswahrscheinlichkeit.
- Gleichzeitig zeigt Muraenidae als Ausnahme ein klares Occurrence-Muster. Dadurch wird die biologische Einordnung praeziser: unterschiedliche Familien reagieren ueber unterschiedliche Mechanismen.

---

## 6. Grafik-Set zum Auswaehlen und Interpretieren

Der neue Ordner [ergaenzende_statistische_grafiken/README.md](ergaenzende_statistische_grafiken/README.md) enthält ein umfangreiches Set an Abbildungen, das die wichtigsten Ergebnisse aus verschiedenen Perspektiven visualisiert.

Die Sammlung deckt die folgenden Kategorien ab:
- Standort-Haupteffekte
- Koeder-Effekte auf die Gemeinschaftsstruktur
- Fish-vs-Algae-Effektgroessen
- Species Richness nach Standort
- Visibility als Rohsignal und nach Adjustierung
- Herbivore-Richtungseffekte
- Evidenzstufen der wichtigsten Befunde
- Hurdle-Zerlegung in Praesenz- vs. Intensitaetseffekte

Die einzelnen Grafiken sind nicht nur dekorativ gedacht, sondern dienen dazu, die Ergebnisse in unterschiedlichen Interpretationsebenen zu vergleichen:
- Grobe Effektstärke
- Effektrichtung
- Stabilitaet nach Korrektur
- Beeinflussung durch Standorte
- Erklaerungswert der Sichtweite
- Biologische Plausibilitaet im a-priori Herbivore-Fokus

So lassen sich verschiedene Formen der Belegkraft je nach Zielgruppe separat hervorheben:
- fuer die fachliche Diskussion
- fuer die Laborterminologie
- fuer die Poster- oder Praesentation
- fuer die kritische Einordnung von Signifikanz und Effektgroessen

---

## 7. Empfehlung fuer die finalen Schlussfolgerungen

Wenn die Ergebnisse in der Praesentation oder im Manuskript festigen sollen, ist folgende Reihenfolge sinnvoll:

1. Standort ist der dominanteste Effekt.
2. Koeder beeinflussen die Gemeinschaftsstruktur global signifikant.
3. Ein breiter Fish-vs-Algae-Vergleich zeigt eher fish-orientierte Muster.
4. Im a priori Herbivore-Fokus und in der Nursery tritt jedoch eine klarere Algenkoeder-Response auf.
5. Visibility ist im Rohmodell sichtbar, verliert aber nach Kontrolle fuer Standort und Koeder ihre Robustheit.
6. Species Richness ist vor allem standortgetrieben und kein robuster Koeder-Effekt.
7. Die Hurdle-Zerlegung zeigt, dass die staerksten Signale haeufig als Intensitaetsunterschiede und nur teilweise als Praesenzunterschiede auftreten.

Diese Reihenfolge macht die Dateninterpretation nicht nur formal konsistent, sondern auch biologisch nachvollziehbar.

Einordnung:
- Species Richness folgt damit vor allem der Standortstruktur.
- Das stuetzt die Interpretation, dass viele der beobachteten Koeder- und Funktionsmuster immer im Kontext der Standortunterschiede gelesen werden muessen.

---

## 5. Fish-vs-Algae: robuster Standard-Funktionsvergleich

Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

### 5.1 Welche Gruppen wurden verglichen?

Der Funktionsvergleich nutzt mehrere Ebenen. Wichtig ist: Viele dieser Gruppen sind keine einzelnen Taxa, sondern biologische Sammelgruppen, die auf Taxa, Familien oder Wortgruppen aus der Annotation gemappt werden.

#### 5.1.1 Wortgruppen mit biologischer Bedeutung
- blennies = Blenniidae
- rabbitfishes = Siganidae
- surgeonfishes = Acanthuridae
- parrotfishes = Scaridae
- wrasses = Labridae
- eels = Muraenidae
- groupers_large = Serranidae
- snappers = Lutjanidae
- triggerfishes = Balistidae
- bigeyes = Priacanthidae
- soldier_squirrelfishes = Holocentridae-nahe Gruppen
- jacks_trevallies = Carangidae-nahe Gruppen
- fusiliers = Caesionidae

#### 5.1.2 Familienebene
Direkt getestete Familien umfassen unter anderem:
- siganidae
- acanthuridae
- scaridae
- blenniidae
- labridae
- muraenidae
- lutjanidae
- serranidae
- balistidae
- caesionidae
- nemipteridae
- lethrinidae
- priacanthidae
- pomacentridae
- chaetodontidae
- cirrhitidae
- haemulidae
- mullidae
- gobiidae
- monacanthidae
- ostraciidae
- tetraodontidae

#### 5.1.3 Zusammengesetzte Gruppen
- herbivore_core_families = Siganidae, Acanthuridae, Scaridae, Blenniidae
- herbivore_extended_with_damselfishes = Kern-Herbivore plus kleinere Damselfish-nahe Gruppen
- piscivore_core_families = Serranidae, Lutjanidae, Muraenidae, Sphyraenidae, Aulostomidae, Fistulariidae
- piscivore_active_hunters = Groupers, eels, snappers, barracudas, trumpetfishes, cornetfishes, jacks_trevallies
- invertivore_benthic_core = Mullidae, Haemulidae, Balistidae, Diodontidae, Nemipteridae, Lethrinidae
- invertivore_general = Goatfishes, sweetlips, triggerfishes, porcupinefishes, coral_breams, emperors, hawkfishes
- planktivore_core = Apogonidae, Caesionidae, Pempheridae plus Anthias
- predator_reef_core = Lutjanidae, Serranidae, Muraenidae, Sphyraenidae, Synanceiidae, Antennariidae
- bioeroder_set = Scaridae + Balistidae
- omnivore_box_puffer_file = Ostraciidae, Tetraodontidae, Monacanthidae
- nocturnal_predator_mixture = eels, snappers, bigeyes, soldier_squirrelfishes
- algae_oriented_diet_mode = alle Taxa mit Algenbezug in der Word/Diet-Zuordnung
- fish_oriented_diet_mode = alle Taxa mit Fischbezug
- invertebrate_oriented_diet_mode = alle Taxa mit Wirbellosenbezug
- plankton_oriented_diet_mode = alle Taxa mit Planktonbezug

### 5.2 Was zeigt der Standard-Funktionsvergleich?

Robuste Richtung:
- Signifikante Fish-vs-Algae-Befunde zeigen ueberwiegend higher_side = fish.
- Besonders deutlich in Utumbi mit mehreren BH-signifikanten Funktionsgruppen.

Die wichtigsten robusten Beispiele:
- wrasses / Labridae in Milimani und Utumbi
- eels / Muraenidae in Utumbi
- triggerfishes / Balistidae in Utumbi
- invertebrates, invertivore_general, invertivore_benthic_core, piscivore_active_hunters, piscivore_core_families

Einordnung fuer die Leitfrage:
- Der Standard-Funktionsvergleich liefert kaum direkte Unterstuetzung fuer die Hypothese, dass algenfressende Taxa mehr von Algenkoedern essen.
- Er zeigt vielmehr, dass mehrere Fisch-orientierte oder invertivore Gruppen bei Fischkoedern aktiver sind.

### 5.3 Was sagt das fuer Algenfresser?

Die Antwort lautet: nur begrenzt.

Im Standardtest gibt es einzelne algennahe Signale, aber sie bleiben meistens explorativ:
- chlorurus in Nursery taucht als Rohsignal auf, aber nicht robust im Funktionsvergleich.
- algae_oriented_diet_mode ist im Standard-Funktionsvergleich nicht robust signifikant.
- Die starken Algen-Signale werden erst sichtbar, wenn man auf Herbivore und/oder Feeding fokussiert.

Kernaussage:
- Der Standard-Funktionsvergleich testet alle Gruppen gleichermassen.
- Damit wird die a priori biologische Hypothese "Algenfresser reagieren staerker auf Algen" nicht optimal ausgelesen.
- Dafuer sind die naechsten Abschnitte wichtiger.

### 5.4 Ergänzende Fish-vs-Algae-Robustheitschecks

Diese Analysen bestaetigen das Grundmuster, ohne die biologische Leitfrage grundlegend zu verschieben.

#### 5.4.1 Modellbasierte Fish-vs-Algae-Analyse mit Standortfaktor

Quelle: [funktionsvergleich_modell/model_report.md](funktionsvergleich_modell/model_report.md)

- Der Fish-vs-Algae-Effekt bleibt auch nach Standortkontrolle in mehreren Feature-Klassen sichtbar.
- BH-signifikante Fisch-Signale finden sich vor allem bei word_group und family.
- Besonders deutlich sind moorish_idol, wrasses, zanclidae und labridae auf der Fischseite.
- Interaktionen deuten darauf hin, dass die Staerke des Effekts zwischen Standorten variiert.

#### 5.4.2 Indikator-/Permutationstest

Quelle: [funktionsvergleich_indicator/indicator_report.md](funktionsvergleich_indicator/indicator_report.md)

- Die robustesten Indikatorgruppen liegen ebenfalls auf der Fischseite.
- Signifikante Beispiele sind wrasses, triggerfishes, labridae und balistidae.
- Algenindikatoren bleiben hier explorativ und werden nicht robust bestaetigt.

#### 5.4.3 Sensitivitaetsanalyse

Quelle: [funktionsvergleich_sensitivity/sensitivity_report.md](funktionsvergleich_sensitivity/sensitivity_report.md)

- Die Fish-vs-Algae-Signale bleiben unter gefilterten Szenarien erhalten.
- Weder dominante Videos noch seltene Features erklaeren die Hauptergebnisse allein.
- Der robuste Kern der Ergebnisse ist damit nicht auf ein einzelnes Ausreisserset reduzierbar.

#### 5.4.4 Interested-/Feeding-Gesamtuebersicht

Quelle: [interested_feeding/interested_feeding_summary.md](interested_feeding/interested_feeding_summary.md)

- Feeding zeigt standortabhaengige koederbezogene Muster: in Milimani und Utumbi gibt es globale Total-Event-Signale, in Nursery ist das Muster schwächer bzw. taxonabhängiger.
- Interested ist insgesamt seltener robust, erreicht aber in Utumbi fuer die Total-Events ebenfalls ein klares Signal.
- Das zielgenaue Nursery-Fokusupdate auf algaemix vs mackerel zeigt fuer zwei vorab definierte Taxa eine sehr starke Trennung, bleibt unter Holm aber knapp nicht robust.

- Insgesamt bestaetigen diese Robustheitschecks das Grundmuster: Fish-vs-Algae ist real, aber die staerksten Gegenhypothesen bleiben standort- und featureabhängig.

---

## 6. Herbivore-Fokus: a priori Tests und Feeding-Filter

Diese Sektion beantwortet die Leitfrage direkt.

Die zentrale Hypothese lautet:
- Algenfressende Taxa zeigen hoeheres MaxN und/oder hoeheres Feeding bei Algenkoedern als bei Fischkoedern.

Diese Hypothese wird in zwei komplementaeren Weisen getestet:
1. a priori Herbivore-MaxN-Test nur fuer die vier Herbivore-Familien
2. Herbivore-Feeding-Responsiveness nur fuer Feeding-Verhalten

### 6.1 Welche Gruppen wurden hier getestet und was verbirgt sich dahinter?

#### 6.1.1 Herbivore-Kernfamilien
- Siganidae = Rabbitfische
- Acanthuridae = Surgeonfische/Chirurgenfische
- Scaridae = Papageienfische
- Blenniidae = Blennies

Konkrete Taxa, die hinter diesen Gruppen stehen, sind im Datensatz u. a.:
- species::bullethead (chlorurus sordidus) = Scaridae
- species::blue barred (scarus ghobban) = Scaridae
- species::sailfin tang (zebrasoma desjardinii) = Acanthuridae
- species::whitetail (acanthurus thompsoni) = Acanthuridae
- genus::zebrasoma = Acanthuridae-nahe Taxa
- genus::siganus = Siganidae
- family_label::parrotfishes (scaridae) = Scaridae

#### 6.1.2 Zusammengesetzte Herbivore-Gruppen im Feeding-Filter
- herbivore_core_families = Siganidae, Acanthuridae, Scaridae, Blenniidae
- herbivore_extended_with_damselfishes = Kern-Herbivore plus kleinere Damselfish-nahe Gruppen

#### 6.1.3 Vergleichsgruppen mit Fisch- oder Invertivoren-Bezug
- piscivore_core_families
- snappers
- groupers_large
- eels
- triggerfishes
- invertivore_general

### 6.2 A priori Herbivore-MaxN-Test

Quelle: [herbivore_analysis/herbivore_maxn_apriori_test.md](herbivore_analysis/herbivore_maxn_apriori_test.md)

#### 6.2.1 Gesamturteil
- Die klare, robuste Bestaetigung der Algen-Hypothese findet sich in Nursery.
- Dort ist Acanthuridae Holm-signifikant mit starkem Effekt.
- In Utumbi gibt es nur Trends, keine robuste Bestaetigung.
- In Milimani gibt es keine Unterstuetzung.

#### 6.2.2 Wo ist die Hypothese bestaetigt?

Nursery: Acanthuridae eindeutig bestaetigt
- Algae MaxN-Median: 22.0
- Fish MaxN-Median: 4.5
- p_raw = 0.0070
- p_Holm = 0.0278
- Cliffs Delta = 1.0
- Interpretation: Hier ist die Hypothese klar bestaetigt.

#### 6.2.3 Wo ist die Hypothese nur bedingt bestaetigt?

Nursery: Siganidae als Trend
- Algae MaxN-Median: 4.0
- Fish MaxN-Median: 1.0
- p_raw = 0.0104
- p_Holm = 0.3373
- Cliffs Delta = 0.5
- Interpretation: biologisch plausibler Algen-Trend, aber nach Holm nicht robust.

Utumbi: Scaridae und Siganidae als Trends
- Scaridae: Algae 11.0 vs Fish 7.0, p_raw = 0.1743, p_Holm = 0.6970, Cliffs Delta = 0.333
- Siganidae: Algae 2.0 vs Fish 1.0, p_raw = 0.2845, p_Holm = 0.8535, Cliffs Delta = 0.20
- Interpretation: Richtung stimmt teilweise, aber der statistische Nachweis ist zu schwach.

#### 6.2.4 Wo gibt es keine klare Aussage?

Milimani
- Acanthuridae: Fish deutlich hoeher als Algae (22.5 vs 5.0)
- Scaridae: Fish leicht hoeher als Algae (6.0 vs 5.0)
- Siganidae: kein Unterschied
- Blenniidae: sehr geringe Werte
- Interpretation: keine Bestaetigung der Algen-Hypothese.

Blenniidae an allen Standorten
- keine robuste Algen-Bestaetigung
- Werte sind zu niedrig oder zu unbalanciert, um einen klaren Algen-Effekt abzusichern

#### 6.2.5 Zusammenfassung des MaxN-Fokus

Wo wird die Hypothese bestaetigt?
- Vor allem in Nursery, und dort besonders fuer Acanthuridae.

Wo nur bedingt?
- Bei Siganidae und Scaridae in Utumbi und Nursery zeigen sich Richtungseffekte, aber keine robuste Holm-Signifikanz.

Wo keine klare Aussage?
- Milimani sowie Blenniidae im gesamten Datensatz.

### 6.3 Herbivore Feeding-Responsiveness

Quelle: [herbivore_analysis/herbivore_feeding_responsiveness.md](herbivore_analysis/herbivore_feeding_responsiveness.md)

Hier geht es nicht um MaxN, sondern um die Frage:
- Zeigen Herbivore bei Algenkoedern haeufiger Feeding als bei Fischkoedern?

#### 6.3.1 Gesamturteil
- Nursery zeigt eine robuste Bestaetigung.
- Milimani und Utumbi zeigen nur sehr schwache oder keine Signale.

#### 6.3.2 Wo ist die Hypothese bestaetigt?

Nursery
- Algae Feeding-Rate: 0.2038
- Fish Feeding-Rate: 0.0000
- p_raw = 0.005709
- p_Holm = 0.017126
- Cliffs Delta = 1.0
- Interpretation: Hier wird die Hypothese klar bestaetigt.

#### 6.3.3 Wo nur bedingt?

Milimani
- Algae Feeding-Rate: 0.0029
- Fish Feeding-Rate: 0.0000
- p_raw = 0.317628
- p_Holm = 0.550985
- Interpretation: kleine Richtung, aber keine statistische Stuetze.

Utumbi
- Algae Feeding-Rate: 0.0030
- Fish Feeding-Rate: 0.0000
- p_raw = 0.275492
- p_Holm = 0.550985
- Interpretation: ebenfalls keine robuste Bestaetigung.

#### 6.3.4 Was bedeutet das biologisch?

- In Nursery werden Algenkoeder von Herbivoren nicht nur praesentieller, sondern auch aktiv als Futterreiz genutzt.
- Das ist inhaltlich naeher an der eigentlichen Hypothese als ein reines MaxN-Mass.

### 6.4 Funktionsvergleich mit Feeding-Filter

Quelle: [funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md](funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md)

#### 6.4.1 Warum ist das wichtig?

- Der Standard-Funktionsvergleich fand primaer Gruppen, die bei Fischkoedern haeufiger sind.
- Der Feeding-Filter fragt eine andere biologische Ebene: Welche Gruppen fressen bei Algenkoedern mehr?

#### 6.4.2 Welche Gruppen wurden dort verglichen?

- herbivore_core_families = Siganidae, Acanthuridae, Scaridae, Blenniidae
- herbivore_extended_with_damselfishes = herbivore Kernfamilien plus kleinere Damselfish-nahe Gruppen
- piscivore_core_families = Serranidae, Lutjanidae, Muraenidae, Sphyraenidae, Aulostomidae, Fistulariidae
- invertivore_general = Triggerfische, Wrasses und verwandte Gruppen
- word_group::snappers = Lutjanidae
- word_group::triggerfishes = Balistidae
- family::acanthuridae = Surgeonfische
- family::siganidae = Rabbitfische
- family::lutjanidae = Snappers
- family::balistidae = Triggerfische

#### 6.4.3 Wo wird die Algen-Hypothese beim Feeding zumindest in Richtung bestaetigt?

Nursery
- composite::herbivore_core_families: Algae 16.0, Fish 0.0, p_raw 0.0112, p_Holm 0.218, Cliffs Delta 1.0
- composite::herbivore_extended_with_damselfishes: Algae 16.0, Fish 0.0, p_raw 0.0112, p_Holm 0.218, Cliffs Delta 1.0
- family::acanthuridae: Algae 11.0, Fish 0.0, p_raw 0.0114, p_Holm 0.218, Cliffs Delta 1.0
- family::siganidae: Algae 1.5, Fish 0.0, p_raw 0.0104, p_Holm 0.218, Cliffs Delta 1.0

Interpretation:
- Die Richtung ist sehr klar: Herbivore fressen in Nursery mehr bei Algenkoedern.
- Die Holm-Korrektur ueber viele Gruppen macht die Befunde jedoch formal nicht signifikant.
- Inhaltlich ist das ein starkes, aber noch nicht ganz formal robustes Algen-Signal.

#### 6.4.4 Wo spricht der Feeding-Filter gegen die Algen-Hypothese?

Utumbi
- family::balistidae und word_group::triggerfishes: Algae 0.0, Fish 3.0, p_Holm 0.050
- piscivore_core_families: Algae 0.0, Fish 3.0, p_Holm 0.106

Milimani
- fast alle Gruppen mit sehr geringer Feeding-Aktivitaet
- keine klare Richtung fuer Algen oder Fisch

#### 6.4.5 Was bedeutet das fuer die Leitfrage?

1. Algenfressende Taxa koennen bei Algenkoedern tatsaechlich mehr Feeding zeigen.
2. Das ist am klarsten in Nursery sichtbar.
3. Die Wirkung ist nicht universell, sondern standortabhaengig.

### 6.5 Durchgefuehrter Zusatztest 2: Einheitliches Bait x Standort-Interaktionsmodell

Quelle: [core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.md](core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.md)

Fragestellung:
- Bleiben Bait-Effekte bestehen, wenn zentrale Endpunkte in einem einheitlichen Modell mit Standort und Interaktion getestet werden?

Modell und Testlogik:
- Modell: log1p(y) ~ bait_type + site + bait_type:site
- Permutation: Bait-Labels innerhalb der Standorte (site-stratifizierte Nullhypothese)
- Endpunkte: species_richness, maxn_video_peak, total_feeding_events, total_interested_events, herbivore_core_total_maxn sowie die vier Herbivore-Familien
- Datengrundlage fuer das Modell: 38 Videos mit fish/algae-Koedern (controls ausgeschlossen)

Hauptergebnisse (BH-korrigiert):
- Signifikante Bait-Effekte: 3 von 9 Endpunkten
  - total_feeding_events: p_perm = 0.00010, q_BH = 0.00090, Richtung fish > algae
  - herbivore_core_total_maxn: p_perm = 0.00290, q_BH = 0.00870, Richtung fish > algae
  - herbivore_acanthuridae_maxn: p_perm = 0.00020, q_BH = 0.00090, Richtung fish > algae
- Signifikante Bait x Standort-Interaktionen: 3 von 9 Endpunkten
  - total_feeding_events: p_perm = 0.00010, q_BH = 0.00090
  - herbivore_core_total_maxn: p_perm = 0.00090, q_BH = 0.00270
  - herbivore_acanthuridae_maxn: p_perm = 0.00020, q_BH = 0.00090
- Nicht robust signifikant: species_richness, maxn_video_peak, total_interested_events, siganidae, scaridae, blenniidae

Interpretation:
- Der globale Bait-Haupteffekt ist nicht einheitlich ueber alle Endpunkte, sondern konzentriert sich auf Feeding und Herbivore-MaxN.
- Gleichzeitig zeigen genau diese Endpunkte robuste Interaktionen, also klare Standortabhaengigkeit der Effektstaerke.
- Damit wird die Kernbotschaft geschaerft: Es gibt einen realen Fish-vs-Algae-Struktureffekt, aber seine Auspraegung ist kontextabhaengig und nicht als universeller Einheits-Effekt zu lesen.

---

## 7. Sichtweite (Visibility): bivariates Signal vs. adjustierte Modelle

Quellen:
- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_additional_tests_summary.md](visibility_analysis/visibility_additional_tests_summary.md)
- [visibility_analysis/visibility_site_stratified_tests_summary.md](visibility_analysis/visibility_site_stratified_tests_summary.md)
- [visibility_analysis/visibility_plausibility_audit.md](visibility_analysis/visibility_plausibility_audit.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

### 7.1 Bivariat (signifikant)

- species_richness: rho = 0.563, BH q = 0.000138
- maxn_video_peak: rho = 0.467, BH q = 0.00161
- first_seen_median_sec: kein signifikanter Zusammenhang

### 7.2 Adjustiert (nicht robust signifikant)

- Kein Endpunkt mit robustem Sicht-Effekt nach Kontrolle fuer Standort + Koeder.
- Zusatztests (blockierte Permutation, Nichtlinearitaet, Quantilsregression) bestaetigen das Gesamtbild.

### 7.3 Zusatztests und standort-stratifizierte Modelle

- Die erweiterten Sicht-Zusatztests liefern keinen robust signifikanten Effekt nach Korrektur.
- Fuer die standort-stratifizierten Modelle bleibt ebenfalls kein Standort-Endpunkt-Test FDR-robust signifikant.
- Die Plausibilitaetspruefung bestaetigt die interne Konsistenz der Sicht-Analysen und stuetzt die Schlussfolgerung, dass Sicht keinen unabhaengigen Treiber-Effekt auf die Endpunkte liefert.

Kernaussage:
- Sicht hat deskriptive Relevanz im Rohmuster.
- Fuer inferenzielle Aussagen ist Standort-/Koederkontrolle entscheidend.

---

## 8. Gesamtinterpretation entlang der Leitfrage

### 8.1 Wo wird die Algenfresser-Hypothese bestaetigt?

Am klarsten in Nursery:
- MaxN: Acanthuridae sind Holm-signifikant hoeher bei Algenkoedern.
- Feeding: Herbivore-Kernfamilien zeigen deutlich mehr Feeding bei Algenkoedern.

Das ist die staerkste Bestaetigung im gesamten Datensatz.

### 8.2 Wo nur bedingt?

Utumbi zeigt vor allem Trends:
- Scaridae und Siganidae reagieren teilweise in die erwartete Richtung.
- Die Signale sind aber nicht robust genug, um sie als gesichert zu bezeichnen.

### 8.3 Wo keine klare Aussage?

Milimani ist fuer die Algen-Hypothese insgesamt schwach:
- keine robuste Algen-Bevorzugung
- teils gegenteilige Richtung im MaxN
- Feeding zu selten, um stabile Aussagen zu erlauben

### 8.4 Was ist die Gesamtbotschaft?

1. Standort ist der staerkste Erklaerer.
2. Der Standard-Funktionsvergleich findet vor allem fish > algae.
3. Das einheitliche Interaktionsmodell bestaetigt robuste Bait- und Interaktionseffekte fuer feeding_total, herbivore_core_total_maxn und acanthuridae.
4. Diese Effekte sind standortabhaengig und damit nicht universell uebertragbar.
5. Im eng gefassten a-priori Herbivore-Fokus bleibt Nursery weiterhin der staerkste Kontext fuer die Algenhypothese.

---

## 9. Methodische Grenzen und offene Punkte

1. Multiple-Test-Belastung bei hoher Taxonzahl
- Viele parallele Tests reduzieren die Chance auf korrigierte Signifikanz fuer Einzeleffekte.

2. Unbalancierte Zellgroessen
- Unterschiedliche n je Standort/Koeder erschweren feinaufgeloeste Inferenz.

3. Unterschied zwischen Verhalten und Abundanz
- MaxN und Feeding messen nicht dasselbe.

4. Hierarchische Modellierung
- Mixed-Effects-Modelle koennen Video-, Standort- und Koederebene integrierter trennen.

5. Standortabhaengige Oekologie
- Es ist plausibel, dass die gleiche Art an einem Standort stark reagiert und an einem anderen kaum.

### 9.1 Priorisierte Zusatztests und bereits durchgefuehrte Sensitivitaetschecks

1. PERMDISP je Standort fuer den Koeder-Kompositionsvergleich
- Ziel: Trennen, ob PERMANOVA-Signale eher durch Gruppenverschiebung oder unterschiedliche Dispersion getrieben sind.
- Mehrwert: Direktere, methodisch sauberere Interpretation der Koedereffekte auf Community-Struktur.

2. Bereits durchgefuehrt: Systematische Leave-one-video-out-Sensitivitaet
- Fokus: robusteste und biologisch zentrale Befunde (v. a. Nursery-Herbivore, Fish-vs-Algae-Hauptsignale).
- Ergebnis: Die Kernsignale bleiben auch nach Entfernen eines einzelnen Videos stabil.
- Nursery Acanthuridae: LOO-p-Werte 0.0079-0.0138, also durchgehend signifikant.
- Coral-Reef-Fish-vs-Algae-Familien: Labridae, Balistidae und Muraenidae bleiben unter jedem einzelnen Videoremoval signifikant.
- Mehrwert: Zeigt explizit, dass einzelne Videos die Kernaussagen nicht dominieren.

Hinweis: Zusatztest 2 (einheitliches Bait x Standort-Interaktionsmodell) wurde inzwischen durchgefuehrt und in Abschnitt 6.5 dokumentiert.

3. Bootstrap-Konfidenzintervalle fuer priorisierte Effektgroessen
- Effektgroessen: Cliff's Delta und Mittelwert-/Mediandifferenzen.
- Mehrwert: Unsicherheit und Praezision der Effekte werden transparent statt nur p-wert-basiert.

4. Praevalenz-/Occupancy-Analysen mit Mindestnachweis-Schwellen
- Ziel: Trennung von seltenen Peak-Taxa gegenueber stabil haeufig nachgewiesenen Taxa.
- Mehrwert: Robustere biologische Einordnung, welche Taxa konsistent auf Koeder reagieren.

5. Erweiterte Mehrfachtest-Sensitivitaet als Standardreport
- Neben Holm systematisch BH/FDR fuer alle Haupttabellen und priorisierte Familien.
- Mehrwert: Vergleich von konservativer (Holm) und entdeckungsorientierter (FDR) Evidenzstufe.

6. Praesenz/Absenz-Modelle fuer seltene, biologisch wichtige Taxa
- Methodisch: logistische/Fisher-basierte Tests zusaetzlich zu MaxN.
- Mehrwert: Bessere Aussage bei Null-lastigen Daten, in denen MaxN allein instabil sein kann.

7. Bereits durchgefuehrt: Hurdle-Modell fuer fokussierte Signale
- Quelle: [hurdle_model/hurdle_model_focal_signals.md](hurdle_model/hurdle_model_focal_signals.md)
- Ergebnisbild: Effekte lassen sich sauber in Praesenz- und Intensitaetskomponente aufteilen; fuer mehrere Schluesselsignale liegt die Hauptinformation im Intensitaetsteil, waehrend Muraenidae ein klares Praesenzsignal zeigt.
- Mehrwert: Konsistente methodische Bruecke zwischen Praesenz-/Absenz-Check und MaxN-basierten Tests.

---

## 10. Quellenverzeichnis

- Standort-Haeufigkeit:
  - [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)
- Koeder-Haeufigkeit:
  - [taxahaeufigkeitkoeder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)
- Koeder-Komposition:
  - [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)
- Standard-Funktionsvergleich:
  - [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)
- Herbivore-MaxN a priori:
  - [herbivore_analysis/herbivore_maxn_apriori_test.md](herbivore_analysis/herbivore_maxn_apriori_test.md)
- Herbivore-Feeding-Responsiveness:
  - [herbivore_analysis/herbivore_feeding_responsiveness.md](herbivore_analysis/herbivore_feeding_responsiveness.md)
- Funktionsvergleich mit Feeding-Filter:
  - [funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md](funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md)
- Algae-Responsiveness (explorativer Reverse-Focus):
  - [algae_responsiveness/algae_responsiveness_summary.md](algae_responsiveness/algae_responsiveness_summary.md)
- Einheitliches Bait x Standort-Interaktionsmodell (Kern-Endpunkte):
  - [core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.md](core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.md)
- Sichtanalyse:
  - [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
  - [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
  - [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)
- Hurdle-Modell (Praesenz + Intensitaet):
  - [hurdle_model/hurdle_model_focal_signals.md](hurdle_model/hurdle_model_focal_signals.md)

---

## Plausibilitaetsnotiz

Diese Fassung trennt bewusst zwischen robusten Aussagen, bedingten Aussagen und explorativen Signalen.
Damit sind Ueberinterpretationen einzelner Rohsignale vermeidbar, ohne informative Muster zu verlieren. Die Leitfrage wird an den Daten entlang beantwortet: Algenfressende Taxa zeigen in Nursery die klarste und biologisch sinnvollste Reaktion auf Algenkoeder; an den anderen Standorten bleibt das Bild deutlich schwächer oder uneinheitlich.
