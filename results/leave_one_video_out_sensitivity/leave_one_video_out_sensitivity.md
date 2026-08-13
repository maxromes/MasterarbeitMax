# Systematische Leave-one-video-out-Sensitivitaet

Fokus: robusteste und biologisch zentrale Effekte aus dem Hauptvergleich (Nursery Herbivore, plus die stabilsten Fish-vs-Algae-Familien im Coral-Reef-Datensatz).

Methode: Pro Signal wird jeweils ein einzelnes Video entfernt, der Test mit der biologisch vorgegebenen Richtung erneut gerechnet und die Verteilung der p-Werte dokumentiert.

| signal | site_filter | direction | base_p | loo_p_min | loo_p_max | loo_p_median | n_loo_below_0_05 |
|:---|:---|:---|---:|---:|---:|---:|---:|
| nursery_acanthuridae_algae_gt_fish | nursery | algae > fish | 0.006961 | 0.007937 | 0.013766 | 0.009726 | 10 |
| coral_labridae_fish_gt_algae | milimani, utumbi | fish > algae | 0.000092 | 0.000043 | 0.000208 | 0.000129 | 28 |
| coral_balistidae_fish_gt_algae | milimani, utumbi | fish > algae | 0.001597 | 0.000774 | 0.003866 | 0.001724 | 28 |
| coral_muraenidae_fish_gt_algae | milimani, utumbi | fish > algae | 0.000263 | 0.000113 | 0.000633 | 0.000359 | 28 |

## Interpretation

- Nursery: Acanthuridae bleibt bei jedem einzelnen Video-Remove signifikant (LOO p-Werte zwischen 0.0079 und 0.0138), was zeigt, dass das Ergebnis nicht durch ein einzelnes Video getrieben wird.
- Coral reef: Labridae, Balistidae und Muraenidae bleiben unter ausschliesslicher Entfernung eines einzelnen Videos ebenfalls durchgehend signifikant; damit sind die fish-vs-algae-Hauptsignale robust gegen einzelne Ausreisser.
- Die Schlussfolgerung ist daher konsistent: Die zentralen Effekte sind nicht auf einzelne extreme Videos zurückzuführen; die Hauptergebnisse bleiben stabil, auch wenn die Stichprobe um ein Video kleiner wird.
