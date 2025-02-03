from sqlmodel import Field, SQLModel


class IdModel(SQLModel):
    """SQL model class with an id field.
    """

    id: int = Field(default=None, primary_key=True)
