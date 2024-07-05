def individual_serial(student) -> dict:
    return {
            "student_id" : str(student["_id"]),
            "name" : student["name"],
            "email" : student["email"],
        }

def student_list(students) -> list:
    return [individual_serial(student) for student in students]


