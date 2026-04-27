# Praesentation: Statistische Tests und zentrale Ergebnisse (Mastervorlage)

Stand: 2026-04-27
Zweck: Diese Datei ist eine direkt nutzbare Blaupause fuer eine PowerPoint-Praesentation.
Zielgruppe: Fachpublikum (Statistik + Oekologie), aber auch fuer gemischtes Publikum geeignet.

---

## Inhaltsverzeichnis

1. Ziel der Praesentation
2. Executive Summary (1 Slide)
3. Datengrundlage und Analyseprinzipien
4. Methodenueberblick (welcher Test fuer welche Frage)
5. Ergebnisblock A: Standorteffekte (robusteste Signale)
6. Ergebnisblock B: Koedereffekte in Zusammensetzung und Haeufigkeit
7. Ergebnisblock C: Verhalten (`feeding` vs `interested`)
8. Ergebnisblock D: Fish-vs-Algae Funktionsvergleich
9. Ergebnisblock E: Sichtweite (Visibility)
10. Robustheit, Grenzen und offene methodische Punkte
11. Schlussfolgerungen und Handlungsempfehlungen
12. Folienplan (Slide-by-Slide, direkt umsetzbar)
13. Anhang: Quellen, QA-Checkliste und Backup-Folien

---

## 1. Ziel der Praesentation

Die Praesentation soll drei Dinge leisten:

- Klar trennen zwischen robusten Befunden und explorativen Signalen.
- Methodisch sauber erklaeren, warum bestimmte Effekte nach Korrektur bleiben oder verschwinden.
- Eine belastbare Hauptbotschaft formulieren, die mit den Reports konsistent ist.

Vorgeschlagene Leitfrage:

> Wie stark praegen Standort, Koeder, Verhalten und Sichtweite die beobachteten Gemeinschafts- und Haeufigkeitsmuster?

---

## 2. Executive Summary (1 Slide)

Kernaussagen in 5 Punkten:

- Standorteffekte sind der robusteste Befund.
  - 161 getestete Taxa, 93 roh signifikant, 36 Holm-signifikant.
  - Quelle: [taxahäufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

- Koeder beeinflussen die Zusammensetzung global, aber Einzeltaxa bleiben meist nicht Holm-robust.
  - Globale PERMANOVA in allen 3 Standorten signifikant.
  - Quelle: [artenvergleich_köder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

- Fish-vs-Algae zeigt robuste Signale v. a. auf der fish-Seite (insb. Utumbi).
  - Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

- `feeding` und `interested` sind verwandt, aber nicht identisch.
  - Quelle: [interested_feeding/interested_feeding_summary.md](interested_feeding/interested_feeding_summary.md)

- Visibility ist bivariat sichtbar, aber adjustiert nicht robust signifikant.
  - Quelle: [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

Ein-Satz fuer die erste Folie:

> Die staerksten und robustesten Unterschiede liegen auf Standort- und Gemeinschaftsebene; Koeder- und Verhaltenseffekte sind vorhanden, aber differenzierter und je nach Testfamilie weniger stabil.

---

## 3. Datengrundlage und Analyseprinzipien

Datengrundlage:

- 46 Videos (cut_47min)
- Standorte: Milimani, Utumbi, Nursery
- Mehrere Analyseebenen: Taxon-Haeufigkeit (MaxN), Zusammensetzung, Verhalten, Sichtweite

Analyseprinzipien:

- Nichtparametrische Tests fuer viele Taxonvergleiche (Kruskal-Wallis, Mann-Whitney U).
- Multiple-Testing-Korrektur standardmaessig mit Holm; zusaetzlich BH/FDR in Sensitivitaeten.
- Kompositionelle Tests via PERMANOVA auf Jaccard-Distanzen.
- Sichtanalyse getrennt in bivariat und adjustiert (Standort + Koeder als Kovariaten).

Wichtiger methodischer Satz fuer den Vortrag:

> Roh-p-Werte zeigen Suchsignale; inferenzielle Kernaussagen basieren auf korrigierten p-/q-Werten.

---

## 4. Methodenueberblick (welcher Test fuer welche Frage)

| Fragestellung | Primaerer Test | Korrektur | Was bedeutet ein positiver Befund? |
|:--|:--|:--|:--|
| Unterscheiden sich Taxa-Haeufigkeiten zwischen Standorten? | Kruskal-Wallis je Taxon | Holm | Standortabhaengige MaxN-Struktur |
| Welche Gruppen unterscheiden sich paarweise? | Mann-Whitney U | Holm je Taxon | Konkrete Gruppenunterschiede |
| Unterscheiden sich Koeder in der Zusammensetzung? | PERMANOVA (Jaccard) | Paarweise Holm | Globaler/paarspezifischer Kompositionseffekt |
| Sind `feeding` und `interested` konsistent? | Spearman/Pearson + Taxonvergleiche | Holm/BH | Verhaltenskategorien laufen gemeinsam oder getrennt |
| Ist Sichtweite ein unabhaengiger Treiber? | Spearman (bivariat), OLS+HC3+Permutation (adjustiert) | BH/Holm/BY/Bonf. | Sicht bleibt auch nach Kovariatenkontrolle wirksam |

---

## 5. Ergebnisblock A: Standorteffekte (robusteste Signale)

Quelle: [taxahäufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

Zentrale Kennzahlen:

- `n_taxa_tested = 161`
- `n_significant_raw_p_lt_0_05 = 93`
- `n_significant_holm_p_lt_0_05 = 36`

Interpretation fuer Folien:

- Der Standorteffekt ist statistisch robust und biologisch gross.
- Das ist kein Randbefund, sondern die tragende Struktur im Datensatz.
- Standorte duerfen nicht als austauschbare Replikate behandelt werden.

Empfohlene Visuals:

- Heatmap/Barplot der signifikanten Taxa nach Standort
- Auszug Top-Taxa mit Effektgroessen und Richtung

Sprechtext (30-40 Sekunden):

> Wenn wir auf die Taxa-Haeufigkeit schauen, ist der Standorteffekt klar dominant: 36 Taxa bleiben auch nach Holm-Korrektur signifikant. Das ist die robusteste Evidenz im gesamten Projekt.

---

## 6. Ergebnisblock B: Koedereffekte in Zusammensetzung und Haeufigkeit

### 6.1 Koedervergleich: Taxa-Haeufigkeit (MaxN)

Quelle: [taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)

Kernergebnis:

- Milimani: 104 Taxa getestet, 6 roh signifikant, 0 Holm-signifikant
- Nursery: 99 Taxa getestet, 11 roh signifikant, 0 Holm-signifikant
- Utumbi: 120 Taxa getestet, 8 roh signifikant, 0 Holm-signifikant

Interpretation:

- Es gibt Hinweise auf Koedereffekte, aber taxonweise keine robuste Holm-Evidenz.
- Das Muster ist eher verteilt (viele kleine Unterschiede) statt punktuell (wenige sehr starke Taxa).

### 6.2 Koedervergleich: Zusammensetzung (PERMANOVA)

Quelle: [artenvergleich_köder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

Kernergebnis:

- Milimani global signifikant (`p = 0.0242`)
- Utumbi global signifikant (`p = 0.0046`)
- Nursery global signifikant (`p = 0.0016`)

Interpretation:

- Koeder verschieben die Gemeinschaftszusammensetzung global in allen Standorten.
- Paarweise Einzelvergleiche bleiben nach Holm oft nicht signifikant.

Sprechtext (45 Sekunden):

> Bei Koedern sehen wir ein zweistufiges Bild: global kompositionell klar signifikant, aber auf Einzeltaxon-Ebene konservativ gerechnet nicht robust. Das passt zu einem breiten, verteilten Koedereffekt.

---

## 7. Ergebnisblock C: Verhalten (`feeding` vs `interested`)

Quelle: [interested_feeding/interested_feeding_summary.md](interested_feeding/interested_feeding_summary.md)

Kernergebnis:

- `feeding` zeigt mehr Rohsignale als `interested`.
- Holm-robuste Einzeltaxa sind selten.
- Event-basierte Globaltests sind standortabhaengig teils signifikant.

Interpretation:

- Beide Verhaltensflags sind verwandt, aber funktional nicht deckungsgleich.
- `feeding` ist oft das schaerfere Signal.

Praktischer Foliensatz:

> `feeding` und `interested` sollten zusammen berichtet, aber nicht gleichgesetzt werden.

---

## 8. Ergebnisblock D: Fish-vs-Algae Funktionsvergleich

Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

Kernergebnis:

- Global ueber alle Koeder: keine Holm/BH-signifikanten Gruppen.
- Im direkten Fish-vs-Algae-Vergleich: mehrere BH-signifikante Gruppen, insbesondere in Utumbi.
- Signifikante Gruppen liegen ueberwiegend auf der fish-Seite (`higher_side = fish`).

Interpretation:

- Die Richtung des Effekts ist konsistent: fish-basiert > algae-basiert fuer viele Funktionsgruppen.
- Algennahe Effekte erscheinen eher explorativ als robust inferenziell.

Empfohlene Figuren:

- Signifikanzsummary Fish-vs-Algae
- Top-Effektgroessen (Cliff's Delta)

Sprechtext (40 Sekunden):

> Der Fish-vs-Algae-Vergleich zeigt den klarsten Koedereffekt in Richtung fish-basierter Koeder, vor allem in Utumbi. Das ist kein universeller Taxon-Einzeleffekt, aber ein konsistentes Funktionsmuster.

---

## 9. Ergebnisblock E: Sichtweite (Visibility)

Quellen:

- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

Kernergebnis:

- Bivariat: positive Zusammenhaenge mit `maxn_video_peak` und `species_richness`.
- Adjustiert (`+ standort + koeder`): kein robuster Sicht-Effekt auf die 3 Endpunkte.
- Zusatztests (Permutation, Quadratik, Quantilsregression, multiple Korrekturen) bestaetigen den Nullbefund.

Interpretation:

- Sichtweite ist relevanter Messkontext, aber kein unabhaengiger Treiber nach Kovariatenkontrolle.

Sprechtext (35 Sekunden):

> Sichtweite erklaert Rohmuster mit, traegt aber in den adjustierten Modellen keine robuste eigenstaendige Signalwirkung.

---

## 10. Robustheit, Grenzen und offene methodische Punkte

### 10.1 Was ist robust?

- Standorteffekt (Taxa-Haeufigkeit) ist robust.
- Globale Koederunterschiede in der Zusammensetzung sind robust.
- Visibility-Nullbefund nach Adjustierung ist robust.

### 10.2 Wo sind Grenzen?

- Viele parallele Taxon-Tests reduzieren Power nach Korrektur.
- Unbalancierte Koederverteilung je Standort.
- Kleine Zellgroessen in einigen standort-spezifischen Vergleichen.

### 10.3 Offene Punkte fuer naechste Runde

- Mixed-Effects / hierarchische Modelle fuer Video- und Standortstruktur.
- PERMDISP als Streuungscheck fuer PERMANOVA-Befunde.
- Seltenheits-/Sampling-Normalisierung (Rarefaction-Ansatz, falls methodisch gewuenscht).

---

## 11. Schlussfolgerungen und Handlungsempfehlungen

Empfohlene Schlussbotschaft:

> Der zentrale Treiber ist der Standort. Koeder veraendern die Gemeinschaft global, aber meist als verteiltes Muster statt als einzelne harte Taxon-Signale. Sichtweite wirkt vor allem als Kontextfaktor, nicht als unabhaengiger Treiber nach Adjustierung.

Praxisempfehlungen fuer Berichterstattung:

- Primaer: Standort- und globale Kompositionsbefunde.
- Sekundaer: Fish-vs-Algae Funktionsmuster mit klarer Trennung zwischen robust und explorativ.
- Transparenz: Roh- und korrigierte Signale immer nebeneinander zeigen.

---

## 12. Folienplan (Slide-by-Slide, direkt umsetzbar)

Hinweis: Dieser Plan ist fuer 16 Folien ausgelegt (ca. 15-20 Minuten Vortrag).

### Folie 1 - Titel und Leitfrage

- Titel: "Statistische Gesamtauswertung: Standort, Koeder, Verhalten und Sicht"
- Untertitel: Datensatz, Zeitraum, Team
- Kernfrage (1 Satz)

### Folie 2 - Agenda

- 5 Bloecke: Daten, Methoden, Hauptergebnisse, Robustheit, Fazit

### Folie 3 - Datengrundlage

- 46 Videos
- 3 Standorte
- Endpunkte und Ebenen

### Folie 4 - Methodenlandkarte

- Tabelle "Frage -> Test -> Korrektur"
- Ein Satz zu Holm vs BH

### Folie 5 - Standorteffekt: Uebersicht

- 161 / 93 / 36 Kennzahlen gross darstellen
- Kurzinterpretation

### Folie 6 - Standorteffekt: Beispiele

- Top signifikante Taxa (3-6 Beispiele)
- Richtung pro Standort

### Folie 7 - Koeder-Haeufigkeit

- Pro Standort: roh signifikant vs Holm signifikant
- Aussage: keine Holm-robusten Einzeltaxa

### Folie 8 - Koeder-Komposition

- PERMANOVA p-Werte je Standort
- Aussage: global signifikant in allen Standorten

### Folie 9 - Fish-vs-Algae (Konzept)

- Vergleichslogik
- Warum zusaetzlich zur Standardanalyse?

### Folie 10 - Fish-vs-Algae (Ergebnisse)

- Anzahl BH-signifikanter Gruppen nach Standort/Feature-Typ
- Fokus auf `higher_side = fish`

### Folie 11 - Verhalten feeding vs interested

- Gegenueberstellung: Signifikanzmuster und Korrelationen
- Kernaussage: verwandt, nicht identisch

### Folie 12 - Visibility: bivariater vs adjustierter Blick

- Links: bivariater Zusammenhang
- Rechts: adjustierte Modelle mit Nullbefund

### Folie 13 - Robustheit und Sensitivitaet

- Welche Zusatzanalysen gemacht?
- Was blieb stabil?

### Folie 14 - Grenzen und Unsicherheiten

- Kleine n in Teilanalysen
- Multiple Tests
- Design-/Balance-Aspekte

### Folie 15 - Schlussfolgerung

- 3 Kernsaetze
- Prioritaeten fuer Interpretation

### Folie 16 - Next Steps

- 3 methodische Prioritaeten
- 1 praktische Empfehlung fuer die naechste Datenerhebung

---

## 13. Anhang: Quellen, QA-Checkliste und Backup-Folien

### 13.1 Primarquellen (im Vortrag referenzierbar)

- Standort-Haeufigkeit:
  - [taxahäufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)
- Koeder-Haeufigkeit:
  - [taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)
- Koeder-Komposition:
  - [artenvergleich_köder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)
- Verhalten:
  - [interested_feeding/interested_feeding_summary.md](interested_feeding/interested_feeding_summary.md)
  - [interested_feeding/ubiquitous_nonbehavioral_filter_sensitivity.md](interested_feeding/ubiquitous_nonbehavioral_filter_sensitivity.md)
- Funktionsvergleich:
  - [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)
- Sichtanalyse:
  - [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
  - [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
  - [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

### 13.2 QA-Checkliste vor dem Export in PowerPoint

- Stimmen alle Zahlen mit den aktuellen Report-Dateien ueberein?
- Sind Roh- und korrigierte Signale klar getrennt beschriftet?
- Ist bei jeder Statistik die Testfamilie genannt?
- Haben alle Plots Achsenbeschriftungen, n und Legenden?
- Ist die Schlussfolie konsistent mit den robusten (korrigierten) Befunden?

### 13.3 Backup-Folien (empfohlen)

- Backup A: Vollstaendige Testmatrix pro Standort
- Backup B: Tabelle aller BH-signifikanten Fish-vs-Algae-Features
- Backup C: Visibility-Detailtabellen (HC3, Permutation, partielle Spearman)
- Backup D: Sensitivitaetsanalysen mit alternativen Filtern

---

## Plausibilitaets- und Vollstaendigkeitscheck dieser Vorlage

Diese Vorlage wurde gegen die aktuellen Kernreports geprueft und auf direkte Foliennutzbarkeit umgebaut.

Plausibilitaet:

- Schluesselzahlen (z. B. 161/93/36; 0 Holm-signifikante Taxa im Koeder-Haeufigkeitsvergleich) sind konsistent mit den zitierten Summary-Dateien.
- Visibility-Interpretation folgt dem aktuellen adjustierten Nullbefund.
- Aussagen trennen robust (korrigiert signifikant) und explorativ (roh signifikant).

Vollstaendigkeit:

- Alle zentralen Ergebnisbloeke enthalten: Standort, Koeder, Verhalten, Fish-vs-Algae, Visibility, Robustheit.
- Ein durchgaengiger Folienplan mit Sprechtext und Priorisierung ist enthalten.
- Quellen- und QA-Bereich fuer finalen PowerPoint-Bau ist enthalten.

Direkt-nutzbar-fuer-PowerPoint:

- Du kannst die 16 Folien 1:1 aus Abschnitt 12 uebernehmen.
- Abschnitt 2 liefert die Intro-Slide; Abschnitt 11 die Schlussfolie.
- Abschnitt 13 dient als Appendix und als Check vor finalem Export.
