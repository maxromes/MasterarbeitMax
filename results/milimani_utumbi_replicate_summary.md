# Milimani vs Utumbi (coral reef annotation reports)

Date: 2026-02-09

## Data coverage

- Reports analyzed: 35 (coral reef only)
- Taxa used: 143
- Taxon key: species > genus > label_name (first available)
- Abundance proxy: number of frame timestamps per label (frames list length)

## Similarity metrics (all reports)

Pairwise distances across all reports, split into within-site and between-site:

- Bray-Curtis (abundance):
  - Within-site: mean 0.5343, sd 0.1173, n=289
  - Between-site: mean 0.6071, sd 0.1100, n=306
  - Delta (between - within): 0.0728
  - Ratio (between / within): 1.1362

- Jaccard (presence/absence):
  - Within-site: mean 0.4730, sd 0.0635, n=289
  - Between-site: mean 0.5690, sd 0.0528, n=306
  - Delta (between - within): 0.0960
  - Ratio (between / within): 1.2031

## Bait counts per site (camera variants merged)

Counts after merging -c8/-c10 into the base bait name:

- control: milimani 3, utumbi 4
- fischmix: milimani 1, utumbi 2
- glasnudel: milimani 3, utumbi 3
- mackerel: milimani 3, utumbi 3
- meersalat: milimani 4, utumbi 3
- sargassum: milimani 3, utumbi 3

## Bait-level site distances (>= 3 reports per site, exclude fischmix)

- control: Bray-Curtis 0.4890, Jaccard 0.4500
- glasnudel: Bray-Curtis 0.5646, Jaccard 0.4639
- mackerel: Bray-Curtis 0.3432, Jaccard 0.4425
- meersalat: Bray-Curtis 0.5079, Jaccard 0.4854
- sargassum: Bray-Curtis 0.4575, Jaccard 0.3918

## Interpretation

- Between-site distances are consistently higher than within-site distances for both Bray-Curtis and Jaccard, indicating that Milimani and Utumbi are not identical replicates.
- The effect is moderate (ratio 1.14 to 1.20), suggesting partial overlap with a systematic site signal rather than complete separation.
- Bait-level distances vary by bait (e.g., lower for mackerel, higher for glasnudel), so replicate suitability depends on bait and should be interpreted per bait or with bait as a factor.

## Additional statistical tests to compare sites

- PERMANOVA (Bray-Curtis, Jaccard) with site as factor and bait as covariate: tests whether site explains community differences beyond bait.
- PERMDISP (beta dispersion): checks whether site differences are driven by dispersion rather than location in multivariate space.
- Mantel or Procrustes tests between sites on the same bait averages: evaluates concordance of community structure across sites.
- Indicator species analysis (IndVal): identifies taxa driving site differences.
- Mixed effects models on richness or total abundance per report with site and bait as fixed effects.

## Notes

- Bait-level means computed after merging -c8/-c10 variants.
- Fischmix is excluded because only 1 report (milimani) vs 2 (utumbi).
