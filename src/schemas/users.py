from pydantic import BaseModel, UUID4


class TokenData(BaseModel):
    email: str | None = None


class Token(BaseModel):
    token: str | None = None


class UserBase(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None

    class ConfigDict:
        from_attributes = True


class UserCreate(UserBase):
    email: str
    password: str


class User(UserBase):
    id: UUID4
