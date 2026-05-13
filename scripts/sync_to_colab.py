"""
Genera el comando de Colab para clonar y configurar el proyecto.
Pega la salida en una celda de Colab para tener el entorno listo al instante.
"""
import shutil
import subprocess
import sys
from pathlib import Path


REPO_URL = "https://github.com/dagarcia2023cosas-cloud/analisismolecular.git"


def generate_colab_setup_cell(branch="master", install_full=False):
    """Genera el código para una celda de Colab que configura todo."""
    lines = [
        f"# === SETUP GENERATED POR sync_to_colab.py ===",
        f"!git clone {REPO_URL} /content/analisismolecular",
        f"%cd /content/analisismolecular",
        f"!git checkout {branch}",
        f"!pip install -q -e .",
    ]

    if install_full:
        lines.append("!pip install -q py3Dmol nglview plotly ipywidgets prody biopython rdkit-pypi")
    else:
        lines.append("!pip install -q py3Dmol nglview plotly ipywidgets")

    lines.append("")
    lines.append("# Verificar instalacion")
    lines.append("import sys")
    lines.append("sys.path.insert(0, '/content/analisismolecular/src')")
    lines.append("from libreria_analisismolecular import colab")
    lines.append(f"print('Proyecto listo en:', '/content/analisismolecular')")
    lines.append("")

    return "\n".join(lines)


def generate_zip_for_colab(output_name="analisismolecular_colab.zip"):
    """Crea un zip del proyecto para subir manualmente a Colab."""
    base = Path.cwd()
    ignore_patterns = {
        ".git", "__pycache__", ".venv", ".ipynb_checkpoints",
        "*.pyc", ".DS_Store", "Thumbs.db",
    }

    out_path = Path(output_name)
    if out_path.exists():
        out_path.unlink()

    with shutil.ZipFile(str(out_path), "w") as zf:
        for f in base.rglob("*"):
            if any(p in f.parts for p in ignore_patterns):
                continue
            if f.is_file():
                zf.write(f, f.relative_to(base))

    return out_path


if __name__ == "__main__":
    print("=" * 60)
    print("  Sincronizacion Local -> Google Colab")
    print("=" * 60)
    print()

    if len(sys.argv) > 1 and sys.argv[1] == "--zip":
        zip_path = generate_zip_for_colab()
        print(f"[OK] Zip creado: {zip_path}")
        print("     Subilo a Colab via: Files > Upload")
    else:
        print("Celda para copiar en Colab:")
        print()
        print("```python")
        print(generate_colab_setup_cell())
        print("```")
