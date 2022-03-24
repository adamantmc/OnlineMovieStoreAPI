from pydantic import BaseModel, Field, validator
import uuid


class UserInfo(BaseModel):
    username: str = Field(None, min_length=4)
    email: str = Field(None, regex='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')


class CreateUser(UserInfo):
    password: str = Field(None, min_length=8, max_length=32)
    password_verification: str = Field(None, min_length=8, max_length=32)

    @validator("password")
    def password_validation(cls, v: str):
        special_chars = set([c for c in "!@#$%^&*()-_=+~<>?:{}[]"])

        if v.isupper() or v.islower():
            raise ValueError("Password must contain both lower case and upper case characters")
        if not any([c in special_chars for c in v]):
            raise ValueError("Password must contain at least one special character")

        return v

    @validator("password_verification")
    def passwords_match(cls, v: str, values: dict, **kwargs):
        if v != values.get("password"):
            raise ValueError("The two passwords must match")

        return v


class User(UserInfo):
    uuid: uuid.UUID

    class Config:
        orm_mode = True


class UserDetails(User):
    id: int


class Login(BaseModel):
    email: str = Field(None, regex='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
    password: str = Field(None, min_length=8, max_length=32)


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
