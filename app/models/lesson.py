from app.models.base.lesson_base import LessonBase


class Lesson(LessonBase):
    __mapper_args__ = {
        "polymorphic_identity": "recap_lesson",
    }