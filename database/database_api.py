from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os

# ======================================
# LOAD ENV VARIABLES
# ======================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = os.getenv("TABLE_NAME", "students_raw")

print("=" * 50)
print("SUPABASE CONFIG")
print("=" * 50)
print("URL:", SUPABASE_URL)
print("KEY EXISTS:", SUPABASE_KEY is not None)
print("TABLE:", TABLE_NAME)

# ======================================
# CREATE CLIENT
# ======================================

try:
    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    print("✅ Supabase Client Created")

    # Test Connection
    test = (
        supabase
        .table(TABLE_NAME)
        .select("*")
        .limit(1)
        .execute()
    )

    print("✅ Database Connected")

except Exception as e:
    print("❌ Connection Error")
    print(e)

# ======================================
# FASTAPI APP
# ======================================

app = FastAPI(
    title="Student Placement API",
    version="1.0.0"
)

# ======================================
# HOME
# ======================================

@app.get("/")
def home():

    return {
        "message": "Student Placement API Running"
    }

# ======================================
# GET ALL STUDENTS
# ======================================

@app.get("/students")
def get_students():

    try:

        result = (
            supabase
            .table(TABLE_NAME)
            .select("*")
            .execute()
        )

        return result.data

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================
# GET STUDENT BY ID
# ======================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    try:

        result = (
            supabase
            .table(TABLE_NAME)
            .select("*")
            .eq(
                "student_id",
                student_id
            )
            .execute()
        )

        return result.data

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================
# INSERT STUDENT
# ======================================

@app.post("/students")
def create_student(data: dict):

    try:

        result = (
            supabase
            .table(TABLE_NAME)
            .insert(data)
            .execute()
        )

        return result.data

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================
# UPDATE STUDENT
# ======================================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    data: dict
):

    try:

        result = (
            supabase
            .table(TABLE_NAME)
            .update(data)
            .eq(
                "student_id",
                student_id
            )
            .execute()
        )

        return result.data

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================
# DELETE STUDENT
# ======================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    try:

        (
            supabase
            .table(TABLE_NAME)
            .delete()
            .eq(
                "student_id",
                student_id
            )
            .execute()
        )

        return {
            "message": f"Student {student_id} deleted"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )