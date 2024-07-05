from fastapi import APIRouter, Body, HTTPException, Path, Depends
from schema.module_schema import module_list
from config.database import db
from auth.auth_bearer import jwtBearer
from bson import ObjectId
from typing import List

module = APIRouter()

student_collection = db["student_collection"]
module_collection = db["module_collection"]

# Get all modules from the database
@module.get("/module", dependencies=[Depends(jwtBearer())], tags=["module"])
async def get_module():
    modules = module_list(module_collection.find())
    return modules


# Get all students by module ID
@module.get("/modules/{module_id}/students", dependencies=[Depends(jwtBearer())], tags=["module"])
async def get_students_by_module_id(module_id: str):
    # Check if module exists
    module_doc = module_collection.find_one({"_id": ObjectId(module_id)})
    if not module_doc:
        raise HTTPException(status_code=404, detail="module not found")

    # Retrieve students for the given module ID
    students = module_doc.get("student", [])
    student_list = []
    for student in students:
        student_details = {
            "student_id": str(student["_id"]),
            "name": student["name"],
            "email": student["email"]
        }
        student_list.append(student_details)
    
    return student_list


# Create a new module with student IDs
@module.post("/modules/", tags=["Admin"])
async def create_module(module_name: str, students: List[str]):
    try:
        # Get student details for the provided student IDs
        student_details = []
        for student_id in students:
            student = student_collection.find_one(
                {"_id": ObjectId(student_id)},
                {"student_id": 1, "name": 1, "email": 1}  # Include student_id, name, and email
            )
            if student:
                student_details.append(student)
            else:
                raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

        # Create a new module
        new_module = {
            "module_name": module_name,
            "student": student_details
        }
        module_collection.insert_one(new_module)
        # module_id = str(inserted_module.inserted_id)

        return {"message": "module created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create module")



#  Add students to the module
@module.post("/modules/{module_id}/students/{student_id}", dependencies=[Depends(jwtBearer())], tags=["module"])
async def add_student_to_module(
    module_id: str = Path(..., title="The ID of the module"),
    student_id: str = Path(..., title="The ID of the student")
):
    # Check if module exists
    module_doc = module_collection.find_one({"_id": ObjectId(module_id)})
    if not module_doc:
        raise HTTPException(status_code=404, detail="module not found")

    # Check if student exists
    student_doc = student_collection.find_one({"_id": ObjectId(student_id)})
    if not student_doc:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if student already in module
    if student_id in module_doc["student"]:
        raise HTTPException(status_code=400, detail="Student already in module")

    # Retrieve student details
    student_details = {
        "_id": ObjectId(student_id),
        "name": student_doc["name"],
        "email": student_doc["email"]
    }
    # Update the module document to add the student ID
    result = module_collection.update_one(
        {"_id": ObjectId(module_id)},
        {"$addToSet": {"student": student_details}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Student already in module")

    return {"message": "Student added to module successfully"}



# Remove a student from the module
@module.delete("/modules/{module_id}/students/{student_id}", dependencies=[Depends(jwtBearer())], tags=["module"])
async def remove_student_from_module(
    module_id: str = Path(..., title="The ID of the module"),
    student_id: str = Path(..., title="The ID of the student")
):
    # Check if module exists
    module_doc = module_collection.find_one({"_id": ObjectId(module_id)})
    if not module_doc:
        raise HTTPException(status_code=404, detail="module not found")

    # Check if student exists
    student_doc = student_collection.find_one({"_id": ObjectId(student_id)})
    if not student_doc:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if student is in the module
    if student_id not in [str(student['_id']) for student in module_doc["student"]]:
        raise HTTPException(status_code=400, detail="Student is not in this module")

    # Update the module document to remove the student ID
    result = module_collection.update_one(
        {"_id": ObjectId(module_id)},
        {"$pull": {"student": {"_id": ObjectId(student_id)}}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to remove student from module")

    return {"message": "Student removed from module successfully"}
