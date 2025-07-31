from pydantic import BaseModel, Field, PositiveInt


class PowIn(BaseModel):
    base: float
    exp: float = Field(..., alias="exponent")


class FibIn(BaseModel):
    n: PositiveInt


class FactIn(BaseModel):
    n: PositiveInt


class ResultOut(BaseModel):
    result: str
