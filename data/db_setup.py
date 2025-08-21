from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base
import config

assert config.DATABASE_URL is not None, "DATABASE_URL must be set in the .env file"

engine = create_async_engine(config.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)