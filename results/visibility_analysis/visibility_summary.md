# Sichtweitenanalyse: Zusammenfassung und Interpretation

Stand: 2026-04-27

## Datenabdeckung

- Insgesamt gingen 46 Videos in die Analyse ein.
- Fuer alle Videos liegt nun eine zugeordnete Sichtweite vor (keine fehlenden Sichtweiten mehr).
- Die Abdeckung ist in allen Standort-Koeder-Kombinationen vollstaendig (n_vis = n_videos).

## Statistische Ergebnisse (Visibility Mean vs. Videometriken)

Korrelationen wurden als Spearman (primaer), Kendall und Pearson berechnet. Zur Korrektur fuer multiples Testen ueber die drei Hauptvergleiche wurde Benjamini-Hochberg (BH/FDR) auf die Spearman-p-Werte angewendet.

| Metrik | n | Spearman rho | Spearman p | BH-q | Kendall tau | Pearson r | Einordnung |
|---|---:|---:|---:|---:|---:|---:|---|
| MaxN (video peak) | 46 | 0.467 | 0.00108 | 0.00161 | 0.342 | 0.433 | Signifikanter positiver Zusammenhang |
| Species Richness | 46 | 0.563 | 0.000046 | 0.000138 | 0.422 | 0.567 | Signifikanter positiver Zusammenhang |
| First Seen (Median, s) | 46 | 0.160 | 0.289 | 0.289 | 0.119 | 0.054 | Kein signifikanter Zusammenhang |

## Interpretation

- Bessere Sichtweite geht konsistent mit hoeheren beobachteten Artenzahlen (Species Richness) einher.
- Bessere Sichtweite geht ebenfalls mit hoeheren beobachteten MaxN-Werten einher.
- Fuer den Median von First Seen zeigt sich dagegen kein belastbarer Zusammenhang mit der Sichtweite.

Oekologische bzw. methodische Einordnung:

- Die positiven Zusammenhaenge bei Richness und MaxN sprechen dafuer, dass Detektierbarkeit mit steigender Sichtweite zunimmt (Beobachtungs-/Erfassungsbias).
- Das Ausbleiben eines deutlichen Effekts bei First Seen kann bedeuten, dass der Erstnachweis staerker von Verhaltensdynamik, Taxon-spezifischer Aktivitaet oder Bait-Attraktivitaet getrieben ist als von Sichtweite allein.
- Fuer Interpretation und Vergleich zwischen Behandlungen sollte Sichtweite daher mindestens als Kovariate mitberuecksichtigt werden, insbesondere fuer Richness- und MaxN-basierte Endpunkte.

## Kurzfazit

Die aktualisierten Sichtweiten schliessen die bisherige Datenluecke vollstaendig. Nach Re-Analyse bleibt das Muster stabil: Sichtweite ist ein relevanter Treiber fuer Richness und MaxN, aber nicht fuer First Seen.
