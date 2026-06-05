import os
import joblib

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV
)

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score
)

from etl import (
    load_training_data,
    clean_data
)

from feature_engineering import (
    prepare_features
)


def train_model(X_train, y_train):

    rf = RandomForestClassifier(
        random_state=42,
        n_jobs=-1
    )

    param_grid = {

        "n_estimators": [
            100,
            200,
            300,
            500
        ],

        "max_depth": [
            5,
            10,
            15,
            20,
            None
        ],

        "min_samples_split": [
            2,
            5,
            10
        ],

        "min_samples_leaf": [
            1,
            2,
            4
        ],

        "max_features": [
            "sqrt",
            "log2"
        ],

        "bootstrap": [
            True,
            False
        ]
    }

    search = RandomizedSearchCV(
        estimator=rf,
        param_distributions=param_grid,
        n_iter=20,
        cv=5,
        scoring="accuracy",
        random_state=42,
        n_jobs=-1,
        verbose=2
    )

    print("\nRunning Hyperparameter Tuning...\n")

    search.fit(
        X_train,
        y_train
    )

    print(
        "\nBest Parameters:\n",
        search.best_params_
    )

    print(
        f"\nBest CV Accuracy: "
        f"{search.best_score_:.4f}"
    )

    return search.best_estimator_


def evaluate_model(
    model,
    X_test,
    y_test
):

    predictions = model.predict(
        X_test
    )

    probabilities = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    auc = roc_auc_score(
        y_test,
        probabilities
    )

    print(
        f"\nAccuracy: {accuracy:.4f}"
    )

    print(
        f"ROC-AUC: {auc:.4f}"
    )

    print(
        "\nClassification Report:\n"
    )

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    return probabilities


def save_artifacts(
    model,
    scaler,
    label_encoders,
    y_encoder,
    feature_columns
):

    os.makedirs(
        "models",
        exist_ok=True
    )

    joblib.dump(
        model,
        "models/placement_model.pkl"
    )

    joblib.dump(
        scaler,
        "models/scaler.pkl"
    )

    joblib.dump(
        label_encoders,
        "models/label_encoders.pkl"
    )

    joblib.dump(
        y_encoder,
        "models/y_encoder.pkl"
    )

    joblib.dump(
        feature_columns,
        "models/feature_columns.pkl"
    )

    print(
        "\nArtifacts Saved Successfully"
    )


def main():

    print(
        "\nLoading Dataset..."
    )

    df = load_training_data()

    print(
        f"Dataset Shape: {df.shape}"
    )

    print(
        "\nCleaning Dataset..."
    )

    df = clean_data(df)

    print(
        "\nPreparing Features..."
    )

    (
        X,
        y,
        feature_columns,
        scaler,
        label_encoders,
        y_encoder
    ) = prepare_features(df)

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = train_model(
        X_train,
        y_train
    )

    probabilities = evaluate_model(
        model,
        X_test,
        y_test
    )

    save_artifacts(
        model,
        scaler,
        label_encoders,
        y_encoder,
        feature_columns
    )

    print(
        "\nSample Employability Scores:\n"
    )

    for i, score in enumerate(
        probabilities[:10]
    ):

        employability_score = round(
            score * 100,
            2
        )

        print(
            f"Student {i + 1}: "
            f"{employability_score}%"
        )


if __name__ == "__main__":
    main()