from fastapi import APIRouter, Body, HTTPException, Path, Depends
from config.database import db
from models.teachers import TeacherLogin
from auth.jwt_handler import signJWT
from pydantic import EmailStr
import bcrypt

teacher = APIRouter()

teacher_collection = db ["teacher_collection"]

# Get all teacher from the database
@teacher.get("/teacher", tags=["Admin"])
async def get_teacher():
    teacher_list = []
    for teacher in teacher_collection.find():
        teacher_id = str(teacher["_id"])
        name = teacher["name"]
        email = teacher["email"]
        password = teacher["password"]
        
        teacher_list.append({
            "teacher_id": teacher_id,
            "name": name,
            "email": email,
            "password": password
        })
    return teacher_list


# Create a new teacher member
@teacher.post("/teacher/insert", tags=["Admin"])
async def teacher_signup(name: str, email: EmailStr, password: str):
    # Check if email already exists in the database
    existing_teacher = teacher_collection.find_one({"email": email})
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
     
    teacher_data = {
        "name": name,
        "email": email,
        "password": hashed_password
    }

    # Insert teacher member into MongoDB collection
    teacher_collection.insert_one(teacher_data)
    
    return signJWT(email)


# Teacher Login
@teacher.post("/teacher/login", tags=["Teacher_authentication"])
async def teacher_login(email: EmailStr, password: str):
    try:
        # Search for teacher in MongoDB collection
        teacher = teacher_collection.find_one({"email": email})
        if not teacher:
            raise HTTPException(status_code=401, detail="Incorrect email")
        
        # Retrieve the hashed password from the database
        stored_hashed_password = teacher["password"]
        
        # Verify the password
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Incorrect password")

        # Generate JWT token
        jwt_token = signJWT(email)
        
        # Return success message along with JWT token
        return {"message": "Login successful", "token": jwt_token}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to authenticate user")


'''
@teacher.post("/teacher/loginn", tags=["Teacher_authentication"])
async def teacher_login(teacher_login: TeacherLogin = Body(default=None)):
    # Search for user in MongoDB collection
    teacher = teacher_collection.find_one({"email": teacher_login.email})
    if not teacher:
        raise HTTPException(status_code=401, detail="Incorrect email")

    # Verify the password
    if teacher and bcrypt.checkpw(teacher_login.password.encode('utf-8'), teacher['password'].encode('utf-8')):
        # Generate JWT token
        jwt_token = signJWT(teacher_login.email)
        
        # Return success message along with JWT token
        return {"message": "Login successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=500, detail="Incorrect Password::Failed to authenticate")
'''
