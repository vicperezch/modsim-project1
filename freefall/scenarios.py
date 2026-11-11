import math
from dataclasses import dataclass

import numpy as np

from .models import Body, LinearDrag, QuadraticDrag, Vacuum
from .solvers import Trajectory, simulate

SKYDIVER = Body("Paracaidista", mass=80.0, drag_coefficient=1.0, area=0.5, length=1.8)
SKYDIVER_HEIGHT = 4000.0

BALLS = [
    Body.sphere("Ping-pong", mass=0.0027, radius=0.020),
    Body.sphere("Tenis", mass=0.058, radius=0.0335),
    Body.sphere("Béisbol", mass=0.145, radius=0.0366),
    Body.sphere("Boliche", mass=7.26, radius=0.108),
]
BALL_HEIGHT = 56.0


@dataclass
class Run:
    label: str
    model: object
    trajectory: Trajectory
    height: float
    body: Body | None = None

    @property
    def terminal_velocity(self):
        return self.model.terminal_velocity()


def time_to_fraction(run, fraction=0.95):
    target = fraction * run.terminal_velocity
    speed = np.abs(run.trajectory.v)
    if not math.isfinite(target) or speed[-1] < target:
        return None
    return float(np.interp(target, speed, run.trajectory.t))


def run_skydiver(dt=0.01, method="rk4", height=SKYDIVER_HEIGHT):
    quadratic = QuadraticDrag.from_body(SKYDIVER)
    linear = LinearDrag.from_terminal_velocity(SKYDIVER.mass, quadratic.terminal_velocity())
    models = [Vacuum(SKYDIVER.mass), linear, quadratic]
    return [
        Run(m.name, m, simulate(m, height, dt=dt, method=method), height, SKYDIVER)
        for m in models
    ]


def run_balls(dt=0.01, method="rk4", height=BALL_HEIGHT):
    runs = []
    for body in BALLS:
        model = QuadraticDrag.from_body(body)
        runs.append(Run(body.name, model, simulate(model, height, dt=dt, method=method), height, body))
    vacuum = Vacuum(1.0)
    reference = Run("Vacío", vacuum, simulate(vacuum, height, dt=dt, method=method), height)
    return runs, reference


def skydiver_metrics(runs, fraction=0.95):
    rows = []
    for run in runs:
        t_frac = time_to_fraction(run, fraction)
        d_frac = None if t_frac is None else run.height - float(np.interp(t_frac, run.trajectory.t, run.trajectory.y))
        vt = run.terminal_velocity
        rows.append({
            "Modelo": run.label,
            "v_t (m/s)": vt if math.isfinite(vt) else None,
            f"t_{int(fraction * 100)} (s)": t_frac,
            f"d_{int(fraction * 100)} (m)": d_frac,
            "t impacto (s)": run.trajectory.impact_time,
            "v impacto (m/s)": abs(run.trajectory.impact_velocity),
        })
    return rows


def ball_metrics(runs, reference):
    t_vacuum = reference.trajectory.impact_time
    rows = []
    for run in runs:
        speed = abs(run.trajectory.impact_velocity)
        rows.append({
            "Pelota": run.label,
            "Masa (kg)": run.body.mass,
            "Diámetro (m)": run.body.length,
            "v_t (m/s)": run.terminal_velocity,
            "t caída (s)": run.trajectory.impact_time,
            "Retraso vs vacío (s)": run.trajectory.impact_time - t_vacuum,
            "v impacto (m/s)": speed,
            "% de v_t": 100 * speed / run.terminal_velocity,
            "Reynolds": run.body.reynolds(speed),
        })
    rows.append({
        "Pelota": "Vacío",
        "t caída (s)": t_vacuum,
        "Retraso vs vacío (s)": 0.0,
        "v impacto (m/s)": abs(reference.trajectory.impact_velocity),
    })
    return rows
