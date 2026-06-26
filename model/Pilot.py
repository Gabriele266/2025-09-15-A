from dataclasses import dataclass

@dataclass
class Pilot:
    id: int
    name: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.name}, id {self.id}"