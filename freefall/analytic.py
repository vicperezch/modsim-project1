import math

import numpy as np

from .models import LinearDrag, QuadraticDrag, Vacuum


def _log_cosh(x):
    x = np.abs(x)
    return x + np.log1p(np.exp(-2 * x)) - math.log(2)


def _vacuum(model, t, h0, v0):
    v = v0 - model.g * t
    y = h0 + v0 * t - 0.5 * model.g * t**2
    return y, v


def _linear(model, t, h0, v0):
    vt = model.terminal_velocity()
    tau = model.mass / model.b
    decay = np.exp(-t / tau)
    v = -vt + (v0 + vt) * decay
    y = h0 - vt * t + tau * (v0 + vt) * (1 - decay)
    return y, v


def _quadratic(model, t, h0, v0):
    vt = model.terminal_velocity()
    if v0 > 0 or abs(v0) >= vt:
        raise ValueError("La solución analítica cuadrática requiere -v_t < v0 <= 0")
    tau0 = math.atanh(-v0 / vt)
    arg = model.g * t / vt + tau0
    v = -vt * np.tanh(arg)
    y = h0 - (vt**2 / model.g) * (_log_cosh(arg) - _log_cosh(tau0))
    return y, v


_SOLUTIONS = {Vacuum: _vacuum, LinearDrag: _linear, QuadraticDrag: _quadratic}


def solution(model, t, h0, v0=0.0):
    t = np.asarray(t, dtype=float)
    return _SOLUTIONS[type(model)](model, t, h0, v0)
