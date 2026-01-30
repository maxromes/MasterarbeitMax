# ===== MaxN Berechnung =====
# MaxN = Maximum Number von Individuen einer Art pro Frame

# 1. Daten einlesen
df <- read.csv2("Annotation_reports/1.csv")

# 2. Neue Liste für Ergebnisse
result_list <- list()

#  3. Für jede Art durchlaufen
unique_species <- unique(df$label_name)

for (spp in unique_species) {
  subset_data <- df[df$label_name == spp, ]
  counts_by_frame <- table(subset_data$frames)
  max_value <- max(counts_by_frame)
  total_rows <- nrow(subset_data)
  avg_value <- mean(as.numeric(counts_by_frame))
  
  result_list[[spp]] <- c(MaxN = max_value, Total = total_rows, Mean = avg_value)
}

# 4. Umwandeln in Dataframe
output_df <- do.call(rbind, result_list)
output_df <- as.data.frame(output_df)
output_df$Species <- rownames(output_df)
rownames(output_df) <- NULL
output_df <- output_df[, c("Species", "MaxN", "Total", "Mean")]
output_df <- output_df[order(output_df$MaxN, decreasing = TRUE), ]

# 5. Anzeigen
print(output_df)

# 6. Speichern
dir.create("results", showWarnings = FALSE)
write.csv(output_df, "results/maxn_analysis.csv", row.names = FALSE)

cat("\nErgebnis gespeichert in: results/maxn_analysis.csv\n")
