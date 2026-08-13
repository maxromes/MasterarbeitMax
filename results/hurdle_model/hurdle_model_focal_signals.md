# Hurdle-Modell fuer fokussierte Signale

Zweistufiges Modell pro Signal:
1) Praesenzteil: GLM Binomial (logistische Regression) fuer Nachweis ja/nein.
2) Intensitaetsteil: OLS auf log1p(MaxN) nur fuer Videos mit MaxN > 0 (HC3 robuste Standardfehler).

Die gerichtete Hypothese folgt der biologischen Erwartung (algae > fish bzw. fish > algae).
BH/FDR wird getrennt fuer Praesenz- und Intensitaetsteil ueber alle fokussierten Signale korrigiert.

| signal | direction | pres_algae | pres_fish | presence_p | presence_q | intensity_beta | intensity_p | intensity_q |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|
| coral_muraenidae | fish > algae | 0.000 | 0.556 | 0.001282 | 0.007692 | nan | nan | nan |
| nursery_acanthuridae | algae > fish | 1.000 | 1.000 | 1.000000 | 1.000000 | 1.3477 | 0.000002 | 0.000009 |
| coral_labridae | fish > algae | 1.000 | 1.000 | 1.000000 | 1.000000 | -0.5912 | 0.000005 | 0.000014 |
| coral_balistidae | fish > algae | 1.000 | 1.000 | 1.000000 | 1.000000 | -0.5333 | 0.001016 | 0.001694 |
| coral_siganidae | algae > fish | 0.632 | 0.667 | 0.571774 | 1.000000 | 0.2169 | 0.043479 | 0.054348 |
| coral_scaridae | algae > fish | 1.000 | 1.000 | 1.000000 | 1.000000 | 0.1867 | 0.251927 | 0.251927 |

## Interpretation

- Das Hurdle-Modell trennt explizit zwischen Occurrence und Dichte. Dadurch wird sichtbar, ob ein Koedereffekt auf haeufigeres Auftreten oder auf staerkere Auspraegung bei bereits vorhandenem Taxon basiert.
- Ein signifikanter Praesenzteil bei nicht-signifikantem Intensitaetsteil spricht fuer occurrence-getriebene Unterschiede.
- Ein signifikanter Intensitaetsteil bei nicht-signifikantem Praesenzteil spricht fuer dichte-/aktivitaetsgetriebene Unterschiede.
- Konsistente Signifikanz in beiden Stufen waere der staerkste Hinweis auf einen breiten, biologisch robusten Koedereffekt.
