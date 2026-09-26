from .config import GEMINI_NUTRITION_MODEL
from .gemini_client import generate_text


def demo_nutrition_tip(
    goal: str
) -> str:

    return f"""
DEMO MODE

For your goal of "{goal}", focus on:

- Regular balanced meals
- Enough water
- Fruits and vegetables
- Protein-containing foods
- Good sleep
- Proper recovery

Avoid extreme diets and unnecessary
supplements.
"""


def generate_nutrition_tip(
    goal: str,
    age: int
) -> str:

    prompt = f"""
You are FitBuddy.

Give one short practical nutrition
or recovery tip.

Goal:
{goal}

Age:
{age}

Rules:

- Give general wellness information.
- Do not prescribe a medical diet.
- Do not give restrictive calorie targets.
- Do not recommend unsafe supplements.
- Do not promote starvation or fasting.
- Do not make body-image judgments.
- Mention balanced food, hydration,
  sleep or recovery when useful.
- Keep the answer below 100 words.

Return only the tip.
"""

    try:

        return generate_text(
            prompt,
            GEMINI_NUTRITION_MODEL
        )

    except Exception:

        return demo_nutrition_tip(
            goal
        )