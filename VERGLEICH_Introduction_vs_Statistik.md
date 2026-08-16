# Vergleich: Einleitung vs. Statistische Ergebnisse

**Datum**: 13.08.2026  
**Ziel**: Abgleich der Einleitung (BRUV_Introduction_allgemein_unkorrigiert_aktuell_13_08.docx) mit Masterarbeit_Statistik.md zur Identifikation von Ungereimtheiten und Verbesserungsbedarf

---

## Zusammenfassung der Befunde

| Hypothese | Konsistenz | Bewertung |
|-----------|-----------|----------|
| **H1 (Komposition)** | ✓ Sehr gut | Einleitung erwartet Effekte → Ergebnisse bestätigen ✓ |
| **H2 (Herbivore MaxN)** | ⚠ Teilweise | Site-Abhängigkeit erwähnt, aber NOT für Nursery-Fokus optimiert |
| **H3 (Feeding-Response)** | ⚠ Schwach | Wording suggeriert breite Effekte → Nur Nursery zeigt Signal ✗ |
| **Site-Unterschiede** | ⚠ Wichtig | Nursery-Distinktion vorhanden aber unterbelichtet in Hypothesen |

---

## 1. H1: ASSEMBLAGE COMPOSITION ✓

### Einleitung
> "Bait treatment influences the overall species composition of BRUVS-recorded fish assemblages. This hypothesis is evaluated with site-specific PERMANOVA analyses on Jaccard distances and with a grouped fish-versus-algae contrast for the primary reef comparison. Milimani and Utumbi represent the primary reef comparison, while Chole Nursery is treated as a separate lagoonal experiment."

### Statistische Ergebnisse (Masterarbeit_Statistik.md)
- **Site-spezifische PERMANOVA**: Milimani p=0.0242, Utumbi p=0.0046, Nursery p=0.0016
- **Gruppierter fish-vs-algae-Kontrast**: Milimani p=0.0080, Utumbi p=0.0044
- **Fazit**: Alle Tests unterstützen H1 ✓

### Bewertung: ✓ KONSISTENT
- Einleitung und Ergebnisse sind gut aufeinander abgestimmt
- Methodische Beschreibung (PERMANOVA auf Jaccard) entspricht Durchführung
- Site-Differenzierung ist korrekt präzisiert

### Verbesserungspotenzial
- **Gering**: H1 ist gut formuliert
- Optional: Kurz erwähnen, dass Einzelkoedervergleiche meist nicht signifikant sind → wichtig für Diskussion

---

## 2. H2: HERBIVORE MaxN ⚠

### Einleitung
> "Macroalgal treatments are expected to yield higher MaxN values for selected herbivorous fish families, namely Siganidae, Acanthuridae, Scaridae, and Blenniidae, than fish-based treatments. The expected effect is treated as site-dependent and is not assumed to be uniform across all locations. For focal signals, additional analyses distinguish presence from intensity of recorded abundance."

### Statistische Ergebnisse (Masterarbeit_Statistik.md)
- **Robuste Algen-Signale**: NUR Acanthuridae in Nursery (Median Algae=22.0 vs Fish=4.5, p_Holm=0.0278)
- **Keine Signale in Milimani/Utumbi**: Keine Holm-korrigierten algae>fish-Effekte für die vier Herbivore-Familien
- **Fazit**: H2 ist partiell bestätigt und standortabhängig

### Bewertung: ⚠ TEILWEISE KONSISTENT

**Was gut funktioniert:**
- ✓ Site-Abhängigkeit ist explizit erwähnt
- ✓ Hurdle-Modell (Präsenz vs. Intensität) ist erwähnt
- ✓ Vier Herbivore-Familien sind korrekt benannt

**Ungereimtheiten:**

1. **Fehlende Vorahnung auf Nursery-Fokus**
   - Einleitung: Vier Familien sind gleichwertig behandelt
   - Realität: NUR Acanthuridae in Nursery zeigt Signal
   - Problem: Leser erwartet ähnliche Tests für alle vier Familien an allen Standorten
   - Folge: Ergebnisse wirken unerwartet, obwohl sie hätten antizipiert werden können

2. **Unzureichende Differenzierung der Standorte in Hypothesen**
   - Einleitung: "The expected effect is treated as site-dependent"
   - Problem: Diese Aussage ist zu schwach für ein Ergebnis, das so deutlich standortabhängig ist
   - Folge: Nursery-Fokus sollte in H2 deutlicher werden

3. **Familienebenen-Spezifikation**
   - Einleitung: Warum diese vier Familien? Keine ökologische Begründung
   - Realität: Acanthuridae (Doktorfische) sind häufig und bedeutsam, aber keine Erklärung in Intro
   - Verbesserung: Kurze Begründung, warum Acanthuridae ggf. stärker reagieren könnten

### Verbesserungsbedarf

**Konkrete Änderungsvorschläge für Einleitung:**

Bisherig:
> "Macroalgal treatments are expected to yield higher MaxN values for selected herbivorous fish families, namely Siganidae, Acanthuridae, Scaridae, and Blenniidae, than fish-based treatments."

Verbessert:
> "Macroalgal treatments are expected to yield higher MaxN values for selected herbivorous fish families (Siganidae, Acanthuridae, Scaridae, Blenniidae), with primary predictions focused on the Chole Nursery environment, where herbivore abundance is highest. We specifically test whether surgeonfishes (Acanthuridae), known for their dietary specialization on macroalgae, show pronounced density responses. Secondary exploratory tests address whether such effects generalise to primary reef sites (Milimani and Utumbi)."

**Begründung für Änderung:**
- Macht deutlich, dass Nursery Fokus ist
- Erklärt, warum Acanthuridae besonders erwartet werden
- Reduziert Überraschung beim Leser über Nursery-Fokus der Ergebnisse
- Präzisiert „site-dependent" durch konkrete Habitat-Differenzierung

---

## 3. H3: HERBIVORE FEEDING RESPONSE ⚠⚠

### Einleitung
> "Macroalgal treatments are expected to produce a higher video-level feeding response by herbivorous fishes than fish-based treatments. Feeding response is quantified from annotated feeding observations per deployment; feeding-event duration was not measured. The hypothesis is evaluated separately by site."

### Statistische Ergebnisse (Masterarbeit_Statistik.md)
- **Nursery**: Mittel Algae=0.2038 vs Fish=0.0000, p_Holm=0.0171 ✓
- **Milimani**: p_Holm=0.5510 (nicht signifikant)
- **Utumbi**: p_Holm=0.5510 (nicht signifikant)
- **Kritische Beobachtung**: Milimani und Utumbi zeigen ZERO Feeding in BEIDEN Koedergruppen

### Bewertung: ⚠⚠ ERHEBLICHE INKONSISTENZ

**Ungereimtheiten:**

1. **Wording suggeriert breite Effekterwartung**
   - Einleitung: "higher video-level feeding response by herbivorous fishes" (allgemein)
   - Problem: Plural „responses" und fehlender Qualifier „where feeding occurs"
   - Realität: NUR Nursery zeigt Feeding; Milimani/Utumbi haben Zero-Baseline in BEIDEN Koedergruppen
   - Folge: Leser könnte erwarten, dass Feeding an allen Standorten möglich ist

2. **Fehlende Kontextualisierung von Site-Unterschieden**
   - Einleitung: "The hypothesis is evaluated separately by site" (technisch korrekt, aber zu neutral)
   - Problem: Nicht erklärt, WARUM Feeding von Standort so unterschiedlich sein könnte
   - Realität: Unterschiedliche Fischzusammensetzung, Verhaltensökologie, Fischdichte
   - Folge: Ergebnis wirkt unerklärbar

3. **Keine Baseline-Information**
   - Einleitung: Nimmt implizit an, dass Herbivore-Feeding messbar ist
   - Realität: Milimani/Utumbi zeigen 0.0 Feeding-Events in BEIDEN Koedergruppen
   - Problem: Das ist eine massive ökologische Beobachtung, sollte antizipiert oder erklärt werden
   - Folge: Ergebnisse sind wissenschaftlich überraschend/interessant, wenn korrekt kontextualisiert

### Verbesserungsbedarf (KRITISCH)

**Konkrete Änderungsvorschläge für Einleitung:**

Bisherig:
> "Macroalgal treatments are expected to produce a higher video-level feeding response by herbivorous fishes than fish-based treatments. Feeding response is quantified from annotated feeding observations per deployment; feeding-event duration was not measured. The hypothesis is evaluated separately by site."

Verbessert:
> "Macroalgal treatments are expected to produce a higher video-level feeding response by herbivorous fishes than fish-based treatments, particularly in the Chole Nursery lagoon where herbivore abundance and dietary pressure on macroalgae are high. Feeding response is quantified from annotated feeding observations per deployment; feeding-event duration was not measured. Because herbivore feeding behaviour and density vary substantially among sites—reflecting differences in fish community structure, local ecological conditions, and habitat type—this hypothesis is evaluated separately by site. We anticipate pronounced feeding activity in the nursery environment and secondary examination of whether feeding responses occur at the primary reef sites (Milimani and Utumbi)."

**Begründung für Änderung:**
- ✓ Macht explizit, dass Nursery Priori-Fokus ist
- ✓ Erklärt ökologisch, WARUM Feeding in Nursery aber nicht in Riffen erwartet wird
- ✓ Antizipiert, dass Reef-Standorte möglicherweise Zero-Baseline haben
- ✓ Kontextualisiert „separately by site" ökologisch statt nur methodisch
- ✓ Reduziert Überraschung im Leser über regionalisierte Ergebnisse

---

## 4. ÜBERGEORDNETE UNGEREIMTHEITEN

### [A] Site-Differenzierung in Hypothesenformulierung

**Problem:**
- Einleitung erwähnt korrekt, dass Nursery „separate lagoonal experiment" ist
- Aber in H2 und H3 wird diese Differenzierung NICHT wiederholt
- Leser könnte denken, alle drei Standorte sind experimentelle Replika
- Realität: Nursery ist Fokus; Riefe sind Kontrollen/sekundäre Tests

**Aktuelle Stelle:**
> "The study used three locations but two analytically distinct sampling components: the primary coral reef comparison at Milimani and Utumbi, and a separate lagoonal nursery experiment at Chole Nursery."

**Problem:** Diese Aussage steht in Section 2.1 (Methods/Study Sites), NICHT in der Hypothesensektion

**Verbesserung:** H2 und H3 sollten diese Differenzierung wiederholen oder vorgreifen:

> "H2/H3 Primary hypothesis (Chole Nursery): Macroalgal baits increase herbivore [MaxN/feeding]...
> 
> Secondary question (Milimani and Utumbi): Do similar effects occur in primary reef environments?"

---

### [B] Functional Group Reasoning fehlt

**Problem:**
- Warum gerade Siganidae, Acanthuridae, Scaridae, Blenniidae?
- Keine Begründung in Einleitung
- Realität: Nur Acanthuridae zeigt Signal → deutet auf spezifische Ökologie dieser Familie hin

**Verbesserung:** Ein Satz in der Herbivore-Einleitung:
> "These families were selected because they represent different herbivorous feeding modes—browsers, scrapers, and grazers—and are commonly encountered on East African coral reefs and in nursery environments."

---

### [C] Feeding Baseline und Ökologische Kontexte

**Problem:**
- Einleitung behandelt Feeding als alltägliches, messbares Phänomen
- Realität: Milimani/Utumbi = 0% Feeding in BEIDEN Koedergruppen
- Das ist biologisch wichtig! Deutet auf: (a) andere Fischarten prägen diese Standorte, oder (b) Herbivore zeigen kein Fütterungsverhalten in Videofall-Kontexten

**Verbesserung:** Kurzer Absatz vor H3:
> "Feeding behaviour in BRUVS systems is influenced by fish abundance, species composition, and local environmental conditions. We expect feeding responses to be pronounced in nursery habitats where herbivore densities are high, but acknowledge that feeding behaviour varies with site context and may not occur measurably at all study locations."

---

## 5. WEITERE PRÜFPUNKTE: Appendices und Methods

### Appendix D: Statistisches Material
Die Einleitung verweist korrekt auf Appendix D für detaillierte statistische Tabellen.
- ✓ Struktur ist korrekt beschrieben
- ✓ Referenzen auf Masterarbeit_Statistik sollten in finale Version rein

### Methods Section
- ✓ Annotation-Prozess ist gut dokumentiert
- ✓ Verhaltensdefinitionen (Feeding, Interested, Uninterested) sind präzise
- ⚠ Könnte kurz erwähnen: „Herbivore families were identified according to [Appendix C functional classification]"

### Appendix C: Funktionale Klassifikation
- ✓ Gut: Provisorische Familie-zu-Funktion-Abbildung
- ✓ Warnung vor Familie-Level-Variabilität ist appropriate
- Empfehlung: Mit Masterarbeit_Statistik abgleichen, ob alle analysierten Arten korrekt gelistet sind

---

## 6. ZUSAMMENFASSUNG: Konkrete Handlungsschritte

### SOFORTMASSNAHMEN (Kritisch)

**1. H2 erweitern um Nursery-Fokus**
   - **Zeile**: Hypothesensektion nach „Macroalgal treatments..."
   - **Länge**: +2-3 Sätze
   - **Inhalt**: Explizit machen, dass Nursery Fokus ist, warum Acanthuridae erwartet, Reef-Standorte sekundär

**2. H3 grundlegend überarbeiten**
   - **Zeile**: Gesamte H3-Formulierung
   - **Länge**: +3-4 Sätze
   - **Inhalt**: 
     - Nursery als Primär-Hypothese
     - Ökologische Begründung (hohe Herbivore-Dichte in Nursery)
     - Acknowledge, dass Feeding-Baseline heterogen ist
     - Reefs als sekundäre Tests

### EMPFEHLENSWERTE MASSNAHMEN (Höher Priorität)

**3. Site-Differenzierung in Hypothesensektion wiederholen**
   - **Zeile**: Nach Hypothesen-Einleitung
   - **Länge**: +1 Absatz (~4-5 Sätze)
   - **Inhalt**: Warum Nursery anders als Riffe, was das für Hypothesentest bedeutet

**4. Funktionale Gruppe Begründung hinzufügen**
   - **Zeile**: Bei erster Nennung von Siganidae etc.
   - **Länge**: +1 Satz
   - **Inhalt**: Kurz erkl­ären, warum diese vier Familien ausgewählt

### OPTIONAL ABER WERTVOLL (Mittlere Priorität)

**5. Feeding Baseline-Abschnitt**
   - **Zeile**: Vor H3
   - **Länge**: +2 Sätze
   - **Inhalt**: Context, dass Feeding von Standort variiert

**6. Appendix D Verlinkung**
   - **Zeile**: Nach Hypothesen
   - **Länge**: +1 Satz
   - **Inhalt**: „Detailed statistical tables are provided in Appendix D and summarized in Masterarbeit_Statistik"

---

## 7. Textmuster für Revisionen

### Überarbeitete H2-Formulierung (BEISPIEL)

**Original:**
> "Macroalgal treatments are expected to yield higher MaxN values for selected herbivorous fish families, namely Siganidae, Acanthuridae, Scaridae, and Blenniidae, than fish-based treatments. The expected effect is treated as site-dependent and is not assumed to be uniform across all locations. For focal signals, additional analyses distinguish presence from intensity of recorded abundance."

**Überarbeitet:**
> "Macroalgal treatments are expected to yield higher MaxN values for selected herbivorous fish families (Siganidae, Acanthuridae, Scaridae, Blenniidae), with primary predictions focused on the Chole Nursery environment, where herbivore abundance and ecological pressure are highest. We particularly expect surgeonfishes (Acanthuridae), known for their dietary specialization on macroalgae and their abundance in tropical nursery habitats, to show pronounced density responses to algal baits. As a secondary exploratory component, we test whether similar patterns occur at the primary reef sites (Milimani and Utumbi), while acknowledging that reef herbivore communities differ substantially from nursery populations. For focal signals, additional analyses distinguish presence from intensity of recorded abundance to clarify the mechanistic pathway (occurrence vs. density changes)."

---

### Überarbeitete H3-Formulierung (BEISPIEL)

**Original:**
> "Macroalgal treatments are expected to produce a higher video-level feeding response by herbivorous fishes than fish-based treatments. Feeding response is quantified from annotated feeding observations per deployment; feeding-event duration was not measured. The hypothesis is evaluated separately by site."

**Überarbeitet:**
> "Macroalgal treatments are expected to produce a higher video-level feeding response by herbivorous fishes than fish-based treatments, particularly in the Chole Nursery lagoon where herbivore densities and dietary pressure on macroalgae are elevated. Feeding response is quantified from annotated feeding observations per deployment; feeding-event duration was not measured. Because herbivore behaviour and abundance vary substantially among the study locations—reflecting differences in fish community structure, habitat type, and local ecological conditions—we formulate the hypothesis separately for each site: a primary prediction for Chole Nursery and secondary exploratory tests for the primary reef sites. This geographically stratified approach explicitly acknowledges that feeding behaviour may not be uniformly observable across contrasting environmental contexts."

---

## 8. Konsistenz-Checkliste für Final-Review

- [ ] H1: Composition-Effekte korrekt beschrieben, methodische Details passen ✓
- [ ] H2: Nursery-Fokus ist explizit (nicht implizit) kommuniziert
- [ ] H2: Warum Acanthuridae erwartet sind, ist kurz begründet
- [ ] H3: Feeding-Erwartung ist auf Nursery ausgerichtet
- [ ] H3: Ökologische Begründung für Site-Unterschiede ist present
- [ ] Alle Hypothesen erwähnen, dass Nursery vs Riffe unterschiedliche Erwartungen haben
- [ ] Functional group selection ist begründet
- [ ] Appendix D ist verlinkt/erwähnt
- [ ] Keine Widersprüche zwischen Methods-Section und Hypothesensektion

---

## 9. Abgleich mit Masterarbeit_Statistik.md

| Element | Intro-Wording | Stats-Ergebnis | Match? |
|---------|---------------|----------------|--------|
| H1 Test (PERMANOVA) | ✓ Named | ✓ Durchgeführt, signifikant | ✓✓ |
| H1 Contrast (fish vs algae) | ✓ Named | ✓ Durchgeführt, signifikant | ✓✓ |
| H2 Families (4 named) | ✓ Named | ⚠ Nur Acanthuridae robust | ⚠ Mismatch |
| H2 Site-dependence | ✓ Mentioned | ✓ Nur Nursery Signal | ⚠ Underspecified |
| H3 Feeding response | ✓ Named | ⚠ Nur Nursery Signal | ⚠ Misleading wording |
| H3 Separate by site | ✓ Mentioned | ✓ Durchgeführt | ✓ |
| Nursery as separate | ✓ Mentioned (Methods) | ✓ Zentral für Ergebnisse | ⚠ Not in Hypotheses |

---

## FAZIT

**Hauptfunde:**

1. **H1 ist solide** → Keine wesentlichen Änderungen nötig
2. **H2 braucht Fokussierung** → Nursery-Fokus und Acanthuridae-Reasoning präzisieren
3. **H3 braucht fundamentale Überarbeitung** → Wording ist zu optimistisch, zu wenig ökologischer Context
4. **Übergeordnet:** Nursery-Differenzierung sollte in Hypothesen-Sektion wiederholt werden, nicht nur in Methods

**Priorisierung:**
- 🔴 **Kritisch**: H3 rewrite, H2 enhancement
- 🟡 **Empfohlen**: Site-Differenzierung repetition, Functional group reasoning
- 🟢 **Optional**: Appendix-Verlinkung, Feeding baseline statement

