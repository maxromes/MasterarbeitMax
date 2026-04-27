# Zusatztests: Einfluss der Sicht auf Endpunkte

Stand: 2026-04-27

## Design

- Datensatz: visibility_video_level_merged.csv mit vorhandener visibility_mean.
- Endpunkte: maxn_video_peak, species_richness, first_seen_median_sec.
- Basismodell: OLS auf log1p(Endpunkt), adjustiert fuer Standort + Koeder, HC3 robuste Standardfehler.
- Zusatztests: blockierter Permutationstest (innerhalb Standort x Koeder), Quadratik-Test (visibility_c2), Quantilsregression (Median).
- Multiple-Testing: BH/FDR, Holm, Bonferroni, BY jeweils innerhalb Testfamilie ueber die drei Endpunkte.

## Ergebnisse

| Metrik | n | Beta (linear) | 95%-CI | p(HC3) | p(Perm blockiert) | p(Quadratik) | p(Quantil) |
|---|---:|---:|---|---:|---:|---:|---:|
| maxn_video_peak | 46 | 0.030 | [-0.056, 0.116] | 0.4829 | 0.4182 | 0.7763 | 0.4962 |
| species_richness | 46 | 0.004 | [-0.020, 0.028] | 0.7343 | 0.7211 | 0.9875 | 0.467 |
| first_seen_median_sec | 46 | -0.017 | [-0.119, 0.085] | 0.7385 | 0.7091 | 0.6672 | 0.03112 |

## Korrigierte p-Werte (Auszug)

| Metrik | q_hc3_fdr_bh | q_hc3_holm | q_hc3_bonferroni | q_perm_blocked_fdr_bh | q_quad_fdr_bh | q_quantile_fdr_bh |
|---|---:|---:|---:|---:|---:|---:|
| maxn_video_peak | 0.7385 | 1 | 1 | 0.7211 | 0.9875 | 0.4962 |
| species_richness | 0.7385 | 1 | 1 | 0.7211 | 0.9875 | 0.4962 |
| first_seen_median_sec | 0.7385 | 1 | 1 | 0.7211 | 0.9875 | 0.09335 |

## Kurzfazit

- Keiner der Zusatztests zeigt einen robust signifikanten Einfluss der Sicht nach Korrektur fuer multiples Testen.
- Die Kernaussage bleibt damit stabil: Sicht erklaert die Endpunkte nicht eigenstaendig, sobald Standort und Koeder kontrolliert werden.
