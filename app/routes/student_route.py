from fastapi import APIRouter, Body, HTTPException, Path, Depends
from config.database import db
from auth.auth_bearer import jwtBearer
from auth.jwt_handler import signJWT
from bson import ObjectId
from pydantic import EmailStr
import bcrypt


student = APIRouter()

student_collection = db["student_collection"]


# Get all student from the database
@student.get("/student", tags=["Admin"])
async def get_students():
    students = []
    for student in student_collection.find():
        student_id = str(student["_id"])
        name= student["name"]
        email = student["email"]
        password = student["password"]
        
        students.append({
            "student_id": student_id,
            "name": name,
            "email": email,
            "password": password
        })
    return students



@student.post("/student/insert", tags=["Admin"])
async def student_signup(name: str, email: EmailStr, password: str):
    # Check if email already exists in the database
    existing_student = student_collection.find_one({"email": email})
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
     
    student = {
        "name": name,
        "email": email,
        "password": hashed_password
    }

    # Insert student into MongoDB collection
    student_collection.insert_one(student)
    
    return signJWT(email)

