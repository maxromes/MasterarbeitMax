# Erweiterte Vergleiche: Mikrozooplankton und Phytoplankton

## Wichtigste Ergebnisse

- Die kontrollkorrigierte Darstellung trennt Treatmentverläufe von den lokalen Controldynamiken von M3 beziehungsweise M6.
- Die Verhältniszeitreihe Mikrozooplankton/Phytoplankton zeigt, ob die Konsumentendichte oder die Ressourcenbasis stärker variiert.
- Die Phasenanalyse trennt Vorbehandlung, frühe, mittlere und späte Nachbehandlung.
- Die Größenklassenanalyse prüft, ob Ciliaten und Dinoflagellaten unterschiedlicher Größe mit Small- oder Large-Phytoplankton gekoppelt sind.
- Die Peak- und Recovery-Werte dokumentieren zeitliche Extrema beider Organismengruppen.

## Kontrollkorrigierte Dynamik

Für Concrete-Treatments wurde gegen M3 und für NaOH-Treatments gegen M6 korrigiert:

 mesocosm    treatment  mean_micro_vs_control  mean_phyto_vs_control
        1 300 concrete                  0.556                  0.949
        2     500 NaOH                  0.319                 -0.108
        8     300 NaOH                  0.070                 -0.211
        9 500 concrete                 -0.125                  0.501

## Difference-in-Differences

 mesocosm    treatment  control_mesocosm       variable  did_log2_change
        1 300 concrete                 3    micro_total            0.563
        1 300 concrete                 3        ciliate            0.849
        1 300 concrete                 3 dinoflagellate            0.400
        1 300 concrete                 3    phyto_total            1.398
        1 300 concrete                 3    phyto_small            1.437
        1 300 concrete                 3    phyto_large            1.161
        2     500 NaOH                 6    micro_total            1.037
        2     500 NaOH                 6        ciliate            1.755
        2     500 NaOH                 6 dinoflagellate            0.754
        2     500 NaOH                 6    phyto_total            0.217
        2     500 NaOH                 6    phyto_small            0.162
        2     500 NaOH                 6    phyto_large            0.771
        8     300 NaOH                 6    micro_total           -0.387
        8     300 NaOH                 6        ciliate           -0.638
        8     300 NaOH                 6 dinoflagellate           -0.227
        8     300 NaOH                 6    phyto_total           -0.263
        8     300 NaOH                 6    phyto_small           -0.353
        8     300 NaOH                 6    phyto_large            0.515
        9 500 concrete                 3    micro_total            0.188
        9 500 concrete                 3        ciliate            0.249
        9 500 concrete                 3 dinoflagellate            0.172
        9 500 concrete                 3    phyto_total            0.618
        9 500 concrete                 3    phyto_small            0.584
        9 500 concrete                 3    phyto_large            0.823

## Verhältnisse und Phasen

Die mittleren Mikrozooplankton/Phytoplankton-Verhältnisse je Mesokosmos waren:

 mesocosm treatment_group  mean_ratio
        1    300 concrete      0.7729
        2        500 NaOH      1.1823
        3       Kontrolle      1.1614
        6       Kontrolle      0.8700
        8        300 NaOH      0.9861
        9    500 concrete      0.6095

Phasenspezifische mittlere Spearman-Korrelationen:

               phase                                       comparison  n_mesokosmen  mean_spearman_rho
Spate Nachbehandlung                 Ciliaten vs. Large-Phytoplankton             6              0.505
Spate Nachbehandlung                Ciliaten vs. Phytoplankton gesamt             6              0.295
Spate Nachbehandlung                 Ciliaten vs. Small-Phytoplankton             6              0.161
Spate Nachbehandlung         Dinoflagellaten vs. Phytoplankton gesamt             6              0.367
Spate Nachbehandlung Mikrozooplankton gesamt vs. Phytoplankton gesamt             6              0.590

## Großenklassen und Lag

Die stärksten mittleren Größenklassen-Lags waren:

              micro_group phyto_group  lag_days  n_mesocosms  mean_spearman_rho  median_spearman_rho
       micro_ciliate_gt30      Gesamt        -2            2              1.000                1.000
       micro_ciliate_gt30       Large        -2            2              0.500                0.500
       micro_ciliate_gt30       Small        -2            2              1.000                1.000
       micro_ciliate_lt30      Gesamt        -2            6              0.917                1.000
       micro_ciliate_lt30       Large        -2            6              0.583                0.500
       micro_ciliate_lt30       Small        -2            6              0.917                1.000
micro_dinoflagellate_gt30      Gesamt        -4            6              0.527                0.559
micro_dinoflagellate_gt30       Large         4            6              0.357                0.221
micro_dinoflagellate_gt30       Small        -4            6              0.507                0.493
micro_dinoflagellate_lt30      Gesamt         0            6              0.381                0.333
micro_dinoflagellate_lt30       Large        -2            6              0.417                0.500
micro_dinoflagellate_lt30       Small         2            6              0.417                0.750

## Phytoplankton-Signalgruppen

Die stärksten explorativen Zusammenhänge zwischen Mikrozooplanktongruppen und ausgewählten Phytoplankton-Signalen waren:

            micro_group                           phyto_signal  n_pairs  spearman_rho  spearman_p
               Ciliaten short chain-forming microphytoplankton       60         0.522       0.000
               Ciliaten       Chain-forming Microphytoplankton       60         0.445       0.000
               Ciliaten             long chain-forming Diatoms       60         0.428       0.001
Mikrozooplankton gesamt                        high SSC (pico)       60         0.405       0.001
        Dinoflagellaten              Picophytoplankton (other)       60         0.378       0.003
        Dinoflagellaten        Nanophytoplankton 2 (FL-orange)       60         0.361       0.005
               Ciliaten                          Cryptophyites       60         0.328       0.011
Mikrozooplankton gesamt              Nanophytoplankton (other)       60         0.318       0.013
               Ciliaten                    Synechococcus right       60        -0.309       0.016
        Dinoflagellaten       Chain-forming Microphytoplankton       60        -0.274       0.034
        Dinoflagellaten             long chain-forming Diatoms       60        -0.273       0.035
               Ciliaten                        high SSC (pico)       60         0.270       0.037
Mikrozooplankton gesamt        Nanophytoplankton 2 (FL-orange)       60         0.261       0.044
        Dinoflagellaten short chain-forming microphytoplankton       60        -0.255       0.049
        Dinoflagellaten              Nanophytoplankton (other)       60         0.228       0.080

## Peak und Recovery

 mesocosm    treatment                organism  minimum_day  minimum_cells_L  maximum_day  maximum_cells_L
        1 300 concrete Mikrozooplankton gesamt            7           5480.0           19          26160.0
        1 300 concrete                Ciliaten           11           1000.0           19          23560.0
        1 300 concrete         Dinoflagellaten           19           2600.0           27          10480.0
        1 300 concrete    Phytoplankton gesamt           11           7897.0           27          57734.9
        2     500 NaOH Mikrozooplankton gesamt           15           6440.0           31          20440.0
        2     500 NaOH                Ciliaten           23            560.0           31          13080.0
        2     500 NaOH         Dinoflagellaten           15           2880.0           23          11200.0
        2     500 NaOH    Phytoplankton gesamt           11           4815.0           31          37394.3
        3    Kontrolle Mikrozooplankton gesamt           27           3400.0           11          15640.0
        3    Kontrolle                Ciliaten           27            320.0           11          11560.0
        3    Kontrolle         Dinoflagellaten           15            840.0            5           8640.0
        3    Kontrolle    Phytoplankton gesamt           11           4126.0           31          12715.5
        6    Kontrolle Mikrozooplankton gesamt            7           4320.0           31          16520.0
        6    Kontrolle                Ciliaten           23            240.0           31           3200.0
        6    Kontrolle         Dinoflagellaten            7           3200.0           31          13320.0
        6    Kontrolle    Phytoplankton gesamt           11           4180.0           27          23215.0
        8     300 NaOH Mikrozooplankton gesamt           19           4160.0           31          16160.0
        8     300 NaOH                Ciliaten           19            400.0           11           4600.0
        8     300 NaOH         Dinoflagellaten           23           3640.0           31          13760.0
        8     300 NaOH    Phytoplankton gesamt           19           3831.2           27          16885.2
        9 500 concrete Mikrozooplankton gesamt           31           3240.0           23          11160.0
        9 500 concrete                Ciliaten           31            520.0           15           8040.0
        9 500 concrete         Dinoflagellaten           15           1440.0           11           7920.0
        9 500 concrete    Phytoplankton gesamt           11           7178.0           19          19822.0

## Bootstrap-Lags

                                      comparison  lag_days  mean_spearman_rho  bootstrap_low_95  bootstrap_high_95
               Ciliaten vs. Phytoplankton gesamt        -4              0.097            -0.129              0.345
               Ciliaten vs. Phytoplankton gesamt        -2              0.322             0.164              0.522
               Ciliaten vs. Phytoplankton gesamt         0              0.179             0.035              0.322
               Ciliaten vs. Phytoplankton gesamt         2             -0.018            -0.300              0.283
               Ciliaten vs. Phytoplankton gesamt         4             -0.081            -0.372              0.320
        Dinoflagellaten vs. Phytoplankton gesamt        -4              0.377             0.254              0.516
        Dinoflagellaten vs. Phytoplankton gesamt        -2              0.417             0.294              0.536
        Dinoflagellaten vs. Phytoplankton gesamt         0              0.358             0.261              0.465
        Dinoflagellaten vs. Phytoplankton gesamt         2              0.183            -0.047              0.433
        Dinoflagellaten vs. Phytoplankton gesamt         4             -0.072            -0.356              0.186
Mikrozooplankton gesamt vs. Phytoplankton gesamt        -4              0.129            -0.101              0.350
Mikrozooplankton gesamt vs. Phytoplankton gesamt        -2              0.432             0.335              0.523
Mikrozooplankton gesamt vs. Phytoplankton gesamt         0              0.395             0.217              0.560
Mikrozooplankton gesamt vs. Phytoplankton gesamt         2              0.251             0.010              0.510
Mikrozooplankton gesamt vs. Phytoplankton gesamt         4              0.094            -0.234              0.367

## Grafiken

- `05_kontrollkorrigiert.png`: Kontrollkorrigierte Gesamtzellzahlen.
- `06_micro_phyto_verhaeltnis.png`: Verhältnis Mikrozooplankton/Phytoplankton.
- `07_phasenvergleich.png`: Mesokosmosgemittelte Kopplung nach Phasen.
- `08_groessen_lags.png`: Lag-Muster für kleine und große Ciliaten.
