# Gesamtbewertung aller Sicht-Analysen

Stand: 2026-04-27

## 1) Ziel und Datengrundlage

Ziel war zu pruefen, inwiefern die Sichtweite (visibility_mean) die zentralen Endpunkte beeinflusst:
- maxn_video_peak
- species_richness
- first_seen_median_sec

Datengrundlage:
- 46 Videos insgesamt
- 0 fehlende Sichtwerte
- Vollstaendige Abdeckung ueber vorhandene Standort-Koeder-Kombinationen

Verwendete Quellen in diesem Ordner:
- visibility_summary.md (bivariat)
- visibility_adjusted_summary.md (adjustierte Hauptmodelle)
- visibility_additional_tests_summary.md (Robustheits- und Sensitivitaetstests)
- visibility_site_stratified_tests_summary.md (standort-stratifiziert)

## 2) Ergebnisse im Ueberblick

### 2.1 Bivariate Zusammenhaenge (ohne Adjustierung)

Befund:
- Sicht korreliert positiv mit maxn_video_peak (Spearman rho = 0.467, BH-q = 0.00161)
- Sicht korreliert positiv mit species_richness (rho = 0.563, BH-q = 0.000138)
- Kein belastbarer Zusammenhang mit first_seen_median_sec (rho = 0.160, BH-q = 0.289)

Interpretation:
- Rohdaten suggerieren zunaechst: bessere Sicht geht mit hoeheren beobachteten MaxN- und Richness-Werten einher.

### 2.2 Adjustierte Hauptanalyse (Standort + Koeder kontrolliert)

Modell:
- OLS auf log1p(Endpunkt) mit visibility_mean + C(standort) + C(koeder)
- HC3-robuste Standardfehler
- zusaetzlich Permutationstest
- multiple Testkorrektur mit BH/FDR

Befund:
- Kein Endpunkt zeigt einen robust signifikanten Sicht-Effekt
- p(HC3): 0.483 bis 0.739
- q(HC3,BH): durchgehend 0.739
- p(Permutation): 0.425 bis 0.709
- q(Permutation,BH): durchgehend 0.709

Kernaussage:
- Der bivariate Sicht-Effekt verschwindet nach Kontrolle fuer Standort und Koeder.

### 2.3 Zusatztests / Sensitivitaet

Geprueft wurden:
- blockierter Permutationstest (innerhalb Standort x Koeder)
- Nichtlinearitaet (Quadratik-Term)
- Median-Quantilsregression
- multiple Korrekturen: BH, Holm, Bonferroni, BY

Befund:
- Keine robuste Signifikanz in den Zusatztests
- Nur ein nominales Signal bei Quantilsregression fuer first_seen_median_sec (p = 0.031), aber nach Korrektur nicht robust (z. B. BH-q = 0.093)

Kernaussage:
- Die Nullbefunde der adjustierten Hauptanalyse sind robust gegen alternative Testverfahren.

### 2.4 Standort-stratifizierte Analyse

Ansatz:
- Modelle separat fuer milimani, nursery, utumbi
- innerhalb Standort Kontrolle fuer Koeder

Befund:
- Kein standortspezifischer Sicht-Effekt bleibt nach Korrektur robust signifikant
- Blockierte Permutationstests bestaetigen die Nullbefunde

Hinweis:
- Kleine Stichproben pro Standort (n = 11 bis 18) und viele Koeder-Stufen fuehren teils zu numerisch instabilen HC3-Intervallen (teilweise +/- inf).
- Die Permutationsergebnisse sind hier methodisch belastbarer.

## 3) Plausibilitaetspruefung

### 3.1 Ist ein scheinbarer Widerspruch zwischen bivariater und adjustierter Analyse plausibel?

Ja. Die Daten zeigen deutliche Strukturierung der Sicht durch Gruppierungsvariablen:

- Sicht nach Standort (Mittelwerte):
  - nursery: 5.36
  - milimani: 10.82
  - utumbi: 11.72

- Sicht-Varianzaufklaerung (ANOVA-artiges eta^2):
  - eta^2(visibility ~ standort) = 0.449
  - eta^2(visibility ~ koeder) = 0.393

Interpretation:
- Ein grosser Teil der Sicht-Variation ist an Standort und Koeder gekoppelt.
- Daher sind starke bivariate Sicht-Korrelationen ohne Adjustierung erwartbar und koennen Konfundierung widerspiegeln.

### 3.2 Ueberlappung und Designbalance

- nursery hat einen sehr engen Sichtbereich (5 bis 6), milimani (5 bis 15), utumbi (5 bis 20).
- Einige Koeder treten nur in einzelnen Standorten auf (unbalancierte Zellen).

Folge:
- Die Trennung zwischen "reinem Sicht-Effekt" und Standort-/Koedereffekt ist datenbedingt begrenzt.
- Das erklaert, warum adjustierte Sicht-Koeffizienten klein und unsicher werden.

### 3.3 Innerhalb-Standort-Rohkorrelationen

Spearman innerhalb Standort (ungekorrigiert):
- Keine robuste Signifikanz fuer die drei Endpunkte innerhalb einzelner Standorte.
- Das stuetzt die Aussage, dass der globale bivariate Effekt vor allem aus zwischen-Gruppen-Unterschieden stammt.

## 4) Gesamtinterpretation

Gesamtschau ueber alle Analysen:
- Bivariat: Sicht scheint fuer MaxN und Richness relevant.
- Kausal-naehere Interpretation (adjustiert + robust): kein belastbarer eigenstaendiger Sicht-Effekt.
- Sensitivitaetsanalysen und stratifizierte Modelle bestaetigen diese Schlussfolgerung.

Fachliche Einordnung:
- Plausibel ist ein Detektierbarkeitsanteil in den Rohdaten.
- Fuer inferenzielle Aussagen zwischen Behandlungen/Standorten sollten Effekte nur aus adjustierten Modellen berichtet werden.
- Die Evidenz spricht derzeit gegen einen starken, unabhaengigen Sicht-Treiber auf die drei Endpunkte.

## 5) Empfehlung fuer die Berichterstattung

Empfohlenes Wording:
- "In unadjustierten Analysen zeigte sich ein positiver Zusammenhang der Sicht mit MaxN und Species Richness. Nach Adjustierung fuer Standort und Koeder sowie in mehreren Robustheitsanalysen blieb jedoch kein signifikanter unabhaengiger Sicht-Effekt bestehen."

Methodische Transparenz:
- Bivariate Ergebnisse als deskriptiv kennzeichnen.
- Adjustierte Ergebnisse als primaere Schlussfolgerung fuehren.
- Hinweis auf eingeschraenkte Praezision in standort-stratifizierten Modellen (kleines n, unbalancierte Zellen, teilweise instabile HC3-Intervalle).

## 6) Fazit in einem Satz

Die Sicht beeinflusst die Endpunkte in den Rohdaten scheinbar deutlich, erklaert aber nach Kontrolle von Standort und Koeder die beobachteten Unterschiede nicht eigenstaendig robust.
