from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase): #The "createPost" class will automatically inherit the "PostBase" proprties and populate every field
    pass

#Return response (this only returns listed fields)
class ReturnedFields(BaseModel):
    title: str
    content: str
    published: bool
    class Config:
        orm_mode = True