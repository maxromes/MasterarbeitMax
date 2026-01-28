# MaxN Berechnung für Fischarten
# MaxN = Maximum Number of individuals of a species observed at the same time

# Daten laden
data <- read.csv2("Annotation_reports/1.csv")

# Ergebnisse speichern
results <- list()

# Für jede eindeutige Art berechnen
for (species in unique(data$label_name)) {
  # Alle Zeilen dieser Art
  species_rows <- data[data$label_name == species, ]
  
  # Frame-Zählung (wie oft kommt die Art pro Frame vor)
  frame_table <- table(species_rows$frames)
  
  # MaxN = Maximum an einem Frame
  maxn_value <- max(frame_table)
  
  # Speichern
  results[[species]] <- list(
    MaxN = maxn_value,
    Total_occurrences = nrow(species_rows),
    Mean_per_frame = mean(as.numeric(frame_table))
  )
}

# In Dataframe konvertieren
maxn_result <- data.frame(
  label_name = names(results),
  MaxN = sapply(results, function(x) x$MaxN),
  Total_occurrences = sapply(results, function(x) x$Total_occurrences),
  Mean_per_frame = sapply(results, function(x) x$Mean_per_frame),
  row.names = NULL,
  stringsAsFactors = FALSE
)

# Nach MaxN sortieren
maxn_result <- maxn_result[order(maxn_result$MaxN, decreasing = TRUE), ]

# Anzeigen
print(maxn_result)

# Speichern
dir.create("results", showWarnings = FALSE)
write.csv(maxn_result, "results/maxn_analysis.csv", row.names = FALSE)

cat("\n=== MaxN Summary ===\n")
cat("Gesamtzahl Fischarten:", nrow(maxn_result), "\n")
cat("Höchste MaxN:", max(maxn_result$MaxN), "\n")
cat("Gespeichert in: results/maxn_analysis.csv\n")
