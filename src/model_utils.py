import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def train_random_forest(
    X_train,
    y_train,
    n_estimators=300,
    random_state=42,
    max_features="sqrt"
):
    """Train a Random Forest regression model."""

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        max_features=max_features
    )

    model.fit(
        X_train,
        y_train
    )

    return model


def evaluate_regression(
    model,
    X_test,
    y_test
):
    """Calculate MAE, RMSE, and R²."""

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }


def get_feature_importance(
    model,
    feature_names
):
    """Return sorted Random Forest feature importance."""

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance":
            model.feature_importances_
    })

    return importance_df.sort_values(
        "importance",
        ascending=False
    ).reset_index(
        drop=True
    )