import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

G = 9.81
RHO_AIR = 1.225
MU_AIR = 1.81e-5


@dataclass(frozen=True)
class Body:
    name: str
    mass: float
    drag_coefficient: float
    area: float
    length: float

    @classmethod
    def sphere(cls, name, mass, radius, drag_coefficient=0.47):
        return cls(name, mass, drag_coefficient, math.pi * radius**2, 2 * radius)

    def reynolds(self, speed, rho=RHO_AIR, mu=MU_AIR):
        return rho * abs(speed) * self.length / mu


class DragModel(ABC):
    name = ""

    def __init__(self, mass, g=G):
        self.mass = mass
        self.g = g

    @abstractmethod
    def drag_acceleration(self, v):
        ...

    @abstractmethod
    def terminal_velocity(self):
        ...

    def acceleration(self, v):
        return -self.g + self.drag_acceleration(v)


class Vacuum(DragModel):
    name = "Vacío"

    def drag_acceleration(self, v):
        return 0.0 * v

    def terminal_velocity(self):
        return math.inf


class LinearDrag(DragModel):
    name = "Lineal"

    def __init__(self, mass, b, g=G):
        super().__init__(mass, g)
        self.b = b

    @classmethod
    def from_terminal_velocity(cls, mass, vt, g=G):
        return cls(mass, mass * g / vt, g)

    def drag_acceleration(self, v):
        return -(self.b / self.mass) * v

    def terminal_velocity(self):
        return self.mass * self.g / self.b


class QuadraticDrag(DragModel):
    name = "Cuadrático"

    def __init__(self, mass, k, g=G):
        super().__init__(mass, g)
        self.k = k

    @classmethod
    def from_body(cls, body, rho=RHO_AIR, g=G):
        return cls(body.mass, 0.5 * rho * body.drag_coefficient * body.area, g)

    def drag_acceleration(self, v):
        return -(self.k / self.mass) * v * abs(v)

    def terminal_velocity(self):
        return math.sqrt(self.mass * self.g / self.k)
