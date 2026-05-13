import numpy as np
import pandas as pd
from pathlib import Path

def load_molecule(filepath):
    """Carga una molécula desde un archivo (mol, sdf, pdb, etc).

    Retorna el contenido del archivo como string.
    Usar con RDKit o py3Dmol para procesamiento posterior.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
    return path.read_text()

def list_data_files(data_dir="data"):
    """Lista archivos de datos disponibles en el proyecto."""
    base = Path(data_dir)
    if not base.exists():
        return []
    return [str(f.relative_to(base.parent)) for f in base.rglob("*") if f.is_file() and f.suffix != ".gitkeep"]

def dataframe_summary(df):
    """Genera un resumen rápido de un DataFrame."""
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "missing": df.isnull().sum().to_dict(),
    }
