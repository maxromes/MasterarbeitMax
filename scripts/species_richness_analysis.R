# Species Richness Analysis for Annotation Reports
# Analysiert die Artenvielfalt in allen Annotation-Dateien

library(dplyr)
library(tidyr)

# Funktion zur Berechnung der Species Richness für eine Datei
calculate_species_richness <- function(file_path, file_name) {
  # Daten einlesen
  data <- read.csv(file_path, stringsAsFactors = FALSE)
  
  # Eindeutige Arten zählen
  unique_species <- data %>%
    select(label_name) %>%
    distinct() %>%
    nrow()
  
  # Gesamtanzahl der Beobachtungen
  total_observations <- nrow(data)
  
  # Arten mit Häufigkeit
  species_counts <- data %>%
    group_by(label_name, label_hierarchy) %>%
    summarise(count = n(), .groups = "drop") %>%
    arrange(desc(count))
  
  # Ergebnis zurückgeben
  list(
    file_name = file_name,
    species_richness = unique_species,
    total_observations = total_observations,
    species_counts = species_counts
  )
}

# Alle CSV-Dateien im Annotation_reports Ordner finden
annotation_dir <- "Annotation_reports"
csv_files <- list.files(annotation_dir, pattern = "\\.csv$", full.names = TRUE)

# Species Richness für alle Dateien berechnen
results_list <- lapply(csv_files, function(file) {
  file_name <- basename(file)
  cat("Analysiere:", file_name, "\n")
  calculate_species_richness(file, file_name)
})

# Zusammenfassung erstellen
summary_df <- do.call(rbind, lapply(results_list, function(res) {
  data.frame(
    file_name = res$file_name,
    species_richness = res$species_richness,
    total_observations = res$total_observations,
    stringsAsFactors = FALSE
  )
}))

# Standort und Köder aus Dateinamen extrahieren
summary_df <- summary_df %>%
  mutate(
    # Dateiname aufteilen
    location = ifelse(grepl("utumbi", tolower(file_name)), "Utumbi", "Milimani"),
    date = sub("^(\\d+)-.*", "\\1", file_name),
    bait_info = sub(".*-c\\d+-(.+)-ganz\\.csv$", "\\1", file_name),
    # Shannon Diversity Index könnte später berechnet werden
    observations_per_species = round(total_observations / species_richness, 2)
  )

# Sortieren nach Species Richness
summary_df <- summary_df %>%
  arrange(desc(species_richness))

# Ergebnisse ausgeben
cat("\n=== SPECIES RICHNESS VERGLEICH ===\n\n")
print(summary_df)

# Detaillierte Artenlisten für jede Datei
cat("\n\n=== DETAILLIERTE ARTENLISTEN ===\n\n")
for (res in results_list) {
  cat("\n--- ", res$file_name, " ---\n")
  cat("Species Richness:", res$species_richness, "\n")
  cat("Gesamtbeobachtungen:", res$total_observations, "\n\n")
  cat("Top 10 häufigste Arten:\n")
  print(head(res$species_counts, 10))
  cat("\n")
}

# Ergebnisse in CSV speichern
output_file <- "results/species_richness_comparison.csv"
write.csv(summary_df, output_file, row.names = FALSE)
cat("\nErgebnisse gespeichert in:", output_file, "\n")

# Zusätzliche detaillierte Artenliste mit allen Arten pro Datei
detailed_species_list <- do.call(rbind, lapply(results_list, function(res) {
  res$species_counts %>%
    mutate(file_name = res$file_name)
}))

detailed_output_file <- "results/species_richness_detailed.csv"
write.csv(detailed_species_list, detailed_output_file, row.names = FALSE)
cat("Detaillierte Artenliste gespeichert in:", detailed_output_file, "\n")
