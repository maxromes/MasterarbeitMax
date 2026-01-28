# MaxN Berechnung für Fischarten
# MaxN = Maximum Number of individuals of a species observed at the same time
# Mit base R - keine zusätzlichen Packages nötig

# Daten laden
data <- read.csv2("Annotation_reports/1.csv")

# Unique Fischarten
species_list <- unique(data$label_name)

# MaxN berechnen für jede Art
maxn_result <- data.frame(
  label_name = species_list,
  MaxN = NA,
  Total_occurrences = NA,
  Mean_per_frame = NA,
  stringsAsFactors = FALSE
)

# Für jede Art berechnen
for (i in 1:nrow(maxn_result)) {
  species <- maxn_result$label_name[i]
  species_data <- data[data$label_name == species, ]
  
  # Total occurrences (Zeilen mit dieser Art)
  maxn_result$Total_occurrences[i] <- nrow(species_data)
  
  # MaxN (max Anzahl pro Frame)
  frame_counts <- table(species_data$frames)
  maxn_result$MaxN[i] <- max(frame_counts)
  
  # Mean per frame
  maxn_result$Mean_per_frame[i] <- mean(as.numeric(frame_counts))
}

# Sortieren nach MaxN
maxn_result <- maxn_result[order(maxn_result$MaxN, decreasing = TRUE), ]
rownames(maxn_result) <- NULL

# Ergebnis anzeigen
print(maxn_result)

# Verzeichnis erstellen falls nötig
if (!dir.exists("results")) {
  dir.create("results")
}

# Speichern als CSV
write.csv(maxn_result, "results/maxn_analysis.csv", row.names = FALSE)

# Zusammenfassung
cat("\n=== MaxN Summary ===\n")
cat("Gesamtzahl Fischarten:", nrow(maxn_result), "\n")
cat("Höchste MaxN-Wert:", max(maxn_result$MaxN), "\n")
