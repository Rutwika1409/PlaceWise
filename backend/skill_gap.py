import json


def load_benchmarks():

    with open(
        "models/benchmarks.json",
        "r"
    ) as f:

        return json.load(f)


def analyze_skill_gap(
    student_data
):

    benchmarks = (
        load_benchmarks()
    )

    reasons = []

    if (
        student_data["cgpa"]
        <
        benchmarks["cgpa"]
    ):
        reasons.append(
            "CGPA below average placed students"
        )

    if (
        student_data[
            "internships_count"
        ]
        <
        benchmarks[
            "internships_count"
        ]
    ):
        reasons.append(
            "Low internship exposure"
        )

    if (
        student_data[
            "projects_count"
        ]
        <
        benchmarks[
            "projects_count"
        ]
    ):
        reasons.append(
            "Insufficient project experience"
        )

    if (
        student_data[
            "coding_skill_score"
        ]
        <
        benchmarks[
            "coding_skill_score"
        ]
    ):
        reasons.append(
            "Weak coding skills"
        )

    if (
        student_data[
            "mock_interview_score"
        ]
        <
        benchmarks[
            "mock_interview_score"
        ]
    ):
        reasons.append(
            "Mock interview performance below average"
        )

    if (
        student_data[
            "logical_reasoning_score"
        ]
        <
        benchmarks[
            "logical_reasoning_score"
        ]
    ):
        reasons.append(
            "Logical reasoning needs improvement"
        )

    if (
        student_data[
            "communication_skill_score"
        ]
        <
        benchmarks[
            "communication_skill_score"
        ]
    ):
        reasons.append(
            "Communication skills below average"
        )

    if (
        student_data[
            "aptitude_score"
        ]
        <
        benchmarks[
            "aptitude_score"
        ]
    ):
        reasons.append(
            "Aptitude score below average"
        )

    if (
        student_data[
            "leadership_score"
        ]
        <
        benchmarks[
            "leadership_score"
        ]
    ):
        reasons.append(
            "Leadership skills need improvement"
        )

    if (
        student_data[
            "extracurricular_score"
        ]
        <
        benchmarks[
            "extracurricular_score"
        ]
    ):
        reasons.append(
            "Low extracurricular participation"
        )

    return reasons