#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modulo AI.zymes — herramientas del pipeline de diseño evolutivo de enzimas.

Basado en: Merlicek et al. (2025), Angew. Chem. Int. Ed.
DOI: 10.1002/anie.202507031
Repo: https://github.com/bunzela/AIzymes

Incluye:
- ESMFold: prediccion de estructura desde secuencia
- Seleccion de Boltzmann: optimizacion multiobjetivo
- Utilidades para campos electricos (FieldTools)
- Ciclo de diseño evolutivo
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Callable

import numpy as np
import pandas as pd


# =============================================================================
# ESMFold — Prediccion de estructura desde secuencia
# =============================================================================

def predict_structure_esmfold(
    sequence: str,
    output_path: Optional[str] = None,
    model_name: str = "esmfold_v1",
) -> str:
    """
    Predice la estructura 3D de una proteina usando ESMFold.

    Args:
        sequence: Secuencia de aminoacidos (string).
        output_path: Ruta para guardar el PDB resultante. Si None, archivo temporal.
        model_name: Nombre del modelo ESMFold.

    Returns:
        Ruta al archivo PDB generado.
    """
    import torch
    import esm

    model = getattr(esm.pretrained, model_name)()
    model = model.eval().cuda()

    with torch.no_grad():
        output = model.infer_pdb(sequence)

    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".pdb", prefix="esmfold_")
        os.close(fd)

    with open(output_path, "w") as f:
        f.write(output)

    return output_path


def predict_batch_esmfold(
    sequences: dict[str, str],
    output_dir: str,
    resume: bool = True,
) -> dict[str, str]:
    """
    Predice estructuras para multiples secuencias.

    Args:
        sequences: Dict {nombre: secuencia}.
        output_dir: Directorio para guardar PDBs.
        resume: Si True, salta secuencias ya procesadas.

    Returns:
        Dict {nombre: ruta_pdb}.
    """
    import torch
    import esm

    model = esm.pretrained.esmfold_v1()
    model = model.eval().cuda()

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    results = {}

    for name, seq in sequences.items():
        pdb_path = os.path.join(output_dir, f"{name}.pdb")
        if resume and os.path.exists(pdb_path):
            results[name] = pdb_path
            continue

        with torch.no_grad():
            output = model.infer_pdb(seq)

        with open(pdb_path, "w") as f:
            f.write(output)

        results[name] = pdb_path

    return results


# =============================================================================
# Seleccion de Boltzmann — Optimizacion multiobjetivo
# =============================================================================

def boltzmann_score(
    affinity: float,
    stability: float,
    electric_field: float,
    weights: Optional[dict[str, float]] = None,
) -> float:
    """
    Calcula score combinado para seleccion de Boltzmann.

    Args:
        affinity: Afinidad al estado de transicion (mayor = mejor).
        stability: Estabilidad termodinamica (mayor = mejor).
        electric_field: Campo electrico en sitio activo (mayor = mejor).
        weights: Pesos para cada componente. Default: {affinity: 0.4, stability: 0.3, electric_field: 0.3}.

    Returns:
        Score combinado.
    """
    if weights is None:
        weights = {"affinity": 0.4, "stability": 0.3, "electric_field": 0.3}

    score = (
        weights["affinity"] * affinity +
        weights["stability"] * stability +
        weights["electric_field"] * electric_field
    )
    return score


def boltzmann_selection(
    scores: np.ndarray,
    temperature: float,
) -> np.ndarray:
    """
    Seleccion probabilistica de Boltzmann.

    Args:
        scores: Array de scores (mayor = mejor).
        temperature: Temperatura de seleccion (alta = mas exploracion).

    Returns:
        Probabilidades de seleccion (suman 1).
    """
    if temperature <= 0:
        # Seleccion greedy: el mejor gana
        probs = np.zeros_like(scores)
        probs[np.argmax(scores)] = 1.0
        return probs

    # Normalizar scores para evitar overflow
    scores = np.asarray(scores, dtype=np.float64)
    scores = scores - np.max(scores)
    exp_scores = np.exp(scores / temperature)
    probs = exp_scores / np.sum(exp_scores)

    return probs


def boltzmann_optimization_loop(
    population: pd.DataFrame,
    score_fn: Callable[[pd.DataFrame], np.ndarray],
    n_iterations: int = 50,
    t_initial: float = 10.0,
    t_final: float = 0.1,
    n_select: int = 10,
    mutate_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
) -> list[dict]:
    """
    Ciclo de optimizacion con seleccion de Boltzmann.

    Args:
        population: DataFrame con variantes iniciales.
        score_fn: Funcion que calcula scores para cada variante.
        n_iterations: Numero de iteraciones.
        t_initial: Temperatura inicial.
        t_final: Temperatura final.
        n_select: Numero de variantes a seleccionar por iteracion.
        mutate_fn: Funcion para generar mutantes de las variantes seleccionadas.

    Returns:
        Lista de registros por iteracion {iter, best_score, mean_score, temp}.
    """
    history = []
    current_pop = population.copy()

    for i in range(n_iterations):
        # Temperatura decreciente (schedule lineal)
        t = t_initial - (t_initial - t_final) * (i / n_iterations)

        # Calcular scores
        scores = score_fn(current_pop)

        # Seleccion de Boltzmann
        probs = boltzmann_selection(scores, t)

        # Seleccionar top variantes
        indices = np.random.choice(
            len(current_pop),
            size=min(n_select, len(current_pop)),
            p=probs,
        )
        selected = current_pop.iloc[indices]

        # Mutar y agregar al pool
        if mutate_fn is not None:
            mutants = mutate_fn(selected)
            current_pop = pd.concat([current_pop, mutants], ignore_index=True)

        # Limitar tamanio del pool
        if len(current_pop) > 500:
            current_pop = current_pop.tail(500)

        history.append({
            "iter": i,
            "best_score": float(np.max(scores)),
            "mean_score": float(np.mean(scores)),
            "temp": float(t),
        })

    return history


# =============================================================================
# FieldTools — Campos electricos en sitio activo
# =============================================================================

def calculate_electric_field(
    pdb_path: str,
    site_residues: list[str],
    output_dir: Optional[str] = None,
) -> dict:
    """
    Calcula campo electrico en el sitio activo usando APBS + FieldTools.

    Args:
        pdb_path: Ruta al archivo PDB.
        site_residues: Lista de residuos del sitio activo (ej: ["LYS166", "ASP194"]).
        output_dir: Directorio para resultados.

    Returns:
        Dict con magnitud y direccion del campo electrico.
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="efield_")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Paso 1: Generar PQR con pdb2pqr
    pqr_path = os.path.join(output_dir, Path(pdb_path).stem + ".pqr")
    subprocess.run(
        ["pdb2pqr30", "--ff=AMBER", pdb_path, pqr_path],
        capture_output=True, text=True,
    )

    # Paso 2: Correr APBS
    apbs_input = os.path.join(output_dir, "apbs.in")
    with open(apbs_input, "w") as f:
        f.write(f"""read
    mol pqr {pqr_path}
end
elec name pb
    mg-auto
    dime 129 129 129
    glen 20 20 20
    mol 1
    lpbe
    bcfl mdh
    sdens 10.0
    srad 1.4
    swin 0.3
    temp 298.15
    pdie 2.0
    sdie 78.5
    chgm spl2
    ion charge 1.0 conc 0.150 radius 2.0
    ion charge -1.0 conc 0.150 radius 2.0
end
print elec pb pot dx {os.path.join(output_dir, "pot.dx")}
quit""")

    subprocess.run(["apbs", apbs_input], capture_output=True, text=True)

    # Paso 3: Calcular campo electrico en residuos del sitio activo
    # (Simplificado: magnitud promedio del gradiente de potencial)
    dx_path = os.path.join(output_dir, "pot.dx")
    if os.path.exists(dx_path):
        # Leer mapa de potencial y calcular gradiente
        field_magnitude = _estimate_field_from_dx(dx_path, site_residues, pqr_path)
    else:
        field_magnitude = np.nan

    return {
        "pdb": Path(pdb_path).stem,
        "site_residues": site_residues,
        "field_magnitude": field_magnitude,
        "output_dir": output_dir,
    }


def _estimate_field_from_dx(dx_path: str, site_residues: list[str], pqr_path: str) -> float:
    """
    Estimacion simplificada del campo electrico desde un archivo DX de APBS.

    En produccion, usar FieldTools de AI.zymes para calculo preciso.
    """
    try:
        # Leer valores del mapa de potencial
        with open(dx_path, "r") as f:
            lines = f.readlines()

        # Extraer valores de potencial (simplificado)
        potentials = []
        for line in lines:
            parts = line.strip().split()
            for p in parts:
                try:
                    potentials.append(float(p))
                except ValueError:
                    continue

        if len(potentials) < 2:
            return np.nan

        # Campo electrico ~ gradiente del potencial
        potentials = np.array(potentials)
        field = np.abs(np.gradient(potentials)).mean()
        return float(field)

    except Exception:
        return np.nan


# =============================================================================
# Utilidades para ciclo de diseño evolutivo
# =============================================================================

def generate_variant_pool(
    reference_seq: str,
    n_variants: int = 100,
    mutation_rate: float = 0.05,
) -> pd.DataFrame:
    """
    Genera un pool de variantes por mutacion aleatoria.

    Args:
        reference_seq: Secuencia de referencia.
        n_variants: Numero de variantes a generar.
        mutation_rate: Probabilidad de mutacion por residuo.

    Returns:
        DataFrame con variantes {id, sequence, mutations}.
    """
    amino_acids = "ACDEFGHIKLMNPQRSTVWY"
    variants = []

    for i in range(n_variants):
        seq = list(reference_seq)
        mutations = []
        for j in range(len(seq)):
            if np.random.random() < mutation_rate:
                original = seq[j]
                new_aa = np.random.choice(list(amino_acids.replace(original, "")))
                seq[j] = new_aa
                mutations.append(f"{original}{j+1}{new_aa}")

        variants.append({
            "id": f"var_{i:04d}",
            "sequence": "".join(seq),
            "mutations": ";".join(mutations) if mutations else "none",
            "n_mutations": len(mutations),
        })

    return pd.DataFrame(variants)


def evaluate_variant(
    variant: dict,
    structure_path: Optional[str] = None,
    metrics: Optional[list[str]] = None,
) -> dict:
    """
    Evalua una variante individual.

    Args:
        variant: Dict con info de la variante.
        structure_path: Ruta a la estructura predicha (opcional).
        metrics: Lista de metricas a calcular.

    Returns:
        Dict con metricas evaluadas.
    """
    if metrics is None:
        metrics = ["affinity", "stability", "electric_field"]

    result = {"id": variant["id"], "sequence": variant["sequence"]}

    # Placeholder: en produccion, calcular metricas reales
    if "affinity" in metrics:
        result["affinity"] = np.random.normal(0.5, 0.1)
    if "stability" in metrics:
        result["stability"] = np.random.normal(-50.0, 5.0)
    if "electric_field" in metrics:
        result["electric_field"] = np.random.normal(0.03, 0.005)

    return result
