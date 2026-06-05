import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client


def load_environment():
    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    table_name = os.getenv(
        "TABLE_NAME",
        "students"
    )
    print("SUPABASE_URL =", supabase_url)
    print("SUPABASE_KEY =", supabase_key[:20] if supabase_key else None)
    local_data_path = os.getenv(
        "LOCAL_DATA_PATH",
        os.path.join(
            "data",
            "student_placement_prediction_dataset_2026.csv"
        )
    )

    return (
        supabase_url,
        supabase_key,
        table_name,
        local_data_path
    )


def get_supabase_client(
    supabase_url,
    supabase_key
):
    if not supabase_url or not supabase_key:
        return None

    return create_client(
        supabase_url,
        supabase_key
    )


def load_data_from_supabase(
    client,
    table_name
):

    all_rows = []

    start = 0
    batch_size = 1000

    while True:

        response = (
            client
            .table(table_name)
            .select("*")
            .range(
                start,
                start + batch_size - 1
            )
            .execute()
        )

        rows = response.data

        if not rows:
            break

        all_rows.extend(rows)

        start += batch_size

        print(
            f"Fetched {len(all_rows)} rows"
        )

    return pd.DataFrame(all_rows)


def load_training_data():
    (
        supabase_url,
        supabase_key,
        table_name,
        local_data_path
    ) = load_environment()

    if os.path.exists(local_data_path):
        return pd.read_csv(local_data_path)

    client = get_supabase_client(
        supabase_url,
        supabase_key
    )

    return load_data_from_supabase(
        client,
        table_name
    )


def clean_data(df):
    df = df.copy()

    df.replace(
        [
            "",
            "NA",
            "N/A",
            "na",
            "n/a",
            "None",
            None
        ],
        np.nan,
        inplace=True
    )

    if "student_id" in df.columns:

        df["student_id"] = pd.to_numeric(
            df["student_id"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["student_id"]
        )

        df["student_id"] = (
            df["student_id"]
            .astype(int)
        )

        df = df.drop_duplicates(
            subset=["student_id"]
        )

    categorical_cols = [
        col
        for col in [
            "gender",
            "branch",
            "college_tier",
            "volunteer_experience"
        ]
        if col in df.columns
    ]

    ignore_cols = [
        "student_id",
        "placement_status",
        "salary_package_lpa"
    ]

    numeric_cols = [
        col
        for col in df.columns
        if col not in categorical_cols + ignore_cols
    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        median_value = df[col].median()

        df[col] = df[col].fillna(
            median_value
        )

    for col in categorical_cols:

        mode_value = (
            df[col]
            .mode()[0]
            if not df[col].mode().empty
            else "missing"
        )

        df[col] = df[col].fillna(
            mode_value
        )

        df[col] = df[col].astype(str)

    os.makedirs(
        "data",
        exist_ok=True
    )

    df.to_csv(
        "data/cleaned_students.csv",
        index=False
    )

    return df


if __name__ == "__main__":

    df = load_training_data()

    cleaned_df = clean_data(df)

    print(cleaned_df.shape)