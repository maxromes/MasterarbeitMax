# Mixed-Effects Modell: Kernendpunkte

Stand: 2026-08-16

## Modell

- Datengrundlage: visibility_video_level_merged.csv, fish- und algae-Koeder.
- Endpunkte: species_richness, maxn_video_peak, first_seen_median_sec.
- Response: log1p(Endpunkt).
- Fixed Effects: bait_type (fish vs algae) + visibility_z.
- Random Effects: Random Intercept fuer Standort.
- Inferenz: p-Werte fuer fish-vs-algae-Koeffizient je Endpunkt; Korrektur via BH und Holm ueber 3 Endpunkte.
- Hinweis: Ein Random-Intercept fuer Video ist in endpoint-spezifischen Modellen nicht identifizierbar, da je Endpunkt genau eine Beobachtung pro Video vorliegt.

## Endpoint-spezifische fish-vs-algae Effekte

| Endpoint | n fish | n algae | Beta (log1p) | 95%-CI | p | q_BH | q_Holm | % fish vs algae |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| species_richness | 13 | 25 | -0.0240 | [-0.1219, 0.0739] | 0.6303 | 0.6303 | 0.6303 | -2.37% |
| maxn_video_peak | 13 | 25 | -0.3198 | [-0.7352, 0.0956] | 0.1313 | 0.197 | 0.2626 | -27.37% |
| first_seen_median_sec | 13 | 25 | -0.4665 | [-0.7066, -0.2265] | 0.0001391 | 0.0004174 | 0.0004174 | -37.28% |

## Kurzfazit

- Mindestens ein endpoint-spezifischer fish-vs-algae-Effekt bleibt im Mixed-Effects-Rahmen Holm-signifikant.
- Das Modell ergaenzt die bisherigen standortgetrennten Analysen um einen hierarchischen Ansatz mit Standort-Random-Intercept.
