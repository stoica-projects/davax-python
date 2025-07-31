from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, utils, crud
from .db import get_session
from .auth import verify_token

router = APIRouter(prefix="/math", tags=["math"])


@router.post("/pow", response_model=schemas.ResultOut, status_code=status.HTTP_200_OK,
             dependencies=[Depends(verify_token)])
async def power(
    payload: schemas.PowIn, session: AsyncSession = Depends(get_session)
):
    res = utils.pow_op(payload.base, payload.exp)
    await crud.log_request(session, "pow", f"{payload.base}^{payload.exp}", str(res))
    return {"result": str(res)}


@router.post("/fib", response_model=schemas.ResultOut, dependencies=[Depends(verify_token)])
async def fibonacci(
    payload: schemas.FibIn, session: AsyncSession = Depends(get_session)
):
    res = utils.fib(payload.n)
    await crud.log_request(session, "fib", str(payload.n), str(res))
    return {"result": str(res)}


@router.post("/fact", response_model=schemas.ResultOut, dependencies=[Depends(verify_token)])
async def factorial(
    payload: schemas.FactIn, session: AsyncSession = Depends(get_session)
):
    res = utils.fact(payload.n)
    await crud.log_request(session, "fact", str(payload.n), str(res))
    return {"result": str(res)}
