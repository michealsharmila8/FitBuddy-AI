from .config import GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str
) -> str:

    prompt = f"""
You are FitBuddy.

The user wants to improve an existing
general wellness plan.

ORIGINAL PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


GOAL:

{goal}


INTENSITY:

{intensity}


TASK:

Create a revised 7-day wellness plan.

Requirements:

- Apply reasonable user feedback.
- Keep Day 1 through Day 7.
- Include recovery days.
- Keep the plan beginner-friendly.
- Include warm-up and cooldown when appropriate.
- Do not provide medical treatment.
- Do not recommend dangerous activities.
- Do not recommend extreme exercise.
- Do not recommend fasting or starvation.
- Do not provide restrictive calorie targets.
- Do not recommend unsafe supplements.
- Do not make body-image judgments.
- Include a short safety note.
- Use simple English.

Return only the revised plan.
"""

    try:

        return generate_text(
            prompt,
            GEMINI_WORKOUT_MODEL
        )

    except Exception:

        return f"""
UPDATED DEMO PLAN

The Gemini API could not be reached.

Your feedback was:

{feedback}


Please continue with a comfortable
7-day wellness routine and adjust
activities according to your comfort.
"""