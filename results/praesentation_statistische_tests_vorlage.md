# Statistische Gesamtauswertung: Standort, Koeder, Verhalten und Sichtweite

Stand: 2026-04-27

Diese Datei ist eine fachliche Gesamtdarstellung der wichtigsten statistischen Befunde.
Der Schwerpunkt liegt auf:
- robusten, multipeltest-korrigierten Ergebnissen
- konkreten Beispielbefunden mit Zahlen
- klarer Trennung zwischen Signifikanz und Tendenz

---

## Inhaltsverzeichnis

1. Datengrundlage und methodische Leitlinien
2. Robust signifikante Hauptergebnisse
3. Konkrete Beispiele fuer signifikante Effekte
4. Konkrete Beispiele fuer Tendenzen (nicht robust signifikant)
5. Fish-vs-Algae: robuste und explorative Muster
6. Verhalten (`feeding` und `interested`): robuste und grenzwertige Befunde
7. Sichtweite (Visibility): bivariates Signal vs. adjustierte Modelle
8. Gesamtinterpretation und Priorisierung der Evidenz
9. Methodische Grenzen und offene Punkte
10. Quellenverzeichnis

---

## 1. Datengrundlage und methodische Leitlinien

Datengrundlage:
- 46 Videos (`cut_47min`)
- Standorte: Milimani, Utumbi, Nursery
- Zielgroessen: Taxa-Haeufigkeit (MaxN), Taxa-Zusammensetzung, Verhaltensereignisse (`feeding`, `interested`), Sichtweite

Methodischer Rahmen:
- Taxonweise Gruppenvergleiche: Kruskal-Wallis (global), Mann-Whitney U (paarweise)
- Multiple Tests: primaer Holm; in Sensitivitaeten zusaetzlich BH/FDR
- Kompositionsanalyse: PERMANOVA auf Jaccard-Distanzen
- Sichtanalyse: bivariate Korrelationen sowie adjustierte Modelle mit Standort- und Koederkontrolle

Interpretationsregel:
- "Robust" = nach Korrektur signifikant
- "Tendenz" = roh signifikant oder konsistenter Richtungseffekt ohne robuste Korrektur-Signifikanz

---

## 2. Robust signifikante Hauptergebnisse

### 2.1 Standorteffekte auf Taxa-Haeufigkeit (MaxN)

Quelle: [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

Zentrale Kennzahlen:
- Getestete Taxa: 161
- Roh signifikant: 93
- Holm-signifikant: 36
- Anteil Holm-signifikant: 22.36%

Einordnung:
- Das ist der robusteste Befund ueber alle Analysen.
- Standort ist ein starker strukturierender Faktor fuer Haeufigkeiten.

### 2.2 Koederunterschiede in der Zusammensetzung (global)

Quelle: [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

PERMANOVA (global je Standort):
- Milimani: p = 0.0242 (signifikant)
- Utumbi: p = 0.0046 (signifikant)
- Nursery: p = 0.0016 (signifikant)

Einordnung:
- Koeder verschieben die Zusammensetzung der beobachteten Gemeinschaft in allen Standorten.
- Der robuste Effekt liegt auf globaler Ebene, nicht zwingend in einzelnen Paarvergleichen.

### 2.3 Fish-vs-Algae (Funktionsvergleich)

Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

Robuste Richtung:
- Signifikante Fish-vs-Algae-Befunde zeigen ueberwiegend `higher_side = fish`.
- Besonders deutlich in Utumbi mit mehreren BH-signifikanten Funktionsgruppen.

### 2.4 Visibility (adjustiert)

Quellen:
- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

Robuster Schluss:
- Bivariat sind Zusammenhaenge mit MaxN und Richness sichtbar.
- Nach Kontrolle fuer Standort + Koeder bleibt kein robuster, unabhaengiger Sicht-Effekt.

---

## 3. Konkrete Beispiele fuer signifikante Effekte

### 3.1 Standortvergleich (taxonweise, Holm-korrigiert signifikant)

Quelle: [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

Beispiel A:
- Taxon: `species::humpback (lutjanus gibbus)`
- Kruskal-Wallis: p = 2.91e-10, Holm p = 4.69e-08
- Mittelwerte: Milimani 0.00, Utumbi 0.00, Nursery 20.18
- Interpretation: sehr starker standortspezifischer Schwerpunkt in Nursery

Beispiel B:
- Taxon: `species::threespot dascyllus (dascyllus trimaculatus)`
- Kruskal-Wallis: p = 2.91e-10, Holm p = 4.69e-08
- Mittelwerte: Milimani 0.00, Utumbi 0.00, Nursery 8.00
- Interpretation: klarer Standortkontrast mit Konzentration in Nursery

Beispiel C:
- Taxon: `genus::genus soldier`
- Kruskal-Wallis: p = 8.77e-09, Holm p = 1.38e-06
- Mittelwerte: Milimani 0.29, Utumbi 3.17, Nursery 0.00
- Interpretation: deutliches Utumbi-Signal

Beispiel D:
- Taxon: `species::arabian monocle (scolopsis ghanam)`
- Kruskal-Wallis: p = 2.36e-05, Holm p = 0.00326
- Mittelwerte: Milimani 0.12, Utumbi 0.44, Nursery 7.00
- Interpretation: starker Nursery-Schwerpunkt

### 3.2 Kompositionsvergleich nach Koeder (global signifikant)

Quelle: [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

Beispiel A:
- Standort: Utumbi
- PERMANOVA global: p = 0.0046
- Top-Overlap-Paar: control vs sargassum (Jaccard 0.764)
- Interpretation: trotz teils hoher Ueberlappung bleibt die Gesamtstruktur zwischen Koedern signifikant verschieden

Beispiel B:
- Standort: Nursery
- PERMANOVA global: p = 0.0016
- Top-Overlap-Paar: algae_strings vs algaemix (Jaccard 0.662)
- Interpretation: Koedereffekt auf Zusammensetzung ist auch in Nursery robust

### 3.3 Fish-vs-Algae (BH-signifikante Einzelfeatures)

Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

Beispiel A (Milimani):
- Feature: `wrasses` (unspecific)
- p = 0.00171, Holm p = 0.02054, BH p = 0.02054
- Richtung: fish > algae
- Effektgroesse: Cliff's Delta = 0.975

Beispiel B (Utumbi):
- Feature: `eels` (unspecific)
- p = 0.00336, Holm p = 0.04703, BH p = 0.02569
- Richtung: fish > algae
- Effektgroesse: Cliff's Delta = 0.800

Beispiel C (Utumbi):
- Feature: `wrasses` (word_group)
- p = 0.00367, BH p = 0.02814
- Richtung: fish > algae
- Effektgroesse: Cliff's Delta = 0.978

Beispiel D (Utumbi):
- Feature: `invertebrates` (diet)
- p = 0.01050, Holm p = 0.04202, BH p = 0.02895
- Richtung: fish > algae
- Effektgroesse: Cliff's Delta = 0.867

### 3.4 Visibility: konkrete bivariate Signifikanz

Quelle: [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)

Beispiel A:
- `visibility_mean` vs `species_richness`
- Spearman rho = 0.563, p = 4.61e-05, BH q = 1.38e-04
- Interpretation: starker positiver Rohzusammenhang

Beispiel B:
- `visibility_mean` vs `maxn_video_peak`
- Spearman rho = 0.467, p = 0.00108, BH q = 0.00161
- Interpretation: moderater positiver Rohzusammenhang

---

## 4. Konkrete Beispiele fuer Tendenzen (nicht robust signifikant)

### 4.1 Koeder-Haeufigkeit je Standort: Rohsignal ohne Holm-Robustheit

Quelle: [taxahaeufigkeitkoeder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)

Gesamtmuster:
- Milimani: 6 Rohsignale, 0 Holm-signifikant
- Nursery: 11 Rohsignale, 0 Holm-signifikant
- Utumbi: 8 Rohsignale, 0 Holm-signifikant

Konkrete Tendenzbeispiele aus den Top-Rohsignalen:
- Milimani: `species::blue-green (chromis viridis)`
- Milimani: `species::moorish idol (zanclus cornutus)`
- Utumbi: `species::longnose (lethrinus olivaceus)`
- Utumbi: `species::orange-lined (balistapus undulatus)`
- Nursery: `family_label::puffers (tetraodontidae)`

Interpretation:
- Es gibt wiederholt gerichtete Koederhinweise, aber keine ausreichende Robustheit nach strenger Korrektur.

### 4.2 Globaltest ohne robuste paarweise Signifikanz

Quelle: [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

Muster:
- Globale PERMANOVA je Standort signifikant.
- Paarweise Koedervergleiche nach Holm meist nicht signifikant.

Interpretation:
- Effekt ist verteilt ueber mehrere Koederbeziehungen.
- Kein einzelnes Paar traegt die komplette Evidenz.

### 4.3 Visibility: bivariates Signal verschwindet nach Adjustierung

Quelle: [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)

Konkrete Beispiele:
- `species_richness`: Beta = 0.004, p(HC3) = 0.734, q = 0.739
- `maxn_video_peak`: Beta = 0.030, p(HC3) = 0.483, q = 0.739
- `first_seen_median_sec`: Beta = -0.017, p(HC3) = 0.739, q = 0.739

Interpretation:
- Konfundierung durch Standort/Koeder ist plausibel.
- Rohzusammenhang ist nicht gleich unabhaengiger Treibereffekt.

---

## 5. Fish-vs-Algae: robuste und explorative Muster

Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

### 5.1 Robuste Muster

- Mehrere BH-signifikante Features mit Richtung fish > algae.
- In Utumbi sind robuste Signale ueber mehrere Feature-Typen verteilt:
  - `word_group`, `family`, `diet`, `composite_group`, `unspecific`

### 5.2 Explorative Muster

Top-Rohsignale (global ueber Koeder), ohne Holm/BH-Robustheit:
- Milimani: `moorish_idol`, `zanclidae`, `zanclus`, `lutjanidae`, `lutjanus`
- Utumbi: `wrasses_trigger_combo`, `wrasses`, `labridae`, `triggerfishes`, `balistidae`
- Nursery: `chlorurus` (explorativ auffaellig)

Kernaussage:
- Robuste Richtung fish > algae ist klar.
- Einzelne algennahe Hinweise existieren, bleiben aber explorativ.

---

## 6. Verhalten (`feeding` und `interested`): robuste und grenzwertige Befunde

Quelle: [interested_feeding/interested_feeding_summary.md](interested_feeding/interested_feeding_summary.md)

### 6.1 Signifikante bzw. robuste Anteile

- Milimani: 1 Holm-signifikantes Feeding-Taxon
- Nursery: 2 Rohsignale Feeding, aber 0 Holm-signifikant
- Utumbi: mehrere Rohsignale in Feeding/Interested, aber 0 Holm-signifikant auf Taxonebene

### 6.2 Konkretes Grenzfall-Beispiel (vorab fokussierte Taxa)

Quelle: [interested_feeding/nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md](interested_feeding/nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md)

Fokus-Taxa:
- `species::paletail unicorn (naso brevirostris)`
- `species::honeycomb (siganus stellatus)`

Beobachtung:
- algaemix: 3/3 positive Videos
- mackerel: 0/4 positive Videos
- Cliff's Delta = 1.0 (maximaler Richtungseffekt)

Tests:
- Mann-Whitney p = 0.0571 je Taxon; Holm(2) = 0.1143
- Permutation p = 0.0268; Holm(2) = 0.0536
- Fisher p = 0.0286; Holm(2) = 0.0571

Interpretation:
- Sehr starkes biologisches Trennmuster, aber unter Holm knapp ueber 0.05.
- Beispiel fuer "starke Tendenz" ohne formale Holm-Robustheit.

---

## 7. Sichtweite (Visibility): bivariates Signal vs. adjustierte Modelle

Quellen:
- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

### 7.1 Bivariat (signifikant)

- `species_richness`: rho = 0.563, BH q = 0.000138
- `maxn_video_peak`: rho = 0.467, BH q = 0.00161
- `first_seen_median_sec`: kein signifikanter Zusammenhang

### 7.2 Adjustiert (nicht robust signifikant)

- Kein Endpunkt mit robustem Sicht-Effekt nach Kontrolle fuer Standort + Koeder.
- Zusatztests (blockierte Permutation, Nichtlinearitaet, Quantilsregression) bestaetigen das Gesamtbild.

Kernaussage:
- Sicht hat deskriptive Relevanz im Rohmuster.
- Fuer inferenzielle Aussagen ist Standort-/Koederkontrolle entscheidend.

---

## 8. Gesamtinterpretation und Priorisierung der Evidenz

Prioritaet 1 (hoch robust):
- Standorteffekte auf Taxa-Haeufigkeit
- Globale Koederunterschiede in der Zusammensetzung

Prioritaet 2 (robust, aber enger gefasst):
- Fish-vs-Algae-Effekte in mehreren Funktionsgruppen, vor allem fish > algae

Prioritaet 3 (kontext- und trendorientiert):
- Verhalten (`feeding`/`interested`) mit standortabhaengigen und teils grenzwertigen Signalen
- Visibility: bivariates Signal ohne robusten unabhaengigen Effekt nach Adjustierung

Pragmatische Lesart:
- Standort ist der staerkste Erklaerer.
- Koeder wirkt, aber oft als verteiltes Muster.
- Verhaltens- und Sichtdaten sind wichtig fuer Kontext und Mechanismus, tragen aber weniger robuste Einzelsignale.

---

## 9. Methodische Grenzen und offene Punkte

1. Multiple-Test-Belastung bei hoher Taxonzahl
- Viele parallele Tests reduzieren die Chance auf korrigierte Signifikanz fuer Einzeleffekte.

2. Unbalancierte Zellgroessen
- Unterschiedliche n je Standort/Koeder erschweren feinaufgeloeste Inferenz.

3. Kompositionelle Streuung
- Ergaenzende PERMDISP-Pruefungen koennen global signifikante PERMANOVA-Befunde weiter absichern.

4. Hierarchische Modellierung
- Mixed-Effects-Modelle koennen Video-, Standort- und Koederebene integrierter trennen.

---

## 10. Quellenverzeichnis

- Standort-Haeufigkeit:
  - [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)
- Koeder-Haeufigkeit:
  - [taxahaeufigkeitkoeder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)
- Koeder-Komposition:
  - [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)
- Verhalten:
  - [interested_feeding/interested_feeding_summary.md](interested_feeding/interested_feeding_summary.md)
  - [interested_feeding/ubiquitous_nonbehavioral_filter_sensitivity.md](interested_feeding/ubiquitous_nonbehavioral_filter_sensitivity.md)
  - [interested_feeding/nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md](interested_feeding/nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md)
- Funktionsvergleich:
  - [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)
- Sichtanalyse:
  - [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
  - [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
  - [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

---

## Plausibilitaetsnotiz

Diese Fassung trennt bewusst zwischen:
- robusten Aussagen (korrigiert signifikant) und
- Tendenzaussagen (roh signifikant, grenzwertig oder konsistent gerichtet).

Damit sind Ueberinterpretationen einzelner Rohsignale vermeidbar, ohne informative Muster zu verlieren.
