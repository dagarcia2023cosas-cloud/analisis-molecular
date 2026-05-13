"""Utilidades para interactuar con Google Drive desde Colab."""

from pathlib import Path


def mount_drive():
    """Monta Google Drive en Colab."""
    try:
        from google.colab import drive
        drive.mount("/content/drive")
        print("Google Drive montado en /content/drive")
    except ImportError:
        print("No se detecta google.colab. Omitiendo montaje.")


def _get_drive_path(subpath=""):
    """Construye la ruta dentro de Google Drive."""
    base = Path("/content/drive/MyDrive/analisismolecular")
    if subpath:
        return base / subpath
    return base


def save_to_drive(local_path, drive_subpath=""):
    """Guarda un archivo local en Google Drive.

    Args:
        local_path: Ruta al archivo local.
        drive_subpath: Subdirectorio dentro de analisismolecular/ en Drive.
    """
    local = Path(local_path)
    if not local.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {local_path}")

    dest = _get_drive_path(drive_subpath) / local.name
    dest.parent.mkdir(parents=True, exist_ok=True)

    import shutil
    shutil.copy2(str(local), str(dest))
    print(f"Guardado en: {dest}")


def load_from_drive(drive_subpath, filename, local_dir="."):
    """Carga un archivo desde Google Drive al entorno local.

    Args:
        drive_subpath: Subdirectorio dentro de analisismolecular/ en Drive.
        filename: Nombre del archivo.
        local_dir: Directorio local de destino.

    Returns:
        Ruta al archivo copiado localmente.
    """
    src = _get_drive_path(drive_subpath) / filename
    if not src.exists():
        raise FileNotFoundError(f"No encontrado en Drive: {src}")

    dest = Path(local_dir) / filename
    dest.parent.mkdir(parents=True, exist_ok=True)

    import shutil
    shutil.copy2(str(src), str(dest))
    print(f"Cargado desde Drive: {dest}")

    return str(dest.absolute())
