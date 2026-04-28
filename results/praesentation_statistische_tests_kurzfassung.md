# Statistische Kurzfassung

Stand: 2026-04-28

Diese Kurzfassung fasst die wichtigsten Befunde der Gesamtanalyse auf wenigen Seiten zusammen. Der Schwerpunkt liegt auf der Leitfrage, ob algenfressende Taxa Algenkoeder bevorzugen, und darauf, welche Signale robust, bedingt oder nur explorativ sind.

---

## 1. Wichtigste Kernaussagen

### 1) Standort ist der staerkste Treiber

- 161 Taxa im Standortvergleich getestet
- 36 Holm-signifikante Taxa

Interpretation: Unterschiede zwischen Milimani, Utumbi und Nursery sind der dominante Struktureffekt in den Daten.

Quelle: [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)

### 2) Koeder verschieben die Zusammensetzung global

- PERMANOVA in allen Standorten signifikant
- Der Effekt ist global klar, aber nicht automatisch in jedem Paarvergleich sichtbar

Interpretation: Koeder beeinflussen die Gemeinschaftsstruktur, ohne dass daraus schon ein spezifischer Algenfresser-Effekt folgt.

Quelle: [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)

### 3) Der Standard-Funktionsvergleich spricht eher fuer fish als fuer algae

- Mehrere BH-signifikante Fish-vs-Algae-Features mit `higher_side = fish`
- Besonders deutlich in Utumbi

Interpretation: Der breite Funktionsvergleich stuetzt die Algenfresser-Hypothese nur schwach; er zeigt eher fish-orientierte Gruppen auf.

Quelle: [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)

### 4) Die Algenfresser-Hypothese wird in Nursery am klarsten bestaetigt

- A priori Herbivore-MaxN: Acanthuridae in Nursery Holm-signifikant fuer Algenkoeder
- Herbivore-Feeding: Nursery zeigt eine klare Algen-gegenueber-Fisch-Differenz

Interpretation: Die staerkste Bestaetigung der Leitfrage liegt in Nursery.

Quellen:
- [herbivore_analysis/herbivore_maxn_apriori_test.md](herbivore_analysis/herbivore_maxn_apriori_test.md)
- [herbivore_analysis/herbivore_feeding_responsiveness.md](herbivore_analysis/herbivore_feeding_responsiveness.md)

### 5) Der Feeding-Filter zeigt dieselbe Richtung, aber nicht immer Holm-robust

- Herbivore-Kernfamilien zeigen in Nursery deutlich mehr Feeding auf Algenkoedern
- Im breiteren Gruppenvergleich bleibt das meist unter Holm knapp nicht signifikant

Interpretation: Biologisch ist das Muster stark, formal aber wegen der Multipeltest-Korrektur teils noch knapp.

Quelle: [funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md](funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md)

### 6) Species Richness ist vor allem standortgetrieben

- Standort robust signifikant
- Koeder global nicht signifikant

Interpretation: Viele Muster sind stark vom Standort geprägt und muessen im Standortkontext gelesen werden.

Quelle: [species_richness_report/species_richness_additional_tests.md](species_richness_report/species_richness_additional_tests.md)

### 7) Visibility ist bivariat sichtbar, aber nicht robust unabhaengig

- Roh positiv fuer Species Richness und MaxN
- Nach Kontrolle von Standort und Koeder kein robuster Effekt mehr

Interpretation: Sicht ist ein Kontextfaktor, aber kein stabiler eigenstaendiger Treiber.

Quellen:
- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_additional_tests_summary.md](visibility_analysis/visibility_additional_tests_summary.md)
- [visibility_analysis/visibility_site_stratified_tests_summary.md](visibility_analysis/visibility_site_stratified_tests_summary.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)

---

## 2. Einordnung

Robust:
- Standorteffekte auf Taxa-Haeufigkeit
- globale Koederunterschiede
- Fish-vs-Algae Richtungseffekte zugunsten fish im Standard-Funktionsvergleich

Bedingt:
- Herbivore-/Feeding-Signale bei Algenkoedern ausserhalb von Nursery
- feeding-basierte Gruppenvergleiche mit grosser Multipeltest-Last

Explorativ:
- Reverse-Fokus-Algenranking jenseits der klaren Nursery-Signale
- einzelne taxonweise Koedertendenzen ohne Holm-Robustheit

---

## 3. Kurzfazit

Der Standort ist der groesste strukturelle Faktor in den Daten. Koeder veraendern die Gemeinschaft global, aber der breite Standardvergleich zeigt eher fish-orientierte als algae-orientierte Gruppen. Die eigentliche Algenfresser-Hypothese wird vor allem in Nursery stark gestuetzt, insbesondere fuer Acanthuridae und im Feeding-Verhalten der Herbivoren.

---

## 4. Quellen

- [taxahaeufigkeitstandord/taxahaeufigkeit_standort.md](taxahäufigkeitstandord/taxahaeufigkeit_standort.md)
- [taxahaeufigkeitkoeder/taxahaeufigkeit_koeder_summary.md](taxahäufigkeitköder/taxahaeufigkeit_koeder_summary.md)
- [artenvergleich_koeder/artenvergleich_koeder_summary.md](artenvergleich_köder/artenvergleich_koeder_summary.md)
- [funktionsvergleich/funktionsvergleich_bericht.md](funktionsvergleich/funktionsvergleich_bericht.md)
- [herbivore_analysis/herbivore_maxn_apriori_test.md](herbivore_analysis/herbivore_maxn_apriori_test.md)
- [herbivore_analysis/herbivore_feeding_responsiveness.md](herbivore_analysis/herbivore_feeding_responsiveness.md)
- [funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md](funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md)
- [species_richness_report/species_richness_additional_tests.md](species_richness_report/species_richness_additional_tests.md)
- [visibility_analysis/visibility_summary.md](visibility_analysis/visibility_summary.md)
- [visibility_analysis/visibility_adjusted_summary.md](visibility_analysis/visibility_adjusted_summary.md)
- [visibility_analysis/visibility_additional_tests_summary.md](visibility_analysis/visibility_additional_tests_summary.md)
- [visibility_analysis/visibility_site_stratified_tests_summary.md](visibility_analysis/visibility_site_stratified_tests_summary.md)
- [visibility_analysis/visibility_gesamtbewertung.md](visibility_analysis/visibility_gesamtbewertung.md)
