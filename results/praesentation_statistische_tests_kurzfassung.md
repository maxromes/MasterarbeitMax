# Statistische Kurzfassung (Top-10 Kernaussagen)

Stand: 2026-04-27

Diese Kurzfassung reduziert die Gesamtauswertung auf die wichtigsten, zahlenbasierten Befunde.

---

## Inhaltsuebersicht

1. Top-10 Kernaussagen
2. Einordnung der Evidenzstaerke
3. Kurzfazit in drei Saetzen
4. Quellen

---

## 1. Top-10 Kernaussagen

### 1) Standort ist der staerkste Treiber der Taxa-Haeufigkeit

- 161 Taxa getestet
- 93 roh signifikant
- 36 Holm-signifikant

Interpretation:
- Der Standorteffekt ist robust und dominiert die inferenzielle Gesamtschau.

Quelle:
- [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

### 2) Koeder beeinflussen die Zusammensetzung global in allen Standorten

PERMANOVA p-Werte (global):
- Milimani: 0.0242
- Utumbi: 0.0046
- Nursery: 0.0016

Interpretation:
- Koeder veraendern die Gemeinschaftsstruktur, auch wenn einzelne Paarvergleiche oft nicht robust sind.

Quelle:
- [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

### 3) Taxonweise Koeder-Haeufigkeitsunterschiede sind meist nicht Holm-robust

- Milimani: 104 Taxa, 6 roh signifikant, 0 Holm-signifikant
- Nursery: 99 Taxa, 11 roh signifikant, 0 Holm-signifikant
- Utumbi: 120 Taxa, 8 roh signifikant, 0 Holm-signifikant

Interpretation:
- Es gibt Koedertendenzen, aber keine robuste taxonweise Einzelsignal-Lage.

Quelle:
- [taxahaeufigkeitkoeder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)

### 4) Fish-vs-Algae zeigt robuste Richtungseffekte zugunsten fish

- Mehrere BH-signifikante Features mit `higher_side = fish`
- Besonders deutlich in Utumbi

Interpretation:
- Der funktionelle Koedereffekt ist gerichtet und konsistent (fish > algae).

Quelle:
- [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

### 5) Konkretes robustes Fish-Beispiel (Milimani)

Feature `wrasses` (unspecific):
- p = 0.00171
- Holm p = 0.02054
- BH p = 0.02054
- Cliff's Delta = 0.975

Interpretation:
- Sehr starker, robust abgesicherter Vorteil auf fish-Seite.

Quelle:
- [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

### 6) Konkrete robuste Standort-Beispiele

`species::humpback (lutjanus gibbus)`:
- Kruskal p = 2.91e-10
- Holm p = 4.69e-08
- Mittelwerte: Milimani 0.00, Utumbi 0.00, Nursery 20.18

`genus::genus soldier`:
- Kruskal p = 8.77e-09
- Holm p = 1.38e-06
- Mittelwerte: Milimani 0.29, Utumbi 3.17, Nursery 0.00

Interpretation:
- Mehrere Taxa zeigen klare, standortspezifische Haeufigkeitsprofile.

Quelle:
- [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

### 7) `feeding` und `interested` sind verwandt, aber nicht identisch

Beispielhafte Muster:
- Mehr Rohsignale in `feeding` als in `interested`
- Holm-robuste Taxa auf Verhaltensebene selten

Interpretation:
- Beide Variablen sollten gemeinsam, aber getrennt interpretiert werden.

Quelle:
- [interested_feeding/interested_feeding_summary.md](interested_feeding/interested_feeding_summary.md)

### 8) Grenzwertiges, biologisch starkes Verhaltensergebnis (nur Tendenz)

Nursery-Fokus (`algaemix` vs `mackerel`, 2 Fokus-Taxa):
- algaemix: 3/3 positive Videos
- mackerel: 0/4 positive Videos
- Cliff's Delta = 1.0
- Mann-Whitney p = 0.0571 je Taxon (Holm(2) = 0.1143)

Interpretation:
- Sehr starkes Richtungsmuster, aber unter Holm knapp nicht robust.

Quelle:
- [interested_feeding/nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md](interested_feeding/nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md)

### 9) Visibility zeigt bivariates Signal fuer Richness und MaxN

- `species_richness`: Spearman rho = 0.563, p = 4.61e-05, BH q = 1.38e-04
- `maxn_video_peak`: Spearman rho = 0.467, p = 0.00108, BH q = 0.00161

Interpretation:
- Rohdaten zeigen klaren positiven Sicht-Zusammenhang.

Quelle:
- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)

### 10) Nach Adjustierung bleibt kein robuster Visibility-Effekt

Modelle mit Standort+Koeder-Kontrolle:
- `species_richness`: p(HC3) = 0.734, q = 0.739
- `maxn_video_peak`: p(HC3) = 0.483, q = 0.739
- `first_seen_median_sec`: p(HC3) = 0.739, q = 0.739

Interpretation:
- Sicht ist wichtiger Kontextfaktor, aber kein unabhaengiger Treiber nach Kovariatenkontrolle.

Quellen:
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

---

## 2. Einordnung der Evidenzstaerke

Hohe Evidenz:
- Standorteffekte auf Taxa-Haeufigkeit
- Globale Koeder-Kompositionsunterschiede
- Fish-vs-Algae Richtungseffekte (mehrere BH-signifikante Features)

Mittlere Evidenz:
- Verhaltensmuster (`feeding`/`interested`) mit standortabhaengigen Signalen

Niedrige bis explorative Evidenz:
- Taxonweise Koeder-Haeufigkeitsunterschiede (ohne Holm-Robustheit)
- Visibility als unabhaengiger Treiber nach Adjustierung

---

## 3. Kurzfazit in drei Saetzen

- Der Standort ist der robusteste Erklaerer fuer Unterschiede in der Taxa-Haeufigkeit.
- Koeder veraendern die Zusammensetzung der Gemeinschaft global, waehrend taxonweise Einzeleffekte meist nicht Holm-robust sind.
- Fish-vs-Algae zeigt konsistente Richtungseffekte zugunsten fish; Visibility bleibt nach Kontrolle von Standort und Koeder ohne robusten unabhaengigen Effekt.

---

## 4. Quellen

- [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)
- [taxahaeufigkeitkoeder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)
- [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)
- [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)
- [interested_feeding/interested_feeding_summary.md](interested_feeding/interested_feeding_summary.md)
- [interested_feeding/nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md](interested_feeding/nursery/feeding/feeding_nursery_algaemix_vs_mackerel_focus_taxa_sensitivity.md)
- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)
