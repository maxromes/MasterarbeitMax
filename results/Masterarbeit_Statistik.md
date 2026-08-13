# Masterarbeit_Statistik

Stand: 2026-08-13

Dieses Dokument ordnet die vorhandenen statistischen Ergebnisse entlang der zentralen Ziele und Hypothesen der Arbeit.
Es trennt zwischen:
- Kernbefunden fuer den Ergebnisteil
- erwaehnenswerten Zusatzbefunden fuer Einordnung und Diskussion
- Material, das methodisch wichtig ist, aber in den Anhang gehoert

Die Formulierungen sind so geschrieben, dass sie direkt in die Masterarbeit uebernommen und im Diskussionsteil weiter eingeordnet werden koennen.

---

## 1. Ziel-Hypothesen-Matrix mit Priorisierung

## Aim 1 / H1

Fragestellung:
- Beeinflusst der Koeder die Zusammensetzung der BRUVS-Gemeinschaften, getrennt nach Milimani, Utumbi und dem separaten Nursery-Experiment?

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

### 1.3 In den Anhang

1. Vollstaendige Paarvergleichstabellen je Standort
2. Overlap- und koederspezifische Taxalisten je Standort
3. Alle Exporttabellen aus [results/artenvergleich_köder/artenvergleich_koeder_summary.md](results/artenvergleich_köder/artenvergleich_koeder_summary.md)

---

## Aim 2 / H2

Fragestellung:
- Erhoehen Makroalgenkoeder die MaxN-Werte der herbivoren Familien (Siganidae, Acanthuridae, Scaridae, Blenniidae) gegenueber Fischkoedern, und ist dieser Effekt standortabhaengig?

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

### 2.3 In den Anhang

1. Vollstaendige Familienlisten je Standort inklusive nicht signifikanter Tests
2. Alle Effektgroessen-Detailtabellen
3. Vollstaendige Hurdle-Ausgabe aus [results/hurdle_model/hurdle_model_focal_signals.md](results/hurdle_model/hurdle_model_focal_signals.md)

---

## Aim 2 / H3

Fragestellung:
- Erhoehen Makroalgenkoeder die video-basierte Feeding-Response herbivorer Fische im Vergleich zu Fischkoedern?

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
2. Fuer die Diskussion wichtig: Feeding-Ereignisse wurden als Ereignisvorkommen/Rate, nicht als Dauer, modelliert.

### 3.3 In den Anhang

1. Standortweise Verteilungsplots und alle Zwischenkennzahlen der Feeding-Raten
2. Vollstaendige Vergleichstabellen aus [results/herbivore_analysis/herbivore_feeding_responsiveness.md](results/herbivore_analysis/herbivore_feeding_responsiveness.md)

---

## 4. Praezise, uebernehmbare Ergebnisformulierungen

Die folgenden Formulierungen sind fuer den Ergebnisteil geeignet.

## 4.1 Formulierung zu H1 (Komposition)

"Die standortspezifischen PERMANOVA-Analysen auf Jaccard-Distanzen zeigten in allen drei Untersuchungssettings signifikante Koedereffekte auf die Artenzusammensetzung (Milimani: p = 0.0242; Utumbi: p = 0.0046; Nursery: p = 0.0016). Im primaeren Riffvergleich blieb auch der gruppierte Kontrast zwischen Fisch- und Algenkoedern signifikant (Milimani: p = 0.0080; Utumbi: p = 0.0044). Damit wird H1 unterstuetzt: Koederbehandlung beeinflusst die Zusammensetzung der BRUVS-Assemblagen, wobei die Evidenz standortspezifisch interpretiert wird und die Nursery als separates Experiment zu lesen ist." 

## 4.2 Formulierung zu H2 (Herbivore-MaxN)

"Im a-priori-Test der vier herbivoren Familien zeigte sich ein robustes Algen-Signal ausschliesslich fuer Acanthuridae in Nursery (Median Algae = 22.0 vs Median Fish = 4.5; p_raw = 0.0070; p_Holm = 0.0278; Cliff's Delta = 1.0). In Milimani und Utumbi wurden fuer die Herbivore-Familien keine Holm-signifikanten Algae>Fish-Effekte nachgewiesen. H2 wird damit partiell bestaetigt und ist klar standortabhaengig." 

## 4.3 Formulierung zu H3 (Feeding-Response)

"Die video-basierte Herbivore-Feeding-Response war in Nursery unter Algenkoedern signifikant hoeher als unter Fischkoedern (mean 0.2038 vs 0.0000; p_raw = 0.005709; p_Holm = 0.017126; Cliff's Delta = 1.0), waehrend in Milimani und Utumbi keine signifikanten Unterschiede auftraten (jeweils p_Holm = 0.5510). H3 wird somit fuer Nursery bestaetigt, jedoch nicht als standortunabhaengiges Muster." 

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
