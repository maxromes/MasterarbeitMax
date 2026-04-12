# Artenvergleich der Standorte (cut_47min) – Ergebnisdarstellung im Thesis-Stil

## Zielsetzung
Ziel dieser Auswertung war es, die Überlappung und die standortspezifischen Unterschiede in der Taxazusammensetzung zwischen Milimani, Utumbi und Nursery zu quantifizieren. Der inhaltliche Schwerpunkt lag auf dem Vergleich Milimani vs. Utumbi, da an beiden Standorten dieselben Köderkategorien eingesetzt wurden.

## Datengrundlage und methodisches Vorgehen
Die Analyse basiert auf allen verfügbaren cut_47min-Videos (n = 46). Pro Standort wurde ein aggregierter Taxa-Pool gebildet. Taxa wurden hierarchisch aus den Annotationen abgeleitet (species > genus > family/label). Einträge mit feeding/interested wurden ausgeschlossen.

Für die Standortvergleiche wurden berechnet:
- Schnittmenge und Vereinigungsmenge der Taxa je Standortpaar
- Jaccard-Ähnlichkeit als Maß der Überlappung
- Anzahl exklusiver (standortspezifischer) Taxa
- Präsenzmuster über alle drei Standorte (z. B. 111 = in allen drei Standorten vorhanden)

## Ergebnisse

### Fokusvergleich Milimani vs. Utumbi
Milimani und Utumbi weisen die höchste Ähnlichkeit aller Standortpaare auf. Beide Standorte teilen 88 Taxa; die Jaccard-Ähnlichkeit beträgt 0.647. Gleichzeitig bestehen standortspezifische Unterschiede: 16 Taxa traten ausschließlich in Milimani auf, 32 ausschließlich in Utumbi.

Diese Befunde zeigen, dass trotz hoher gemeinsamer Artenbasis eine relevante standortbezogene Differenzierung der Artenzusammensetzung vorliegt.

### Vergleich aller drei Standorte
Im Paarvergleich ergaben sich folgende Überlappungen:

| Standortpaar | Schnittmenge | Vereinigungsmenge | Jaccard-Ähnlichkeit | Exklusiv Site A | Exklusiv Site B |
|:--|--:|--:|--:|--:|--:|
| Milimani vs. Utumbi | 88 | 136 | 0.647 | 16 | 32 |
| Milimani vs. Nursery | 63 | 140 | 0.450 | 41 | 36 |
| Utumbi vs. Nursery | 63 | 156 | 0.404 | 57 | 36 |

Damit ist Milimani vs. Utumbi das ähnlichste Paar, während Utumbi vs. Nursery die geringste Überlappung aufweist.

### Standortspezifische Taxa
Die Anzahl ausschließlich standortspezifischer Taxa verteilte sich wie folgt:

| Standort | Standortspezifische Taxa |
|:--|--:|
| Milimani | 5 |
| Utumbi | 21 |
| Nursery | 25 |

Nursery und Utumbi zeigten demnach die höchste Zahl exklusiver Taxa, Milimani die niedrigste.

### Taxa mit breiter Standortverteilung
In allen drei Standorten gemeinsam wurden 52 Taxa nachgewiesen (Präsenzmuster 111). Zusätzlich traten 36 Taxa ausschließlich in Milimani und Utumbi gemeinsam auf (Präsenzmuster 110). Dieses Muster unterstreicht die vergleichsweise stärkere Nähe zwischen Milimani und Utumbi.

## Interpretation
Die Ergebnisse sprechen für eine zweigeteilte Struktur:
- Einerseits existiert ein substantieller gemeinsamer Kern an Taxa zwischen den Standorten.
- Andererseits zeigen die standortspezifischen Taxa, insbesondere in Utumbi und Nursery, deutliche lokale Unterschiede in der Gemeinschaftszusammensetzung.

Der Fokusvergleich bestätigt, dass Milimani und Utumbi trotz identischer Köderlandschaft nicht als vollständig austauschbar betrachtet werden sollten. Die hohe Überlappung wird von relevanten exklusiven Anteilen begleitet, was auf zusätzliche standortabhängige ökologische oder habitatbezogene Effekte hinweist.

## Zugehörige Ergebnisdateien und Abbildungen
- Paarvergleich: [pairwise_site_overlap.csv](pairwise_site_overlap.csv)
- Präsenzmuster: [taxa_presence_patterns_summary.csv](taxa_presence_patterns_summary.csv)
- Standortspezifische Taxa (Anzahlen): [site_specific_taxa_counts.csv](site_specific_taxa_counts.csv)
- Fokuslisten Milimani/Utumbi: [focus_milimani_utumbi_taxa_lists.csv](focus_milimani_utumbi_taxa_lists.csv)

Abbildungen:
- [figures/pairwise_shared_unique_taxa.png](figures/pairwise_shared_unique_taxa.png)
- [figures/taxa_presence_patterns.png](figures/taxa_presence_patterns.png)
- [figures/focus_milimani_utumbi_shared_unique.png](figures/focus_milimani_utumbi_shared_unique.png)
- [figures/site_specific_taxa_counts.png](figures/site_specific_taxa_counts.png)
