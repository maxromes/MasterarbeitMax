# MaxN Berechnung für Fischarten
# MaxN = Maximum Number of individuals of a species observed at the same time

# Paket installieren falls nötig
if (!require("tidyverse", quietly = TRUE)) {
  install.packages("tidyverse")
  library(tidyverse)
} else {
  library(tidyverse)
}

# Daten laden
data <- read.csv2("Annotation_reports/1.csv")

# MaxN berechnen: Zähle pro Frame wie viele Individuen pro Art
maxn_result <- data %>%
  group_by(frames, label_name) %>%
  summarise(count = n(), .groups = 'drop') %>%
  group_by(label_name) %>%
  summarise(MaxN = max(count), 
            Total_occurrences = n(),
            Mean_per_frame = mean(count),
            .groups = 'drop') %>%
  arrange(desc(MaxN))

# Ergebnis anzeigen
print(maxn_result)

# Optional: Speichern als CSV
write.csv(maxn_result, "results/maxn_analysis.csv", row.names = FALSE)

# Zusammenfassung
cat("\n=== MaxN Summary ===\n")
cat("Gesamtzahl Fischarten:", nrow(maxn_result), "\n")
cat("Höchste MaxN-Wert:", max(maxn_result$MaxN), "\n")
