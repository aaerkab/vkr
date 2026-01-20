from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    status: str | None = "new"


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class ItemOut(ItemBase):
    id: int

    class Config:
        orm_mode = True
