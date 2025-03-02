from pydantic import BaseModel

# Models for testing purposes
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True