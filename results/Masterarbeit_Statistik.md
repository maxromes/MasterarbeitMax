# Masterarbeit_Statistik

Stand: 2026-08-24

Dieses Dokument ordnet die vorhandenen statistischen Ergebnisse entlang der zentralen Ziele und Hypothesen der Arbeit.
Es trennt zwischen:
- Kernbefunden fuer den Ergebnisteil
- erwaehnenswerten Zusatzbefunden fuer Einordnung und Diskussion
- Material, das methodisch wichtig ist, aber in den Anhang gehoert

Die Formulierungen sind so geschrieben, dass sie direkt in die Masterarbeit uebernommen und im Diskussionsteil weiter eingeordnet werden koennen.

---

## 0. Analyse-Setup und Vergleichslogik (vollstaendig)

Dieser Abschnitt dokumentiert explizit, welche Fragen mit welcher statistischen Analyse beantwortet wurden, welche Gruppen konkret gegeneinander getestet wurden und auf welcher Dateneinheit die Tests laufen.

### 0.1 Dateneinheiten und Grundregeln

1. Primaere Inferenz-Einheit ist das Video.
2. Standorte: milimani, utumbi, nursery.
3. Taxonbildung in den allgemeinen Community-Analysen: species > genus > family/label.
4. MaxN-Analysen basieren auf Peak-Haeufigkeiten pro Taxon/Familie und Zeitpunkt.
5. Feeding/Interested wurden als Verhaltensannotation ausgewertet, mit zusaetzlicher MaxN-konsistenter Sensitivitaetspruefung.

### 0.2 Exakte Koederstruktur je Standort

| standort | koeder im Datensatz | primaere Analysekontraste |
|:--|:--|:--|
| milimani | control, fischmix, mackerel, sargassum, ulva_salad, ulva_gutweed | global all-koeder; paarweise je Koeder; gruppiert fish vs algae |
| utumbi | control, fischmix, mackerel, sargassum, ulva_salad, ulva_gutweed | global all-koeder; paarweise je Koeder; gruppiert fish vs algae |
| nursery | control, mackerel, algaemix, algae_strings | global all-koeder; paarweise je Koeder; algae_strings vs algaemix; algaemix vs mackerel |

### 0.3 Fish-vs-Algae Mapping (modelluebergreifend)

1. fish: mackerel, fischmix.
2. algae: sargassum, ulva_salad, ulva_gutweed, algaemix, algae_strings.
3. control: separat; in fish-vs-algae-Modellen ausgeschlossen.

### 0.4 Welche Analyse beantwortet welche Frage?

| analyseblock | hauptfrage | response/endpoint | testtyp | gruppierung |
|:--|:--|:--|:--|:--|
| Artenzusammensetzung (H1) | Veraendert Koeder die Community-Komposition innerhalb eines Standorts? | Presence/Absence-Vektoren je Video | PERMANOVA (Jaccard), plus PERMDISP | je Standort ueber alle Koeder; zusaetzlich fish vs algae (Riff) |
| Herbivore-MaxN (H2) | Sind Herbivore unter Algenkoedern dichter als unter Fischkoedern? | family-level MaxN je Video (4 Herbivore-Familien) | gerichteter Mann-Whitney (algae > fish), Holm je Standort | je Standort, familienweise |
| Herbivore-Feeding (H3) | Zeigen Herbivore mehr Feeding unter Algenkoedern? | feeding_rate je Video | gerichteter Mann-Whitney (algae > fish), Holm ueber Standorte | je Standort |
| Feeding-Sensitivitaet (H3-robust) | Bleibt H3 stabil unter MaxN-konsistenter Definition? | feeding_maxn_sum, family_presence je Video | gerichteter Mann-Whitney, Holm ueber Standorte | je Standort |
| Hurdle-Modell (Mechanismus) | Praesenz- vs Intensitaetsmechanismus? | Praesenz + log1p(Intensitaet) | 2-stufiges Hurdle-Modell, BH | fokussierte Signale |
| LOO-Sensitivitaet | Wird ein Befund von Einzelvideos getrieben? | Effekt/P-Wert pro LOO-Lauf | wiederholte Refit-Tests | je Schluesselbefund |
| Bootstrap-Effektgroessen | Wie praezise sind priorisierte Effekte? | mean differences + CI | Bootstrap-CI | priorisierte Kontraste |

### 0.5 Multiple-Testing-Strategie

1. Holm (FWER) fuer kleine, a-priori Testfamilien (z. B. 3 Standorte oder 4 Familien je Standort).
2. BH/FDR fuer breitere explorative Testfamilien.
3. Roh-p-Werte werden nur als trendhaft interpretiert, wenn Holm/BH nicht signifikant sind.

### 0.6 Exakte Vergleichspaare nach Analyse

1. Community-Komposition (H1):
- Global je Standort: alle Standort-Koeder gleichzeitig.
- Paarweise je Standort: alle Koederpaare im Standort.
- Gruppiert: fish vs algae in milimani und utumbi.
2. Nursery-Methodikvergleich:
- algae_strings vs algaemix.
- algaemix vs mackerel.
- algae_strings vs algaemix vs mackerel.
- control nur explorativ (n=1).
3. Herbivore H2/H3:
- je Standort algae (alle Algenkoeder) vs fish (alle Fischkoeder).
- fuer H2 pro Herbivore-Familie separat.
- fuer H3 auf Videoebene (Rate + Sensitivitaetsmetriken).

### 0.7 Verbindliche Farbcodierung (ohne Rot/Gruen)

Diese Farbcodierung ist fuer alle Statistikgrafiken verbindlich und wird konsistent ueber alle Analysebloecke verwendet.

1. Grundregel:
- Keine Rot-/Gruentoene in kategorialen Kodierungen.
- Nur farbenblindsichere Kontraste mit Blau, Orange, Violett, Braun, Tuerkis, Grau.

2. Standorte:
| element | hex |
|:--|:--|
| milimani | #4C78A8 |
| utumbi | #B279A2 |
| nursery | #F28E2B |

3. Koeder (global einheitlich):
| koeder | hex |
|:--|:--|
| mackerel | #1F77B4 |
| fischmix | #2F4B7C |
| sargassum | #F28E2B |
| ulva_gutweed | #76B7B2 |
| ulva_salad | #B279A2 |
| algae_strings | #8F63B8 |
| algaemix | #9C755F |
| control | #9D9D9D |

4. Short-Control-Video (nursery, 20240108-nursery-control.csv):
- Farbe: #9D9D9D (neutral grau).
- Zusaetzliche Formkodierung in Plots: gestrichelte Kontur oder Marker-Hinweis "CTRL-short".
- Inferenzregel bleibt unveraendert: nur explorativ, nicht gleichwertig mit Hauptkontrasten.

5. Richtungs- und Evidenzkodierung:
| bedeutung | hex |
|:--|:--|
| fish > algae | #4C78A8 |
| algae > fish | #F28E2B |
| robust | #4C78A8 |
| bedingt | #F28E2B |
| teilweise | #9C755F |
| explorativ | #B279A2 |

6. Sequentielle Heatmaps:
- Bevorzugt: cividis (oder cividis_r), da farbenblindsicher und ohne Rot/Gruen.
- Divergierende Richtungs-Heatmaps: PuOr statt Rot-Blau-Skalen.

---

## 1. Ziel-Hypothesen-Matrix mit Priorisierung

## Aim 1 / H1

Fragestellung:
- Beeinflusst der Koeder die Zusammensetzung der BRUVS-Gemeinschaften, getrennt nach Milimani, Utumbi und dem separaten Nursery-Experiment?

### 1.0 Was wurde genau getestet?

1. Dateneinheit: Video (Presence/Absence je Taxon im Video).
2. Teststruktur:
- Globaltest pro Standort: PERMANOVA auf Jaccard-Distanzen mit Faktor koeder.
- Paarvergleiche: Koeder A vs Koeder B innerhalb desselben Standorts.
- Zusatztest: PERMDISP zur Pruefung, ob Signale (teilweise) aus unterschiedlichen Streuungen statt Zentroid-Lagen stammen.
3. Kontrastlogik:
- Milimani und Utumbi: sowohl all-koeder als auch gruppiert fish vs algae.
- Nursery: all-koeder und paarweise Koederkontraste inkl. algae_strings vs algaemix.

### 1.1 Kernbefunde (Haupttext)

1. Standort-spezifische PERMANOVA (Jaccard, Presence/Absence) je Standort:
- Milimani: p = 0.0242
- Utumbi: p = 0.0046
- Nursery: p = 0.0016
- Schluss: In allen drei Systemen ist der globale Koedereffekt auf die Artenzusammensetzung statistisch signifikant.

2. Primärer Riffvergleich mit gruppiertem Kontrast fish vs algae:
- Milimani: p = 0.0080
- Utumbi: p = 0.0044
- Schluss: Auch im biologisch fokussierten fish-vs-algae-Vergleich bleibt der Kompositionseffekt in beiden Riffstandorten signifikant.

### 1.2 Erwaehnenswert (Diskussion)

1. Trotz global signifikanter PERMANOVA waren einzelne paarweise Koedervergleiche nach Holm meist nicht signifikant.
- Interpretation: Der Effekt ist eher multivariat verteilt als durch ein einzelnes Koederpaar dominiert.

2. Die staerkere Standortstruktur der Gesamtfauna bleibt als Hintergrundtreiber relevant.
- Interpretation: Koedereffekte muessen standortkontextualisiert interpretiert werden.

3. PERMDISP-Zusatztest (Jaccard-basiert) zeigt in allen Standorten signifikante Streuungsunterschiede zwischen Koedern.
- Milimani: p = 0.0042, q_BH = 0.0063
- Utumbi: p = 0.0176, q_BH = 0.0176
- Nursery: p = 0.0018, q_BH = 0.0054
- Interpretation: Die PERMANOVA-Signale koennen nicht rein als Lageverschiebung interpretiert werden; ein Teil der Evidenz wird durch unterschiedliche multivariate Streuung mitgetragen.

### 1.3 In den Anhang

1. Vollstaendige Paarvergleichstabellen je Standort
2. Overlap- und koederspezifische Taxalisten je Standort
3. Alle Exporttabellen aus [results/artenvergleich_köder/artenvergleich_koeder_summary.md](results/artenvergleich_köder/artenvergleich_koeder_summary.md)
4. Zusatzreport zu PERMDISP und Rarefaction aus [results/composition_robustness/composition_robustness_open_tests.md](results/composition_robustness/composition_robustness_open_tests.md)

---

## Aim 2 / H2

Fragestellung:
- Erhoehen Makroalgenkoeder die MaxN-Werte der herbivoren Familien (Siganidae, Acanthuridae, Scaridae, Blenniidae) gegenueber Fischkoedern, und ist dieser Effekt standortabhaengig?

### 2.0 Was wurde genau getestet?

1. Dateneinheit: Video; Outcome je Familie = family-MaxN.
2. Familien: Siganidae, Acanthuridae, Scaridae, Blenniidae.
3. Kontrast pro Standort: algae (alle Algenkoeder) > fish (mackerel/fischmix).
4. Test: gerichteter Mann-Whitney U je Familie; Holm-Korrektur innerhalb des Standorts ueber die 4 Familien.
5. Erweiterte Mechaniktests:
- Hurdle: getrennte Inferenz fuer Praesenz und positive Intensitaet.
- Presence/Absence und Prevalence-Threshold als Robustheitsrahmen.

### 2.1 Kernbefunde (Haupttext)

1. A-priori Herbivore-MaxN-Test (gerichtet: algae > fish; Holm je Standort):
- Nursery Acanthuridae: Algae-Median 22.0 vs Fish-Median 4.5, p_raw = 0.0070, p_Holm = 0.0278, Cliff's Delta = 1.0.
- Milimani und Utumbi: keine Holm-signifikanten Algae>Fish-Effekte fuer die vier Herbivore-Familien.
- Schluss: H2 wird robust fuer Acanthuridae in Nursery gestuetzt, nicht jedoch standortunabhaengig ueber alle Standorte.

2. Standortabhaengigkeit als zentrales Ergebnis:
- Das Muster variiert klar zwischen Standorten (starke Nursery-Unterstuetzung, schwache/fehlende Evidenz in Milimani und Utumbi).
- Schluss: Die erwartete Wirkung ist standortabhaengig und nicht generalisierbar als uniforme Gesamtantwort.

### 2.2 Erwaehnenswert (Diskussion)

1. Hurdle-Modell (Praesenz + Intensitaet) fuer fokussierte Signale:
- Nursery Acanthuridae: kein Praesenzunterschied (1.0 vs 1.0), aber starkes Intensitaetssignal (beta_log1p = 1.3477, p = 0.000002, q_BH = 0.000009).
- Interpretation: Der Algeneffekt ist hier primaer dichte-/intensitaetsgetrieben und nicht durch Nachweiswahrscheinlichkeit erklaert.

2. Presence/Absence-Check als Konsistenzpruefung:
- Acanthuridae in Nursery praesent in beiden Koedergruppen; kein Praevalenzsignal.
- Interpretation: konsistent mit einem Intensitaets- statt Occurrence-Mechanismus.

3. Leave-one-video-out-Sensitivitaet fuer den Schluesselbefund:
- Nursery Acanthuridae bleibt bei allen LOO-Laeufen signifikant (p-Bereich 0.0079-0.0138).
- Interpretation: Der Haupteffekt ist nicht durch ein einzelnes Video getrieben.

4. Bootstrap-CIs fuer priorisierte Effektgroessen (neu abgeschlossen):
- Nursery Acanthuridae bleibt auch in den 95%-Bootstrap-CIs klar positiv (mean diff 17.83; CI [11.67, 25.33]).
- Interpretation: Der zentrale H2-Befund ist nicht nur signifikant, sondern auch praezise und in der Effektgroesse substanziell.

### 2.3 In den Anhang

1. Vollstaendige Familienlisten je Standort inklusive nicht signifikanter Tests
2. Alle Effektgroessen-Detailtabellen
3. Vollstaendige Hurdle-Ausgabe aus [results/hurdle_model/hurdle_model_focal_signals.md](results/hurdle_model/hurdle_model_focal_signals.md)
4. Bootstrap-Tabellen aus [results/effectsize_bootstrap/prioritized_effectsize_bootstrap.md](results/effectsize_bootstrap/prioritized_effectsize_bootstrap.md)

---

## Aim 2 / H3

Fragestellung:
- Erhoehen Makroalgenkoeder die video-basierte Feeding-Response herbivorer Fische im Vergleich zu Fischkoedern?

### 3.0 Was wurde genau getestet?

1. Dateneinheit: Video mit Herbivore-Fokus (gleiche 4 Familien wie in H2).
2. Primaere Metrik: feeding_rate = feeding_count / total_herbivore_entries.
3. Primaerer Kontrast pro Standort: algae > fish (gerichtet).
4. Test: Mann-Whitney U, Holm ueber die 3 Standorttests.
5. Sensitivitaetsmetriken (automatisiert im gleichen Analyseblock):
- feeding_maxn_sum pro Video (Summe familienweiser Feeding-Maxima, MaxN-konsistent).
- feeding_family_presence pro Video (Anteil Herbivore-Familien mit >= 1 Feeding).
6. Zweck der Sensitivitaet: pruefen, ob die H3-Inferenz von einer event-count-Interpretation abhaengt.

### 3.1 Kernbefunde (Haupttext)

1. Herbivore Feeding Responsiveness (gerichtet: algae > fish; Holm ueber Standorte):
- Nursery: mean Feeding-Rate Algae = 0.2038 vs Fish = 0.0000, p_raw = 0.005709, p_Holm = 0.017126, Cliff's Delta = 1.0.
- Milimani: p_Holm = 0.5510 (nicht signifikant).
- Utumbi: p_Holm = 0.5510 (nicht signifikant).
- Schluss: H3 wird robust in Nursery gestuetzt, jedoch nicht in Milimani oder Utumbi.

2. Direktes Fazit zur Standortabhaengigkeit:
- Die Feeding-Reaktion auf Algenkoeder ist stark ortsgebunden; ein einheitlicher standortunabhaengiger Effekt wird nicht getragen.

### 3.2 Erwaehnenswert (Diskussion)

1. Interaktionsmodell ueber Kernendpunkte zeigt, dass Bait-Effekte bei Feeding-Ereignissen stark von Standortkontexten abhaengen.
2. Methodische Klarstellung zur Annotation: Feeding/Interested wurden in der Kodierung MaxN-nah erfasst (Peak-orientierte Frames), daher ist die reine Event-Zaehlung nur eingeschraenkt als "Frequenz ueber Zeit" interpretierbar.
3. Sensitivitaetscheck mit MaxN-konsistenter Feeding-Metrik (pro Video: Summe familienweiser Feeding-Maxima) bestaetigt den Nursery-Befund:
- Nursery: mean Algae = 13.83 vs Fish = 0.00, p_raw = 0.005709, p_Holm = 0.017126.
- Alternative robuste Metriken zeigen dasselbe Muster (z. B. family_presence mit p_Holm = 0.013016).
- Schluss: Die H3-Inferenz fuer Nursery bleibt in Richtung und Signifikanz stabil; es liegt kein Artefakt der bisherigen Event-Zaehlung vor.
4. Hierarchischer Mixed-Effects-Zusatztest auf Kernendpunkten (Random Intercept Standort):
- first_seen_median_sec zeigt einen robusten fish-vs-algae-Effekt (Beta = -0.4665, q_Holm = 0.000417), konsistent mit frueheren Erstnachweisen unter fish.
- Fuer species_richness und maxn_video_peak bleiben keine robusten fish-vs-algae-Effekte (q_Holm >= 0.2626).
- Interpretation: Fish-vs-algae ist im hierarchischen Rahmen endpoint-spezifisch und nicht als uniforme Gesamtantwort ueber alle Kernendpunkte zu lesen.

5. Prevalence-Threshold-Analyse (neu abgeschlossen):
- Family-level-Occupancy mit Mindestnachweis-Schwellen zeigt nach BH/Holm je Standort kein robust signifikantes Richtungssignal (min q_Holm = 0.1199).
- Interpretation: Die zentrale H3-Evidenz bleibt ein Intensitaets-/Rate-Effekt (Feeding), nicht ein breit robuster Praevalenz-Effekt.

### 3.3 In den Anhang

1. Standortweise Verteilungsplots und alle Zwischenkennzahlen der Feeding-Raten
2. Vollstaendige Vergleichstabellen aus [results/herbivore_analysis/herbivore_feeding_responsiveness.md](results/herbivore_analysis/herbivore_feeding_responsiveness.md)
3. Occupancy-Threshold-Tabellen aus [results/prevalence_threshold_model/prevalence_threshold_model.md](results/prevalence_threshold_model/prevalence_threshold_model.md)

---

## 4. Praezise, uebernehmbare Ergebnisformulierungen

Die folgenden Formulierungen sind fuer den Ergebnisteil geeignet.

## 4.1 Formulierung zu H1 (Komposition)

"Die standortspezifischen PERMANOVA-Analysen auf Jaccard-Distanzen zeigten in allen drei Untersuchungssettings signifikante Koedereffekte auf die Artenzusammensetzung (Milimani: p = 0.0242; Utumbi: p = 0.0046; Nursery: p = 0.0016). Im primaeren Riffvergleich blieb auch der gruppierte Kontrast zwischen Fisch- und Algenkoedern signifikant (Milimani: p = 0.0080; Utumbi: p = 0.0044). Ergaenzende PERMDISP-Tests waren ebenfalls in allen Standorten signifikant (BH-korrigiert), was auf zusaetzliche Streuungsunterschiede zwischen Koedern hinweist. Damit wird H1 unterstuetzt: Koederbehandlung beeinflusst die Zusammensetzung der BRUVS-Assemblagen, wobei die Evidenz standortspezifisch interpretiert wird und Lage- sowie Streuungskomponenten gemeinsam zu diskutieren sind." 

## 4.2 Formulierung zu H2 (Herbivore-MaxN)

"Im a-priori-Test der vier herbivoren Familien zeigte sich ein robustes Algen-Signal ausschliesslich fuer Acanthuridae in Nursery (Median Algae = 22.0 vs Median Fish = 4.5; p_raw = 0.0070; p_Holm = 0.0278; Cliff's Delta = 1.0). In Milimani und Utumbi wurden fuer die Herbivore-Familien keine Holm-signifikanten Algae>Fish-Effekte nachgewiesen. H2 wird damit partiell bestaetigt und ist klar standortabhaengig." 

## 4.3 Formulierung zu H3 (Feeding-Response)

"Die video-basierte Herbivore-Feeding-Response war in Nursery unter Algenkoedern signifikant hoeher als unter Fischkoedern (Rate-Metrik: mean 0.2038 vs 0.0000; p_raw = 0.005709; p_Holm = 0.017126; Cliff's Delta = 1.0). Eine MaxN-konsistente Sensitivitaetsmetrik bestaetigte denselben Befund (Feeding-MaxN-Summe: mean 13.83 vs 0.00; p_raw = 0.005709; p_Holm = 0.017126). In Milimani und Utumbi traten keine signifikanten Unterschiede auf (jeweils p_Holm = 0.5510). H3 wird somit fuer Nursery bestaetigt, jedoch nicht als standortunabhaengiges Muster." 

## 4.4 Formulierung zu Robustheit und Mechanismus

"Die Zusatzanalysen praezisieren den Wirkmechanismus: Das Hurdle-Modell zeigte fuer Nursery-Acanthuridae keinen Praesenzunterschied, aber einen hochsignifikanten Intensitaetseffekt (beta_log1p = 1.3477; q_BH = 0.000009), was fuer einen dichtebasierten statt rein praevalenzbasierten Koedereffekt spricht. Zusaetzlich blieb der Nursery-Acanthuridae-Befund in der systematischen Leave-one-video-out-Sensitivitaet durchgehend signifikant (p = 0.0079-0.0138), wodurch eine Dominanz einzelner Ausreisservideos unwahrscheinlich ist." 

---

## 5. Was in die Diskussion gehoert (gezielte Leitpunkte)

1. Oekologische Kontextualisierung der Standortabhaengigkeit
- Warum Nursery eine starke Algenantwort zeigt, Milimani/Utumbi jedoch nicht konsistent.

2. Mechanistische Trennung von Occurrence und Intensitaet
- Schwerpunkt: Algeneffekte muessen nicht ueber haeufigeres Auftreten laufen, sondern koennen als staerkere Auspraegung bei vorhandenen Taxa auftreten.

3. Abgleich zwischen globalen und fokussierten Tests
- Global fish-orientierte Muster in breiten Funktionsanalysen versus a-priori Herbivore-Response in Nursery.

4. Inferenzgrenzen
- Kleine und unbalancierte Zellgroessen, Mehrfachtest-Last, und standortabhaengige Generalisierbarkeit.

5. Lage- vs. Streuungseffekte in der Komposition
- Signifikante PERMDISP-Befunde in allen Standorten bedeuten, dass PERMANOVA nicht als reiner Zentroid-Effekt gelesen werden darf.
- Interpretation der Koedereffekte deshalb immer gemeinsam mit Dispersion und Samplingstruktur.

6. Hierarchische Modellierung als Robustheitsbaustein
- Mixed-Effects-Ergebnisse bestaetigen die starke Kontextabhaengigkeit: robuste fish-vs-algae-Signale sind nicht ueber alle Endpunkte konsistent.
- Fuer Gesamtinferenz deshalb immer Kombination aus standortgetrennten Haupttests und hierarchischem Zusatzmodell berichten.

---

## 6. Update-Protokoll fuer kuenftige Statistiken

Damit [results/Masterarbeit_Statistik.md](results/Masterarbeit_Statistik.md), [results/praesentation_statistische_tests_vorlage.md](results/praesentation_statistische_tests_vorlage.md) und der Grafikordner konsistent bleiben, gilt bei jeder neuen Analyse folgender Workflow:

1. Neue Statistik zuerst in einen eigenen Ergebnisordner schreiben (inkl. CSV + MD + falls sinnvoll Plot).
2. In [results/praesentation_statistische_tests_vorlage.md](results/praesentation_statistische_tests_vorlage.md) nur die inferenziell wichtigsten Kennzahlen ergaenzen (Effektrichtung, p/q, Effektgroesse, Stichprobengroessen).
3. In [results/Masterarbeit_Statistik.md](results/Masterarbeit_Statistik.md) sofort neu einordnen:
- Kernbefund
- erwaehnenswert
- Anhang
4. In [results/ergaenzende_statistische_grafiken/README.md](results/ergaenzende_statistische_grafiken/README.md) die neue Abbildung mit Kurzinterpretation aufnehmen.
5. Konsistenzcheck vor Abschluss:
- Stimmen Zahlen zwischen Detailreport, Hauptreport und dieser Priorisierungsvorlage ueberein?
- Sind Richtung und Hypothesentest (gerichtet/ungerichtet) korrekt benannt?
- Wurde klar markiert, ob ein Befund robust (korrigiert signifikant), bedingt oder explorativ ist?

Empfohlene Versionsregel:
- Bei jeder inhaltlichen Aenderung das Stand-Datum oben in diesem Dokument aktualisieren.

---

## 7. Direkt zugeordnete Quellreports

- Komposition/PERMANOVA: [results/artenvergleich_köder/artenvergleich_koeder_summary.md](results/artenvergleich_köder/artenvergleich_koeder_summary.md)
- Herbivore MaxN: [results/herbivore_analysis/herbivore_maxn_apriori_test.md](results/herbivore_analysis/herbivore_maxn_apriori_test.md)
- Herbivore Feeding: [results/herbivore_analysis/herbivore_feeding_responsiveness.md](results/herbivore_analysis/herbivore_feeding_responsiveness.md)
- Interaktionsmodell: [results/core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.md](results/core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.md)
- Praesenz/Absenz: [results/presence_absence_model/presence_absence_model.md](results/presence_absence_model/presence_absence_model.md)
- Hurdle-Modell: [results/hurdle_model/hurdle_model_focal_signals.md](results/hurdle_model/hurdle_model_focal_signals.md)
- LOO-Sensitivitaet: [results/leave_one_video_out_sensitivity/leave_one_video_out_sensitivity.md](results/leave_one_video_out_sensitivity/leave_one_video_out_sensitivity.md)
- Kompositions-Robustheit (PERMDISP + Rarefaction): [results/composition_robustness/composition_robustness_open_tests.md](results/composition_robustness/composition_robustness_open_tests.md)
- Mixed-Effects Kernendpunkte: [results/mixed_effects_core_endpoints/mixed_effects_core_endpoints.md](results/mixed_effects_core_endpoints/mixed_effects_core_endpoints.md)
- Bootstrap-Effektgroessen: [results/effectsize_bootstrap/prioritized_effectsize_bootstrap.md](results/effectsize_bootstrap/prioritized_effectsize_bootstrap.md)
- Prevalence-Threshold-Modell: [results/prevalence_threshold_model/prevalence_threshold_model.md](results/prevalence_threshold_model/prevalence_threshold_model.md)

---

## 8. Supplement Data (vollstaendig, nicht nur Kernbefunde)

Dieser Abschnitt ist als Arbeits-Supplement gedacht und listet datenhaltige Exportdateien inklusive Inhaltstyp auf, damit alle Analysen reproduzierbar und vollstaendig nachvollziehbar bleiben.

### 8.1 Community-Komposition und Koederstruktur

1. Ueberblick und globale/paarweise Kompositionsbefunde:
- [results/artenvergleich_köder/artenvergleich_koeder_summary.md](results/artenvergleich_köder/artenvergleich_koeder_summary.md)
- [results/artenvergleich_köder/artenvergleich_koeder_summary.csv](results/artenvergleich_köder/artenvergleich_koeder_summary.csv)
2. Fish-vs-algae PERMANOVA-Tabellen:
- [results/artenvergleich_köder/fishmix_mackerel_vs_algae_permanova.csv](results/artenvergleich_köder/fishmix_mackerel_vs_algae_permanova.csv)
3. Standortdetails inkl. Paarvergleiche und Jaccard-Overlap:
- [results/artenvergleich_köder/milimani/artenvergleich_koeder_milimani.md](results/artenvergleich_köder/milimani/artenvergleich_koeder_milimani.md)
- [results/artenvergleich_köder/utumbi/artenvergleich_koeder_utumbi.md](results/artenvergleich_köder/utumbi/artenvergleich_koeder_utumbi.md)
- [results/artenvergleich_köder/nursery/artenvergleich_koeder_nursery.md](results/artenvergleich_köder/nursery/artenvergleich_koeder_nursery.md)

### 8.2 Feeding/Interested Gesamt-Outputs (alle Taxa)

1. Standortzusammenfassungen:
- [results/interested_feeding/feeding_summary.md](results/interested_feeding/feeding_summary.md)
- [results/interested_feeding/interested_feeding_summary.md](results/interested_feeding/interested_feeding_summary.md)
- [results/interested_feeding/feeding_site_summary.csv](results/interested_feeding/feeding_site_summary.csv)
- [results/interested_feeding/interested_feeding_site_summary.csv](results/interested_feeding/interested_feeding_site_summary.csv)
2. Video- und Long-Formatdaten fuer Folgeanalysen:
- [results/interested_feeding/interested_feeding_video_level.csv](results/interested_feeding/interested_feeding_video_level.csv)
- [results/interested_feeding/interested_feeding_taxon_event_long.csv](results/interested_feeding/interested_feeding_taxon_event_long.csv)
3. Standortordner mit detailreichen Taxon-/Paarvergleichstabellen:
- [results/interested_feeding/milimani](results/interested_feeding/milimani)
- [results/interested_feeding/utumbi](results/interested_feeding/utumbi)
- [results/interested_feeding/nursery](results/interested_feeding/nursery)

### 8.3 Herbivore-Fokus (H2/H3)

1. H2 MaxN:
- [results/herbivore_analysis/herbivore_maxn_apriori_test.md](results/herbivore_analysis/herbivore_maxn_apriori_test.md)
- [results/herbivore_analysis/herbivore_maxn_apriori_test.csv](results/herbivore_analysis/herbivore_maxn_apriori_test.csv)
- [results/herbivore_analysis/herbivore_maxn_by_family.csv](results/herbivore_analysis/herbivore_maxn_by_family.csv)
2. H3 Feeding inkl. Sensitivitaet:
- [results/herbivore_analysis/herbivore_feeding_responsiveness.md](results/herbivore_analysis/herbivore_feeding_responsiveness.md)
- [results/herbivore_analysis/herbivore_feeding_responsiveness.csv](results/herbivore_analysis/herbivore_feeding_responsiveness.csv)
3. Zusatzinteraktion Herbivore x Standort x Koedertyp:
- [results/herbivore_analysis/herbivore_bait_site_interaction.csv](results/herbivore_analysis/herbivore_bait_site_interaction.csv)

### 8.4 Robustheit, Mechanismus, Zusatzmodelle

1. Kompositionsrobustheit:
- [results/composition_robustness/composition_robustness_open_tests.md](results/composition_robustness/composition_robustness_open_tests.md)
- [results/composition_robustness/permdisp_site_anova.csv](results/composition_robustness/permdisp_site_anova.csv)
- [results/composition_robustness/permdisp_site_by_bait.csv](results/composition_robustness/permdisp_site_by_bait.csv)
- [results/composition_robustness/rarefaction_standardized_by_bait.csv](results/composition_robustness/rarefaction_standardized_by_bait.csv)
- [results/composition_robustness/rarefaction_standardized_by_bait_no_control.csv](results/composition_robustness/rarefaction_standardized_by_bait_no_control.csv)
- [results/composition_robustness/rarefaction_standardized_by_bait_type.csv](results/composition_robustness/rarefaction_standardized_by_bait_type.csv)
2. Core-Endpoint Interaktionsmodell:
- [results/core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.md](results/core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.md)
- [results/core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.csv](results/core_endpoints_bait_site_interaction/core_endpoints_bait_site_interaction.csv)
- [results/core_endpoints_bait_site_interaction/core_endpoints_model_input.csv](results/core_endpoints_bait_site_interaction/core_endpoints_model_input.csv)
3. Praesenz-/Intensitaetszerlegung und Praevalenz:
- [results/hurdle_model/hurdle_model_focal_signals.md](results/hurdle_model/hurdle_model_focal_signals.md)
- [results/hurdle_model/hurdle_model_summary.csv](results/hurdle_model/hurdle_model_summary.csv)
- [results/presence_absence_model/presence_absence_model.md](results/presence_absence_model/presence_absence_model.md)
- [results/presence_absence_model/presence_absence_summary.csv](results/presence_absence_model/presence_absence_summary.csv)
- [results/prevalence_threshold_model/prevalence_threshold_model.md](results/prevalence_threshold_model/prevalence_threshold_model.md)
- [results/prevalence_threshold_model/prevalence_threshold_summary.csv](results/prevalence_threshold_model/prevalence_threshold_summary.csv)
4. Stabilitaet und Effektgroessen:
- [results/leave_one_video_out_sensitivity/leave_one_video_out_sensitivity.md](results/leave_one_video_out_sensitivity/leave_one_video_out_sensitivity.md)
- [results/leave_one_video_out_sensitivity/leave_one_video_out_sensitivity_summary.csv](results/leave_one_video_out_sensitivity/leave_one_video_out_sensitivity_summary.csv)
- [results/effectsize_bootstrap/prioritized_effectsize_bootstrap.md](results/effectsize_bootstrap/prioritized_effectsize_bootstrap.md)
- [results/effectsize_bootstrap/prioritized_effectsize_bootstrap.csv](results/effectsize_bootstrap/prioritized_effectsize_bootstrap.csv)

### 8.5 Supplement-Empfehlung fuer Abgabe

1. MD-Dateien als narrative Supplement-Sections (Methodik + Interpretation).
2. CSV-Dateien als maschinenlesbare Supplemental Tables (alle Tests, Effektgroessen, p/q-Korrekturen).
3. Fuer Transparenz je Analyseblock immer gemeinsam bereitstellen:
- Summary-MD.
- Volltabellen-CSV.
- ggf. Input-/Designmatrix-CSV (falls vorhanden, z. B. core_endpoints_model_input.csv).

### 8.6 Neue Supplement-Indexdateien

1. Detaillierter Analyseindex mit Fragestellung, Kontrast, Dateneinheit, Testfamilie und Korrektur:
- [results/supplement_data/supplement_index_detailed.csv](results/supplement_data/supplement_index_detailed.csv)
2. Vollstaendiges Manifest aller aktuellen Ergebnisdateien (MD/CSV) mit Dateigroesse und Analyseblock:
- [results/supplement_data/supplement_file_manifest.csv](results/supplement_data/supplement_file_manifest.csv)
