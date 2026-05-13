"""Funciones para configurar el entorno en Google Colab."""

import subprocess
import sys
import importlib
from pathlib import Path


def is_colab():
    """Detecta si el código se está ejecutando en Google Colab."""
    try:
        import google.colab
        return True
    except ImportError:
        return False


def install_dependencies(include_rdkit=True, include_torch=False, quiet=True):
    """Instala dependencias necesarias en Colab.

    Args:
        include_rdkit: Instalar RDKit (vía conda-forge).
        include_torch: Instalar PyTorch.
        quiet: Suprimir output verbose.
    """
    if not is_colab():
        print("No se detecta entorno Colab. Omitiendo instalación.")
        return

    quiet_flag = "-q" if quiet else ""

    if include_rdkit:
        print("Instalando RDKit desde conda-forge...")
        subprocess.run(
            f"pip install {quiet_flag} rdkit-pypi",
            shell=True, check=False
        )

    if include_torch:
        print("Instalando PyTorch...")
        subprocess.run(
            f"pip install {quiet_flag} torch torchvision torchaudio",
            shell=True, check=False
        )

    print("Instalando dependencias adicionales...")
    subprocess.run(
        f"pip install {quiet_flag} py3Dmol nglview plotly ipywidgets "
        f"prody biopython",
        shell=True, check=False
    )

    print("¡Dependencias instaladas correctamente!")


def setup_colab_environment():
    """Configura el entorno completo de Colab para el proyecto.

    - Monta Google Drive
    - Clona/actualiza el repositorio
    - Instala dependencias
    """
    if not is_colab():
        print("No se detecta entorno Colab.")
        return

    from .drive_utils import mount_drive

    mount_drive()

    repo_url = "https://github.com/tu-usuario/analisismolecular.git"
    project_dir = Path("/content/analisismolecular")

    if project_dir.exists():
        print("Actualizando repositorio...")
        subprocess.run("git pull", shell=True, check=False, cwd=str(project_dir))
    else:
        print("Clonando repositorio...")
        subprocess.run(
            f"git clone {repo_url} {project_dir}",
            shell=True, check=False
        )

    sys.path.insert(0, str(project_dir))

    install_dependencies()

    print(f"Proyecto listo en: {project_dir}")
    print("¡Entorno Colab configurado!")
