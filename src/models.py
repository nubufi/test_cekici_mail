from pydantic import BaseModel


class Context(BaseModel):
    yibf: int
    average_R: list
    R: list
    bore_axises: list
    building_element: list
    concrete_age: int
    hammer_angle: list
    date: str
    building_owner: str
    concrete_volume: float
