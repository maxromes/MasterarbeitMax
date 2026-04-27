# Plausibilitaets-Audit der Sicht-Analysen

Stand: 2026-04-27

## Ziel

Systematische Plausibilitaetspruefung der durchgefuehrten Sicht-Skripte und ihrer Ergebnisse:
- update_visibility_analysis.py
- visibility_adjusted_models.py
- visibility_additional_tests.py
- visibility_site_stratified_tests.py

## 1) Reproduzierbarkeit

Alle vier Skripte wurden erneut ausgefuehrt und liefen ohne Abbruch durch.

Hinweis:
- Bei der standort-stratifizierten Analyse treten Runtime-Warnungen in HC3 auf (`invalid value encountered in divide`).
- Diese Warnungen sind bei kleinen, unbalancierten Teilstichproben mit hoher Leverage plausibel und konsistent mit den teilweise unendlichen Konfidenzintervallen.
- Die permutationbasierten p-Werte bleiben davon unberuehrt und dienen als robustere Orientierung.

## 2) Datenkonsistenz-Checks

Verifiziert:
- Stichprobe durchgaengig `n = 46` in
  - bivariaten Korrelationen,
  - adjustierten Modellen,
  - partiellen Korrelationen,
  - Zusatztests.
- Keine fehlenden Sichtwerte (`N missing visibility = 0`).

## 3) Ergebniskonsistenz ueber Analyseebenen

### 3.1 Bivariat

- 2 von 3 Endpunkten sind roh und FDR-signifikant (MaxN, Species Richness).
- First Seen bleibt nicht signifikant.

### 3.2 Adjustierte Hauptmodelle

- Alle BH-korrigierten p-Werte fuer Sicht > 0.05.
- Gilt fuer HC3-Inferenz, Permutation und partielle Spearman-Korrelation.

### 3.3 Zusatztests

Minimale FDR-q-Werte:
- q_hc3_fdr_bh: 0.7385
- q_perm_blocked_fdr_bh: 0.7211
- q_quad_fdr_bh: 0.9875
- q_quantile_fdr_bh: 0.0933

Interpretation:
- Kein Zusatztest liefert einen robusten Signifikanznachweis.

### 3.4 Standort-stratifizierte Tests

- 9 Standort-Endpunkt-Kombinationen geprueft.
- Minimale FDR-q-Werte:
  - q_hc3_fdr_bh: 1.0
  - q_perm_fdr_bh: 1.0
- 12 CI-Grenzen sind unendlich (`+/- inf`), konsistent mit geringer Praezision in kleinen, unbalancierten Zellen.

## 4) Konfundierungs-/Design-Plausibilitaet

Zusatzchecks aus den Rohdaten:
- eta^2(visibility ~ standort) = 0.449
- eta^2(visibility ~ koeder) = 0.393

Interpretation:
- Sicht ist stark mit Standort und Koeder strukturiert.
- Damit ist es plausibel, dass bivariate Sicht-Effekte durch Gruppenstruktur miterklaert werden und nach Adjustierung verschwinden.

## 5) Gesamturteil

Die Ergebnisse sind intern konsistent und methodisch plausibel:
- Rohdaten zeigen Sicht-Signale (Detektierbarkeitskomponente plausibel).
- Nach Kontrolle fuer Standort und Koeder sowie in Robustheits- und Strata-Analysen bleibt kein unabhaengiger Sicht-Effekt robust signifikant.
- Die berichtete Schlussfolgerung bleibt damit stabil und belastbar.
