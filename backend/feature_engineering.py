import pandas as pd

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)


FEATURES = [
    "cgpa",
    "branch",
    "backlogs",
    "internships_count",
    "projects_count",
    "coding_skill_score",
    "mock_interview_score",
    "logical_reasoning_score",
    "communication_skill_score",
    "aptitude_score",
    "leadership_score",
    "extracurricular_score"
]


def prepare_features(df):

    df = df.copy()

    X = df[FEATURES].copy()

    branch_encoder = LabelEncoder()

    X["branch"] = (
        branch_encoder
        .fit_transform(
            X["branch"]
            .astype(str)
        )
    )

    y_encoder = LabelEncoder()

    y = (
        y_encoder
        .fit_transform(
            df["placement_status"]
        )
    )

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        X
    )

    return (
        X_scaled,
        y,
        FEATURES,
        scaler,
        branch_encoder,
        y_encoder
    )


if __name__ == "__main__":

    df = pd.read_csv(
        "data/cleaned_students.csv"
    )

    (
        X,
        y,
        feature_columns,
        scaler,
        branch_encoder,
        y_encoder
    ) = prepare_features(df)

    print("Features Shape:", X.shape)

    print(
        "Number of Features:",
        len(feature_columns)
    )