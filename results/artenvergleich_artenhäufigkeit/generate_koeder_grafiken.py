from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def bait_sort_key(name: str) -> tuple[int, str]:
    order = {
        "control": 0,
        "fischmix": 1,
        "mackerel": 2,
        "sargassum": 3,
        "ulva_gutweed": 4,
        "ulva_salad": 5,
        "algae_strings": 6,
        "algaemix": 7,
    }
    return (order.get(name, 999), name)


def load_data(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    profiles = pd.read_csv(base_dir / "integrierte_koederprofile.csv")
    overlap = pd.read_csv(base_dir / "integrierte_overlap_paare.csv")
    return profiles, overlap


def plot_dominant_taxa_per_bait(profiles: pd.DataFrame, out_dir: Path) -> None:
    sites = sorted(profiles["standort"].dropna().unique().tolist())
    fig, axes = plt.subplots(len(sites), 1, figsize=(14, 4.4 * len(sites)), sharex=False)
    if len(sites) == 1:
        axes = [axes]

    for ax, site in zip(axes, sites):
        sub = profiles[profiles["standort"] == site].copy()
        sub = sub.sort_values(by="koeder", key=lambda s: s.map(lambda x: bait_sort_key(str(x))))

        x = np.arange(len(sub))
        width = 0.4
        ax.bar(
            x - width / 2,
            sub["n_taxa_dominant_mean_maxn"],
            width=width,
            label="Dominante Taxa (MaxN)",
            color="#2a9d8f",
        )
        ax.bar(
            x + width / 2,
            sub["n_dominant_taxa_ratio_ge_3"],
            width=width,
            label="Starke Dominanz (Ratio >= 3)",
            color="#264653",
        )

        ax.set_title(f"Standort: {site}")
        ax.set_ylabel("Anzahl Taxa")
        ax.set_xticks(x)
        ax.set_xticklabels(sub["koeder"], rotation=20, ha="right")
        ax.grid(axis="y", alpha=0.25)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.suptitle("Artenhaeufigkeit nach Koeder: dominante Taxa und starke Dominanz", y=0.992)
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, 0.972),
    )
    fig.subplots_adjust(top=0.88, hspace=0.32)
    fig.savefig(out_dir / "koeder_dominante_taxa_und_dominanz.png", dpi=220)
    plt.close(fig)


def plot_signal_and_specific_taxa(profiles: pd.DataFrame, out_dir: Path) -> None:
    plot_df = profiles.copy()
    plot_df["n_koederspezifische_taxa_presence"] = plot_df[
        "n_koederspezifische_taxa_presence"
    ].fillna(0)

    sites = sorted(plot_df["standort"].dropna().unique().tolist())
    fig, axes = plt.subplots(len(sites), 1, figsize=(14, 4.4 * len(sites)), sharex=False)
    if len(sites) == 1:
        axes = [axes]

    for ax, site in zip(axes, sites):
        sub = plot_df[plot_df["standort"] == site].copy()
        sub = sub.sort_values(by="koeder", key=lambda s: s.map(lambda x: bait_sort_key(str(x))))

        x = np.arange(len(sub))
        width = 0.35
        ax.bar(
            x - width / 2,
            sub["n_dominant_taxa_raw_sig"],
            width=width,
            label="Roh-signifikante dominante Taxa",
            color="#e76f51",
        )
        ax.bar(
            x + width / 2,
            sub["n_koederspezifische_taxa_presence"],
            width=width,
            label="Koederspezifische Taxa (Vorkommen)",
            color="#f4a261",
        )

        ax.set_title(f"Standort: {site}")
        ax.set_ylabel("Anzahl Taxa")
        ax.set_xticks(x)
        ax.set_xticklabels(sub["koeder"], rotation=20, ha="right")
        ax.grid(axis="y", alpha=0.25)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.suptitle("Artenvergleich je Koeder: Roh-Signale und koederspezifische Taxa", y=0.992)
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, 0.972),
    )
    fig.subplots_adjust(top=0.88, hspace=0.32)
    fig.savefig(out_dir / "koeder_rohsignale_und_spezifische_taxa.png", dpi=220)
    plt.close(fig)


def plot_dominant_and_specific_taxa(profiles: pd.DataFrame, out_dir: Path) -> None:
    plot_df = profiles.copy()

    sites = sorted(plot_df["standort"].dropna().unique().tolist())
    fig, axes = plt.subplots(len(sites), 1, figsize=(14, 4.6 * len(sites)), sharex=False)
    if len(sites) == 1:
        axes = [axes]

    for ax, site in zip(axes, sites):
        sub = plot_df[plot_df["standort"] == site].copy()
        sub = sub.sort_values(by="koeder", key=lambda s: s.map(lambda x: bait_sort_key(str(x))))

        x = np.arange(len(sub))
        bars = ax.bar(
            x,
            sub["n_taxa_dominant_mean_maxn"],
            width=0.6,
            color="#2a9d8f",
            alpha=0.9,
            label="Dominante Taxa (MaxN)",
        )

        ax2 = ax.twinx()
        specific = sub["n_koederspezifische_taxa_presence"]
        has_specific_data = specific.notna().any()

        line = [None]
        if has_specific_data:
            line = ax2.plot(
                x,
                specific,
                color="#e76f51",
                marker="o",
                linewidth=2.2,
                markersize=6.5,
                label="Koederspezifische Taxa (Vorkommen)",
            )
            max_specific = float(np.nanmax(specific.to_numpy(dtype=float)))
            ax2.set_ylim(0, max(1.0, max_specific + 0.8))
        else:
            ax2.set_ylim(0, 1)
            ax2.set_yticks([])
            ax2.text(
                0.985,
                0.86,
                "Keine Angaben",
                transform=ax2.transAxes,
                ha="right",
                va="center",
                color="#a44a3f",
                fontsize=9,
            )

        ax.set_title(f"Standort: {site}")
        ax.set_ylabel("Dominante Taxa (Anzahl)")
        ax2.set_ylabel("Koederspezifische Taxa (Anzahl)")
        ax.set_xticks(x)
        ax.set_xticklabels(sub["koeder"], rotation=20, ha="right")
        ax.grid(axis="y", alpha=0.25)

        # Kombinierte Legende aus Balken- und Linienobjekten je Subplot.
        handles = [bars[0]]
        labels = ["Dominante Taxa (MaxN)"]
        if has_specific_data and line[0] is not None:
            handles.append(line[0])
            labels.append("Koederspezifische Taxa (Vorkommen)")
        ax.legend(handles, labels, loc="upper left", frameon=False)

    fig.suptitle(
        "Kombination je Koeder: dominante Taxa und koederspezifische Taxa",
        y=0.992,
    )
    fig.subplots_adjust(top=0.92, hspace=0.33)
    fig.savefig(out_dir / "koeder_dominant_und_spezifisch_kombiniert.png", dpi=220)
    plt.close(fig)


def _matrix_from_pairs(sub: pd.DataFrame) -> pd.DataFrame:
    labels = sorted(
        set(sub["bait_a"].dropna().astype(str).tolist())
        | set(sub["bait_b"].dropna().astype(str).tolist()),
        key=bait_sort_key,
    )
    matrix = pd.DataFrame(np.nan, index=labels, columns=labels)
    for _, row in sub.iterrows():
        a = str(row["bait_a"])
        b = str(row["bait_b"])
        d = float(row["jaccard_distance"])
        matrix.loc[a, b] = d
        matrix.loc[b, a] = d
    arr = matrix.to_numpy(copy=True)
    np.fill_diagonal(arr, 0.0)
    matrix.loc[:, :] = arr
    return matrix


def plot_jaccard_distance_heatmaps(overlap: pd.DataFrame, out_dir: Path) -> None:
    sites = sorted(overlap["standort"].dropna().unique().tolist())
    fig, axes = plt.subplots(
        1,
        len(sites),
        figsize=(7.0 * len(sites), 6.0),
        sharey=False,
        constrained_layout=True,
    )
    if len(sites) == 1:
        axes = [axes]

    for ax, site in zip(axes, sites):
        sub = overlap[overlap["standort"] == site].copy()
        mat = _matrix_from_pairs(sub)
        im = ax.imshow(mat.values, cmap="YlOrRd", vmin=0.0, vmax=1.0)
        ax.set_title(f"{site}")
        ax.set_xticks(np.arange(len(mat.columns)))
        ax.set_yticks(np.arange(len(mat.index)))
        ax.set_xticklabels(mat.columns, rotation=35, ha="right")
        ax.set_yticklabels(mat.index)

        # Werte in die Felder schreiben, damit Kontraste direkt sichtbar sind.
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                val = mat.values[i, j]
                if np.isnan(val):
                    continue
                txt_color = "black" if val < 0.55 else "white"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=txt_color, fontsize=8)

    cbar = fig.colorbar(im, ax=axes, fraction=0.024, pad=0.02)
    cbar.set_label("Jaccard-Distanz")
    fig.suptitle("Artenvergleich nach Koeder: Distanz der Taxa-Zusammensetzung", y=0.99)
    fig.savefig(out_dir / "koeder_jaccard_distanz_heatmaps.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    out_dir = base_dir / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles, overlap = load_data(base_dir)

    plot_dominant_taxa_per_bait(profiles, out_dir)
    plot_signal_and_specific_taxa(profiles, out_dir)
    plot_dominant_and_specific_taxa(profiles, out_dir)
    plot_jaccard_distance_heatmaps(overlap, out_dir)

    print(f"Grafiken erstellt in: {out_dir}")


if __name__ == "__main__":
    main()
