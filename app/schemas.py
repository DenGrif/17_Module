from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    age: int | None = None


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel):
    title: str | None = None
    content: str | None = None
    priority: int | None = None
