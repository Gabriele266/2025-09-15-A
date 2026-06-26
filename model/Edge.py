from dataclasses import dataclass

@dataclass
class Edge:
    driver_id_a: int
    driver_id_b: int
    weight: int