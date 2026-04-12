# Koedervergleich: Bisherige Ergebnisse und weitere Analyseideen

## Bereits abgearbeitet
1. Standortvergleich (alle 3 Standorte, cut_47min) inklusive Signifikanztests:
   results/Standortvergleich/standortvergleich.md
2. Ergebnis: Alle Standortpaare waren signifikant unterschiedlich (global + paarweise), daher keine Replikatbehandlung von Milimani und Utumbi.
3. Artenvergleich nach Standort (Ueberlappung, exklusive Taxa, Praesenzmuster, Grafiken):
   results/Artenvergleich_standort/artenvergleich_standort.md
4. Vollstaendige Liste standortspezifischer Taxa ergaenzt:
   results/Artenvergleich_standort/artenvergleich_standort.md
5. Koedervergleich getrennt nach Standort umgesetzt (Milimani/Utumbi separat):
   results/artenvergleich_köder/artenvergleich_koeder_summary.md
6. Standort-spezifische Koederberichte + Grafiken erzeugt:
   results/artenvergleich_köder/milimani/artenvergleich_koeder_milimani.md
   results/artenvergleich_köder/utumbi/artenvergleich_koeder_utumbi.md

## Wichtige bisherige Koeder-Erkenntnisse
1. Milimani: hoechste Koeder-Ueberlappung control vs ulva_gutweed (Jaccard 0.697).
2. Utumbi: hoechste Koeder-Ueberlappung control vs sargassum (Jaccard 0.764).
3. Taxa in allen Koedern:
   Milimani 31, Utumbi 43.
4. Es gibt in beiden Standorten klar koederspezifische Taxa (bereits als Listen exportiert).

## Moegliche weitere statistische Ideen (Koedervergleich)
1. Signifikanztest der Community-Unterschiede je Standort mit PERMANOVA (Jaccard/Bray-Curtis):
   Testet, ob sich die gesamte Artenzusammensetzung zwischen Koedern statistisch unterscheidet.
2. Pruefen der Dispersion mit PERMDISP:
   Wichtig, um PERMANOVA korrekt zu interpretieren (Unterschiede in Zentroiden vs Streuung).
3. Paarweise PERMANOVA zwischen Koedern mit FDR/Holm-Korrektur:
   Gibt konkrete Aussagen, welche Koeder sich innerhalb eines Standorts unterscheiden.
4. Indikatorarten-Analyse (IndVal) je Koeder:
   Findet Taxa, die besonders typisch fuer einzelne Koeder sind.
5. Taxonweise Tests (Praesenz/Absenz) zwischen Koedern:
   Fisher-Exact oder logistische Modelle pro Taxon, dann multiple Testkorrektur.
6. Artenreichtum je Video modellieren:
   GLM/Negative Binomial oder robuste nichtparametrische Tests innerhalb jedes Standorts fuer Koeder-Effekte auf Richness.
7. Rarefaction/Standardisierung auf Stichprobentiefe:
   Sinnvoll wegen ungleicher Videoanzahl pro Koeder (z. B. fischmix in Milimani nur n=1).
8. Konsistenzanalyse zwischen Standorten:
   Vergleichen, ob derselbe Koeder in Milimani und Utumbi aehnliche Rangfolgen/Community-Effekte zeigt (ohne Replikatannahme).
