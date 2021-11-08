
class Quad:

    def __init__(
        self, 
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        w: float = 0.0
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    def __str__(self) -> str:
        return f"x: {self.x} y: {self.y} z: {self.z} w: {self.w}"

    def Sql(self) -> str:
        return f"{self.x}, {self.y}, {self.z}, {self.w}"

    def SqlValues(prefix="") -> str:
        return f"{prefix}_x, {prefix}_y, {prefix}_z, {prefix}_w"

    def tableCreationSql(prefix = "") -> str:
        return f"{prefix}_x FLOAT(24), {prefix}_y FLOAT(24), {prefix}_z FLOAT(24), {prefix}_w FLOAT(24)"