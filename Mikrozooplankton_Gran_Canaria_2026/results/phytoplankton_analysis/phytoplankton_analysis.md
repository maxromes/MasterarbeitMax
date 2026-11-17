# Phytoplanktonanalyse

## Datengrundlage

Die Auswertung wurde aus `concatenated_file_2026_GC_M1_M2_M3_M6_M8_M9_T31.csv` erstellt. Berücksichtigt wurden M1, M2, M3, M6, M8 und M9 sowie die Probetage T1 bis T31 (ungerade Probetage; T4 ist der Behandlungstag und wurde nicht gemessen). Die Flow-Cytometrie enthält pro Probe eine `small`- und eine `large`-Messung.

Für die Gesamtzellzahl wurden ausschließlich die beiden `All cells`-Zeilen verwendet und zu Zellen L⁻¹ addiert. Die spezifischen Signalgruppen wurden getrennt ausgewertet. Aggregierte Zeilen wie `All cells Not Microphytoplankton total`, `Microphytoplankton total` oder `Nanophytoplankyon_total` wurden nicht zu den spezifischen Signalgruppen addiert, um Doppelzählungen zu vermeiden. Die Phytoplankton-Komposition bezieht sich deshalb auf die ausgewählten spezifischen Signale und nicht auf eine künstlich geschlossene taxonomische Summe.

## Ergebnisse

### Genereller Verlauf und Vorbehandlung

Vor T4 zeigten **0 von 6 Mesokosmen einen Anstieg** und **6 eine Abnahme** der Gesamtzellzahl. Die Ausgangsentwicklung war daher nicht vollständig synchron.

### Deskriptive Treatment-Effekte

Die folgenden Werte sind deskriptive Muster trotz fehlender Replikate:

 Mesocosm    treatment  mean_post_cells_L  T31_cells_L  mean_change_vs_T3
        1 300 Concrete       23287.064286      33658.1          27.896792
        2     500 NaOH       11655.342857      37394.3         -27.626345
        3    Kontrolle        8190.114286      12715.5         -48.786179
        6    Kontrolle       11214.685714       9343.2         -50.271880
        8     300 NaOH        9608.471429      10564.6         -46.734420
        9 500 Concrete       13032.121429       9532.7         -20.772561

M2 (500 NaOH) und M1 (300 Concrete) werden ebenso wie die Kontrollen und die übrigen Treatments einzeln berichtet. Die Treatmentkombinationen sind nicht unabhängig repliziert; Unterschiede dürfen daher nicht als allgemeine statistische Dosis- oder Materialeffekte verallgemeinert werden.

### AUC und Minimum

Die AUC fasst die gesamte Nachbehandlungszellzahl von T5 bis T31 zusammen. `AUC_Minimum` enthält außerdem den Zeitpunkt und die Größe des Minimums.

 mesocosm    treatment  post_auc_cells_day_L  minimum_cells_L  minimum_day  T31_cells_L
        1 300 Concrete              604989.7           7897.0           11      33658.1
        2     500 NaOH              280125.3           3117.6           13      37394.3
        3    Kontrolle              208846.7           3703.5           21      12715.5
        6    Kontrolle              296186.0           3833.3           17       9343.2
        8     300 NaOH              249425.6           3831.2           19      10564.6
        9 500 Concrete              344863.7           7178.0           11       9532.7

### Kontrollbasierte Effekte

Die Treatments wurden zusätzlich gegen die jeweils passende Kontrolle verglichen (Concrete gegen M3, NaOH gegen M6). Ein Verhältnis über 1 bedeutet höhere Gesamtzellzahlen im Treatment:

 mesocosm    treatment  mean_ratio_treatment_control  mean_difference_cells_L
        1 300 Concrete                      2.799078              13210.81250
        2     500 NaOH                      1.123605                -18.52500
        8     300 NaOH                      0.938444              -1582.88750
        9 500 Concrete                      1.853353               4212.50625

### Spezifische Signalgruppen

Die häufigsten ausgewerteten spezifischen Signale waren:

                                   Set  total_cells_L  samples_with_signal  mean_share
             Nanophytoplankton (other)    390746.7000                   96    0.274701
                   Synechococcus right    288912.5700                   95    0.208573
       Nanophytoplankton 2 (FL-orange)    266618.8200                   96    0.171097
                       high SSC (pico)    228914.4000                   96    0.233441
      Chain-forming Microphytoplankton     31367.2220                   94    0.047590
            long chain-forming Diatoms     24115.3513                   88    0.036959
             Picophytoplankton (other)     17056.7280                   85    0.013931
short chain-forming microphytoplankton      7250.9390                   94    0.010630

Diese Signalgruppen sind durch das Messverfahren definiert und teilweise nicht als vollständig exklusive biologische Taxa zu interpretieren. Die vollständigen Einzelverläufe stehen im Blatt `Signalgruppen`.

### Ähnlichkeit: Zellzahlen oder Komposition?

Die absolute Gesamtzellzahl wurde über den Variationskoeffizienten zwischen Mesokosmen verglichen. Die Komposition wurde über die Streuung der Anteile der spezifischen Signalgruppen verglichen.

Vor T4 betrug der mittlere CV der Gesamtzellzahl **8.4%**. Die mittlere Standardabweichung der Signalprofile lag bei **0.012**. Nach T4 lag der CV der Gesamtzellzahl im Mittel bei **49.1%**, während die mittlere Profilstreuung **0.043** betrug. Die vollständige Zeitreihe befindet sich im Blatt `Aehnlichkeit_Zeitverlauf`.

## Einschränkungen

Jede Treatmentkombination ist nur durch einen Mesokosmos repräsentiert. Die Ergebnisse sind deshalb deskriptive Verläufe und Effektmuster. Zusätzlich unterscheiden sich die Flow-Cytometrie-Signalgruppen von vollständig taxonomischen Zählkategorien; aggregierte Signale wurden daher nicht mit ihren Untergruppen zusammenaddiert.

## Dateien

- `phytoplankton_analysis.xlsx`: Rohdaten, Gesamtverlauf, Signalgruppen, Vorbehandlung, Treatments, AUC, Kontrollen und Ähnlichkeitsvergleich.
- `figures/01_zeitverlauf.png`: Small- und Large-Signalverläufe.
- `figures/02_signale.png`: häufigste spezifische Signalgruppen.
