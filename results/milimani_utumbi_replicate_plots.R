# Milimani vs Utumbi replicate analysis plots
# Uses coral reef annotation reports and saves figures to results/figures

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(stringr)
  library(ggplot2)
  library(vegan)
  library(jsonlite)
})

script_path <- tryCatch(
  normalizePath(sys.frame(1)$ofile, winslash = "/"),
  error = function(e) NA_character_
)
script_dir <- if (!is.na(script_path)) dirname(script_path) else getwd()
repo_dir <- normalizePath(file.path(script_dir, ".."), winslash = "/", mustWork = FALSE)

report_paths <- list.files(
  file.path(repo_dir, "Annotation_reports_coral_reef"),
  pattern = "\\.csv$",
  full.names = TRUE
)

if (length(report_paths) == 0) {
  stop("No coral reef annotation reports found.")
}

parse_meta <- function(path) {
  name <- basename(path)
  stem <- str_replace(name, "\\.csv$", "")
  parts <- str_split(stem, "-", simplify = TRUE)
  if (ncol(parts) < 3) {
    return(NULL)
  }
  list(
    date = parts[1],
    site = parts[2],
    bait = paste(parts[3:ncol(parts)], collapse = "-")
  )
}

normalize_bait <- function(bait) {
  if (str_ends(bait, "-c8") || str_ends(bait, "-c10")) {
    return(str_replace(bait, "-(c8|c10)$", ""))
  }
  bait
}

parse_frames_len <- function(frames) {
  if (is.na(frames) || frames == "") {
    return(1L)
  }
  frames <- trimws(frames)
  if (str_starts(frames, "\\[") && str_ends(frames, "\\]")) {
    # jsonlite can parse numeric arrays directly
    parsed <- tryCatch(fromJSON(frames), error = function(e) NULL)
    if (is.null(parsed)) {
      return(1L)
    }
    if (is.atomic(parsed)) {
      return(length(parsed))
    }
  }
  1L
}

report_rows <- lapply(report_paths, function(path) {
  meta <- parse_meta(path)
  if (is.null(meta)) {
    return(NULL)
  }
  df <- read.csv(path, stringsAsFactors = FALSE)
  df <- df %>%
    mutate(
      report = path,
      site = meta$site,
      bait = normalize_bait(meta$bait),
      taxon = ifelse(species != "", species, ifelse(genus != "", genus, label_name)),
      frames_len = vapply(frames, parse_frames_len, integer(1))
    )
  df
})

report_rows <- bind_rows(report_rows)

# Abundance matrix (report x taxon)
report_abund <- report_rows %>%
  group_by(report, site, bait, taxon) %>%
  summarise(abundance = sum(frames_len), .groups = "drop")

abund_wide <- report_abund %>%
  tidyr::pivot_wider(names_from = taxon, values_from = abundance, values_fill = 0)

meta <- abund_wide %>% select(report, site, bait)
mat <- abund_wide %>% select(-report, -site, -bait) %>% as.data.frame()

# Distance matrices
bray <- vegdist(mat, method = "bray")
jacc <- vegdist(mat, method = "jaccard", binary = TRUE)

pairwise_df <- function(dist_obj, meta, metric_name) {
  dist_mat <- as.matrix(dist_obj)
  n <- nrow(dist_mat)
  rows <- list()
  k <- 1
  for (i in 1:(n - 1)) {
    for (j in (i + 1):n) {
      s1 <- meta$site[i]
      s2 <- meta$site[j]
      rows[[k]] <- data.frame(
        metric = metric_name,
        distance = dist_mat[i, j],
        comparison = ifelse(s1 == s2, "within", "between")
      )
      k <- k + 1
    }
  }
  bind_rows(rows)
}

pairwise <- bind_rows(
  pairwise_df(bray, meta, "Bray-Curtis"),
  pairwise_df(jacc, meta, "Jaccard")
)

# Boxplots: within vs between
p_bc <- pairwise %>%
  filter(metric == "Bray-Curtis") %>%
  ggplot(aes(x = comparison, y = distance, fill = comparison)) +
  geom_boxplot(outlier.size = 0.8) +
  scale_fill_manual(values = c("within" = "#377eb8", "between" = "#e41a1c")) +
  labs(title = "Bray-Curtis distances", x = NULL, y = "Distance") +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")

ggsave(
  file.path(repo_dir, "results", "figures", "bray_curtis_within_between.png"),
  p_bc,
  width = 6,
  height = 4,
  dpi = 150
)

p_j <- pairwise %>%
  filter(metric == "Jaccard") %>%
  ggplot(aes(x = comparison, y = distance, fill = comparison)) +
  geom_boxplot(outlier.size = 0.8) +
  scale_fill_manual(values = c("within" = "#377eb8", "between" = "#e41a1c")) +
  labs(title = "Jaccard distances", x = NULL, y = "Distance") +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")

ggsave(
  file.path(repo_dir, "results", "figures", "jaccard_within_between.png"),
  p_j,
  width = 6,
  height = 4,
  dpi = 150
)

# NMDS (Bray-Curtis)
set.seed(42)
ord <- metaMDS(mat, distance = "bray", k = 2, trymax = 50)
ord_df <- as.data.frame(scores(ord, display = "sites"))
ord_df$site <- meta$site
ord_df$bait <- meta$bait

p_nmds <- ggplot(ord_df, aes(x = NMDS1, y = NMDS2, color = site, shape = bait)) +
  geom_point(size = 2.5, alpha = 0.85) +
  scale_color_manual(values = c("milimani" = "#4daf4a", "utumbi" = "#984ea3")) +
  labs(title = "NMDS (Bray-Curtis)", color = "Site", shape = "Bait") +
  theme_minimal(base_size = 12)

ggsave(
  file.path(repo_dir, "results", "figures", "nmds_bray.png"),
  p_nmds,
  width = 7,
  height = 5,
  dpi = 150
)

# Bait counts by site
bait_counts <- meta %>%
  count(site, bait)

p_counts <- ggplot(bait_counts, aes(x = bait, y = n, fill = site)) +
  geom_col(position = position_dodge(width = 0.8)) +
  labs(title = "Report counts per bait (merged -c8/-c10)", x = NULL, y = "Reports") +
  theme_minimal(base_size = 12) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave(
  file.path(repo_dir, "results", "figures", "bait_counts.png"),
  p_counts,
  width = 7,
  height = 4.5,
  dpi = 150
)

# Bait-level distances (>=3 per site, exclude fischmix)
valid_baits <- bait_counts %>%
  group_by(bait) %>%
  summarise(
    milimani = sum(site == "milimani"),
    utumbi = sum(site == "utumbi"),
    .groups = "drop"
  ) %>%
  filter(bait != "fischmix", milimani >= 3, utumbi >= 3) %>%
  pull(bait)

# Mean vectors per site/bait
mean_vectors <- report_abund %>%
  filter(bait %in% valid_baits) %>%
  group_by(site, bait, taxon) %>%
  summarise(abundance = mean(abundance), .groups = "drop") %>%
  tidyr::pivot_wider(names_from = taxon, values_from = abundance, values_fill = 0)

bait_dist <- list()
for (b in valid_baits) {
  m <- mean_vectors %>% filter(bait == b, site == "milimani") %>% select(-site, -bait)
  u <- mean_vectors %>% filter(bait == b, site == "utumbi") %>% select(-site, -bait)
  if (nrow(m) == 1 && nrow(u) == 1) {
    bc <- as.numeric(vegdist(rbind(m, u), method = "bray"))
    jc <- as.numeric(vegdist(rbind(m, u), method = "jaccard", binary = TRUE))
    bait_dist[[length(bait_dist) + 1]] <- data.frame(bait = b, metric = "Bray-Curtis", distance = bc)
    bait_dist[[length(bait_dist) + 1]] <- data.frame(bait = b, metric = "Jaccard", distance = jc)
  }
}

bait_dist <- bind_rows(bait_dist)

p_bait <- ggplot(bait_dist, aes(x = bait, y = distance, fill = metric)) +
  geom_col(position = position_dodge(width = 0.8)) +
  labs(title = "Bait-level Milimani vs Utumbi distances", x = NULL, y = "Distance") +
  theme_minimal(base_size = 12) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave(
  file.path(repo_dir, "results", "figures", "bait_level_distances.png"),
  p_bait,
  width = 7,
  height = 4.5,
  dpi = 150
)

message("Done. Figures saved to ", file.path(repo_dir, "results", "figures"))
