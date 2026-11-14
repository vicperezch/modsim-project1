from dataclasses import dataclass

import numpy as np

from .analytic import solution
from .models import LinearDrag, QuadraticDrag
from .scenarios import SKYDIVER, SKYDIVER_HEIGHT
from .solvers import simulate

TIME_STEPS = [1.0, 0.5, 0.25, 0.1, 0.05, 0.025, 0.01, 0.005, 0.0025, 0.001, 5e-4, 2.5e-4, 1e-4]
METHODS = ["euler", "rk4"]
ROUNDOFF_FLOOR = 1e-9


@dataclass
class ConvergenceResult:
    model_name: str
    method: str
    dts: np.ndarray
    error_y: np.ndarray
    error_v: np.ndarray

    def fitted_order(self, errors):
        mask = (errors > ROUNDOFF_FLOOR) & (self.dts <= 0.5)
        if mask.sum() < 2:
            return None
        slope, _ = np.polyfit(np.log(self.dts[mask]), np.log(errors[mask]), 1)
        return float(slope)


def convergence_models():
    quadratic = QuadraticDrag.from_body(SKYDIVER)
    linear = LinearDrag.from_terminal_velocity(SKYDIVER.mass, quadratic.terminal_velocity())
    return [linear, quadratic]


def max_errors(model, method, dt, t_final, h0=SKYDIVER_HEIGHT):
    tr = simulate(model, h0, dt=dt, t_max=t_final, method=method, stop_at_ground=False)
    y_exact, v_exact = solution(model, tr.t, h0)
    return np.max(np.abs(tr.y - y_exact)), np.max(np.abs(tr.v - v_exact))


def run_convergence(t_final=20.0, dts=TIME_STEPS):
    results = []
    for model in convergence_models():
        for method in METHODS:
            errors = np.array([max_errors(model, method, dt, t_final) for dt in dts])
            results.append(ConvergenceResult(model.name, method, np.array(dts), errors[:, 0], errors[:, 1]))
    return results


def error_rows(results):
    rows = []
    for r in results:
        for i, dt in enumerate(r.dts):
            local_order = None
            if i > 0 and r.error_v[i] > ROUNDOFF_FLOOR:
                local_order = float(np.log(r.error_v[i - 1] / r.error_v[i]) / np.log(r.dts[i - 1] / dt))
            rows.append({
                "Modelo": r.model_name,
                "Método": r.method.upper(),
                "dt (s)": float(dt),
                "Error máx. y (m)": float(r.error_y[i]),
                "Error máx. v (m/s)": float(r.error_v[i]),
                "Orden local (v)": local_order,
            })
    return rows


def order_rows(results):
    return [
        {
            "Modelo": r.model_name,
            "Método": r.method.upper(),
            "Orden teórico": 1 if r.method == "euler" else 4,
            "Orden observado (y)": r.fitted_order(r.error_y),
            "Orden observado (v)": r.fitted_order(r.error_v),
        }
        for r in results
    ]


def large_step_runs(dt=2.0, t_final=30.0):
    model = QuadraticDrag.from_body(SKYDIVER)
    runs = {m: simulate(model, SKYDIVER_HEIGHT, dt=dt, t_max=t_final, method=m, stop_at_ground=False) for m in METHODS}
    t = np.linspace(0, t_final, 400)
    exact = solution(model, t, SKYDIVER_HEIGHT)
    return model, t, exact, runs
