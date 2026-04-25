# Sensitivitaetsanalyse fuer Fish-vs-Algae (Nursery)

Szenarien: Baseline, ohne dominante Videos, ohne seltene Features, kombiniert.

| scenario                |   n_videos |   n_sig_bait_bh |   n_sig_interaction_bh |   n_tested |
|:------------------------|-----------:|----------------:|-----------------------:|-----------:|
| baseline                |         10 |               3 |                      0 |         88 |
| no_dominant_videos      |          9 |               5 |                      0 |         77 |
| no_rare_features        |         10 |               3 |                      0 |         88 |
| no_dominant_and_no_rare |          9 |               5 |                      0 |         77 |

## Interpretation
- Die Fish-vs-Algae-Signale bleiben unter den Filtern erhalten, verlieren aber erwartungsgemaess etwas an Testanzahl.
- Dominante Videos und seltene Features erklaeren die Hauptergebnisse nicht allein.
- Die robustesten Gruppen werden in den Kern-Features weiter beobachtet, wenn sie im Filterset enthalten bleiben.