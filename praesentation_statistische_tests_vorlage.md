# Statistische Gesamtauswertung: Standort, Koeder, Verhalten und funktionelle Reaktionen

Stand: 2026-04-28

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

### 2.5 Species-Richness-Zusatzauswertung

Quelle: [species_richness_report/species_richness_additional_tests.md](species_richness_report/species_richness_additional_tests.md)

Ergebnisbild:
- Der Standort ist fuer Species Richness robust signifikant, sowohl im Kruskal-Wallis-Test als auch in der Permutation.
- Der Koeder-Faktor ist dagegen global nicht signifikant.
- Auch paarweise bleibt der Standortkontrast deutlich, waehrend fuer Koeder nach Korrektur keine robusten Unterschiede mehr uebrig bleiben.

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
3. Wenn man die biologische Hypothese gezielt auf Herbivore und Feeding fokussiert, entsteht ein klares Bild: Nursery bestaetigt die Algenhypothese deutlich.
4. Der Effekt ist also real, aber nicht universell ueber alle Standorte.

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
- Sichtanalyse:
  - [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
  - [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
  - [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

---

## Plausibilitaetsnotiz

Diese Fassung trennt bewusst zwischen robusten Aussagen, bedingten Aussagen und explorativen Signalen.
Damit sind Ueberinterpretationen einzelner Rohsignale vermeidbar, ohne informative Muster zu verlieren. Die Leitfrage wird an den Daten entlang beantwortet: Algenfressende Taxa zeigen in Nursery die klarste und biologisch sinnvollste Reaktion auf Algenkoeder; an den anderen Standorten bleibt das Bild deutlich schwächer oder uneinheitlich.
