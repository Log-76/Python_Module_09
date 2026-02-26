from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field(default_factory=datetime.now)
    duration_days: int = Field(ge=1, le=3650)
    crew: CrewMember = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_mission(self) -> None:
        if self.mission_id[0] != "M":
            raise Exception("Mission ID must start with 'M'")
        if self.crew != "Commander" and self.crew != "Captain":
            raise Exception("Must have at least one Commander or Captain")
        if self.duration_days > 365 and self.crew.years_experience < 5:
            raise Exception("Long missions (> 365 days) need 50%"
                            " experienced crew (5+ years)")
        if self.crew.is_active is False:
            raise Exception("All crew members must be active")


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================")
    print("Valid mission created:")
    member = []
    member.append(CrewMember("sc1", "Sarah Connor", "commander", 25,
                             "Mission Command", 6))
    member.append(CrewMember("js1", "John Smith", "lieutenant", 40,
                             "Navigation", 6))
    member.append(CrewMember("aj1", "Alice Johnson", "officer", 20,
                             "Engineering", 6))
    data = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "duration_days": 900,
        "crew": 60,
        "budget_millions": 2500.0}
    try:
        mission = SpaceMission(**data)
        print("✅ Succès !")
        mission.check_mission()
    except Exception as e:
        print(f"❌ Erreur : {e}")
