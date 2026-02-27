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

    def get_info(self) -> str:
        return f"- {self.name} ({self.rank}) - {self.specialization}"


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field(default_factory=datetime.now)
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_mission(self) -> None:
        if self.mission_id[0] != "M":
            raise Exception("Mission ID must start with 'M'")
        for i in self.crew:
            if i.rank == Rank.commander or i.rank == Rank.captain:
                break
        if i.rank != Rank.commander and i.rank != Rank.captain:
            raise Exception("Must have at least one Commander or Captain")
        if self.duration_days > 365 and i.years_experience < 5:
            raise Exception("Long missions (> 365 days) need 50%"
                            " experienced crew (5+ years)")
        for i in self.crew:
            if i.is_active is False:
                raise Exception("All crew members must be active")
        return self

    def get_info(self) -> str:
        return (f"Mission: {self.mission_name}\n"
                f"ID:  {self.mission_id}\n"
                f"Destination: {self.destination} \n"
                f"Duration: {self.duration_days}\n"
                f"Budget: {self.budget_millions} M\n"
                f"Crew size: {len(self.crew)}")


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================")
    print("Valid mission created:")
    Sarah = {"member_id": "sc1_01",
             "name": "Sarah Connor",
             "rank": "commander",
             "age": 25,
             "specialization": "Mission Command",
             "years_experience": 6}
    John = {"member_id": "js1",
            "name": "John Smith",
            "rank": "lieutenant",
            "age": 40,
            "specialization": "Navigation",
            "years_experience": 3}
    Alice = {"member_id": "aj1",
             "name": "Alice Johnson",
             "rank": "officer",
             "age": 20,
             "specialization": "Engineering",
             "years_experience": 2}
    member = []
    member.append(CrewMember(**Sarah))
    member.append(CrewMember(**John))
    member.append(CrewMember(**Alice))
    data = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "duration_days": 900,
        "crew": member,
        "budget_millions": 2500.0}
    try:
        mission = SpaceMission(**data)
        print("✅ Succès !")
        mission.check_mission()
        print(mission.get_info())
        print("Crew members:")
        for crew in mission.crew:
            print(crew.get_info())
    except Exception as e:
        print(f"❌ Erreur : {e}")

    member2 = []
    member2.append(CrewMember(**Alice))
    member2.append(CrewMember(**John))
    data = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "duration_days": 900,
        "crew": member2,
        "budget_millions": 2500.0}
    print("========================================")
    print("Expected validation error:")
    try:
        mission = SpaceMission(**data)
        print("✅ Succès !")
        mission.check_mission()
        print(mission.get_info())
        print("Crew members:")
        for crew in mission.crew:
            print(crew.get_info())
    except Exception as e:
        print(f"❌ Erreur : {e}")


main()
