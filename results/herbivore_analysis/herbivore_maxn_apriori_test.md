# A Priori Herbivore MaxN Test

**A priori Hypothese**: Herbivore zeigen signifikant höhere MaxN bei Algenködern als bei Fischködern.

**Begründung**: Herbivore ernähren sich evolutiv von Algen; daher sollte ein Algenköder attraktiver sein.

**Testdesign**: Pro Familie (Siganidae, Acanthuridae, Scaridae, Blenniidae) und Standort wird MaxN verglichen.
- Nur 4 Familien getestet (keine 161+ Taxa wie im globalen Test)
- Holm-Korrektur über 4 Hypothesen pro Standort
- Gerichtete Tests (Algae > Fish)

## Ergebnisse nach Standort

### Milimani

**Alle Familien (sortiert nach p-Wert):**

- blennies (Blenniidae): Algae=1.0|1.00, Fish=0.5|1.00, p=0.4117 (Holm: 1.0000), Δ=0.1000
- rabbitfishes (Siganidae): Algae=2.0|1.40, Fish=2.0|1.50, p=0.6066 (Holm: 1.0000), Δ=-0.0500
- parrotfishes (Scaridae): Algae=5.0|7.90, Fish=6.0|7.75, p=0.6910 (Holm: 1.0000), Δ=-0.1500
- surgeonfishes (Acanthuridae): Algae=5.0|5.00, Fish=22.5|28.75, p=0.9271 (Holm: 1.0000), Δ=-0.4750

### Utumbi

**Alle Familien (sortiert nach p-Wert):**

- parrotfishes (Scaridae): Algae=11.0|18.78, Fish=7.0|8.80, p=0.1743 (Holm: 0.6970), Δ=0.3333
- rabbitfishes (Siganidae): Algae=2.0|1.67, Fish=1.0|0.80, p=0.2845 (Holm: 0.8535), Δ=0.2000
- surgeonfishes (Acanthuridae): Algae=3.0|2.89, Fish=3.0|5.00, p=0.8542 (Holm: 1.0000), Δ=-0.3111
- blennies (Blenniidae): Algae=1.0|0.67, Fish=1.0|1.20, p=0.9228 (Holm: 1.0000), Δ=-0.4000

### Nursery

**Holm-signifikante Familien (p < 0.05):**

- **surgeonfishes (Acanthuridae)**: Algae-Median = 22.0, Fish-Median = 4.5, p = 0.0278, Cliffs Δ = 1.0000

**Alle Familien (sortiert nach p-Wert):**

- surgeonfishes (Acanthuridae)*: Algae=22.0|23.33, Fish=4.5|5.50, p=0.0070 (Holm: 0.0278), Δ=1.0000
- rabbitfishes (Siganidae): Algae=4.0|4.00, Fish=1.0|1.75, p=0.1124 (Holm: 0.3373), Δ=0.5000
- parrotfishes (Scaridae): Algae=7.0|7.67, Fish=8.5|7.75, p=0.5428 (Holm: 1.0000), Δ=0.0000
- blennies (Blenniidae): Algae=0.0|0.00, Fish=0.5|0.75, p=0.9760 (Holm: 1.0000), Δ=-0.5000

## Zusammenfassung (alle Standorte)

| site     | family_common                |   algae_maxn_median |   fish_maxn_median |   median_diff_algae_minus_fish |    p_value |   p_value_holm |   cliffs_delta |
|:---------|:-----------------------------|--------------------:|-------------------:|-------------------------------:|-----------:|---------------:|---------------:|
| milimani | surgeonfishes (Acanthuridae) |                   5 |               22.5 |                          -17.5 | 0.92713    |      1         |      -0.475    |
| milimani | blennies (Blenniidae)        |                   1 |                0.5 |                            0.5 | 0.411691   |      1         |       0.1      |
| milimani | parrotfishes (Scaridae)      |                   5 |                6   |                           -1   | 0.691049   |      1         |      -0.15     |
| milimani | rabbitfishes (Siganidae)     |                   2 |                2   |                            0   | 0.60658    |      1         |      -0.05     |
| utumbi   | surgeonfishes (Acanthuridae) |                   3 |                3   |                            0   | 0.854227   |      1         |      -0.311111 |
| utumbi   | blennies (Blenniidae)        |                   1 |                1   |                            0   | 0.92278    |      1         |      -0.4      |
| utumbi   | parrotfishes (Scaridae)      |                  11 |                7   |                            4   | 0.17426    |      0.697041  |       0.333333 |
| utumbi   | rabbitfishes (Siganidae)     |                   2 |                1   |                            1   | 0.284498   |      0.853493  |       0.2      |
| nursery  | surgeonfishes (Acanthuridae) |                  22 |                4.5 |                           17.5 | 0.00696096 |      0.0278438 |       1        |
| nursery  | blennies (Blenniidae)        |                   0 |                0.5 |                           -0.5 | 0.976029   |      1         |      -0.5      |
| nursery  | parrotfishes (Scaridae)      |                   7 |                8.5 |                           -1.5 | 0.542837   |      1         |       0        |
| nursery  | rabbitfishes (Siganidae)     |                   4 |                1   |                            3   | 0.11242    |      0.337259  |       0.5      |

**Global signifikante Befunde (Holm, alle Standorte kombiniert):**

- NURSERY / surgeonfishes (Acanthuridae): p_holm = 0.0278
