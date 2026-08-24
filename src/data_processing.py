import pandas as pd


def load_activity_data(path):
    """Load raw ChEMBL activity data."""
    return pd.read_csv(path)


def remove_missing_pchembl(df):
    """Keep records with experimentally measured pChEMBL values."""
    return df.dropna(
        subset=["pchembl_value"]
    ).copy()


def remove_duplicate_measurements(df):
    """Remove duplicate drug-target activity records."""
    return df.drop_duplicates().copy()


def summarize_dataset(df):
    """Return basic dataset statistics."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "unique_compounds": (
            df["molecule_chembl_id"].nunique()
            if "molecule_chembl_id" in df.columns
            else None
        ),
        "unique_targets": (
            df["target_chembl_id"].nunique()
            if "target_chembl_id" in df.columns
            else None
        ),
        "missing_values": int(
            df.isna().sum().sum()
        )
    }