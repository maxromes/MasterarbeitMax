# Herbivore Feeding Responsiveness Test

**A priori Hypothese**: Herbivore zeigen signifikant häufiger Feeding-Verhalten bei Algenködern als bei Fischködern.

**Methode**: Pro Video und Standort wird die Feeding-Rate berechnet als (# Feeding-Events bei Herbivoren) / (# Gesamteinträge von Herbivoren).
Mann-Whitney U Test (gerichtet) testet: Algae Feeding-Rate > Fish Feeding-Rate.

## Ergebnisse nach Standort

### Milimani

- **N Videos (Algae | Fish)**: 10 | 4
- **Feeding-Rate Algae**: μ = 0.0029, σ = 0.0090, median = 0.0000
- **Feeding-Rate Fish**: μ = 0.0000, σ = 0.0000, median = 0.0000
- **Differenz (Algae - Fish)**: μ = 0.0029, median = 0.0000
- **p-Wert (roh)**: 0.317628
- **Cliffs Delta**: 0.1000

### Utumbi

- **N Videos (Algae | Fish)**: 9 | 5
- **Feeding-Rate Algae**: μ = 0.0030, σ = 0.0090, median = 0.0000
- **Feeding-Rate Fish**: μ = 0.0000, σ = 0.0000, median = 0.0000
- **Differenz (Algae - Fish)**: μ = 0.0030, median = 0.0000
- **p-Wert (roh)**: 0.275492
- **Cliffs Delta**: 0.1111

### Nursery

- **N Videos (Algae | Fish)**: 6 | 4
- **Feeding-Rate Algae**: μ = 0.2038, σ = 0.0730, median = 0.1938
- **Feeding-Rate Fish**: μ = 0.0000, σ = 0.0000, median = 0.0000
- **Differenz (Algae - Fish)**: μ = 0.2038, median = 0.1938
- **p-Wert (roh)**: 0.005709
- **Cliffs Delta**: 1.0000

## Zusammenfassung (Holm-korrigiert)

| site     |   algae_feeding_rate_mean |   fish_feeding_rate_mean |   rate_diff_mean_algae_minus_fish |    p_value |   p_value_holm |   cliffs_delta |
|:---------|--------------------------:|-------------------------:|----------------------------------:|-----------:|---------------:|---------------:|
| milimani |                0.00285714 |                        0 |                        0.00285714 | 0.317628   |      0.550985  |       0.1      |
| utumbi   |                0.003003   |                        0 |                        0.003003   | 0.275492   |      0.550985  |       0.111111 |
| nursery  |                0.203757   |                        0 |                        0.203757   | 0.00570861 |      0.0171258 |       1        |

**Holm-signifikant (p < 0.05):**
- nursery: p = 0.0171
