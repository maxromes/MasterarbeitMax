# Prevalence-/Occupancy-Modell mit Mindestnachweis-Schwellen

Stand: 2026-08-16

## Methode

- Einheit: Familie x Video (Presence via family-maxn > 0; fish/algae-Koeder).
- Filter 1: max(Prevalenz_algae, Prevalenz_fish) >= 0.20.
- Filter 2: Gesamtzahl praesenter Videos >= 3.
- Test: Fisher-Exact (two-sided und zusaetzlich one-sided in beobachteter Richtung).
- Multiple Tests: BH/Holm je Standort.

## milimani

| family         |   algae_present |   algae_total |   fish_present |   fish_total |   algae_rate |   fish_rate | direction_observed   |   fisher_p_directional |   q_holm_directional_site |   q_bh_directional_site |
|:---------------|----------------:|--------------:|---------------:|-------------:|-------------:|------------:|:---------------------|-----------------------:|--------------------------:|------------------------:|
| tetraodontidae |               9 |            10 |              1 |            4 |       0.9000 |      0.2500 | algae>fish           |                 0.0410 |                    0.8601 |                  0.7343 |
| zanclidae      |               4 |            10 |              4 |            4 |       0.4000 |      1.0000 | fish>algae           |                 0.0699 |                    1.0000 |                  0.7343 |
| carangidae     |               3 |            10 |              3 |            4 |       0.3000 |      0.7500 | fish>algae           |                 0.1748 |                    1.0000 |                  0.8654 |
| holocentridae  |               4 |            10 |              0 |            4 |       0.4000 |      0.0000 | algae>fish           |                 0.2098 |                    1.0000 |                  0.8654 |
| pinguipedidae  |               4 |            10 |              3 |            4 |       0.4000 |      0.7500 | fish>algae           |                 0.2797 |                    1.0000 |                  0.8654 |
| lethrinidae    |              10 |            10 |              3 |            4 |       1.0000 |      0.7500 | algae>fish           |                 0.2857 |                    1.0000 |                  0.8654 |
| aulostomidae   |               8 |            10 |              2 |            4 |       0.8000 |      0.5000 | algae>fish           |                 0.3107 |                    1.0000 |                  0.8654 |
| lutjanidae     |               7 |            10 |              4 |            4 |       0.7000 |      1.0000 | fish>algae           |                 0.3297 |                    1.0000 |                  0.8654 |
| blenniidae     |               7 |            10 |              2 |            4 |       0.7000 |      0.5000 | algae>fish           |                 0.4545 |                    1.0000 |                  1.0000 |
| monacanthidae  |               7 |            10 |              3 |            4 |       0.7000 |      0.7500 | fish>algae           |                 0.6893 |                    1.0000 |                  1.0000 |
| siganidae      |               7 |            10 |              3 |            4 |       0.7000 |      0.7500 | fish>algae           |                 0.6893 |                    1.0000 |                  1.0000 |
| cirrhitidae    |               5 |            10 |              2 |            4 |       0.5000 |      0.5000 | algae>fish           |                 0.7203 |                    1.0000 |                  1.0000 |
| acanthuridae   |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| balistidae     |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| chaetodontidae |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| labridae       |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| mullidae       |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| pomacanthidae  |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| pomacentridae  |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| scaridae       |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| serranidae     |              10 |            10 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |

## utumbi

| family         |   algae_present |   algae_total |   fish_present |   fish_total |   algae_rate |   fish_rate | direction_observed   |   fisher_p_directional |   q_holm_directional_site |   q_bh_directional_site |
|:---------------|----------------:|--------------:|---------------:|-------------:|-------------:|------------:|:---------------------|-----------------------:|--------------------------:|------------------------:|
| muraenidae     |               0 |             9 |              4 |            5 |       0.0000 |      0.8000 | fish>algae           |                 0.0050 |                    0.1199 |                  0.1199 |
| aulostomidae   |               9 |             9 |              3 |            5 |       1.0000 |      0.6000 | algae>fish           |                 0.1099 |                    1.0000 |                  0.7552 |
| zanclidae      |               9 |             9 |              3 |            5 |       1.0000 |      0.6000 | algae>fish           |                 0.1099 |                    1.0000 |                  0.7552 |
| carangidae     |               5 |             9 |              5 |            5 |       0.5556 |      1.0000 | fish>algae           |                 0.1259 |                    1.0000 |                  0.7552 |
| nemipteridae   |               3 |             9 |              0 |            5 |       0.3333 |      0.0000 | algae>fish           |                 0.2308 |                    1.0000 |                  0.9231 |
| tetraodontidae |               3 |             9 |              0 |            5 |       0.3333 |      0.0000 | algae>fish           |                 0.2308 |                    1.0000 |                  0.9231 |
| cirrhitidae    |               8 |             9 |              3 |            5 |       0.8889 |      0.6000 | algae>fish           |                 0.2747 |                    1.0000 |                  0.9419 |
| blenniidae     |               6 |             9 |              4 |            5 |       0.6667 |      0.8000 | fish>algae           |                 0.5455 |                    1.0000 |                  1.0000 |
| lethrinidae    |               6 |             9 |              4 |            5 |       0.6667 |      0.8000 | fish>algae           |                 0.5455 |                    1.0000 |                  1.0000 |
| caesionidae    |               6 |             9 |              3 |            5 |       0.6667 |      0.6000 | algae>fish           |                 0.6224 |                    1.0000 |                  1.0000 |
| lutjanidae     |               8 |             9 |              5 |            5 |       0.8889 |      1.0000 | fish>algae           |                 0.6429 |                    1.0000 |                  1.0000 |
| monacanthidae  |               4 |             9 |              2 |            5 |       0.4444 |      0.4000 | algae>fish           |                 0.6573 |                    1.0000 |                  1.0000 |
| siganidae      |               5 |             9 |              3 |            5 |       0.5556 |      0.6000 | fish>algae           |                 0.6573 |                    1.0000 |                  1.0000 |
| scombridae     |               2 |             9 |              1 |            5 |       0.2222 |      0.2000 | algae>fish           |                 0.7253 |                    1.0000 |                  1.0000 |
| acanthuridae   |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| balistidae     |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| chaetodontidae |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| holocentridae  |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| labridae       |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| mullidae       |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| pomacanthidae  |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| pomacentridae  |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| scaridae       |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| serranidae     |               9 |             9 |              5 |            5 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |

## nursery

| family         |   algae_present |   algae_total |   fish_present |   fish_total |   algae_rate |   fish_rate | direction_observed   |   fisher_p_directional |   q_holm_directional_site |   q_bh_directional_site |
|:---------------|----------------:|--------------:|---------------:|-------------:|-------------:|------------:|:---------------------|-----------------------:|--------------------------:|------------------------:|
| muraenidae     |               5 |             6 |              0 |            4 |       0.8333 |      0.0000 | algae>fish           |                 0.0238 |                    0.5476 |                  0.5476 |
| caesionidae    |               6 |             6 |              2 |            4 |       1.0000 |      0.5000 | algae>fish           |                 0.1333 |                    1.0000 |                  0.6133 |
| nemipteridae   |               6 |             6 |              2 |            4 |       1.0000 |      0.5000 | algae>fish           |                 0.1333 |                    1.0000 |                  0.6133 |
| siganidae      |               6 |             6 |              2 |            4 |       1.0000 |      0.5000 | algae>fish           |                 0.1333 |                    1.0000 |                  0.6133 |
| zanclidae      |               6 |             6 |              2 |            4 |       1.0000 |      0.5000 | algae>fish           |                 0.1333 |                    1.0000 |                  0.6133 |
| pinguipedidae  |               3 |             6 |              4 |            4 |       0.5000 |      1.0000 | fish>algae           |                 0.1667 |                    1.0000 |                  0.6389 |
| lethrinidae    |               2 |             6 |              3 |            4 |       0.3333 |      0.7500 | fish>algae           |                 0.2619 |                    1.0000 |                  0.7530 |
| serranidae     |               2 |             6 |              3 |            4 |       0.3333 |      0.7500 | fish>algae           |                 0.2619 |                    1.0000 |                  0.7530 |
| balistidae     |               6 |             6 |              3 |            4 |       1.0000 |      0.7500 | algae>fish           |                 0.4000 |                    1.0000 |                  0.8671 |
| carangidae     |               6 |             6 |              3 |            4 |       1.0000 |      0.7500 | algae>fish           |                 0.4000 |                    1.0000 |                  0.8671 |
| aulostomidae   |               3 |             6 |              1 |            4 |       0.5000 |      0.2500 | algae>fish           |                 0.4524 |                    1.0000 |                  0.8671 |
| monacanthidae  |               3 |             6 |              1 |            4 |       0.5000 |      0.2500 | algae>fish           |                 0.4524 |                    1.0000 |                  0.8671 |
| fistulariidae  |               4 |             6 |              2 |            4 |       0.6667 |      0.5000 | algae>fish           |                 0.5476 |                    1.0000 |                  0.9689 |
| diodontidae    |               2 |             6 |              1 |            4 |       0.3333 |      0.2500 | algae>fish           |                 0.6667 |                    1.0000 |                  1.0000 |
| tetraodontidae |               4 |             6 |              3 |            4 |       0.6667 |      0.7500 | fish>algae           |                 0.6667 |                    1.0000 |                  1.0000 |
| pomacanthidae  |               3 |             6 |              2 |            4 |       0.5000 |      0.5000 | algae>fish           |                 0.7381 |                    1.0000 |                  1.0000 |
| acanthuridae   |               6 |             6 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| chaetodontidae |               6 |             6 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| labridae       |               6 |             6 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| lutjanidae     |               6 |             6 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| mullidae       |               6 |             6 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| pomacentridae  |               6 |             6 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |
| scaridae       |               6 |             6 |              4 |            4 |       1.0000 |      1.0000 | algae>fish           |                 1.0000 |                    1.0000 |                  1.0000 |

