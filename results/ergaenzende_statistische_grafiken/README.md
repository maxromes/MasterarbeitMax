# Ergänzende Grafiken zur statistischen Ergebnisinterpretation

Diese Sammlung ergänzt die Hauptvorlage in [../praesentation_statistische_tests_vorlage.md](../praesentation_statistische_tests_vorlage.md) um visuelle Optionen, die unterschiedliche Facetten der Ergebnisse klarer machen. Ziel ist es, möglichst viele Interpretationswege bereitzustellen, ohne die Kernbotschaften zu verwässern.

## 1) Standort-Häufigkeit: Roh vs. Holm-signifikante Taxa

- Datei: [01_taxa_standort_significance_counts.png](01_taxa_standort_significance_counts.png)
- Beschreibung: Balkendiagramm mit der Anzahl der Taxa, die roh signifikant waren und derjenigen, die nach Holm-Korrektur noch signifikant blieben.
- Interpretation: Der große Unterschied zwischen Roh- und Holm-signifikanten Taxa zeigt, dass die Standortmuster sehr stark sind, aber zugleich durch Multiple-Testing-Korrektur deutlich eingegrenzt werden. Der Befund bleibt trotzdem robust: Standort ist der dominierende Strukturfaktor.

## 2) Fish-vs-Algae: Effektgrößen der stärksten Signale

- Datei: [02_fish_vs_algae_cliffs_delta.png](02_fish_vs_algae_cliffs_delta.png)
- Beschreibung: Forest-Plot der Cliff's Delta-Werte für die stärksten Fish-vs-Algae-Effekte.
- Interpretation: Die Richtung ist überwiegend fish > algae. Das ist besonders wichtig, weil es zeigt, dass die Breite der Analyse nicht automatisch eine Algenfresser-Hypothese stützt, sondern eher das Gegenteil nahelegt – außer in gezielten Herbivore-Fokusanalysen.

## 3) Species Richness nach Standort

- Datei: [03_species_richness_by_site_boxplot.png](03_species_richness_by_site_boxplot.png)
- Beschreibung: Boxplot der Species Richness pro Video mit Standortvergleich.
- Interpretation: Das Muster zeigt deutlich, dass die Artendiversität nicht zufällig verteilt ist, sondern von der Standortsituation geprägt wird. Die Variable ist damit in der Gesamtinterpretation als Standort-abhängig zu lesen und nicht als direkter Koeder-Effekt.

## 4) Visibility: roher Zusammenhang mit Species Richness

- Datei: [04_visibility_raw_correlation.png](04_visibility_raw_correlation.png)
- Beschreibung: Scatterplot zwischen Sichtweite und Species Richness mit hervorstehender Korrelation.
- Interpretation: Im Rohdatenvergleich erscheint Sichtweite als möglicher Treiber. Die Grafik ist deshalb gut geeignet, um die ursprüngliche Hypothese zu visualisieren – aber sie muss immer zusammen mit dem adjustierten Modell interpretiert werden, weil dort kein robustes Eigensignal mehr bleibt.

## 5) Visibility: adjustierte Effektgrößen

- Datei: [05_visibility_adjusted_forest_plot.png](05_visibility_adjusted_forest_plot.png)
- Beschreibung: Forest-Plot der adjustierten Regressionskoeffizienten nach Kontrolle von Standort und Köder.
- Interpretation: Das verschwindende Effektmuster nach Adjustierung ist ein zentrales Ergebnis. Es spricht dafür, dass Sichtweite eher ein Kontextmerkmal ist als ein unabhängiger, robuster Einflussfaktor auf die Community.

## 6) PERMANOVA je Standort

- Datei: [06_permanova_site_comparison.png](06_permanova_site_comparison.png)
- Beschreibung: Balkenplot der negativen Logarithmen der PERMANOVA-p-Werte je Standort.
- Interpretation: Die Gemeinschaftsstruktur unterscheidet sich zwischen Ködern in allen Standorten signifikant. Der Effekt ist global klar, aber nicht automatisch mit einem pauschalen Algenfresser-Signal gleichzusetzen.

## 7) Herbivore: Richtung des Koeder-Effekts je Standort

- Datei: [07_herbivore_direction_heatmap.png](07_herbivore_direction_heatmap.png)
- Beschreibung: Heatmap mit dem Richtungssignal herbivorer Gruppen (Algae > Fish vs. Fish > Algae) pro Standort.
- Interpretation: Die Grafik zeigt der Hauptfrage sehr gut, dass im Fokus herbivorer Gruppen der stärkste Effekt in Nursery sichtbar wird, während die Gesamtanalyse insgesamt eher fish-orientierte Muster zeigt. Das ist eine biologisch sinnvolle Trennung zwischen „globalem Muster" und „a priori Fokus".

## 8) Evidenzstufen der wichtigsten Befunde

- Datei: [08_evidence_level_overview.png](08_evidence_level_overview.png)
- Beschreibung: Übersichtsdiagramm, das die wichtigsten Ergebnisse nach Robustheit klassifiziert.
- Interpretation: Diese Grafik hilft dabei, zwischen robusten, bedingten und explorativen Befunden sauber zu unterscheiden. Gerade bei multiplen Testungen und biologischen Hypothesen ist diese Einordnung für die Präsentation wichtig.

## 9) Systematische Leave-one-video-out-Sensitivität

- Datei: [09_leave_one_video_out_robustness.png](09_leave_one_video_out_robustness.png)
- Beschreibung: Logarithmische p-Wert-Verteilung für die wichtigsten Effekte unter systematischer Entfernung eines einzelnen Videos. Jede Punktwolke zeigt einen LOO-Run; die horizontale Linie markiert den Referenzwert p=0.05.
- Interpretation: Die Kernsignale bleiben auch nach Entfernen jedes einzelnen Videos stabil. Besonders deutlich ist dies für die Nursery-Herbivore (Acanthuridae), aber auch für die wichtigsten Fish-vs-Algae-Familien im Coral-Reef-Datensatz. Die Grafik zeigt damit, dass die Hauptergebnisse nicht auf einen einzelnen Ausreisser zurückzuführen sind.

## 10) Präsenz-/Absenz-Modell der fokussierten Signale

- Datei: [10_presence_absence_focal_signals.png](10_presence_absence_focal_signals.png)
- Beschreibung: Balkendiagramm der Videoebenen-Präsenzrate für die wichtigsten Familien unter Algen- vs. Fischkoeder. Jede Gruppe zeigt den Anteil videos mit Nachweis der jeweiligen Familie; die Werte sind getrennt nach Algen- und Fischvideos dargestellt.
- Interpretation: Das Präsenz-/Absenz-Muster bestätigt den Dichte-Effekt in der Nursery-Acanthuridae nur teilweise, weil Acanthuridae in beiden Koedergruppen praktisch immer vorkommt. Für Labridae und Balistidae bleibt der Unterschied im bloßen Vorkommen klein oder null, während Muraenidae den stärksten Presence/Absence-Effekt zeigt. Insgesamt zeigt die Grafik, dass der robusteste Effekt eher in der Intensität und nicht im bloßen Auftreten liegt, wodurch die MaxN-basierte Interpretation weiter gestützt wird.

## 11) Hurdle-Modell: Praesenz vs. Intensitaet

- Datei: [11_hurdle_model_effect_decomposition.png](11_hurdle_model_effect_decomposition.png)
- Beschreibung: Zwei-Panel-Darstellung der fokussierten Signale. Links: Praesenzteil als log(OR) mit Konfidenzintervallen (Algae vs Fish). Rechts: Intensitaetsteil als Koeffizient auf log1p(MaxN) nur fuer positive Beobachtungen.
- Interpretation: Die Grafik macht sichtbar, dass mehrere Schluesselsignale nicht durch haeufigeres Auftreten, sondern durch staerkere Intensitaet bei Praesenz getragen werden. Gleichzeitig bleibt Muraenidae als klares Praesenzsignal erkennbar. Damit wird die Kombination aus Praesenz-/Absenz- und MaxN-Befunden mechanistisch deutlich besser interpretierbar.

## 12) PERMDISP: Streuung der Komposition pro Standort

- Datei: [12_permdisp_dispersion_by_site.png](12_permdisp_dispersion_by_site.png)
- Beschreibung: Balkendiagramm der mittleren Distanz zum Koeder-Zentrum (PCoA auf Jaccard-Distanzen) fuer jeden Standort und Koeder.
- Interpretation: In allen drei Standorten sind die Dispersionen zwischen Koedern ungleich (PERMDISP signifikant). Damit sind die PERMANOVA-Befunde nicht ausschliesslich als Lageverschiebung interpretierbar, sondern enthalten auch Streuungskomponenten.

## 13) Rarefaction: standardisierte Taxa-Richness je Koeder

- Datei: [13_rarefaction_standardized_richness.png](13_rarefaction_standardized_richness.png)
- Beschreibung: Standortweise Balken mit 95%-Intervallen fuer rarefied Union Richness bei standardisierter Videozahl je Koeder.
- Interpretation: Die Sampling-Normalisierung macht sichtbar, welche Koeder auch bei gleicher Stichprobengroesse die hoehere Taxa-Abdeckung behalten. Sie reduziert Artefakte durch ungleiche Videozahlen und dient als Robustheitskontext fuer Richness-basierte Aussagen.

## 14) Mixed-Effects Forest-Plot (fish vs algae)

- Datei: [14_mixed_effects_fish_vs_algae_forest.png](14_mixed_effects_fish_vs_algae_forest.png)
- Beschreibung: Forest-Plot der endpoint-spezifischen fish-vs-algae Koeffizienten aus dem hierarchischen Mixed-Effects-Modell (Random Intercept Standort) fuer species_richness, maxn_video_peak und first_seen_median_sec.
- Interpretation: Der Plot zeigt, dass nur first_seen_median_sec robust von null abweicht, waehrend species_richness und maxn_video_peak im hierarchischen Rahmen keine robusten fish-vs-algae-Effekte tragen.

## 15) Prevalence-Threshold Fisher-Exact Tests (neu)

- Dateien: 
  - [15_prevalence_threshold_fisher_results.png](15_prevalence_threshold_fisher_results.png)
  - [15b_prevalence_threshold_summary_counts.png](15b_prevalence_threshold_summary_counts.png)
  - [15c_prevalence_threshold_direction_breakdown.png](15c_prevalence_threshold_direction_breakdown.png)
- Beschreibung (15): Standortweise Balkendiagramme der Family-Level-Occupancy (Praesenzrate) mit Fisher-Exact-Test-Ergebnissen. Rot = Algae > Fish (haeufiger auf Algae-Videos), Blau = Fish > Algae (haeufiger auf Fisch-Videos). Die Intensitaet (Laenge des Balkens) zeigt -log10(p); gestrichelte Linien markieren die Signifikanzgrenze p=0.05.
- Beschreibung (15b): Zusammenfassung der robusten (q_Holm <= 0.05) und trendmaessigen (0.05 < q <= 0.10) Occupancy-Signale nach Standort.
- Beschreibung (15c): Breakdown der Richtungseffekte: Anzahl der Familien, die hoeher auf Algen- vs. Fisch-Videos nachgewiesen wurden, nach Standort.
- Interpretation: Die Grafiken zeigen, dass nach standortweiser Mehrfachtestkorrektur kein Family-Occupancy-Signal robust signifikant wird (min q_Holm = 0.1199 in Utumbi-Muraenidae). Dies staerkt die Interpretation, dass die Haupteffekte primaer auf Intensitaets-/MaxN-Unterschiede und nicht auf breite Praevalenzverschiebungen zurueckgehen. Einzelne gerichtete Tendenzen existieren (z. B. Utumbi-Muraenidae fish>algae), halten aber nicht die Robustheitsschwelle.

---

## Nutzung in der Präsentation

- Für die Einleitung: 01, 03, 06
- Für die Hauptfrage und Interpretation: 02, 07, 09
- Für die Sensibilisierung gegenüber Konfundierung: 04, 05
- Für Lage-vs-Streuung und Sampling-Robustheit: 12, 13
- Für hierarchische Zusatzinferenz: 14
- Für Occupancy-Robustheit und Mechanismus: 15, 15b, 15c
- Für die Abschlussinterpretation: 08, 11

Diese Abfolge ist besonders geeignet, um die Evidenz schrittweise von „großem Standorteffekt" über „Koedereinfluss auf die Gemeinschaft" hin zu „biologischer Interpretation" zu führen und abschließend die mechanistische Trennung von Präsenz- vs. Intensitätseffekten zu verdeutlichen.
