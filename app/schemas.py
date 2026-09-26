from pydantic import BaseModel, Field, field_validator


class UserInput(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=50
    )

    name: str = Field(
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=0,
        le=500
    )

    goal: str = Field(
        min_length=2,
        max_length=100
    )

    intensity: str = Field(
        min_length=2,
        max_length=20
    )

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value):

        value = value.strip().lower()

        allowed = {
            "low",
            "medium",
            "high"
        }

        if value not in allowed:
            raise ValueError(
                "Intensity must be Low, Medium, or High."
            )

        return value


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=50
    )

    feedback: str = Field(
        min_length=3,
        max_length=1000
    )