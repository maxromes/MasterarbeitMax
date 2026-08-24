# Herbivore Feeding Responsiveness Test

**A priori Hypothese**: Herbivore zeigen signifikant häufiger Feeding-Verhalten bei Algenködern als bei Fischködern.

**Methode**: Pro Video und Standort wird die Feeding-Rate berechnet als (# Feeding-Events bei Herbivoren) / (# Gesamteinträge von Herbivoren).
Mann-Whitney U Test (gerichtet) testet: Algae Feeding-Rate > Fish Feeding-Rate.
Sensitivitaetsmetriken (automatisch): (a) Summe familienweiser Feeding-Maxima pro Video (MaxN-konsistent), (b) Anteil Herbivore-Familien mit mindestens einem Feeding-Eintrag.

## Ergebnisse nach Standort

### Milimani

- **N Videos (Algae | Fish)**: 10 | 4
- **Feeding-Rate Algae**: μ = 0.0029, σ = 0.0090, median = 0.0000
- **Feeding-Rate Fish**: μ = 0.0000, σ = 0.0000, median = 0.0000
- **Differenz (Algae - Fish)**: μ = 0.0029, median = 0.0000
- **p-Wert (roh)**: 0.317628
- **Cliffs Delta**: 0.1000

Sensitivitaet:
- Feeding-MaxN-Summe (mean Algae | Fish): 0.1000 | 0.0000; p_raw = 0.317628
- Family-Presence (mean Algae | Fish): 0.0250 | 0.0000; p_raw = 0.317628

### Utumbi

- **N Videos (Algae | Fish)**: 9 | 5
- **Feeding-Rate Algae**: μ = 0.0030, σ = 0.0090, median = 0.0000
- **Feeding-Rate Fish**: μ = 0.0000, σ = 0.0000, median = 0.0000
- **Differenz (Algae - Fish)**: μ = 0.0030, median = 0.0000
- **p-Wert (roh)**: 0.275492
- **Cliffs Delta**: 0.1111

Sensitivitaet:
- Feeding-MaxN-Summe (mean Algae | Fish): 0.1111 | 0.0000; p_raw = 0.275492
- Family-Presence (mean Algae | Fish): 0.0278 | 0.0000; p_raw = 0.275492

### Nursery

- **N Videos (Algae | Fish)**: 6 | 4
- **Feeding-Rate Algae**: μ = 0.2038, σ = 0.0730, median = 0.1938
- **Feeding-Rate Fish**: μ = 0.0000, σ = 0.0000, median = 0.0000
- **Differenz (Algae - Fish)**: μ = 0.2038, median = 0.1938
- **p-Wert (roh)**: 0.005709
- **Cliffs Delta**: 1.0000

Sensitivitaet:
- Feeding-MaxN-Summe (mean Algae | Fish): 13.8333 | 0.0000; p_raw = 0.005709
- Family-Presence (mean Algae | Fish): 0.6667 | 0.0000; p_raw = 0.004339

## Zusammenfassung (Holm-korrigiert)

| site     |   algae_feeding_rate_mean |   fish_feeding_rate_mean |   rate_diff_mean_algae_minus_fish |    p_value |   p_value_holm |   cliffs_delta |   algae_feeding_maxn_sum_mean |   fish_feeding_maxn_sum_mean |   maxn_sum_diff_mean_algae_minus_fish |   p_value_maxn_sum |   p_value_maxn_sum_holm |   algae_family_presence_mean |   fish_family_presence_mean |   family_presence_diff_mean_algae_minus_fish |   p_value_family_presence |   p_value_family_presence_holm |
|:---------|--------------------------:|-------------------------:|----------------------------------:|-----------:|---------------:|---------------:|------------------------------:|-----------------------------:|--------------------------------------:|-------------------:|------------------------:|-----------------------------:|----------------------------:|---------------------------------------------:|--------------------------:|-------------------------------:|
| milimani |                0.00285714 |                        0 |                        0.00285714 | 0.317628   |      0.550985  |       0.1      |                      0.1      |                            0 |                              0.1      |         0.317628   |               0.550985  |                    0.025     |                           0 |                                    0.025     |                0.317628   |                      0.550985  |
| utumbi   |                0.003003   |                        0 |                        0.003003   | 0.275492   |      0.550985  |       0.111111 |                      0.111111 |                            0 |                              0.111111 |         0.275492   |               0.550985  |                    0.0277778 |                           0 |                                    0.0277778 |                0.275492   |                      0.550985  |
| nursery  |                0.203757   |                        0 |                        0.203757   | 0.00570861 |      0.0171258 |       1        |                     13.8333   |                            0 |                             13.8333   |         0.00570861 |               0.0171258 |                    0.666667  |                           0 |                                    0.666667  |                0.00433876 |                      0.0130163 |

**Holm-signifikant (p < 0.05):**
- nursery: p = 0.0171

**Holm-signifikant (MaxN-Sensitivitaet, p < 0.05):**
- nursery: p = 0.0171

**Holm-signifikant (Family-Presence-Sensitivitaet, p < 0.05):**
- nursery: p = 0.0130
