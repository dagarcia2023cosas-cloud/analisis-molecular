#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper para CASTpFold — analisis de cavidades y bolsillos en proteinas.

Llama directamente a la API web de CASTpFold (sts.bioe.uic.edu)
sin depender del paquete castpfoldpy (incompatible con Python <3.12).

Paper: Ye et al. (2024), Nucleic Acids Research, 52(W1), W194-W199.
DOI: 10.1093/nar/gkae415
"""

import time
import tempfile
import zipfile
import os
from pathlib import Path
from typing import Optional

import requests
import numpy as np
import pandas as pd


CASTPFOLD_URL = "http://sts.bioe.uic.edu/castpdev"
DOWNLOAD_URL = f"{CASTPFOLD_URL}/download_castpfold.php"


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
    Envia un PDB al servidor CASTpFold y descarga los resultados.

    Args:
        pdb_path: Ruta al archivo PDB.
        output_dir: Directorio para guardar resultados.
        probe_radius: Radio de la sonda en Angstroms (default 1.4).
        compute_pocket: Si True, solicita coordenadas del bolsillo.
        wait_time: Tiempo inicial de espera en segundos.
        extra_wait: Tiempo extra entre reintentos.
        retries: Numero de reintentos.
        email: Email opcional para notificacion.

    Returns:
        Ruta al directorio con los resultados extraidos.
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="castpfold_")
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    pdb_name = Path(pdb_path).stem

    # Paso 1: Subir PDB al servidor
    print(f"  Subiendo {pdb_name} a CASTpFold...")
    with open(pdb_path, "rb") as f:
        files = {"file": (f"{pdb_name}.pdb", f, "application/octet-stream")}
        data = {
            "probe_radius": str(probe_radius),
            "email": email or "N/A",
        }
        try:
            response = requests.post(
                f"{CASTPFOLD_URL}/upload.php",
                files=files,
                data=data,
                timeout=120,
            )
        except requests.exceptions.Timeout:
            raise RuntimeError("Timeout al conectar con el servidor CASTpFold")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("No se pudo conectar con CASTpFold. Verifica internet.")

    if response.status_code != 200:
        raise RuntimeError(
            f"CASTpFold upload fallo (HTTP {response.status_code}): {response.text[:300]}"
        )

    # Extraer job ID de la respuesta
    response_text = response.text
    job_id = _extract_job_id(response_text, pdb_name)
    if not job_id:
        raise RuntimeError(
            f"No se pudo obtener job ID. Respuesta del servidor: {response_text[:300]}"
        )

    print(f"  Job ID: {job_id}")

    # Paso 2: Esperar y descargar resultados
    time.sleep(wait_time)

    zip_path = os.path.join(output_dir, f"{pdb_name}.zip")
    downloaded = False

    for attempt in range(retries + 1):
        try:
            dl_response = requests.get(
                DOWNLOAD_URL,
                params={"jobid": job_id},
                timeout=60,
            )

            if dl_response.status_code == 200 and len(dl_response.content) > 500:
                with open(zip_path, "wb") as f:
                    f.write(dl_response.content)
                downloaded = True
                print(f"  Resultados descargados ({len(dl_response.content)} bytes)")
                break
            else:
                if attempt < retries:
                    print(f"  Esperando resultados... (intento {attempt + 1}/{retries})")
                    time.sleep(extra_wait)

        except Exception as e:
            if attempt < retries:
                print(f"  Reintentando... ({e})")
                time.sleep(extra_wait)

    if not downloaded:
        print("  No se pudieron descargar resultados. Guardando respuesta como txt.")
        txt_path = os.path.join(output_dir, f"{pdb_name}_response.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(response_text)
        return output_dir

    # Paso 3: Extraer ZIP si existe
    if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
        extract_dir = os.path.join(output_dir, "results")
        os.makedirs(extract_dir, exist_ok=True)
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)
            print(f"  Extraido en {extract_dir}")
            return extract_dir
        except zipfile.BadZipFile:
            print("  ZIP corrupto, guardando sin extraer")
            return output_dir

    return output_dir


def _extract_job_id(response_text: str, pdb_name: str) -> Optional[str]:
    """
    Extrae el job ID de la respuesta HTML del servidor CASTpFold.
    """
    import re

    # Patron comun: jobid=XXXXX o similar
    for pattern in [
        r'jobid[=:]\s*["\']?(\w+)["\']?',
        r'job[=:]\s*["\']?(\w+)["\']?',
        r'id[=:]\s*["\']?(\w+)["\']?',
        r'value=["\'](\w+)["\']',
        f'{re.escape(pdb_name)}.*?(\w{{8,}})',
    ]:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            return match.group(1)

    # Fallback: buscar cualquier string que parezca un ID (alfanumerico, al menos 8 chars)
    match = re.search(r'[A-Za-z0-9_]{8,32}', response_text)
    if match and match.group() not in ("CASTpFold", "PDB", "CASTp"):
        return match.group()

    return None


def parse_castpfold_results(results_dir: str) -> pd.DataFrame:
    """
    Parsea los resultados de CASTpFold.

    Args:
        results_dir: Directorio con los resultados extraidos.

    Returns:
        DataFrame con metricas de cavidades.
    """
    results_path = Path(results_dir)
    rows = []

    # Buscar archivos CSV
    for csv_file in results_path.rglob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            # Estandarizar nombres de columnas
            cols = {c.lower(): c for c in df.columns}
            if "area" in cols or "area_sa" in cols or "surface" in str(df.columns).lower():
                return df
            rows = df.to_dict("records")
            break
        except Exception:
            continue

    # Buscar archivos de texto con datos de cavidades
    if not rows:
        for txt_file in results_path.rglob("*.txt"):
            try:
                content = txt_file.read_text(encoding="utf-8", errors="ignore")
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith("//"):
                        continue
                    # Intentar parsear como tabla (espacios/tabs)
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

    if not rows:
        return pd.DataFrame(columns=["pocket_id", "volume", "area", "depth"])

    return pd.DataFrame(rows)


def filter_cavities_by_volume(
    cavities_df: pd.DataFrame,
    volume_threshold: float = 50.0,
    volume_col: str = "volume",
) -> pd.DataFrame:
    if volume_col not in cavities_df.columns:
        return cavities_df.copy()
    return cavities_df[cavities_df[volume_col] >= volume_threshold].copy()


def filter_cavities_by_area(
    cavities_df: pd.DataFrame,
    area_threshold: float = 10.0,
    area_col: str = "area",
) -> pd.DataFrame:
    if area_col not in cavities_df.columns:
        return cavities_df.copy()
    return cavities_df[cavities_df[area_col] >= area_threshold].copy()


def pipeline_castpfold_rubisco(
    pdb_path: str,
    specificity: Optional[float] = None,
    group: Optional[str] = None,
    volume_threshold: float = 50.0,
    probe_radius: float = 1.4,
    output_dir: Optional[str] = None,
) -> pd.DataFrame:
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
