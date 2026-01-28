# MaxN Berechnung für Fischarten
# MaxN = Maximum Number of individuals of a species observed at the same time
# Mit base R - keine zusätzlichen Packages nötig

# Daten laden
data <- read.csv2("Annotation_reports/1.csv")

# MaxN berechnen: Zähle pro Frame wie viele Individuen pro Art
count_per_frame_species <- table(data$frames, data$label_name)
maxn_per_species <- apply(count_per_frame_species, 2, max)

# Detaillierte Statistiken
maxn_result <- data.frame(
  label_name = names(maxn_per_species),
  MaxN = as.numeric(maxn_per_species),
  stringsAsFactors = FALSE
)

# Zusätzliche Statistiken hinzufügen
maxn_result$Total_occurrences <- sapply(maxn_result$label_name, function(species) {
  sum(data$label_name == species)
})

maxn_result$Mean_per_frame <- sapply(maxn_result$label_name, function(species) {
  species_data <- count_per_frame_species[, species]
  mean(species_data[species_data > 0])
})

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
