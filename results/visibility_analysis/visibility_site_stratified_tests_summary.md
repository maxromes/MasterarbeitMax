# Standort-stratifizierte Sicht-Analyse

Stand: 2026-04-27

## Methode

- Analyse getrennt fuer jeden Standort (milimani, nursery, utumbi).
- Endpunkte: maxn_video_peak, species_richness, first_seen_median_sec.
- Modell je Standort/Endpunkt: OLS auf log1p(Endpunkt) mit visibility_c, plus C(koeder) sofern >= 2 Koeder im Standort.
- Inferenz: HC3 robuste Standardfehler und blockierter Permutationstest innerhalb Koeder.
- Multiple-Testing ueber alle 9 Standort-Endpunkt-Tests: BH/FDR, Holm, Bonferroni, BY.

## Ergebnisse

| Standort | Metrik | n | Beta | 95%-CI | p(HC3) | p(Perm blockiert) | q(HC3,BH) | q(Perm,BH) |
|---|---|---:|---:|---|---:|---:|---:|---:|
| milimani | maxn_video_peak | 17 | 0.060 | [-inf, inf] | 1 | 0.997 | 1 | 1 |
| milimani | species_richness | 17 | -0.005 | [-inf, inf] | 1 | 0.999 | 1 | 1 |
| milimani | first_seen_median_sec | 17 | -0.034 | [-inf, inf] | 1 | 0.995 | 1 | 1 |
| nursery | maxn_video_peak | 11 | 0.361 | [-inf, inf] | 1 | 1 | 1 | 1 |
| nursery | species_richness | 11 | 0.009 | [-inf, inf] | 1 | 1 | 1 | 1 |
| nursery | first_seen_median_sec | 11 | -0.294 | [-inf, inf] | 1 | 1 | 1 | 1 |
| utumbi | maxn_video_peak | 18 | -0.012 | [-0.109, 0.086] | 0.7947 | 0.7203 | 1 | 1 |
| utumbi | species_richness | 18 | 0.009 | [-0.015, 0.034] | 0.4207 | 0.3167 | 1 | 1 |
| utumbi | first_seen_median_sec | 18 | -0.016 | [-0.179, 0.146] | 0.828 | 0.7463 | 1 | 1 |

## Kurzfazit

- Kein standortspezifischer Sicht-Effekt bleibt nach FDR-Korrektur robust signifikant.
- Die uebergeordnete Schlussfolgerung bleibt stabil: Sicht zeigt keinen belastbaren eigenstaendigen Treiber-Effekt auf die Endpunkte.
