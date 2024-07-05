from fastapi import FastAPI, Body, Depends
from routes.teacher_route import teacher
from routes.student_route import student
from routes.module_route import module
from routes.studymaterial_route import studymaterial
from routes.exercise_route import exercise

app = FastAPI()

app.include_router(teacher)
app.include_router(student)
app.include_router(module)
app.include_router(studymaterial)
app.include_router(exercise)






