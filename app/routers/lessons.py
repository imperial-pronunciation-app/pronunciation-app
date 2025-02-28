from fastapi import APIRouter, Depends, HTTPException

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.lesson import LessonResponse
from app.services.lesson import LessonService
from app.users import current_active_user


router = APIRouter()


@router.get("/api/v1/lessons/{lesson_id}", response_model=LessonResponse)
async def get_exercise(lesson_id: int, uow: UnitOfWork = Depends(get_unit_of_work), user: User = Depends(current_active_user)) -> LessonResponse:
    lesson = uow.lessons.find_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return LessonService(uow).to_response(lesson, user)
