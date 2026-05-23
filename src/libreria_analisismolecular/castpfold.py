#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper para CASTpFold — analisis de cavidades y bolsillos en proteinas.

Usa castpfoldpy (pip install castpfoldpy) que envia PDBs al servidor
CASTpFold (sts.bioe.uic.edu/castpdev/) y descarga los resultados.

Paper: Ye et al. (2024), Nucleic Acids Research, 52(W1), W194-W199.
DOI: 10.1093/nar/gkae415
"""

import subprocess
import tempfile
import zipfile
import shutil
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def run_castpfold(
    pdb_path: str,
    output_dir: Optional[str] = None,
    probe_radius: float = 1.4,
    compute_pocket: bool = True,
    wait_time: int = 20,
    extra_wait: int = 30,
    retries: int = 3,
    email: Optional[str] = None,
) -> str:
    """
    Ejecuta CASTpFold sobre un archivo PDB.

    Args:
        pdb_path: Ruta al archivo PDB.
        output_dir: Directorio para guardar resultados. Si None, crea uno temporal.
        probe_radius: Radio de la sonda en Angstroms (default 1.4).
        compute_pocket: Si True, calcula coordenadas del bolsillo.
        wait_time: Tiempo inicial de espera en segundos.
        extra_wait: Tiempo extra entre reintentos.
        retries: Numero de reintentos.
        email: Email opcional para notificacion del servidor.

    Returns:
        Ruta al directorio con los resultados extraidos.
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="castpfold_")
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    cmd = [
        "castpfoldpy",
        "--submit-download",
        "-p", pdb_path,
        "-d", output_dir,
        "-r", str(probe_radius),
        "-w", str(wait_time),
        "-ew", str(extra_wait),
        "-t", str(retries),
    ]

    if compute_pocket:
        cmd.append("--pocket")

    if email:
        cmd.extend(["--email", email])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"CASTpFold failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )

    # Extraer ZIP si existe
    zip_files = list(Path(output_dir).glob("*.zip"))
    if zip_files:
        zip_path = zip_files[0]
        extract_dir = Path(output_dir) / "results"
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)
        return str(extract_dir)

    return output_dir


def parse_castpfold_results(results_dir: str) -> pd.DataFrame:
    """
    Parsea los resultados de CASTpFold y devuelve un DataFrame.

    Busca archivos de area/volumen y sitios activos.

    Args:
        results_dir: Directorio con los resultados extraidos.

    Returns:
        DataFrame con metricas de cavidades.
    """
    results_path = Path(results_dir)
    rows = []

    # Buscar archivos de informacion de cavidades
    # CASTpFold genera archivos con datos de pockets/cavities
    for txt_file in results_path.rglob("*.txt"):
        if "pocket" in txt_file.name.lower() or "cavity" in txt_file.name.lower() or "area" in txt_file.name.lower():
            try:
                content = txt_file.read_text()
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            row = {
                                "pocket_id": parts[0],
                                "volume": float(parts[1]),
                                "area": float(parts[2]),
                            }
                            if len(parts) >= 4:
                                row["depth"] = float(parts[3])
                            rows.append(row)
                        except (ValueError, IndexError):
                            continue
            except Exception:
                continue

    # Si no se encontraron archivos de texto, buscar CSV
    if not rows:
        for csv_file in results_path.rglob("*.csv"):
            try:
                df = pd.read_csv(csv_file)
                rows = df.to_dict("records")
                break
            except Exception:
                continue

    if not rows:
        # Fallback: crear DataFrame vacio con columnas esperadas
        return pd.DataFrame(columns=["pocket_id", "volume", "area", "depth"])

    return pd.DataFrame(rows)


def filter_cavities_by_volume(
    cavities_df: pd.DataFrame,
    volume_threshold: float = 50.0,
    volume_col: str = "volume",
) -> pd.DataFrame:
    """
    Filtra cavidades por volumen minimo.

    Args:
        cavities_df: DataFrame con cavidades.
        volume_threshold: Volumen minimo en Angstroms cubicos.
        volume_col: Nombre de la columna de volumen.

    Returns:
        DataFrame filtrado.
    """
    return cavities_df[cavities_df[volume_col] >= volume_threshold].copy()


def filter_cavities_by_area(
    cavities_df: pd.DataFrame,
    area_threshold: float = 10.0,
    area_col: str = "area",
) -> pd.DataFrame:
    """
    Filtra cavidades por area superficial minima.

    Args:
        cavities_df: DataFrame con cavidades.
        area_threshold: Area minima en Angstroms cuadrados.
        area_col: Nombre de la columna de area.

    Returns:
        DataFrame filtrado.
    """
    return cavities_df[cavities_df[area_col] >= area_threshold].copy()


def pipeline_castpfold_rubisco(
    pdb_path: str,
    specificity: Optional[float] = None,
    group: Optional[str] = None,
    volume_threshold: float = 50.0,
    probe_radius: float = 1.4,
    output_dir: Optional[str] = None,
) -> pd.DataFrame:
    """
    Pipeline completo de CASTpFold para analisis de RuBisCO.

    Args:
        pdb_path: Ruta al archivo PDB.
        specificity: Valor de especificidad S (CO2/O2) para correlacion.
        group: Grupo de RuBisCO (G-I, G-II, G-III, etc.).
        volume_threshold: Volumen minimo para filtrar cavidades.
        probe_radius: Radio de sonda para CASTpFold.
        output_dir: Directorio para resultados.

    Returns:
        DataFrame con cavidades filtradas y metadata.
    """
    results_dir = run_castpfold(
        pdb_path,
        output_dir=output_dir,
        probe_radius=probe_radius,
    )

    cavities = parse_castpfold_results(results_dir)
    cavities = filter_cavities_by_volume(cavities, volume_threshold)

    if specificity is not None:
        cavities["S"] = specificity
    if group is not None:
        cavities["group"] = group
    cavities["pdb"] = Path(pdb_path).stem

    return cavities
