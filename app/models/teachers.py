from pydantic import BaseModel, Field, EmailStr

class Teacher(BaseModel):
    name: str = Field(min_length=1, max_length=16)
    email: EmailStr
    password: str


class TeacherLogin(BaseModel):
    email: EmailStr
    password: str
