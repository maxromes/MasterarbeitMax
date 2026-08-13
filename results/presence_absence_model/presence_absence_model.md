# Präsenz-/Absenz-Modell für fokussierte Taxa und Familien

Methodik: Videoebene, Presence/Absence je Taxon/Familie; Fisher-Exact-Test mit gerichteter Alternative auf den biologisch erwarteten Effekt.

- For the herbivore signal in Nursery, the key question is whether the signal is driven by actual occurrence differences or by stronger abundance once present.
- For the broader coral-reef fish-vs-algae signals, the question is whether one bait type triggers consistently more occurrence of the focal taxon.

| signal | family | sites | algae_present | algae_total | fish_present | fish_total | algae_rate | fish_rate | fisher_p | fisher_p_bh | sig_bh_0_05 |
|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| coral_muraenidae | muraenidae | milimani, utumbi | 0 | 19 | 5 | 9 | 0.000 | 0.556 | 0.001282 | 0.007692 | true |
| coral_siganidae | siganidae | milimani, utumbi | 12 | 19 | 6 | 9 | 0.632 | 0.667 | 0.722266 | 1.000000 | false |
| coral_balistidae | balistidae | milimani, utumbi | 19 | 19 | 9 | 9 | 1.000 | 1.000 | 1.000000 | 1.000000 | false |
| coral_labridae | labridae | milimani, utumbi | 19 | 19 | 9 | 9 | 1.000 | 1.000 | 1.000000 | 1.000000 | false |
| coral_scaridae | scaridae | milimani, utumbi | 19 | 19 | 9 | 9 | 1.000 | 1.000 | 1.000000 | 1.000000 | false |
| nursery_acanthuridae | acanthuridae | nursery | 6 | 6 | 4 | 4 | 1.000 | 1.000 | 1.000000 | 1.000000 | false |

## Interpretation

- Nursery Acanthuridae: Presence/Absence liefert hier kein klares Koeder-Signal, weil die Familie in beiden Ködergruppen auf fast allen Videos vorhanden ist. Das deutet auf einen Abundanz-Effekt statt auf einen reinen Occurrence-Effekt hin.
- Coral Reef Labridae, Balistidae, Muraenidae: Die Fisch-vs-Algae-Differenzen bleiben im Präsenz-/Absenz-Raum nur teilweise sichtbar; für Labridae und Balistidae ist die Präsenz in beiden Gruppen so häufig, dass kein starker Unterschied im Vorkommen entsteht. Muraenidae zeigt den klarsten Presence/Absence-Effekt (0/19 vs 5/9), was die Richtung der Fish-vs-Algae-Analysen zusätzlich stützt.
- Die Gesamtbotschaft ist damit methodisch wichtig: Der robuste Kern der Befunde liegt eher in der Intensität/MaxN als in der bloßen Präsenz. Für Algenfresser ist der Effekt bei Acanthuridae damit eher ein starker Dichte- oder Aktivitätsunterschied als ein reiner Präsenzunterschied.
