# Sichtweiten-adjustierte Ergebnisse

Stand: 2026-04-27

## Methode

- Datengrundlage: visibility_video_level_merged.csv (nur Zeilen mit vorhandener Sichtweite).
- Modell pro Endpunkt: OLS auf log1p(Endpunkt) mit Kovariaten visibility_mean, Standort und Koeder.
- Inferenz: robuste HC3-Standardfehler, zusaetzlich Permutationstest (3000 Permutationen).
- Multiple Tests: Benjamini-Hochberg (BH/FDR) ueber die drei Endpunkte.
- Robustheitscheck: partielle Spearman-Korrelation (um Standort und Koeder bereinigt).

## Modellresultate (Effekt der Sichtweite)

| Metrik | n | Beta log1p | 95%-CI | % pro +1 Sichtweite | p(HC3) | q(HC3) | p(Perm) | q(Perm) |
|---|---:|---:|---|---:|---:|---:|---:|---:|
| maxn_video_peak | 46 | 0.030 | [-0.056, 0.116] | 3.0% | 0.4829 | 0.7385 | 0.4245 | 0.7091 |
| species_richness | 46 | 0.004 | [-0.020, 0.028] | 0.4% | 0.7343 | 0.7385 | 0.7091 | 0.7091 |
| first_seen_median_sec | 46 | -0.017 | [-0.119, 0.085] | -1.7% | 0.7385 | 0.7385 | 0.7044 | 0.7091 |

## Partielle Spearman-Korrelation (bereinigt um Standort + Koeder)

| Metrik | n | partial rho | p | q(BH) |
|---|---:|---:|---:|---:|
| maxn_video_peak | 46 | 0.092 | 0.542 | 0.542 |
| species_richness | 46 | 0.139 | 0.3584 | 0.5377 |
| first_seen_median_sec | 46 | -0.183 | 0.2231 | 0.5377 |

## Kurzinterpretation

- In den adjustierten Modellen (Standort + Koeder kontrolliert) zeigt keiner der drei Endpunkte einen signifikanten Sichtweiten-Effekt (alle BH-q > 0.70).
- Der zuvor beobachtete bivariate Zusammenhang mit MaxN und Species Richness wird damit weitgehend durch Standort-/Koedereffekte erklaert.
- Fuer Schlussfolgerungen sollten primaer die adjustierten Effektschaetzungen berichtet werden.

## Weitere Tests (Robustheit)

Zusatzanalysen wurden in `results/visibility_analysis/visibility_additional_tests_summary.md` dokumentiert. Kurzfassung:

- Blockierter Permutationstest (Permutation innerhalb Standort x Koeder) bestaetigt die Nullbefunde fuer alle Endpunkte (alle unadjustierten p >= 0.418; BH-q >= 0.721).
- Nichtlinearitaetstest (Quadratik-Term der Sichtweite) zeigt keinen Hinweis auf gekruemmte Zusammenhaenge (alle p >= 0.667; BH-q = 0.988).
- Median-Quantilsregression zeigt nur fuer `first_seen_median_sec` ein nominales Signal (p = 0.031), das nach Mehrfachtest-Korrektur nicht robust bleibt (BH-q = 0.093; Holm-q = 0.093; Bonferroni-q = 0.093).
- Ergebnisstabilitaet ueber Korrekturverfahren: BH, Holm, Bonferroni und BY fuehren durchgehend zur gleichen inhaltlichen Schlussfolgerung (kein robuster Sicht-Effekt).

## Standort-stratifizierte Zusatzanalyse

Die standortweise Analyse ist in results/visibility_analysis/visibility_site_stratified_tests_summary.md dokumentiert.

- Auch getrennt nach milimani, nursery und utumbi bleibt kein robuster Sicht-Effekt nach Korrektur fuer multiples Testen bestehen.
- Blockierte Permutationstests innerhalb Koeder bestaetigen ebenfalls die Nullbefunde (alle BH-q = 1.0).
- Damit gibt es keinen Hinweis, dass der Sicht-Effekt nur lokal in einem einzelnen Standort auftritt.

Hinweis zur Praezision:

- Pro Standort sind die Stichproben klein (n = 11 bis 18) bei gleichzeitig mehreren Koeder-Kategorien.
- Daher sind standortweise HC3-Intervalle teilweise numerisch instabil (teilweise +/- unendlich); die Permutationsergebnisse sind hier die robustere Orientierung.
