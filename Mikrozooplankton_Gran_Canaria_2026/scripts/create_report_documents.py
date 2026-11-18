from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_DIR / "results"
MICRO_XLSX = RESULTS_DIR / "microzooplankton_analysis" / "microzooplankton_analysis.xlsx"
PHYTO_XLSX = RESULTS_DIR / "phytoplankton_analysis" / "phytoplankton_analysis.xlsx"
COMPARISON_DIR = RESULTS_DIR / "microzooplankton_vs_phytoplankton"
REPORT_DIR = RESULTS_DIR / "report_documents"
FIGURES_DIR = REPORT_DIR / "figures"
MESOCOSMS = [1, 2, 3, 6, 8, 9]
COMMON_DAYS = [1, 3, 5, 7, 11, 15, 19, 23, 27, 31]

COLORS = {"concrete": "#0072B2", "naoh": "#D55E00"}
MARKERS = {0: "o", 300: "^", 500: "s"}
GROUP_COLORS = {
    "Mikrozooplankton gesamt": "#333333",
    "Ciliaten": "#009E73",
    "Dinoflagellaten": "#E69F00",
}
PHYTO_COLORS = {
    "Phytoplankton gesamt": "#333333",
    "Small-Phytoplankton": "#56B4E9",
    "Large-Phytoplankton": "#CC79A7",
}


def treatment_style(label: str, mesocosm: int) -> tuple[str, str, int]:
    text = str(label).lower()
    if "kontrolle" in text:
        return "#555555", MARKERS[0], 0
    material = "concrete" if "concrete" in text else "naoh"
    dose_match = re.search(r"\d+", text)
    dose = int(dose_match.group()) if dose_match else 0
    return COLORS[material], MARKERS.get(dose, "o"), dose


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    micro = pd.read_excel(MICRO_XLSX, sheet_name="Gruppenverlauf")
    micro = micro[micro.mesocosm.isin(MESOCOSMS)].pivot_table(
        index=["mesocosm", "sample_day", "treatment_group"],
        columns="group",
        values="cells_L",
        aggfunc="sum",
    ).reset_index()
    micro = micro.rename(
        columns={
            "sample_day": "day",
            "Ciliate": "ciliate_cells_L",
            "Dinoflagellate": "dinoflagellate_cells_L",
        }
    )
    micro["micro_total_cells_L"] = micro.ciliate_cells_L + micro.dinoflagellate_cells_L

    phyto = pd.read_excel(PHYTO_XLSX, sheet_name="Gesamtverlauf")
    phyto = phyto[phyto.Mesocosm.isin(MESOCOSMS)].rename(
        columns={
            "Mesocosm": "mesocosm",
            "Day": "day",
            "total_cells_L": "phyto_total_cells_L",
            "small_cells_L": "phyto_small_cells_L",
            "large_cells_L": "phyto_large_cells_L",
        }
    )
    phyto = phyto[
        ["mesocosm", "day", "phyto_total_cells_L", "phyto_small_cells_L", "phyto_large_cells_L"]
    ]
    comparison = pd.read_excel(COMPARISON_DIR / "microzooplankton_vs_phytoplankton.xlsx", sheet_name="Korrelationen")
    effects = pd.read_excel(COMPARISON_DIR / "microzooplankton_vs_phytoplankton.xlsx", sheet_name="Mesokosmos_Effekte")
    return micro, phyto, comparison, effects


def plot_micro(micro: pd.DataFrame) -> None:
    labels = [
        ("micro_total_cells_L", "Mikrozooplankton gesamt"),
        ("ciliate_cells_L", "Ciliaten"),
        ("dinoflagellate_cells_L", "Dinoflagellaten"),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(10, 11), sharex=True)
    sns.set_theme(style="ticks", context="notebook")
    legend_done: set[str] = set()
    for ax, (column, title) in zip(axes, labels):
        for mesocosm, frame in micro.groupby("mesocosm"):
            color, marker, dose = treatment_style(frame.treatment_group.iloc[0], mesocosm)
            material = "Concrete" if color == COLORS["concrete"] else "NaOH"
            line_label = f"{dose} {material}"
            ax.plot(
                frame.day,
                frame[column],
                color=color,
                marker=marker,
                linewidth=2,
                markersize=7,
                markeredgecolor="white",
                markeredgewidth=0.5,
                label=line_label if line_label not in legend_done else None,
            )
            legend_done.add(line_label)
        ax.axvline(4, color="black", linestyle="--", linewidth=1)
        ax.set_yscale("log")
        ax.set_ylabel("Zellen L$^{-1}$")
        ax.set_title(title)
    axes[-1].set_xlabel("Probetag")
    handles = [
        plt.Line2D([0], [0], color=color, marker=marker, linewidth=1.5, label=label)
        for label, color, marker in [
            ("Kontrolle: 0", "#555555", "o"),
            ("300 Concrete", COLORS["concrete"], "^"),
            ("500 Concrete", COLORS["concrete"], "s"),
            ("300 NaOH", COLORS["naoh"], "^"),
            ("500 NaOH", COLORS["naoh"], "s"),
        ]
    ]
    fig.legend(handles=handles, title="Material / Dosierung", loc="center right", bbox_to_anchor=(1.02, 0.5))
    fig.suptitle("Mikrozooplankton: zeitlicher Verlauf", y=0.995)
    fig.tight_layout(rect=(0, 0, 0.83, 0.98))
    fig.savefig(FIGURES_DIR / "01_mikrozooplankton_zeitverlauf.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_comparison(micro: pd.DataFrame, phyto: pd.DataFrame) -> None:
    data = micro.merge(phyto, on=["mesocosm", "day"], validate="one_to_one")
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    for ax, column, title in [
        (axes[0], "micro_total_cells_L", "Mikrozooplankton gesamt"),
        (axes[1], "phyto_total_cells_L", "Phytoplankton gesamt"),
    ]:
        for mesocosm, frame in data.groupby("mesocosm"):
            color, marker, dose = treatment_style(frame.treatment_group.iloc[0], mesocosm)
            material = "Concrete" if color == COLORS["concrete"] else "NaOH"
            ax.plot(
                frame.day,
                frame[column],
                color=color,
                marker=marker,
                linewidth=1.6,
                markersize=6,
                label=f"{dose} {material}",
            )
        ax.axvline(4, color="black", linestyle="--", linewidth=1)
        ax.set_yscale("log")
        ax.set_ylabel("Zellen L$^{-1}$")
        ax.set_title(title)
    axes[-1].set_xlabel("Probetag")
    handles = [
        plt.Line2D([0], [0], color=color, marker=marker, linewidth=1.5, label=label)
        for label, color, marker in [
            ("Kontrolle: 0", "#555555", "o"),
            ("300 Concrete", COLORS["concrete"], "^"),
            ("500 Concrete", COLORS["concrete"], "s"),
            ("300 NaOH", COLORS["naoh"], "^"),
            ("500 NaOH", COLORS["naoh"], "s"),
        ]
    ]
    fig.legend(handles=handles, title="Material / Dosierung", loc="center right", bbox_to_anchor=(1.02, 0.5))
    fig.suptitle("Vergleich Mikrozooplankton und Phytoplankton", y=0.995)
    fig.tight_layout(rect=(0, 0, 0.83, 0.98))
    fig.savefig(FIGURES_DIR / "02_mikro_vs_phyto_zeitverlauf.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_lags(comparison: pd.DataFrame) -> None:
    selected = comparison[
        comparison.comparison.isin(
            ["Ciliaten vs. Phytoplankton gesamt", "Dinoflagellaten vs. Phytoplankton gesamt"]
        )
    ]
    mean_lags = selected.groupby(["comparison", "lag_days"], as_index=False).spearman_rho.mean()
    fig, ax = plt.subplots(figsize=(9, 5))
    comparison_colors = {
        "Ciliaten vs. Phytoplankton gesamt": GROUP_COLORS["Ciliaten"],
        "Dinoflagellaten vs. Phytoplankton gesamt": GROUP_COLORS["Dinoflagellaten"],
    }
    sns.lineplot(
        data=mean_lags,
        x="lag_days",
        y="spearman_rho",
        hue="comparison",
        marker="o",
        palette=comparison_colors,
        linewidth=2.5,
        markersize=8,
        ax=ax,
    )
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set_xlabel("Lag: Phytoplankton relativ zum Mikrozooplankton (Tage)")
    ax.set_ylabel("Mittlere Spearman-Korrelation")
    ax.set_title("Zeitverzögerte Beziehungen zwischen Mikro- und Phytoplankton")
    ax.legend(title="")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "03_zeitverzoegerte_beziehungen.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_report(micro: pd.DataFrame, phyto: pd.DataFrame, comparison: pd.DataFrame, effects: pd.DataFrame) -> None:
    post = micro[micro.day >= 5]
    micro_summary = (
        post.groupby("mesocosm", as_index=False)
        .agg(
            treatment=("treatment_group", "first"),
            mean_micro_total=("micro_total_cells_L", "mean"),
            T31_micro_total=("micro_total_cells_L", "last"),
        )
        .round(1)
    )
    t3 = micro[micro.day == 3].set_index("mesocosm")
    t31 = micro[micro.day == 31].set_index("mesocosm")
    micro_summary["change_T3_T31_percent"] = (
        (t31.micro_total_cells_L - t3.micro_total_cells_L)
        / t3.micro_total_cells_L
        * 100
    ).round(1).to_numpy()
    lag = comparison.groupby(["comparison", "lag_days"], as_index=False).spearman_rho.mean()
    best_lag = lag.loc[lag.groupby("comparison").spearman_rho.idxmax()].sort_values("comparison")
    tests = pd.read_excel(COMPARISON_DIR / "microzooplankton_vs_phytoplankton.xlsx", sheet_name="Signifikanztests")
    report = f"""# Mikrozooplankton und seine Beziehung zum Phytoplankton

## Datengrundlage und Auswertungsansatz

Die Auswertung umfasst die sechs ausgewerteten Mesokosmen M1, M2, M3, M6, M8 und M9 sowie Probetage bis einschließlich T31. Die Behandlung erfolgte an T4; T1–T3 werden als Vorbehandlung und T5–T31 als Nachbehandlung betrachtet. Das Mikrozooplankton wurde ausschließlich aus den Rohzählungen der Spalte `Count` berechnet. Die Umrechnung erfolgte mit `Zellen L⁻¹ = Count × 40`, da ein halber Boden eines 50-ml-Zylinders gezählt und anschließend auf einen Liter hochgerechnet wurde. Ciliaten und Dinoflagellaten wurden getrennt ausgewertet; Biomasse wurde nicht berücksichtigt.

Für den Vergleich mit dem Phytoplankton wurden die geprüften `All cells`-Summen der Small- und Large-Messungen verwendet. Zeitverzögerte Beziehungen wurden über die tatsächlich vorhandenen Zeitpunkte beider Datensätze geprüft. Ein negativer Lag bedeutet, dass das Phytoplankton zeitlich vor dem Mikrozooplankton liegt.

## Einheitlicher Farb- und Symbolcode

Der Bericht verwendet getrennte, eindeutig erkennbare Codierungen für Mesokosmos-Treatments und biologische Gruppen:

| Verwendung | Kennzeichnung | Farbe / Symbol |
|---|---|---|
| Concrete | Material | Blau `#0072B2` |
| NaOH | Material | Orange `#D55E00` |
| Kontrolle | Dosierung 0 | Grau `#555555`, Kreis |
| 300 | Dosierung | Dreieck |
| 500 | Dosierung | Quadrat |
| Gesamt-Mikrozooplankton | Gruppe | Schwarzgrau `#333333` |
| Ciliaten | Gruppe | Grün `#009E73` |
| Dinoflagellaten | Gruppe | Gelborange `#E69F00` |

Die Treatment-Farbe kennzeichnet das Material und das Symbol die Dosierung. In getrennten Gruppenvergleichen kennzeichnen die Grün-/Gelborange-Töne Ciliaten und Dinoflagellaten; diese Farbdaten sind nicht mit der Materialcodierung zu vermischen. Für gute Lesbarkeit verwenden alle Berichtsgrafiken klare Linienstärken, ausgefüllte Symbole und ausreichend Kontrast. Die Kontrollfarbe ist grau, da Kontrollen keinem Material zugeordnet werden.

## Ergebnisse des Mikrozooplanktons

Die Gesamtzellzahlen des Mikrozooplanktons zeigten zwischen T1 und T3 keinen einheitlichen Vorbehandlungstrend. Nach der Behandlung verliefen die Mesokosmen deutlich unterschiedlich. Die mittleren Nachbehandlungswerte und die Veränderung zwischen T3 und T31 sind:

{micro_summary.to_string(index=False)}

Die Ciliaten reagierten insgesamt empfindlicher als die Dinoflagellaten. Über die sechs Mesokosmen war die mittlere T3-normalisierte Ciliatenänderung signifikant von null verschieden (Wilcoxon-Test, p = 0,031), während die Dinoflagellaten keine statistisch signifikante gemeinsame Änderung zeigten (p = 0,156). Aufgrund von n = 6 und fehlender Replikation einzelner Material-Dosis-Kombinationen sind diese Tests als deskriptiv-explorativ einzuordnen.

Die Ciliatenrückgänge waren besonders ausgeprägt in den Kontrollmesokosmen und in M8 (300 NaOH). Gleichzeitig blieben Dinoflagellaten in einzelnen Mesokosmen stabil oder nahmen zu, beispielsweise in M2 (500 NaOH). Dies weist auf unterschiedliche Reaktionen der beiden Mikrozooplanktongruppen hin und spricht gegen eine einheitliche Antwort des Mikrozooplanktons.

![Zeitlicher Verlauf des Mikrozooplanktons](figures/01_mikrozooplankton_zeitverlauf.png)

**Abbildung 1:** Zeitlicher Verlauf der Gesamtzellzahl des Mikrozooplanktons sowie der Ciliaten und Dinoflagellaten. Blaue Linien kennzeichnen Concrete und orange Linien NaOH; 0 = Kreis, 300 = Dreieck und 500 = Quadrat. Die gestrichelte Linie markiert T4.

## Vergleich mit dem Phytoplankton

Das Phytoplankton zeigte nach T4 in mehreren Mesokosmen zunächst einen Rückgang, während sich einzelne Mesokosmen im späteren Verlauf wieder erholten. Die Small-Fraktion und das Phytoplankton gesamt zeigten über die sechs Mesokosmen eine signifikante mittlere Abnahme (jeweils p = 0,031); die Large-Fraktion zeigte dagegen keine gemeinsame signifikante Veränderung (p = 0,844).

Zeitgleiche Korrelationen zwischen Mikrozooplankton und Phytoplankton waren nach Korrektur für multiples Testen nicht signifikant. Daraus folgt, dass hohe Phytoplanktonwerte nicht unmittelbar und konsistent mit hohen Mikrozooplanktonwerten am selben Probetag verbunden waren.

![Vergleich von Mikrozooplankton und Phytoplankton](figures/02_mikro_vs_phyto_zeitverlauf.png)

**Abbildung 2:** Vergleich der zeitlichen Entwicklung des Gesamt-Mikrozooplanktons und des Gesamtphytoplanktons an den gemeinsamen Probetagen.

## Zeitverzögerte Beziehungen

Die zeitverzögerte Analyse ist für die Interpretation einer möglichen trophischen Beziehung besonders relevant. Die stärksten mittleren Spearman-Zusammenhänge wurden bei folgenden Verzögerungen beobachtet:

{best_lag.to_string(index=False)}

Der stärkste mittlere Zusammenhang zwischen Ciliaten und Large-Phytoplankton trat bei Lag −2 auf (mittlere Spearman-Korrelation ρ = {best_lag.loc[best_lag.comparison == "Ciliaten vs. Large-Phytoplankton", "spearman_rho"].iloc[0]:.3f}). Das bedeutet, dass das Phytoplanktonsignal ungefähr zwei Tage vor dem Ciliatensignal lag. Ein solches Muster ist grundsätzlich mit einer verzögerten Konsumentenreaktion nach erhöhter Nahrungsverfügbarkeit vereinbar.

Auch für das Mikrozooplankton gesamt lag der stärkste mittlere Zusammenhang mit dem Gesamtphytoplankton bei Lag −2 (ρ = {best_lag.loc[best_lag.comparison == "Mikrozooplankton gesamt vs. Phytoplankton gesamt", "spearman_rho"].iloc[0]:.3f}). Dieses Ergebnis unterstützt die Hypothese einer zeitlich verzögerten Reaktion stärker als die zeitgleichen Korrelationen. Es ist jedoch nicht über alle Mesokosmen gleich ausgeprägt und blieb nach FDR-Korrektur nicht signifikant.

Die Unterschiede zwischen den Mesokosmen sind biologisch relevant: Für Ciliaten lagen die besten individuellen Lags zwischen 0 und +4 Tagen, bei Dinoflagellaten zwischen −4 und +2 Tagen. Damit existiert kein einheitlicher zeitlicher Versatz. Mögliche Ursachen sind unterschiedliche Nahrungspräferenzen, wechselnde Phytoplanktonzusammensetzungen, abweichende Entwicklungsstadien der Populationen oder zusätzliche Umwelt- und Treatmentwirkungen.

![Zeitverzögerte Beziehungen zwischen Mikro- und Phytoplankton](figures/03_zeitverzoegerte_beziehungen.png)

**Abbildung 3:** Mittlere Spearman-Korrelationen bei unterschiedlichen zeitlichen Verschiebungen. Ein negativer Lag bedeutet, dass das Phytoplankton zeitlich vor dem Mikrozooplankton liegt.

## Wissenschaftliche Interpretation

Die Daten sind mit einer trophischen Kopplung zwischen Phytoplankton und Mikrozooplankton vereinbar, liefern jedoch keinen allgemeinen statistischen Nachweis einer einheitlichen Räuber-Beute-Beziehung. Besonders die negative Lag-Struktur von ungefähr zwei Tagen ist als biologisch plausible Arbeitshypothese hervorzuheben: Eine Veränderung des Phytoplanktons könnte der Reaktion des Mikrozooplanktons zeitlich vorausgehen. Der fehlende konsistente Nachweis über alle Mesokosmen zeigt jedoch, dass die Dynamik nicht allein durch die Gesamtzellzahl des Phytoplanktons erklärt wird.

Ein weiterer wichtiger Befund ist die unterschiedliche Reaktion von Ciliaten und Dinoflagellaten. Die Ciliaten zeigten den deutlichsten gemeinsamen Rückgang, während Dinoflagellaten teilweise unabhängig oder gegenläufig reagierten. Für eine ökologische Interpretation sollten beide Gruppen deshalb getrennt betrachtet werden.

Die Treatmentvergleiche dürfen nicht als allgemeine Material- oder Dosiseffekte interpretiert werden, da jede Kombination nur in einem Mesokosmos vorliegt. Außerdem sind die Messreihen kurz und teilweise unregelmäßig beprobt. Die Lag-Korrelationen sind daher primär hypothesengenerierend. Eine belastbare Prüfung der trophischen Beziehung würde replizierte Mesokosmen, häufigere Probenahmen und möglichst taxonspezifische Phytoplanktondaten erfordern.

## Berichtstaugliche Kernaussage

> Die Ergebnisse weisen auf eine mögliche zeitverzögerte Kopplung zwischen Phytoplankton und Mikrozooplankton hin. Insbesondere lagen die stärksten mittleren Zusammenhänge für Ciliaten und das Mikrozooplankton gesamt bei einem Phytoplanktonvorsprung von etwa zwei Tagen. Dieses Muster ist mit einer verzögerten Reaktion der Konsumenten auf die Nahrungsverfügbarkeit vereinbar, blieb jedoch zwischen den Mesokosmen uneinheitlich und nach Korrektur für multiple Tests statistisch nicht signifikant. Die Ciliaten reagierten insgesamt stärker als die Dinoflagellaten, weshalb beide Gruppen getrennt interpretiert werden müssen.
"""
    (REPORT_DIR / "mikrozooplankton_phytoplankton_bericht.md").write_text(report, encoding="utf-8")


def write_figure_document() -> None:
    document = """# Berichtsgrafiken: Mikrozooplankton und Phytoplankton

Die folgenden Abbildungen wurden für die direkte Verwendung im Bericht neu gestaltet und verwenden einen konsistenten, kontrastreichen Farb- und Symbolcode.

## Wiederverwendbarer Berichtscode

| Zweck | Kennzeichnung | Farbe / Symbol |
|---|---|---|
| Concrete | Material | Blau `#0072B2` |
| NaOH | Material | Orange `#D55E00` |
| Kontrolle | Dosierung 0 | Grau `#555555`, Kreis |
| Dosierung 300 | Treatment | Dreieck |
| Dosierung 500 | Treatment | Quadrat |
| Mikrozooplankton gesamt | Gruppe | Schwarzgrau `#333333` |
| Ciliaten | Gruppe | Grün `#009E73` |
| Dinoflagellaten | Gruppe | Gelborange `#E69F00` |

Die Coding-Ebene ist kontextabhängig: In Mesokosmos-Zeitreihen kennzeichnet die Farbe das Material und das Symbol die Dosierung. In Abbildungen, die Ciliaten und Dinoflagellaten direkt gegenüberstellen, kennzeichnen die Gruppenfarben die biologische Gruppe. Die gestrichelte vertikale Linie markiert T4, den Behandlungstag. Die y-Achsen der Zellzahlverläufe sind logarithmisch skaliert.

## Abbildung 1: Mikrozooplankton

![Mikrozooplankton-Zeitverlauf](figures/01_mikrozooplankton_zeitverlauf.png)

**Abbildungslegende:** Zeitlicher Verlauf der Gesamtzellzahl des Mikrozooplanktons sowie der Ciliaten und Dinoflagellaten in den sechs ausgewerteten Mesokosmen. Die Farbe zeigt das Material (Concrete blau `#0072B2`, NaOH orange `#D55E00`), das Symbol die Dosierung (0 = Kreis, 300 = Dreieck, 500 = Quadrat). Die gestrichelte Linie markiert die Behandlung an T4.

## Abbildung 2: Vergleich Mikro- und Phytoplankton

![Vergleich Mikro- und Phytoplankton](figures/02_mikro_vs_phyto_zeitverlauf.png)

**Abbildungslegende:** Vergleich der zeitlichen Entwicklung des Gesamt-Mikrozooplanktons und des Gesamtphytoplanktons. Dargestellt sind nur Messwerte, die für beide Analysen an denselben Probetagen vorliegen.

## Abbildung 3: Zeitverzögerte Beziehungen

![Zeitverzögerte Beziehungen](figures/03_zeitverzoegerte_beziehungen.png)

**Abbildungslegende:** Mittlere Spearman-Korrelationen zwischen Mikrozooplankton und Phytoplankton bei verschiedenen zeitlichen Verschiebungen. Ciliaten sind grün (`#009E73`) und Dinoflagellaten gelborange (`#E69F00`) dargestellt. Ein negativer Lag bedeutet, dass das Phytoplankton zeitlich vor der Mikrozooplanktongruppe liegt.

## Ergänzende Lag-Abbildung

![Lag-Profile der Mesokosmen](../microzooplankton_vs_phytoplankton/figures/04_lag_profile_mesokosmen.png)

**Abbildungslegende:** Lag-Profile der einzelnen Mesokosmen für Ciliaten und Dinoflagellaten gegenüber dem Gesamtphytoplankton. Die Abbildung zeigt die mesokosmspezifische Streuung der optimalen zeitlichen Verschiebung.
"""
    (REPORT_DIR / "berichtsgrafiken_mikrozooplankton_phytoplankton.md").write_text(
        document, encoding="utf-8"
    )


def main() -> None:
    for path in [MICRO_XLSX, PHYTO_XLSX, COMPARISON_DIR / "microzooplankton_vs_phytoplankton.xlsx"]:
        if not path.exists():
            raise FileNotFoundError(path)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    micro, phyto, comparison, effects = load_data()
    plot_micro(micro)
    plot_comparison(micro, phyto)
    plot_lags(comparison)
    write_report(micro, phyto, comparison, effects)
    write_figure_document()
    print(f"Dokumente: {REPORT_DIR}")


if __name__ == "__main__":
    main()
