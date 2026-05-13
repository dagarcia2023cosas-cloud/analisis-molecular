"""
Script de configuración para Google Colab.
Ejecutar en una celda de Colab:

    !wget -q https://raw.githubusercontent.com/tu-usuario/analisismolecular/main/colab/setup_colab.py
    from setup_colab import setup
    setup()
"""

import subprocess
import sys
from pathlib import Path


def setup(repo_url=None, install_full=False):
    """Configura el proyecto en Google Colab.

    Args:
        repo_url: URL del repositorio (por defecto usa el GitHub del proyecto).
        install_full: Si True, instala todas las dependencias (RDKit, PyTorch, etc.).
    """
    if repo_url is None:
        repo_url = "https://github.com/tu-usuario/analisismolecular.git"

    project_dir = Path("/content/analisismolecular")

    print("=" * 60)
    print("  Configuración de analisismolecular en Google Colab")
    print("=" * 60)

    if project_dir.exists():
        print("\n[1/3] Actualizando repositorio...")
        subprocess.run(["git", "-C", str(project_dir), "pull"], check=False)
    else:
        print("\n[1/3] Clonando repositorio...")
        subprocess.run(["git", "clone", repo_url, str(project_dir)], check=False)

    sys.path.insert(0, str(project_dir))

    print("\n[2/3] Instalando el paquete...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", str(project_dir)],
        check=False, capture_output=True
    )

    print("\n[3/3] Instalando dependencias...")
    deps = ["py3Dmol", "nglview", "plotly", "ipywidgets", "prody", "biopython"]

    if install_full:
        deps.extend(["rdkit-pypi", "torch", "torchvision", "torchaudio"])

    for dep in deps:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", dep],
            check=False
        )

    print("\n" + "=" * 60)
    print("  ¡Configuración completada!")
    print(f"  Proyecto listo en: {project_dir}")
    print("=" * 60)

    return project_dir
