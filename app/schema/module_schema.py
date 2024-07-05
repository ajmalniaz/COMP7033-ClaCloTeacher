from typing import List
from .student_schema import individual_serial as student_individual_serial

def module_individual_serial(module) -> dict:
    return {
        "module_id": str(module["_id"]),
        "module_name": module["module_name"],
        "student": [student_individual_serial(student) for student in module["student"]]
    }

def module_list(modules) -> list:
    return [module_individual_serial(module) for module in modules]


