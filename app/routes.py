from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db

from .gemini_generator import (
    generate_workout_gemini
)

from .nutrition_generator import (
    generate_nutrition_tip
)

from .models import User
from .models import Plan

from .schemas import UserInput
from .schemas import FeedbackRequest

from .plan_updater import (
    update_workout_plan
)


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)

router = APIRouter()


def save_user(
    db: Session,
    data: UserInput
):

    user = db.scalar(
        select(User).where(
            User.user_id == data.user_id
        )
    )

    if user:

        user.name = data.name
        user.age = data.age
        user.weight = data.weight
        user.goal = data.goal
        user.intensity = data.intensity

    else:

        user = User(
            user_id=data.user_id,
            name=data.name,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity
        )

        db.add(user)

    db.commit()

    db.refresh(user)

    return user


def save_plan(
    db: Session,
    data: UserInput,
    workout_plan: str,
    nutrition_tip: str
):

    plan = Plan(
        user_id=data.user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(plan)

    db.commit()

    db.refresh(plan)

    return plan


def get_latest_plan(
    db: Session,
    user_id: str
):

    return db.scalar(
        select(Plan)
        .where(
            Plan.user_id == user_id
        )
        .order_by(
            Plan.id.desc()
        )
    )


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "FitBuddy"
        }
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(
    request: Request,

    user_id: str = Form(...),

    name: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)
):

    data = UserInput(
        user_id=user_id,
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    save_user(
        db,
        data
    )

    workout_plan = generate_workout_gemini(
        name=data.name,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity
    )

    nutrition_tip = generate_nutrition_tip(
        goal=data.goal,
        age=data.age
    )

    plan = save_plan(
        db,
        data,
        workout_plan,
        nutrition_tip
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "title": "Your FitBuddy Plan",
            "user": data,
            "plan": plan,
            "message": "Your 7-day plan was created successfully."
        }
    )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    feedback_data = FeedbackRequest(
        user_id=user_id,
        feedback=feedback
    )

    user = db.scalar(
        select(User).where(
            User.user_id == feedback_data.user_id
        )
    )

    plan = get_latest_plan(
        db,
        feedback_data.user_id
    )

    if not user or not plan:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "title": "Not Found",
                "message": "User or plan was not found."
            },
            status_code=404
        )

    current_plan = (
        plan.updated_plan
        or plan.original_plan
    )

    revised_plan = update_workout_plan(
        original_plan=current_plan,
        feedback=feedback_data.feedback,
        goal=user.goal,
        intensity=user.intensity
    )

    plan.updated_plan = revised_plan

    plan.feedback = feedback_data.feedback

    plan.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(plan)

    updated_user = UserInput(
        user_id=user.user_id,
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "title": "Updated FitBuddy Plan",
            "user": updated_user,
            "plan": plan,
            "message": "Your plan was updated using your feedback."
        }
    )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(
    request: Request,
    db: Session = Depends(get_db)
):

    users = db.scalars(
        select(User)
        .order_by(User.id.desc())
    ).all()

    plans = db.scalars(
        select(Plan)
        .order_by(Plan.id.desc())
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "title": "All Users",
            "users": users,
            "plans": plans
        }
    )


# -----------------------------
# API ROUTES
# -----------------------------


@router.get("/api/health")
def health():

    return {
        "status": "ok",
        "application": "FitBuddy"
    }


@router.get("/api/users")
def api_users(
    db: Session = Depends(get_db)
):

    users = db.scalars(
        select(User)
        .order_by(User.id.desc())
    ).all()

    return [
        {
            "user_id": user.user_id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "created_at": user.created_at.isoformat()
        }

        for user in users
    ]


@router.post("/api/generate")
def api_generate(
    data: UserInput,
    db: Session = Depends(get_db)
):

    save_user(
        db,
        data
    )

    workout_plan = generate_workout_gemini(
        name=data.name,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity
    )

    nutrition_tip = generate_nutrition_tip(
        goal=data.goal,
        age=data.age
    )

    plan = save_plan(
        db,
        data,
        workout_plan,
        nutrition_tip
    )

    return {
        "success": True,
        "user_id": data.user_id,
        "plan_id": plan.id,
        "workout_plan": workout_plan,
        "nutrition_tip": nutrition_tip
    }


@router.post("/api/feedback")
def api_feedback(
    data: FeedbackRequest,
    db: Session = Depends(get_db)
):

    user = db.scalar(
        select(User).where(
            User.user_id == data.user_id
        )
    )

    plan = get_latest_plan(
        db,
        data.user_id
    )

    if not user or not plan:

        return {
            "success": False,
            "error": "User or plan not found."
        }

    current_plan = (
        plan.updated_plan
        or plan.original_plan
    )

    revised_plan = update_workout_plan(
        original_plan=current_plan,
        feedback=data.feedback,
        goal=user.goal,
        intensity=user.intensity
    )

    plan.updated_plan = revised_plan

    plan.feedback = data.feedback

    plan.updated_at = datetime.utcnow()

    db.commit()

    return {
        "success": True,
        "user_id": data.user_id,
        "updated_plan": revised_plan
    }