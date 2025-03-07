from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

users_db = {
    "admin": {
        "username": "admin",
        "password": "password123"
    }
}

todos_db = [
    {"id": 1, "task": "A", "status": "completed"},
    {"id": 2, "task": "B", "status": "in-progress"},
    {"id": 3, "task": "C", "status": "pending"},
    {"id": 4, "task": "D", "status": "pending"},
    {"id": 5, "task": "E", "status": "pending"}
]

class User(BaseModel):
    username: str
    password: str

class Todo(BaseModel):
    id: int
    task: str
    status: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Func to create jwt token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Func to authenticate user
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user:
        return False
    if user["password"] != password:
        return False
    return user

# Func to get cur user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
        
    return user

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/todos", response_model=List[Todo])
async def get_todos(current_user: User = Depends(get_current_user)):
    return todos_db


@app.get("/")
async def root():
    return {"message": "test"}
