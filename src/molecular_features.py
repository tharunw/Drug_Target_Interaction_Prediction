from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Crippen, rdMolDescriptors
from rdkit.Chem import AllChem
import pandas as pd
import numpy as np


def smiles_to_mol(smiles):
    """Convert a SMILES string to an RDKit molecule."""
    if pd.isna(smiles):
        return None
    return Chem.MolFromSmiles(smiles)


def calculate_molecular_descriptors(smiles):
    """Calculate basic molecular descriptors from SMILES."""
    mol = smiles_to_mol(smiles)

    if mol is None:
        return [np.nan] * 8

    return [
        Descriptors.MolWt(mol),
        Crippen.MolLogP(mol),
        rdMolDescriptors.CalcTPSA(mol),
        Lipinski.NumHDonors(mol),
        Lipinski.NumHAcceptors(mol),
        Lipinski.NumRotatableBonds(mol),
        Lipinski.RingCount(mol),
        rdMolDescriptors.CalcFractionCSP3(mol)
    ]


def generate_morgan_fingerprint(
    smiles,
    radius=2,
    n_bits=256
):
    """Generate a Morgan fingerprint from a SMILES string."""
    mol = smiles_to_mol(smiles)

    if mol is None:
        return np.zeros(n_bits, dtype=int)

    fingerprint = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius,
        nBits=n_bits
    )

    return np.array(
        fingerprint
    )


def build_descriptor_dataframe(
    df,
    smiles_column="canonical_smiles"
):
    """Generate molecular descriptor columns for a dataframe."""
    descriptors = df[
        smiles_column
    ].apply(
        calculate_molecular_descriptors
    )

    descriptor_columns = [
        "mol_weight",
        "logp",
        "tpsa",
        "hbd",
        "hba",
        "rotatable_bonds",
        "ring_count",
        "fraction_csp3"
    ]

    descriptor_df = pd.DataFrame(
        descriptors.tolist(),
        columns=descriptor_columns,
        index=df.index
    )

    return pd.concat(
        [df.copy(), descriptor_df],
        axis=1
    )


def build_morgan_dataframe(
    df,
    smiles_column="canonical_smiles",
    id_column="molecule_chembl_id",
    radius=2,
    n_bits=256
):
    """Generate a Morgan fingerprint dataframe."""
    fingerprints = df[
        smiles_column
    ].apply(
        lambda x: generate_morgan_fingerprint(
            x,
            radius=radius,
            n_bits=n_bits
        )
    )

    fingerprint_columns = [
        f"morgan_{i}"
        for i in range(n_bits)
    ]

    fingerprint_matrix = np.vstack(
        fingerprints.values
    )

    fingerprint_df = pd.DataFrame(
        fingerprint_matrix,
        columns=fingerprint_columns,
        index=df.index
    )

    if id_column in df.columns:
        fingerprint_df.insert(
            0,
            id_column,
            df[id_column].values
        )

    return fingerprint_df