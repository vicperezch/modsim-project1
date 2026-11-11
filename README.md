# Caída libre con resistencia del aire

Proyecto final de Modelación y Simulación 2026 (Opción 2: simulación de un fenómeno dinámico).

Se simula la caída vertical de un cuerpo bajo gravedad y resistencia del aire, resolviendo la EDO de movimiento con Euler explícito y Runge-Kutta de orden 4 implementados a mano, y comparando contra las soluciones analíticas.

## Modelo

Con el eje positivo hacia arriba y estado `(y, v)`:

```
dy/dt = v
dv/dt = -g + F_d(v) / m
```

| Modelo | Fuerza de arrastre | Velocidad terminal |
|---|---|---|
| Vacío | `0` | no existe |
| Lineal | `-b v` | `m g / b` |
| Cuadrático | `-½ ρ Cd A v abs(v)` | `sqrt(2 m g / (ρ Cd A))` |

## Instalación

```
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Estructura

- `freefall/models.py`: cuerpos y modelos de arrastre.
- `freefall/analytic.py`: soluciones cerradas `y(t)`, `v(t)`.
- `freefall/solvers.py`: pasos de Euler y RK4, integración con detección de impacto contra el suelo.
