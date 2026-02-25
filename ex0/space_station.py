from pydantic import BaseModel, Field


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(max_length=1, min_length=30)
    crew_size: int = Field(min_digits=1, max_digits=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    # last_maintenance:
    is_operational: bool = True
    notes: str = Field(max_length=200)
