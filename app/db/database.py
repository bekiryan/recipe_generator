from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """
    Get the database session

    :return: AsyncSession: The database session
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

