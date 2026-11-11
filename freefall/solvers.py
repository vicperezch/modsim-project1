from dataclasses import dataclass

import numpy as np


@dataclass
class Trajectory:
    t: np.ndarray
    y: np.ndarray
    v: np.ndarray
    a: np.ndarray
    impact_time: float | None
    impact_velocity: float | None


def euler_step(f, state, dt):
    return state + dt * f(state)


def rk4_step(f, state, dt):
    k1 = f(state)
    k2 = f(state + 0.5 * dt * k1)
    k3 = f(state + 0.5 * dt * k2)
    k4 = f(state + dt * k3)
    return state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


STEPPERS = {"euler": euler_step, "rk4": rk4_step}


def simulate(model, h0, v0=0.0, dt=0.01, t_max=1000.0, method="rk4", stop_at_ground=True):
    step = STEPPERS[method]

    def f(state):
        return np.array([state[1], model.acceleration(state[1])])

    n_steps = int(round(t_max / dt))
    times = [0.0]
    states = [np.array([h0, v0], dtype=float)]
    impact_time = impact_velocity = None

    for k in range(1, n_steps + 1):
        new = step(f, states[-1], dt)
        if stop_at_ground and new[0] <= 0:
            old = states[-1]
            s = old[0] / (old[0] - new[0])
            impact_time = times[-1] + s * dt
            impact_velocity = old[1] + s * (new[1] - old[1])
            times.append(impact_time)
            states.append(np.array([0.0, impact_velocity]))
            break
        times.append(k * dt)
        states.append(new)

    t = np.array(times)
    y, v = np.array(states).T
    return Trajectory(t, y, v, model.acceleration(v), impact_time, impact_velocity)
