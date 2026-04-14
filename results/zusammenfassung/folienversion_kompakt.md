# Kompakte Folienversion: wichtigste Ergebnisse

Diese Version ist als direkte Foliengrundlage gedacht. Sie reduziert die lange Vorlage auf eine klare, praesentationstaugliche Struktur mit den zentralen Befunden.

## Folie 1: Fragestellung

- Unterscheiden sich die Fischgemeinschaften zwischen Standorten und Koedern?
- Zeigen Taxa-Haeufigkeiten, Zusammensetzung und Verhalten dieselben Muster?
- Welche Ergebnisse sind statistisch robust, welche nur explorativ?

## Folie 2: Methoden in Kurzform

- Kruskal-Wallis fuer Taxa-Haeufigkeiten (MaxN)
- Holm-Korrektur fuer Mehrfachtests
- Mann-Whitney-U fuer Paarvergleiche
- PERMANOVA mit Jaccard-Distanzen fuer Zusammensetzung
- Spearman/Pearson fuer `feeding` vs `interested`
- FDR-/Filter-Sensitivitaet als Robustheitscheck

## Folie 3: Standortunterschiede sind am staerksten

- 161 getestete Taxa im Standortvergleich
- 93 Rohsignale, 36 Holm-signifikant
- Standort ist damit der robusteste Einflussfaktor

![Jaccard-Aehnlichkeit der Standort-Artenpools](figures/site_pool_jaccard_heatmap.png)

![Überlappung der Standorte (PCoA auf Jaccard-Distanzen)](figures/site_overlap_pcoa_jaccard.png)

## Folie 4: Koeder beeinflussen die Zusammensetzung

- In allen drei Standorten ist die Koeder-Zusammensetzung global signifikant verschieden
- Paarweise Unterschiede sind nach Holm meist nicht robust
- Der Effekt ist also global vorhanden, aber verteilt

![Standortspezifische Taxa-Zahl](figures/site_specific_taxa_counts.png)

## Folie 5: Taxa-Haeufigkeit zeigt Trends, aber wenig robuste Koeder-Einzelsignale

- Milimani: 104 Taxa getestet, 0 Holm-signifikant
- Nursery: 99 Taxa getestet, 0 Holm-signifikant
- Utumbi: 120 Taxa getestet, 0 Holm-signifikant
- Rohsignale existieren, aber sie ueberstehen die Mehrfachtest-Korrektur nicht

![Top-20 Taxa nach mittlerem MaxN](figures/top20_taxa_mean_maxn_heatmap.png)

## Folie 6: feeding und interested sind verwandt, aber nicht identisch

- Gesamt-Jaccard der Taxa: 0.529
- Spearman der Video-Totals: 0.720
- Pearson der Video-Totals: 0.692
- Beide Flags treten in 52.2 Prozent der Videos gemeinsam auf

![Taxa-Praesenzmuster im Utumbi-Beispiel](figures/taxa_presence_patterns.png)

## Folie 7: Grouper-Zusatzanalyse

- `family_label::groupers (serranidae)` zeigt in allen Standorten eine Tendenz zu `mackerel` und `fischmix`
- Milimani: p = 0.394, Holm p = 1.0
- Utumbi: p = 0.438, Holm p = 1.0
- Nursery: p = 0.367, Holm p = 1.0
- Die Richtung ist konsistent, aber statistisch nicht robust

## Folie 8: Robustheit und Schlussfolgerung

- Auch nach staerkerer Filterung entstehen keine neuen Holm-signifikanten Taxa
- Die fehlende Einzelsignifikanz ist also stabil
- Staerkste Signale: Standort > Koederzusammensetzung > Verhalten auf Taxa-Ebene

### Schlussbotschaft

> Die staerksten und statistisch robustesten Unterschiede liegen auf der Standort- und Taxa-Haeufigkeitsebene. Koeder beeinflussen die Zusammensetzung klar, aber oft verteilt und nicht als einzelne harte Einzeltaxa-Effekte. `feeding` und `interested` sind biologisch verwandt, liefern aber eine ergaenzende, nicht identische Perspektive.

## Empfohlene Folienreihenfolge

1. Fragestellung
2. Methoden
3. Standortunterschiede
4. Koederzusammensetzung
5. Taxa-Haeufigkeit
6. feeding vs interested
7. Robustheit und Fazit
