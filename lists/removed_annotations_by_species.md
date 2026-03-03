# Entfernte Annotationen nach 47min-Cut - AKTUALISIERT

**Status: Keine Annotationen mehr entfernt!**

Nach dem Hinzufügen von Genus Chromis und Indian Half-and-Half bei Sekunde 1 sind alle Annotationen in den normalisierten Dateien (cut_47min) nun <= 47min.

## Statistik

- **Ursprüngliche Anzahl Annotationen:** 13.370
- **Nach 47min-Cut entfernt:** 1.197 (9,0%)
- **Nach Wiederhinzufügen von 2 Arten:** 12.237 (in cut_47min)
  - Neu hinzugefügt: 64 Annotationen (Genus Chromis: 31 Dateien, Indian Half-and-Half: 33 Dateien)
  - Alle neu hinzugefügten Annotationen bei time_sec=1.0 Sekunde

## Vergleich: Vorher vs. Nachher

| Metrik | Vorher | Nachher | Änderung |
|--------|--------|---------|----------|
| Genus Chromis (entfernt) | 271 | 31* | -240 |
| Indian Half-and-Half (entfernt) | 168 | 33* | -135 |
| Gesamt entfern Annotationen | 1.195 | 0 | -1.195 |

*Die 31 und 33 sind nun in cut_47min vorhanden (bei Sekunde 1), also nicht mehr "entfernt"

## Original-Entfernte Annotationen (aus all_with_flags)

Diese Annotationen wurden ursprünglich aus dem 47min-Cut entfernt, werden aber jetzt durch die Neu-Hinzufügung kompensiert:

### Genus Chromis
- **271 Annotationen ursprünglich entfernt**
- **31 Dateien betroffen**
- Diese sind jetzt in allen betroffenen Dateien bei Sekunde 1 vorhanden

### Indian Half-and-Half (Pycnochromis dimidiatus)
- **168 Annotationen ursprünglich entfernt**
- **33 Dateien betroffen**
- Diese sind jetzt in allen betroffenen Dateien bei Sekunde 1 vorhanden

## Andere Taxa (weiterhin entfernt, nur in all_with_flags)

Die folgenden Taxa werden weiterhin in all_with_flags als entfernt markiert (but nicht in cut_47min):

| Taxa | Anzahl | Ebene |
|------|--------|-------|
| Parrotfishes (Scaridae) | 132 | Familie |
| Fusiliers (Caesionidae) | 75 | Familie |
| Sailfin Tang (Zebrasoma desjardinii) | 44 | Art |
| Humpnose Bigeye (Monotaxis grandoculis) | 37 | Art |
| Brown Tang (Zebrasoma scopas) | 32 | Art |
| Longbarbel (Parupeneus macronemus) | 28 | Art |
| Genus Soldier (Myripristis) | 22 | Genus |
| Genus Squirrel (Sargocentron) | 20 | Genus |
| Arabian Monocle (Scolopsis ghanam) | 15 | Art |
| Moorish Idol (Zanclus cornutus) | 13 | Art |

*(Vollständige Liste siehe: removed_annotations_by_species.csv)*
