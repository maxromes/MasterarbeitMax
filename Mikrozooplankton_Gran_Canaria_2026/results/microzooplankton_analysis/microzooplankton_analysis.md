# Mikrozooplanktonanalyse

## Datengrundlage

Die Auswertung wurde direkt aus `MicroZP_Gran_Canaria_2026_MaxRomes_AntoniaKirner (1).xlsx` erstellt. Berücksichtigt wurden M1, M2, M3, M6, M8 und M9 mit den Probetagen T1, T2, T3, T5, T6, T7, T11, T15, T19, T23, T27 und T31. Die Behandlung erfolgte an T4; T1–T3 werden daher als Vorbehandlung und T5–T31 als Nachbehandlung behandelt.

Es wurden ausschließlich die Rohzählungen (`Count`) der taxonomischen Größenklassen verwendet. Für jede Zeile gilt:

`Zellen L⁻¹ = Count × 2 × 1000 / 50 ml = Count × 40`

Leere Count-Felder und Count = 0 wurden als kein Fund behandelt. Ciliaten umfassen genau die zehn festgelegten Kategorien von Strombidium, Strobilidium, Tintinnid, Mesodinium und Unknown Ciliate. Alle übrigen Kategorien wurden als Dinoflagellaten klassifiziert. Biomasse wurde nicht ausgewertet.

## Ergebnisse

### Genereller Verlauf und Vorbehandlung

Die Gesamtzellzahlen zeigen vor T4 unterschiedliche Richtungen: Zwischen T1 und T3 zeigen **4 von 6 Mesokosmen einen Anstieg** und **2 von 6 eine Abnahme**. Ein vollständig gemeinsamer Vorbehandlungstrend liegt somit nicht vor. Die Zeitreihen sind in `figures/01_zeitverlauf.png` dargestellt.

### Kontrollen

M3 (0 Concrete) und M6 (0 NaOH) wurden als Kontrollen verglichen. Die mittlere absolute relative Differenz der Gesamtzellzahl beträgt vor T4 **46.8%** und nach T4 **62.6%**. Die Kontrollen sind damit als Referenz verwendbar, aber nicht gleichwertig identisch; ihre Ausgangsunterschiede müssen bei Treatment-Interpretationen berücksichtigt werden.

### Treatment-Effekte

Die Treatmentverläufe sind in `figures/02_normalisiert_T3.png` relativ zu T3 dargestellt. Die folgenden Werte sind ausdrücklich deskriptive Effekte und werden trotz fehlender Replikate berichtet. `mean_change_vs_T3_percent` ist die mittlere prozentuale Veränderung der Nachbehandlungstage gegenüber T3; `T31_cells_L` ist der Wert am letzten Probetag.

#### Gesamtzellzahl

 mesocosm  mean_post_cells_L  T31_cells_L  mean_change_vs_T3_percent
        1       13111.111111      11360.0                 -27.802252
        2       11915.555556      20440.0                  18.209877
        3        9128.888889       3640.0                 -50.707943
        6        8466.666667      16520.0                 -39.176245
        8        8706.666667      16160.0                 -49.024200
        9        7640.000000       3240.0                 -20.416667

#### Hauptgruppen

 mesocosm          group  mean_post_cells_L  T31_cells_L  mean_change_vs_T3_percent
        1        Ciliate        5715.555556       1600.0                 -22.342995
        1 Dinoflagellate        7395.555556       9760.0                 -31.522634
        2        Ciliate        4355.555556      13080.0                  -7.721281
        2 Dinoflagellate        7560.000000       7360.0                  41.044776
        3        Ciliate        3946.666667        520.0                 -60.533333
        3 Dinoflagellate        5182.222222       3120.0                 -39.175796
        6        Ciliate        1697.777778       3200.0                 -72.076023
        6 Dinoflagellate        6768.888889      13320.0                 -13.662132
        8        Ciliate        1982.222222       2400.0                 -79.090483
        8 Dinoflagellate        6724.444444      13760.0                 -11.520468
        9        Ciliate        3204.444444        520.0                 -38.846480
        9 Dinoflagellate        4435.555556       2720.0                   1.732926

#### Größenklassen

 mesocosm          group size_class  mean_change_vs_T3_percent  T31_cells_L
        1        Ciliate        <30                  -6.182796        280.0
        1        Ciliate        >30                 -55.740741       1320.0
        1 Dinoflagellate        <30                 -20.041537       9720.0
        1 Dinoflagellate        >30                 -75.396825         40.0
        2        Ciliate        <30                  10.978836      10800.0
        2        Ciliate        >30                 -53.921569       2280.0
        2 Dinoflagellate        <30                  62.020202       7120.0
        2 Dinoflagellate        >30                 -55.092593        240.0
        3        Ciliate        <30                 -55.942510        440.0
        3        Ciliate        >30                 -79.365079         80.0
        3 Dinoflagellate        <30                 -37.275986       3080.0
        3 Dinoflagellate        >30                 -52.263374         40.0
        6        Ciliate        <30                 -67.878788       2600.0
        6        Ciliate        >30                 -83.068783        600.0
        6 Dinoflagellate        <30                 -14.197531       6120.0
        6 Dinoflagellate        >30                 -11.111111       7200.0
        8        Ciliate        <30                 -81.570513       1320.0
        8        Ciliate        >30                 -61.302682       1080.0
        8 Dinoflagellate        <30                 -16.279070       8160.0
        8 Dinoflagellate        >30                  33.950617       5600.0
        9        Ciliate        <30                 -35.515873        400.0
        9        Ciliate        >30                 -58.479532        120.0
        9 Dinoflagellate        <30                   2.505447       2400.0
        9 Dinoflagellate        >30                  -9.523810        320.0

Die Kombinationen aus Material und Dosierung werden ebenfalls direkt verglichen: 300 Concrete (M1) zeigt bei den Ciliaten eine mittlere Veränderung von -22.3% gegenüber T3, während 300 NaOH (M8) -79.1% zeigt. Bei 500 Concrete (M9) beträgt der entsprechende Wert -38.8%, bei 500 NaOH (M2) -7.7%. Diese Unterschiede sind Beobachtungsmuster und keine replizierten Treatmentmittelwerte.

Ein unabhängiger statistischer Treatmentvergleich ist nicht möglich, weil jede Kombination aus Dosis und Material nur in einem Mesokosmos vorkommt. Die deskriptiven Einzelverläufe und Effekte bleiben dennoch für die Ergebnisdarstellung relevant; Treatment und Mesokosmos müssen dabei als konfundiert bezeichnet werden.

### Zusätzliche deskriptive Tests

**AUC und Zeitpunkt des Minimums:** Die Fläche unter der Nachbehandlungskurve (T5–T31) und das Minimum der Gesamtzellzahl zeigen die integrierte Besiedlungsstärke und den Zeitpunkt der stärksten Abnahme:

 mesocosm  group    treatment  post_auc_cells_day_L  minimum_cells_L  minimum_day  T31_cells_L
        1 Gesamt 300 concrete              346860.0           5480.0            7      11360.0
        2 Gesamt     500 NaOH              306520.0           6440.0           15      20440.0
        3 Gesamt   0 concrete              218280.0           3400.0           27       3640.0
        6 Gesamt       0 NaOH              217240.0           4320.0            7      16520.0
        8 Gesamt     300 NaOH              212980.0           4160.0           19      16160.0
        9 Gesamt 500 concrete              212680.0           3240.0           31       3240.0

**Ciliaten-Dinoflagellaten-Verhältnis:** Nach T4 lag der mittlere Ciliatenanteil bzw. das mittlere Ciliaten-Dinoflagellaten-Verhältnis je Mesokosmos bei:

 mesocosm  mean_ciliate_share  mean_ciliate_dino_ratio
        1            0.341440                 1.593760
        2            0.348303                 0.688825
        3            0.373801                 1.586402
        6            0.208913                 0.279436
        8            0.218081                 0.322341
        9            0.379578                 1.321949

**Kontrollbasierte Treatmentabweichung:** Die Treatments wurden zusätzlich gegen die jeweils passende Kontrolle verglichen (Concrete gegen M3, NaOH gegen M6). Ein Verhältnis über 1 bedeutet höhere Zellzahlen im Treatment:

 mesocosm    treatment          group  mean_ratio_treatment_control  mean_difference_cells_L
        1 300 concrete        Ciliate                      2.140389              1768.888889
        1 300 concrete Dinoflagellate                      1.956593              2213.333333
        2     500 NaOH        Ciliate                      2.469619              2657.777778
        2     500 NaOH Dinoflagellate                      1.259388               791.111111
        8     300 NaOH        Ciliate                      1.430581               284.444444
        8     300 NaOH Dinoflagellate                      1.144448               -44.444444
        9 500 concrete        Ciliate                      1.381312              -742.222222
        9 500 concrete Dinoflagellate                      1.069058              -746.666667

**Gewinner und Verlierer einzelner Kategorien:** Kategorien mit einer mittleren Veränderung von mindestens +25 % gegenüber T3 wurden als deskriptive Gewinner, Kategorien mit höchstens −25 % als Verlierer klassifiziert. Die stärksten Beispiele sind:

Gewinner:
 mesocosm             category  mean_change_vs_T3_percent
        8 Unknown Athecate >30                 355.555556
        3   Mesodinium sp. <30                 355.555556
        9   Mesodinium sp. <30                 333.333333
        3  Unknown Thecate <30                 242.222222
        8  Unknown Thecate <30                 222.222222
        1   Mesodinium sp. <30                 216.666667
        6 Unknown Athecate >30                 151.111111
        3 Unknown Athecate >30                 114.814815

Verlierer:
 mesocosm               category  mean_change_vs_T3_percent
        3 Prorocentrales sp. >30                     -100.0
        3      Tintinnid sp. <30                     -100.0
        3      Tintinnid sp. >30                     -100.0
        6   Strobilidium sp. <30                     -100.0
        6      Tintinnid sp. >30                     -100.0
        8   Strobilidium sp. <30                     -100.0
        8      Tintinnid sp. <30                     -100.0
        9       Ceratium sp. <30                     -100.0

**Zeitverzögerte Beziehungen:** Für Ciliaten und Dinoflagellaten wurden Korrelationen mit Verschiebungen von −4 bis +4 Probetagen berechnet. Der jeweils stärkste positive Zusammenhang je Mesokosmos war:

 mesocosm  lag_days  correlation_log10
        1        -2           0.505805
        2         2           0.836836
        3         4           0.665274
        6         1           0.455310
        8         1           0.542311
        9        -2           0.805404

Diese sechs Tests dienen der Mustererkennung. Sie liefern keine unabhängigen Signifikanznachweise, können aber direkt als deskriptive Ergebnisse im Bericht verwendet werden.

### Ähnlichkeit der Mesokosmen: Zellzahlen oder Komposition?

An T1 lagen die Gesamtzellzahlen zwischen 7840 und 17240 Zellen L⁻¹ (CV: 30.8%). Der Ciliatenanteil lag dagegen zwischen 16.3% und 23.4% (CV: 13.9%). Die relative Komposition war an T1 somit ähnlicher als die absoluten Zellzahlen.

Von T1 bis T3 blieb dieses Muster grundsätzlich bestehen: Der mittlere CV der Gesamtzellzahl betrug 31.5%, der mittlere CV des Ciliatenanteils 16.7%. T2 war dabei der unähnlichste Vorbehandlungstag hinsichtlich der Komposition.

Über den gesamten Zeitraum bis T31 war die absolute Zellzahl geringfügig homogener als die Komposition (mittlerer CV: 40.2% gegenüber 41.6%; Median: 36.9% gegenüber 38.5%). Nach T4 nahm die Heterogenität der Komposition jedoch deutlich zu. An T31 betrug der CV der Gesamtzellzahl 60.2%, während der CV des Ciliatenanteils 83.3% erreichte; der Ciliatenanteil lag dabei zwischen 14.1% und 64.0%.

Damit waren die Mesokosmen vor der Behandlung kompositorisch ähnlicher als hinsichtlich ihrer absoluten Zellzahlen. Bis T31 entwickelten sie sich insbesondere in der Ciliaten-/Dinoflagellaten-Zusammensetzung zunehmend auseinander.

### Ciliaten, Dinoflagellaten und Größenklassen

Ciliaten und Dinoflagellaten wurden getrennt sowie als Gesamtzellzahl ausgewertet. Zusätzlich wurden die Größenklassen <30 µm und >30 µm separat aggregiert. Dadurch werden spezifische Kategorien und Unknown-Kategorien innerhalb der jeweiligen Hauptgruppe addiert, ohne Zellen doppelt zu zählen. Die häufigsten Kategorien über alle Proben sind:

  group             category  total_count  samples_with_count
Ciliate  Unknown Ciliate <30       4852.0                  71
Ciliate  Unknown Ciliate >30        839.0                  62
Ciliate   Mesodinium sp. <30        288.0                  32
Ciliate  Strombidium sp. <30        266.0                  26
Ciliate Strobilidium sp. <30        242.0                  21
Ciliate  Strombidium sp. >30        218.0                  36
Ciliate    Tintinnid sp. >30        180.0                  20
Ciliate Strobilidium sp. >30        130.0                  32
Ciliate    Tintinnid sp. <30         46.0                   7
Ciliate   Mesodinium sp. >30          6.0                   4

### Einzelkategorien

Die vollständige Tabelle der deskriptiven Effekte jeder einzelnen Kategorie befindet sich in `microzooplankton_analysis.xlsx`, Blatt `Effekt_Kategorien`. Besonders hohe oder niedrige Werte können dort anhand der mittleren Veränderung gegenüber T3 und des T31-Wertes identifiziert werden. Die Tabelle berücksichtigt weiterhin die Regel, dass jede Zelle nur einer spezifischen Kategorie und damit genau einer Hauptgruppe zugeordnet wird.

## Datenprüfung

Die Prüfung bestätigt 72 Arbeitsblätter, 6 Mesokosmen und 12 Probetage. Insgesamt wurden 1234 Count-Zeilen mit 0 bzw. leerem Feld als kein Fund behandelt. Biomasse- oder bereits berechnete Cells/L-Spalten wurden nicht für die Ergebnisse verwendet.

## Dateien

- `microzooplankton_analysis.xlsx`: alle Rohzählungen, Aggregationen, Vorbehandlung, Kontrollen, Treatment-Normalisierung sowie deskriptive Effekte für Gesamt, Hauptgruppen, Größenklassen und Einzelkategorien.
- `figures/01_zeitverlauf.png`: Gesamtzellzahl, Ciliaten und Dinoflagellaten im Zeitverlauf.
- `figures/02_normalisiert_T3.png`: Veränderungen relativ zum letzten Vorbehandlungstag.
- `figures/03_kontrollen.png`: M3 und M6.
- `figures/04_ciliaten_groessenklassen.png`: Ciliaten nach Größe.
