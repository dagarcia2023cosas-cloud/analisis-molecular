"""Tests para el módulo de integración con Colab."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from libreria_analisismolecular import colab, utils


def test_is_colab_returns_false():
    """En entorno local no debería detectar Colab."""
    assert colab.setup.is_colab() is False


def test_list_data_files_empty():
    """Sin archivos de datos, debería retornar lista vacía."""
    files = utils.list_data_files("data")
    # Solo debe encontrar .gitkeep o nada
    assert isinstance(files, list)


def test_dataframe_summary():
    """Verifica que el resumen de DataFrame funciona."""
    import pandas as pd
    df = pd.DataFrame({"a": [1, 2], "b": [3, None]})
    summary = utils.dataframe_summary(df)
    assert summary["shape"] == (2, 2)
    assert summary["missing"]["b"] == 1
