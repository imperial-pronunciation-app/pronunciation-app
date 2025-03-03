from fastapi import APIRouter, Depends, HTTPException

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.exercise import ExerciseResponse
from app.services.exercise import ExerciseService
from app.users import current_active_user


router = APIRouter()


@router.get("/api/v1/exercises/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: int, uow: UnitOfWork = Depends(get_unit_of_work), user: User = Depends(current_active_user)) -> ExerciseResponse:
    exercise = uow.exercises.find_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    return ExerciseService(uow).to_response(exercise, user)
