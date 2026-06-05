import json
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generate_eda_report(
    df,
    report_path="data/eda_report.json"
):
    os.makedirs(
        "data",
        exist_ok=True
    )

    report = {
        "rows": int(df.shape[0]),

        "columns": int(df.shape[1]),

        "column_names":
            list(df.columns),

        "column_types":
            df.dtypes.astype(str).to_dict(),

        "missing_values":
            df.isna().sum().to_dict(),

        "duplicate_rows":
            int(df.duplicated().sum()),

        "target_distribution":
            (
                df["placement_status"]
                .value_counts()
                .to_dict()
            )
            if "placement_status" in df.columns
            else {},

        "numeric_summary":
            (
                df.select_dtypes(
                    include=[np.number]
                )
                .describe()
                .to_dict()
            )
    }

    numeric_df = df.select_dtypes(
        include=[np.number]
    )

    correlation = numeric_df.corr()

    report[
        "correlation_matrix"
    ] = correlation.round(
        3
    ).to_dict()

    if (
        "placement_status" in df.columns
        and df["placement_status"].dtype != "object"
    ):

        placement_corr = (
            correlation["placement_status"]
            .sort_values(
                ascending=False
            )
            .to_dict()
        )

        report[
            "placement_correlation"
        ] = placement_corr

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    plt.figure(
        figsize=(14, 12)
    )

    plt.imshow(
        correlation,
        cmap="coolwarm"
    )

    plt.colorbar()

    plt.xticks(
        range(
            len(
                correlation.columns
            )
        ),
        correlation.columns,
        rotation=90
    )

    plt.yticks(
        range(
            len(
                correlation.columns
            )
        ),
        correlation.columns
    )

    plt.tight_layout()

    plt.savefig(
        "data/correlation_heatmap.png",
        dpi=150
    )

    plt.close()

    print(
        "EDA report saved successfully."
    )

    return report


if __name__ == "__main__":

    df = pd.read_csv(
        "data/cleaned_students.csv"
    )

    generate_eda_report(df)

    print(
        "EDA Completed"
    )