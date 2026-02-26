from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field(default_factory=datetime.now)
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str = Field(default=" ", max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def check_valid(self) -> None:
        if self.contact_id[0] != "A" or self.contact_id[1] != "C":
            raise Exception("Contact ID must start with 'AC' (Alien Contact)")
        if self.contact_type == "telepathic" and self.witness_count < 3:
            raise Exception("Telepathic contact requires at least 3 witnesses")
        if self.is_verified is False:
            raise Exception("Physical contact reports must be verified")
        if self.signal_strength > 7 and self.message_received == " ":
            raise Exception("Strong signals (> 7.0) should include"
                            "received messages")

    def get_info(self) -> str:
        return (f"Station {self.contact_id}\n"
                f"Nom: {self.contact_type}\n"
                f"Crew: {self.location} people\n"
                f"Power: {self.signal_strength}%\n"
                f"Oxygen: {self.duration_minutes}%\n"
                f"Status operationel: {self.witness_count}"
                f"Message: {self.message_received}")


def main():
    print("Alien Contact Log Validation")
    print("========================================")
    print("Valid contact report:")
    data = {
        "contact_id": "AC-01",
        "location": "Alpha One",
        "signal_strength": 8.5,
        "contact_type": "physical",
        "duration_minutes": 60,
        "witness_count": 15,
        "is_verified": True,
        "message_received": "Greetings from Zeta Reticuli"}
    try:
        alien = AlienContact(**data)
        print("✅ Succès !")
        alien.check_valid()
        print(alien.get_info())
    except Exception as e:
        print(f"❌ Erreur : {e}")
    print("========================================")
    print("Expected validation error:")
    data2 = {
        "contact_id": "AC-01",
        "location": "Alpha One",
        "signal_strength": 5,
        "contact_type": "telepathic",
        "duration_minutes": 60,
        "witness_count": 1}
    try:
        alien = AlienContact(**data2)
        print("✅ Succès !")
        alien.check_valid()
    except Exception as e:
        print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    main()
