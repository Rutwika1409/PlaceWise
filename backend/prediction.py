import joblib
import pandas as pd


MODEL = joblib.load(
    "models/placement_model.pkl"
)

SCALER = joblib.load(
    "models/scaler.pkl"
)

LABEL_ENCODERS = joblib.load(
    "models/label_encoders.pkl"
)

FEATURE_COLUMNS = joblib.load(
    "models/feature_columns.pkl"
)

Y_ENCODER = joblib.load(
    "models/y_encoder.pkl"
)


def predict_student(student_data):

    df = pd.DataFrame(
        [student_data]
    )

    # Handle label encoding - LABEL_ENCODERS might be a dict or single encoder
    if isinstance(LABEL_ENCODERS, dict):
        for column, encoder in LABEL_ENCODERS.items():
            if column in df.columns:
                try:
                    df[column] = encoder.transform(df[column].values)
                except Exception:
                    df[column] = 0
    else:
        # Single encoder for branch column
        try:
            if "branch" in df.columns:
                df["branch"] = LABEL_ENCODERS.transform(df["branch"].values)
        except Exception:
            df["branch"] = 0

    df = df[
        FEATURE_COLUMNS
    ]

    df_scaled = (
        SCALER.transform(df)
    )

    prediction = (
        MODEL.predict(
            df_scaled
        )[0]
    )

    probability = (
        MODEL.predict_proba(
            df_scaled
        )[0][1]
    )

    prediction_label = (
        Y_ENCODER.inverse_transform(
            [prediction]
        )[0]
    )

    return {

        "prediction":
            prediction_label,

        "placement_probability":
            round(
                probability * 100,
                2
            )
    }