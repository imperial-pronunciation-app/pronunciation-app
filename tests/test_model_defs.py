# from sqlalchemy.ext.asyncio import create_async_engine

# from app.models.base_model import Base


# async def test_create_database() -> None:
#     engine = create_async_engine("sqlite+aiosqlite://", connect_args={"check_same_thread": False})
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     assert True
