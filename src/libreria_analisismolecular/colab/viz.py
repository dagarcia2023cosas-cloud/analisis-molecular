"""Utilidades de visualización molecular para Colab."""

from pathlib import Path

import matplotlib.pyplot as plt


def display_molecule_3d(mol_block_or_file, fmt="sdf"):
    """Muestra una molécula en 3D usando py3Dmol en Colab.

    Args:
        mol_block_or_file: Bloque molecular (string) o ruta a archivo.
        fmt: Formato ('sdf', 'mol', 'pdb', 'xyz').
    """
    try:
        import py3Dmol
        import ipywidgets as widgets
        from IPython.display import display

        view = py3Dmol.view(width=600, height=400)

        if Path(mol_block_or_file).exists():
            with open(mol_block_or_file) as f:
                mol_data = f.read()
        else:
            mol_data = mol_block_or_file

        view.addModel(mol_data, fmt)
        view.setStyle({"stick": {}, "sphere": {"radius": 0.5}})
        view.setBackgroundColor("white")
        view.zoomTo()

        display(view)

    except ImportError:
        print("py3Dmol no disponible. Instala con: pip install py3Dmol")


def plot_molecular_properties(
    data, x_label="Propiedad", y_label="Valor", title="Propiedades Moleculares"
):
    """Grafica propiedades moleculares usando matplotlib/seaborn.

    Args:
        data: dict o DataFrame con datos a graficar.
        x_label: Etiqueta del eje X.
        y_label: Etiqueta del eje Y.
        title: Título del gráfico.
    """
    import pandas as pd
    import seaborn as sns

    sns.set_theme(style="whitegrid")

    if isinstance(data, dict):
        data = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    if isinstance(data, pd.DataFrame):
        data.plot(kind="bar", ax=ax)
    else:
        ax.plot(data)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.tight_layout()

    return fig
