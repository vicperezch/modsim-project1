from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_MUTED = "#52514e"
GRID = "#e4e3df"
REFERENCE = "#8a8984"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID,
    "axes.labelcolor": TEXT_MUTED,
    "axes.titlecolor": TEXT,
    "axes.titleweight": "bold",
    "axes.titlesize": 12,
    "axes.titlelocation": "left",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": TEXT_MUTED,
    "ytick.color": TEXT_MUTED,
    "lines.linewidth": 2,
    "legend.frameon": False,
    "legend.labelcolor": TEXT,
    "font.size": 10,
    "figure.dpi": 110,
})


def series_style(index, label):
    if label == "Vacío":
        return {"color": REFERENCE, "linestyle": "--", "linewidth": 1.5}
    return {"color": SERIES[index % len(SERIES)]}


def _save(fig, outdir, name):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / name
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_skydiver(runs, outdir):
    vt = max(r.terminal_velocity for r in runs if r.label != "Vacío")
    t_end = max(r.trajectory.t[-1] for r in runs)
    fig, (ax_y, ax_v, ax_a) = plt.subplots(3, 1, figsize=(8, 9), sharex=True)

    color_index = 0
    for run in runs:
        style = series_style(color_index, run.label)
        if run.label != "Vacío":
            color_index += 1
        tr = run.trajectory
        ax_y.plot(tr.t, tr.y, label=run.label, **style)
        ax_v.plot(tr.t, abs(tr.v), **style)
        ax_a.plot(tr.t, -tr.a / run.model.g, **style)

    ax_v.axhline(vt, color=TEXT_MUTED, linewidth=0.8, linestyle=":")
    ax_v.annotate(f"v_t = {vt:.1f} m/s", (t_end, vt), xytext=(0, 4), textcoords="offset points",
                  ha="right", va="bottom", color=TEXT_MUTED)
    ax_v.set_ylim(0, 1.5 * vt)

    ax_y.set_title("Paracaidista: comparación de modelos de arrastre")
    ax_y.set_ylabel("Altura (m)")
    ax_y.set_ylim(bottom=0)
    ax_v.set_ylabel("Rapidez de caída (m/s)")
    ax_a.set_ylabel("Aceleración hacia abajo (g)")
    ax_a.set_ylim(-0.05, 1.1)
    ax_a.set_xlabel("Tiempo (s)")
    ax_a.set_xlim(0, t_end)
    ax_y.legend(loc="upper right")
    fig.tight_layout()
    return _save(fig, outdir, "paracaidista_modelos.png")


def plot_ball_trajectories(runs, reference, outdir):
    fig, (ax_y, ax_v) = plt.subplots(1, 2, figsize=(11, 4.5))
    for i, run in enumerate(runs + [reference]):
        style = series_style(i, run.label)
        tr = run.trajectory
        ax_y.plot(tr.t, tr.y, label=run.label, **style)
        ax_v.plot(tr.t, abs(tr.v), **style)
        if run.label != "Vacío":
            ax_v.plot(tr.t[-1], abs(tr.v[-1]), "o", color=style["color"], markersize=6,
                      markeredgecolor=SURFACE, markeredgewidth=1.5)

    ax_y.set_title(f"Altura vs tiempo (caída desde {reference.height:.0f} m)")
    ax_y.set_xlabel("Tiempo (s)")
    ax_y.set_ylabel("Altura (m)")
    ax_y.set_ylim(bottom=0)
    ax_y.set_xlim(left=0)
    ax_y.legend(loc="lower left")
    ax_v.set_title("Rapidez de caída vs tiempo")
    ax_v.set_xlabel("Tiempo (s)")
    ax_v.set_ylabel("Rapidez (m/s)")
    ax_v.set_ylim(bottom=0)
    ax_v.set_xlim(left=0)
    fig.tight_layout()
    return _save(fig, outdir, "pelotas_trayectorias.png")


def plot_ball_summary(runs, reference, outdir):
    names = [r.label for r in runs]
    colors = [SERIES[i] for i in range(len(runs))]
    times = [r.trajectory.impact_time for r in runs]
    reached = [100 * abs(r.trajectory.impact_velocity) / r.terminal_velocity for r in runs]
    positions = range(len(runs))[::-1]

    fig, (ax_t, ax_p) = plt.subplots(1, 2, figsize=(11, 3.8))
    ax_t.barh(positions, times, color=colors, height=0.6, edgecolor=SURFACE, linewidth=2)
    t_vacuum = reference.trajectory.impact_time
    ax_t.axvline(t_vacuum, color=REFERENCE, linestyle="--", linewidth=1.5)
    ax_t.annotate(f"Vacío: {t_vacuum:.2f} s", (t_vacuum, len(runs) - 0.45), xytext=(4, 0),
                  textcoords="offset points", color=TEXT_MUTED, va="center")
    for y, value in zip(positions, times):
        ax_t.annotate(f"{value:.2f} s", (value, y), xytext=(4, 0), textcoords="offset points",
                      va="center", color=TEXT)
    ax_t.set_title("Tiempo de caída")
    ax_t.set_xlabel("Tiempo (s)")
    ax_t.set_xlim(0, max(times) * 1.2)

    ax_p.barh(positions, reached, color=colors, height=0.6, edgecolor=SURFACE, linewidth=2)
    for y, value in zip(positions, reached):
        ax_p.annotate(f"{value:.1f} %", (value, y), xytext=(4, 0), textcoords="offset points",
                      va="center", color=TEXT)
    ax_p.set_title("Rapidez de impacto (% de v_t)")
    ax_p.set_xlabel("% de v_t")
    ax_p.set_xlim(0, 115)

    for ax in (ax_t, ax_p):
        ax.set_yticks(list(positions), names)
        ax.set_ylim(-0.5, len(runs) - 0.2)
        ax.grid(axis="y", visible=False)
    fig.tight_layout()
    return _save(fig, outdir, "pelotas_resumen.png")
