# ===== Umfassende Analyse: Species Richness + MaxN + Vergleichskennzahlen =====
# Kombiniert alle Annotation Reports (Coral Reef + Nursery)
# Erstellt große Vergleichstabelle mit Species Richness, MaxN und statistischen Kennzahlen

library(dplyr)
library(tidyr)
library(vegan)

# ===== 1. FUNKTIONEN DEFINIEREN =====

# Berechnet comprehensive Statistics für eine Datei
calculate_comprehensive_stats <- function(file_path, file_name, area_type) {
  tryCatch({
    # Daten einlesen
    data <- read.csv(file_path, stringsAsFactors = FALSE)
    
    if (nrow(data) == 0) {
      cat("Warnung: Datei leer -", file_name, "\n")
      return(NULL)
    }
    
    # Basic Statistics
    unique_species <- n_distinct(data$label_name)
    total_observations <- nrow(data)
    
    # MaxN Berechnung für jede Art
    maxn_by_species <- data %>%
      group_by(label_name, frames) %>%
      summarise(count = n(), .groups = "drop") %>%
      group_by(label_name) %>%
      summarise(MaxN = max(count), .groups = "drop")
    
    # Gesamtes MaxN (höchste Anzahl einer Art in einem Frame)
    overall_maxn <- max(maxn_by_species$MaxN)
    
    # Beobachtungen pro Art
    observations_per_species <- data %>%
      group_by(label_name) %>%
      summarise(count = n(), .groups = "drop")
    
    obs_per_species_mean <- mean(observations_per_species$count)
    obs_per_species_sd <- sd(observations_per_species$count)
    
    # Shannon Diversity Index
    species_freq <- table(data$label_name)
    shannon_h <- diversity(species_freq, index = "shannon")
    
    # Simpson Diversity Index
    simpson_d <- diversity(species_freq, index = "simpson")
    
    # Evenness (Pielou's J)
    pielou_j <- shannon_h / log(unique_species)
    
    # Anzahl der Frames im Video
    unique_frames <- n_distinct(data$frames)
    
    # Top 3 häufigste Arten
    top_species <- observations_per_species %>%
      arrange(desc(count)) %>%
      head(3) %>%
      pull(label_name) %>%
      paste(collapse = ", ")
    
    # Informationen aus Dateinamen extrahieren
    location <- ifelse(grepl("utumbi", tolower(file_name)), "Utumbi", "Milimani")
    date <- sub("^(\\d+)-.*", "\\1", file_name)
    
    # Datum formatieren (DDMMJJJJ -> DD.MM.JJJJ)
    if (nchar(date) == 8) {
      date_formatted <- paste0(substr(date, 1, 2), ".", substr(date, 3, 4), ".", substr(date, 5, 8))
    } else {
      date_formatted <- date
    }
    
    # Köder/Bait Information
    bait_info <- sub(".*-c\\d+-(.+)-ganz\\.csv$", "\\1", tolower(file_name))
    if (!grepl("-", file_name)) {
      bait_info <- sub(".*-(.+)-ganz\\.csv$", "\\1", tolower(file_name))
    }
    
    # Ergebnis als Dataframe
    result <- data.frame(
      file_name = file_name,
      area_type = area_type,
      location = location,
      date = date_formatted,
      bait_type = bait_info,
      species_richness = unique_species,
      total_observations = total_observations,
      maxn_overall = overall_maxn,
      obs_per_species_mean = round(obs_per_species_mean, 2),
      obs_per_species_sd = round(obs_per_species_sd, 2),
      shannon_h = round(shannon_h, 3),
      simpson_d = round(simpson_d, 3),
      pielou_j = round(pielou_j, 3),
      unique_frames = unique_frames,
      obs_per_frame = round(total_observations / unique_frames, 2),
      top_3_species = top_species,
      stringsAsFactors = FALSE
    )
    
    return(result)
    
  }, error = function(e) {
    cat("Fehler bei Datei:", file_name, "-", e$message, "\n")
    return(NULL)
  })
}

# ===== 2. ALLE DATEIEN SAMMELN =====

cat("\n===== ANALYSIERE ALLE ANNOTATION REPORTS =====\n\n")

# Coral Reef Dateien
coral_reef_dir <- "Annotation_reports_coral_reef"
coral_reef_files <- list.files(coral_reef_dir, pattern = "\\.csv$", full.names = TRUE)

# Nursery Dateien
nursery_dir <- "Annotation_reports_Nursery"
nursery_files <- list.files(nursery_dir, pattern = "\\.csv$", full.names = TRUE)

cat("Coral Reef Dateien gefunden:", length(coral_reef_files), "\n")
cat("Nursery Dateien gefunden:", length(nursery_files), "\n\n")

# ===== 3. ANALYSIERE ALLE DATEIEN =====

all_results <- list()

# Coral Reef
cat("Analysiere Coral Reef Dateien...\n")
for (file in coral_reef_files) {
  file_name <- basename(file)
  cat("  -", file_name, "\n")
  result <- calculate_comprehensive_stats(file, file_name, "Coral Reef")
  if (!is.null(result)) {
    all_results[[length(all_results) + 1]] <- result
  }
}

# Nursery
cat("\nAnalysiere Nursery Dateien...\n")
for (file in nursery_files) {
  file_name <- basename(file)
  cat("  -", file_name, "\n")
  result <- calculate_comprehensive_stats(file, file_name, "Nursery")
  if (!is.null(result)) {
    all_results[[length(all_results) + 1]] <- result
  }
}

# ===== 4. ZUSAMMENFASSUNG IN DATAFRAME =====

comprehensive_df <- do.call(rbind, all_results)
rownames(comprehensive_df) <- NULL

# Sortieren nach Species Richness (absteigend)
comprehensive_df <- comprehensive_df %>%
  arrange(desc(species_richness))

# ===== 5. ERGEBNISSE ANZEIGEN =====

cat("\n\n===== UMFASSENDE VERGLEICHSTABELLE =====\n\n")
print(comprehensive_df, n = Inf)

# ===== 6. STATISTIKEN NACH BEREICH =====

cat("\n\n===== STATISTIKEN NACH BEREICH =====\n\n")

stats_by_area <- comprehensive_df %>%
  group_by(area_type) %>%
  summarise(
    anzahl_dateien = n(),
    richness_mean = round(mean(species_richness), 2),
    richness_sd = round(sd(species_richness), 2),
    richness_min = min(species_richness),
    richness_max = max(species_richness),
    maxn_mean = round(mean(maxn_overall), 2),
    maxn_sd = round(sd(maxn_overall), 2),
    observations_total = sum(total_observations),
    shannon_mean = round(mean(shannon_h), 3),
    evennes_mean = round(mean(pielou_j), 3),
    .groups = "drop"
  )

print(stats_by_area)

# ===== 7. STATISTIKEN NACH STANDORT (Location) =====

cat("\n\n===== STATISTIKEN NACH STANDORT =====\n\n")

stats_by_location <- comprehensive_df %>%
  group_by(location, area_type) %>%
  summarise(
    anzahl_dateien = n(),
    richness_mean = round(mean(species_richness), 2),
    richness_sd = round(sd(species_richness), 2),
    maxn_mean = round(mean(maxn_overall), 2),
    observations_total = sum(total_observations),
    shannon_mean = round(mean(shannon_h), 3),
    .groups = "drop"
  )

print(stats_by_location)

# ===== 8. TOP KÖDERTYPEN =====

cat("\n\n===== TOP KÖDERTYPEN (Bait Types) =====\n\n")

bait_stats <- comprehensive_df %>%
  group_by(bait_type) %>%
  summarise(
    anzahl_videos = n(),
    richness_mean = round(mean(species_richness), 2),
    richness_sd = round(sd(species_richness), 2),
    maxn_mean = round(mean(maxn_overall), 2),
    obs_mean = round(mean(total_observations), 0),
    shannon_mean = round(mean(shannon_h), 3),
    .groups = "drop"
  ) %>%
  arrange(desc(richness_mean))

print(bait_stats)

# ===== 9. STATISTISCHE SIGNIFIKANZTESTS =====

cat("\n\n===== STATISTISCHE SIGNIFIKANZTESTS =====\n\n")

significance_results <- data.frame()

# Test 1: Coral Reef vs Nursery (Species Richness)
coral_reef_richness <- comprehensive_df %>%
  filter(area_type == "Coral Reef") %>%
  pull(species_richness)

nursery_richness <- comprehensive_df %>%
  filter(area_type == "Nursery") %>%
  pull(species_richness)

if (length(coral_reef_richness) > 0 && length(nursery_richness) > 0) {
  test_result <- wilcox.test(coral_reef_richness, nursery_richness)
  significance_results <- rbind(significance_results, data.frame(
    comparison = "Coral Reef vs Nursery (Species Richness)",
    n_group1 = length(coral_reef_richness),
    n_group2 = length(nursery_richness),
    test = "Mann-Whitney U (Wilcox)",
    statistic = round(test_result$statistic, 4),
    p_value = round(test_result$p.value, 6),
    significant_alpha_005 = ifelse(test_result$p.value < 0.05, "Yes", "No"),
    mean_group1 = round(mean(coral_reef_richness), 2),
    mean_group2 = round(mean(nursery_richness), 2)
  ))
}

# Test 2: Milimani vs Utumbi (Species Richness)
milimani_richness <- comprehensive_df %>%
  filter(location == "Milimani") %>%
  pull(species_richness)

utumbi_richness <- comprehensive_df %>%
  filter(location == "Utumbi") %>%
  pull(species_richness)

if (length(milimani_richness) > 0 && length(utumbi_richness) > 0) {
  test_result <- wilcox.test(milimani_richness, utumbi_richness)
  significance_results <- rbind(significance_results, data.frame(
    comparison = "Milimani vs Utumbi (Species Richness)",
    n_group1 = length(milimani_richness),
    n_group2 = length(utumbi_richness),
    test = "Mann-Whitney U (Wilcox)",
    statistic = round(test_result$statistic, 4),
    p_value = round(test_result$p.value, 6),
    significant_alpha_005 = ifelse(test_result$p.value < 0.05, "Yes", "No"),
    mean_group1 = round(mean(milimani_richness), 2),
    mean_group2 = round(mean(utumbi_richness), 2)
  ))
}

# Test 3: Milimani vs Utumbi (MaxN)
milimani_maxn <- comprehensive_df %>%
  filter(location == "Milimani") %>%
  pull(maxn_overall)

utumbi_maxn <- comprehensive_df %>%
  filter(location == "Utumbi") %>%
  pull(maxn_overall)

if (length(milimani_maxn) > 0 && length(utumbi_maxn) > 0) {
  test_result <- wilcox.test(milimani_maxn, utumbi_maxn)
  significance_results <- rbind(significance_results, data.frame(
    comparison = "Milimani vs Utumbi (MaxN)",
    n_group1 = length(milimani_maxn),
    n_group2 = length(utumbi_maxn),
    test = "Mann-Whitney U (Wilcox)",
    statistic = round(test_result$statistic, 4),
    p_value = round(test_result$p.value, 6),
    significant_alpha_005 = ifelse(test_result$p.value < 0.05, "Yes", "No"),
    mean_group1 = round(mean(milimani_maxn), 2),
    mean_group2 = round(mean(utumbi_maxn), 2)
  ))
}

# Test 4: Kruskal-Wallis für alle Baits (Species Richness)
bait_types <- unique(comprehensive_df$bait_type)
if (length(bait_types) > 2) {
  bait_groups <- list()
  for (bait in bait_types) {
    bait_groups[[bait]] <- comprehensive_df %>%
      filter(bait_type == bait) %>%
      pull(species_richness)
  }
  
  # Kruskal-Wallis Test
  test_result <- kruskal.test(comprehensive_df$species_richness, comprehensive_df$bait_type)
  significance_results <- rbind(significance_results, data.frame(
    comparison = paste("All Baits (", length(bait_types), ") - Species Richness", sep=""),
    n_group1 = nrow(comprehensive_df),
    n_group2 = length(bait_types),
    test = "Kruskal-Wallis H",
    statistic = round(test_result$statistic, 4),
    p_value = round(test_result$p.value, 6),
    significant_alpha_005 = ifelse(test_result$p.value < 0.05, "Yes", "No"),
    mean_group1 = round(mean(comprehensive_df$species_richness), 2),
    mean_group2 = ""
  ))
}

# Test 5: Paarweise Bait-Vergleiche
bait_list <- sort(unique(comprehensive_df$bait_type))
for (i in 1:min(5, length(bait_list))) {
  for (j in (i+1):min(5, length(bait_list))) {
    group1 <- comprehensive_df %>%
      filter(bait_type == bait_list[i]) %>%
      pull(species_richness)
    
    group2 <- comprehensive_df %>%
      filter(bait_type == bait_list[j]) %>%
      pull(species_richness)
    
    if (length(group1) > 0 && length(group2) > 0) {
      test_result <- wilcox.test(group1, group2)
      significance_results <- rbind(significance_results, data.frame(
        comparison = paste(bait_list[i], " vs ", bait_list[j], sep=""),
        n_group1 = length(group1),
        n_group2 = length(group2),
        test = "Mann-Whitney U (Wilcox)",
        statistic = round(test_result$statistic, 4),
        p_value = round(test_result$p.value, 6),
        significant_alpha_005 = ifelse(test_result$p.value < 0.05, "Yes", "No"),
        mean_group1 = round(mean(group1), 2),
        mean_group2 = round(mean(group2), 2)
      ))
    }
  }
}

# Test 6: Shannon Diversity Index - Coral Reef vs Nursery
coral_reef_shannon <- comprehensive_df %>%
  filter(area_type == "Coral Reef") %>%
  pull(shannon_h)

nursery_shannon <- comprehensive_df %>%
  filter(area_type == "Nursery") %>%
  pull(shannon_h)

if (length(coral_reef_shannon) > 0 && length(nursery_shannon) > 0) {
  test_result <- wilcox.test(coral_reef_shannon, nursery_shannon)
  significance_results <- rbind(significance_results, data.frame(
    comparison = "Coral Reef vs Nursery (Shannon Diversity)",
    n_group1 = length(coral_reef_shannon),
    n_group2 = length(nursery_shannon),
    test = "Mann-Whitney U (Wilcox)",
    statistic = round(test_result$statistic, 4),
    p_value = round(test_result$p.value, 6),
    significant_alpha_005 = ifelse(test_result$p.value < 0.05, "Yes", "No"),
    mean_group1 = round(mean(coral_reef_shannon), 3),
    mean_group2 = round(mean(nursery_shannon), 3)
  ))
}

print(significance_results)

# ===== 10. SPEICHERE ERGEBNISSE =====

dir.create("results", showWarnings = FALSE)

# Haupttabelle
write.csv(comprehensive_df, "results/comprehensive_analysis_table.csv", row.names = FALSE)
cat("\n\nHaupttabelle gespeichert: results/comprehensive_analysis_table.csv\n")

# Bereichs-Statistiken
write.csv(stats_by_area, "results/statistics_by_area.csv", row.names = FALSE)
cat("Bereichs-Statistiken gespeichert: results/statistics_by_area.csv\n")

# Standort-Statistiken
write.csv(stats_by_location, "results/statistics_by_location.csv", row.names = FALSE)
cat("Standort-Statistiken gespeichert: results/statistics_by_location.csv\n")

# Köder-Statistiken
write.csv(bait_stats, "results/statistics_by_bait.csv", row.names = FALSE)
cat("Köder-Statistiken gespeichert: results/statistics_by_bait.csv\n")

# Signifikanz-Tests
write.csv(significance_results, "results/statistical_significance_tests.csv", row.names = FALSE)
cat("Signifikanz-Tests gespeichert: results/statistical_significance_tests.csv\n")

cat("\n===== ANALYSE ABGESCHLOSSEN =====\n\n")
