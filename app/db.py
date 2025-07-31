from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./requests.db"


engine = create_async_engine(DATABASE_URL, echo=False, future=True)


SessionLocal = async_sessionmaker(engine, expire_on_commit=False)



async def get_session() -> AsyncSession:
    """
    Yield a SQLAlchemy AsyncSession, și FastAPI se ocupă de cleanup
    după ce handler‐ul s‐a terminat.
    """
    async with SessionLocal() as session:
        yield session
