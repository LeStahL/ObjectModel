from glm import vec3
from typing import Self
from PyQt6.QtGui import QColor

class ColorMap:
    @staticmethod
    def cmap(t: float) -> vec3:
        c0: vec3 = vec3(0.646961, 0.597154, 0.908626)
        c1: vec3 = vec3(-0.170691, 1.38043, -0.227154)
        c2: vec3 = vec3(-5.9448, 1.16471, 12.1713)
        c3: vec3 = vec3(28.245, -7.06169, -73.8803)
        c4: vec3 = vec3(-31.6389, 2.92034, 158.794)
        c5: vec3 = vec3(3.38824, 3.98187, -144.598)
        c6: vec3 = vec3(6.14323, -2.36647, 47.7489)
            
        return c0+t*(c1+t*(c2+t*(c3+t*(c4+t*(c5+t*c6)))))
    
    def __init__(self: Self, colorCount: int = 8) -> None:
        self._colorCount = colorCount

        self.colors = list(map(
            lambda colorIndex: QColor.fromRgbF(*ColorMap.cmap(float(colorIndex) / float(colorCount))),
            range(self._colorCount + 1),
        ))
