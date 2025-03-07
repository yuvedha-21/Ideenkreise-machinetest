from fastapi import  FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()



@app.get("/")

class Post(BaseModel):
    title:str
    content:str

async def root():
    return {"message": "Hello World"}

@app.post("/enterMessage")
async def enterMessage():
    return {"data":"Hi"}

@app.post("/createPost")
async def createPost(post:Post): 
    print(post)
    return {"data":post.title} 