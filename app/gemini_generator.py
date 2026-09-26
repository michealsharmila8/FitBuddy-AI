from .config import GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text


def demo_workout(
    goal: str,
    intensity: str
) -> str:

    return f"""
DEMO MODE

Gemini API key is not configured.

FITBUDDY 7-DAY WELLNESS PLAN

Goal:
{goal}

Intensity:
{intensity.title()}


DAY 1 - FULL BODY

Warm-up:
5 to 10 minutes of easy movement.

Main activity:
- Squats: 2 sets of 8 to 12
- Wall push-ups: 2 sets of 8 to 12
- Glute bridges: 2 sets of 10 to 12

Cooldown:
Gentle stretching for 5 minutes.


DAY 2 - CARDIO AND MOBILITY

- Comfortable walking or cycling: 15 to 25 minutes
- Gentle shoulder movements
- Gentle hip movements
- Gentle ankle movements


DAY 3 - RECOVERY

- Easy walking
- Gentle stretching
- Relaxation and recovery


DAY 4 - FULL BODY

- Step-ups: 2 sets of 8 each side
- Light resistance-band rows: 2 sets of 8 to 12
- Bird-dog: 2 sets of 6 each side


DAY 5 - CARDIO AND CORE

- Comfortable low-impact cardio: 15 to 25 minutes
- Gentle core exercises


DAY 6 - LIGHT STRENGTH

Repeat a few comfortable exercises
from the previous days.

Focus on good form instead of intensity.


DAY 7 - REST / ACTIVE RECOVERY

- Easy walking
- Gentle stretching
- Relaxing movement


SAFETY

Stop if you experience pain, dizziness,
or unusual symptoms.
"""


def generate_workout_gemini(
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
) -> str:

    prompt = f"""
You are FitBuddy, a cautious general wellness
planning assistant.

Create a simple 7-day fitness and wellness plan.

USER INFORMATION

Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}


REQUIREMENTS

1. Create Day 1 through Day 7.

2. Include rest or recovery days.

3. Active days should include:
   - Warm-up
   - Main activity
   - Sets/repetitions or duration when appropriate
   - Cooldown or recovery

4. Keep the plan beginner-friendly.

5. Do not prescribe medical treatment.

6. Do not recommend:
   - dangerous challenges
   - extreme exercise
   - fasting
   - starvation
   - restrictive calorie targets
   - unsafe supplement use

7. Do not make body-image judgments.

8. For weight-management goals,
   focus on sustainable activity
   and healthy habits.

9. Include a short safety note.

10. Use simple English.

11. Use clear headings.

Return only the fitness plan.
"""

    try:

        result = generate_text(
            prompt,
            GEMINI_WORKOUT_MODEL
        )

        return result

    except Exception:

        return demo_workout(
            goal,
            intensity
        )