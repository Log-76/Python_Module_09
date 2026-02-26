from pydantic import BaseModel, Field
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=30)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime = Field(default_factory=datetime.now)
    is_operational: bool = True
    notes: str = Field(default="", max_length=200)

    def get_info(self) -> str:
        return (f"Station {self.station_id}\n"
                f"Nom: {self.name}\n"
                f"Crew: {self.crew_size} people\n"
                f"Power: {self.power_level}%\n"
                f"Oxygen: {self.oxygen_level}%\n"
                f"Status operationel: {self.is_operational}")


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    data = {
        "station_id": "ISS-01",
        "name": "Alpha One",
        "crew_size": 5,
        "power_level": 95.5,
        "oxygen_level": 98.0}
    try:
        station = SpaceStation(**data)
        print("✅ Succès !")
        print(station.get_info())
    except Exception as e:
        print(f"❌ Erreur : {e}")
    print("========================================")
    data2 = {
        "station_id": "ISS-01",
        "name": "Alpha One",
        "crew_size": 21,
        "power_level": 95.5,
        "oxygen_level": 98.0,
    }

    try:
        station = SpaceStation(**data2)
        print("✅ Succès !")
        print(station.get_info())
    except Exception as e:
        print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    main()
