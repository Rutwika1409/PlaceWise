from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.prediction import predict_student
from backend.skill_gap import analyze_skill_gap
from backend.recommendation import generate_recommendation


app = FastAPI(
    title="Student Placement Prediction System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/css",
    StaticFiles(directory=FRONTEND_DIR / "css"),
    name="css"
)

app.mount(
    "/js",
    StaticFiles(directory=FRONTEND_DIR / "js"),
    name="js"
)

app.mount(
    "/assets",
    StaticFiles(directory=FRONTEND_DIR / "assets"),
    name="assets"
)


class StudentInput(BaseModel):

    cgpa: float
    branch: str

    backlogs: int
    internships_count: int
    projects_count: int

    coding_skill_score: float
    mock_interview_score: float
    logical_reasoning_score: float
    communication_skill_score: float
    aptitude_score: float
    leadership_score: float
    extracurricular_score: float


# ---------- FRONTEND ROUTES ----------

@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/index.html")
def home_html():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/predict")
def predict_page():
    return FileResponse(
        FRONTEND_DIR / "predict.html"
    )


@app.get("/predict.html")
def predict_html():
    return FileResponse(
        FRONTEND_DIR / "predict.html"
    )


@app.get("/analytics")
def analytics_page():
    return FileResponse(
        FRONTEND_DIR / "analytics.html"
    )


@app.get("/analytics.html")
def analytics_html():
    return FileResponse(
        FRONTEND_DIR / "analytics.html"
    )


@app.get("/about")
def about_page():
    return FileResponse(
        FRONTEND_DIR / "about.html"
    )


@app.get("/about.html")
def about_html():
    return FileResponse(
        FRONTEND_DIR / "about.html"
    )


# ---------- API ROUTE ----------

@app.post("/predict")
def predict(student: StudentInput):

    student_data = student.model_dump()

    prediction_result = predict_student(
        student_data
    )

    skill_gaps = analyze_skill_gap(
        student_data
    )

    recommendation = generate_recommendation(
        student_data,
        prediction_result,
        skill_gaps
    )

    return {

        "placement_probability":
            prediction_result[
                "placement_probability"
            ],

        "placement_status":
            prediction_result[
                "prediction"
            ],

        "skill_gaps":
            skill_gaps,

        "recommendation":
            recommendation
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }