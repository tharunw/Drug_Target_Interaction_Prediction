import itertools
from collections import Counter
import pandas as pd


AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"


def amino_acid_composition(sequence):
    """Calculate amino-acid frequency features."""
    sequence = str(sequence).upper()
    length = len(sequence)

    if length == 0:
        return {
            f"{aa}_freq": 0.0
            for aa in AMINO_ACIDS
        }

    counts = Counter(sequence)

    return {
        f"{aa}_freq": counts.get(aa, 0) / length
        for aa in AMINO_ACIDS
    }


def calculate_protein_features(sequence):
    """Calculate basic protein sequence features."""
    sequence = str(sequence).upper()

    length = len(sequence)

    aa_features = amino_acid_composition(
        sequence
    )

    hydrophobic = set(
        "AVILMFWY"
    )

    charged = set(
        "DEKR"
    )

    aromatic = set(
        "FWY"
    )

    if length == 0:
        hydrophobic_fraction = 0.0
        charged_fraction = 0.0
        aromatic_fraction = 0.0
    else:
        hydrophobic_fraction = sum(
            aa in hydrophobic
            for aa in sequence
        ) / length

        charged_fraction = sum(
            aa in charged
            for aa in sequence
        ) / length

        aromatic_fraction = sum(
            aa in aromatic
            for aa in sequence
        ) / length

    features = {
        "sequence_length": length,
        **aa_features,
        "hydrophobic_fraction":
            hydrophobic_fraction,
        "charged_fraction":
            charged_fraction,
        "aromatic_fraction":
            aromatic_fraction
    }

    return features


def calculate_dipeptide_features(sequence):
    """Calculate normalized frequencies of all 400 dipeptides."""
    sequence = str(sequence).upper()

    dipeptides = [
        aa1 + aa2
        for aa1, aa2 in itertools.product(
            AMINO_ACIDS,
            repeat=2
        )
    ]

    counts = Counter(
        sequence[i:i + 2]
        for i in range(
            len(sequence) - 1
        )
    )

    total = max(
        len(sequence) - 1,
        1
    )

    return {
        f"di_{dipeptide}":
            counts.get(
                dipeptide,
                0
            ) / total
        for dipeptide in dipeptides
    }


def build_protein_feature_dataframe(
    df,
    sequence_column="sequence"
):
    """Generate basic protein sequence features."""
    features = df[
        sequence_column
    ].apply(
        calculate_protein_features
    )

    feature_df = pd.DataFrame(
        features.tolist(),
        index=df.index
    )

    return pd.concat(
        [
            df.copy(),
            feature_df
        ],
        axis=1
    )


def build_enhanced_protein_features(
    df,
    sequence_column="sequence"
):
    """
    Generate basic protein features plus
    400 normalized dipeptide features.
    """
    basic_features = df[
        sequence_column
    ].apply(
        calculate_protein_features
    )

    dipeptide_features = df[
        sequence_column
    ].apply(
        calculate_dipeptide_features
    )

    basic_df = pd.DataFrame(
        basic_features.tolist(),
        index=df.index
    )

    dipeptide_df = pd.DataFrame(
        dipeptide_features.tolist(),
        index=df.index
    )

    return pd.concat(
        [
            df.copy(),
            basic_df,
            dipeptide_df
        ],
        axis=1
    )