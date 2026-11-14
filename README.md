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
- `freefall/scenarios.py`: escenarios del paracaidista y de las pelotas, y sus métricas.
- `freefall/convergence.py`: error contra la solución analítica y orden observado de cada método.
- `freefall/plots.py`: figuras estáticas.
- `freefall/report.py`: formato de tablas.
- `freefall/__main__.py`: interfaz de línea de comandos.

## Uso

```
.venv/bin/python -m freefall paracaidista [--dt 0.01] [--metodo rk4|euler] [--altura 4000] [--salida results]
.venv/bin/python -m freefall pelotas      [--dt 0.01] [--metodo rk4|euler] [--altura 56]   [--salida results]
.venv/bin/python -m freefall convergencia [--t-final 20] [--dt-grande 2] [--salida results]
```

Cada comando imprime una tabla de métricas y guarda las figuras en `results/`.

## Análisis de convergencia

Se integra el salto del paracaidista en `[0, t_final]` sin detener la simulación en el suelo, para aislar el error del integrador del error de la detección de impacto. Para cada `dt` entre 1 s y 1e-4 s se mide el error máximo en `y` y en `v` contra la solución analítica. El orden observado se obtiene con un ajuste lineal de `log(error)` contra `log(dt)`, descartando los puntos por debajo de 1e-9, donde domina el error de redondeo.
