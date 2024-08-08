from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

class User (BaseModel):
    email: EmailStr

class updateUserEmail (BaseModel):
    new_email: EmailStr

class updateUserPassword (BaseModel):
    new_password: str


class responseUserModel (BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

# ==================================

class Token (BaseModel):
    access_token: str
    token_type: str

class TokenData (BaseModel):
    user_name_token: str

# ==================================

class basePost (BaseModel):
    title: str
    content: str
    published: bool = True

class updatedPost (basePost):
    pass # nothing to add

class createdPost (basePost):
    pass # nothing to add

class responsePostModel (BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner: User

    class Config:
        from_attributes = True

class responsePostModel_VoteExtra (BaseModel):
    Post: responsePostModel
    vote: int

    class Config:
        from_attributes = True

# ===============================
class Votes (BaseModel):
    post_id: int
    dir : int 