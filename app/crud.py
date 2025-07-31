from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import RequestLog


async def log_request(
    session: AsyncSession, operation: str, inp: str, res: str
) -> RequestLog:
    entry = RequestLog(operation=operation, input_value=inp, result=res)
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


async def list_requests(session: AsyncSession):
    stmt = select(RequestLog).order_by(RequestLog.created_at.desc())
    return (await session.execute(stmt)).scalars().all()
