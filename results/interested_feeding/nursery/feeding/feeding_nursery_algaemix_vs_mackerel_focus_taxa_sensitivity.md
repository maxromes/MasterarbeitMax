# Sensitivitaetsanalyse: Nursery Feeding (algaemix vs mackerel)

Fokus-Taxa: `species::paletail unicorn (naso brevirostris)`, `species::honeycomb (siganus stellatus)`

Methoden: exakter Mann-Whitney-U, Permutationstest auf Mittelwertdifferenz (20.000), Fisher-Exact auf Praesenz (event_count>0), Cliff's Delta, Bootstrap-CI der Mittelwertdifferenz; Holm/BH ueber die 2 vordefinierten Fokus-Taxa.

| taxon_key                                     |   n_algaemix |   n_mackerel |   mean_algaemix |   mean_mackerel |   median_algaemix |   median_mackerel |   mean_diff_algaemix_minus_mackerel |   mw_u_stat |   mw_p_exact |   perm_p_mean_diff |   cliffs_delta_algaemix_minus_mackerel |   bootstrap95ci_mean_diff_lo |   bootstrap95ci_mean_diff_hi |   presence_algaemix_pos |   presence_algaemix_zero |   presence_mackerel_pos |   presence_mackerel_zero |   fisher_p_presence |   mw_p_exact_holm_focus2 |   mw_p_exact_bh_focus2 |   perm_p_mean_diff_holm_focus2 |   perm_p_mean_diff_bh_focus2 |   fisher_p_presence_holm_focus2 |   fisher_p_presence_bh_focus2 |   mw_p_from_existing |   mw_p_holm_within_taxon_existing |
|:----------------------------------------------|-------------:|-------------:|----------------:|----------------:|------------------:|------------------:|------------------------------------:|------------:|-------------:|-------------------:|---------------------------------------:|-----------------------------:|-----------------------------:|------------------------:|-------------------------:|------------------------:|-------------------------:|--------------------:|-------------------------:|-----------------------:|-------------------------------:|-----------------------------:|--------------------------------:|------------------------------:|---------------------:|----------------------------------:|
| species::paletail unicorn (naso brevirostris) |            3 |            4 |        30.3333  |               0 |                26 |                 0 |                            30.3333  |          12 |    0.0571429 |          0.0267987 |                                      1 |                           13 |                           52 |                       3 |                        0 |                       0 |                        4 |           0.0285714 |                 0.114286 |              0.0571429 |                      0.0535973 |                    0.0267987 |                       0.0571429 |                     0.0285714 |            0.0319112 |                          0.180392 |
| species::honeycomb (siganus stellatus)        |            3 |            4 |         1.33333 |               0 |                 1 |                 0 |                             1.33333 |          12 |    0.0571429 |          0.0267987 |                                      1 |                            1 |                            2 |                       3 |                        0 |                       0 |                        4 |           0.0285714 |                 0.114286 |              0.0571429 |                      0.0535973 |                    0.0267987 |                       0.0571429 |                     0.0285714 |            0.0300653 |                          0.180392 |

## Kurzinterpretation
- species::paletail unicorn (naso brevirostris): Rohsignal vorhanden (MW exact p=0.05714), aber Holm(2 Taxa) MW p=0.1143; robust_signifikant=False.
- species::honeycomb (siganus stellatus): Rohsignal vorhanden (MW exact p=0.05714), aber Holm(2 Taxa) MW p=0.1143; robust_signifikant=False.

## Erweiterte Interpretation
- Beide Taxa zeigen eine sehr starke und konsistente Trennung zwischen den Koedern: bei `algaemix` ist die Praesenz in allen Videos vorhanden (3/3), bei `mackerel` in keinem Video (0/4). Das wird durch `cliffs_delta = 1.0` fuer beide Taxa bestaetigt.
- Die Richtung ist biologisch eindeutig (`algaemix > mackerel`), aber die inferenzstatistische Absicherung ist aufgrund der kleinen Stichprobe (`n=3` vs `n=4`) grenzwertig und methodenabhaengig.
- Unter strenger Familienfehlerkontrolle (Holm) bleiben die Signale knapp ueber der Schwelle:
	- Mann-Whitney exact Holm(2) = 0.1143
	- Permutation Holm(2) = 0.0536
	- Fisher Holm(2) = 0.0571
- Unter FDR/BH (fuer die 2 vorab definierten Fokus-Taxa) werden die Signale signifikant:
	- Permutation BH(2) = 0.0268
	- Fisher BH(2) = 0.0286
- Interpretation fuer die Arbeit: Der Effekt ist biologisch stark plausibel und in allen Effektmassen konsistent, sollte aber unter Holm-konservativer Lesart als "starkes, knapp nicht robustes Signal" und nicht als endgueltig abgesicherter Nachweis formuliert werden.
- Methodischer Zusatz: Die zuvor berichteten taxonweisen Holm-Werte innerhalb des gesamten Taxon-Sets (`~0.1804`) sind deutlich strenger, weil dort gegen mehr Hypothesentests korrigiert wurde. Die hier gezeigte Fokuskorrektur (2 Taxa) dient als zielgerichtete Sensitivitaetsanalyse.
