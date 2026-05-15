#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
import tempfile
import shutil
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns


def run_fpocket(
    pdb_path: str,
    output_dir: Optional[str] = None,
    fpocket_bin: str = "fpocket",
) -> str:
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="fpocket_")
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    cmd = [fpocket_bin, "-f", pdb_path, "-o", output_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"fpocket failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return output_dir


def parse_fpocket_pockets(fpocket_dir: str) -> pd.DataFrame:
    fp_dir = Path(fpocket_dir)
    info_files = sorted(fp_dir.glob("*_info.json"))
    pockets = []
    for info_path in info_files:
        with open(info_path) as f:
            data = json.load(f)
        pockets.append(
            {
                "pocket_id": data.get("pocket_id", info_path.stem),
                "score": data.get("score", np.nan),
                "area": data.get("area", np.nan),
                "volume": data.get("volume", np.nan),
                "mean_charge": data.get("mean_charge", np.nan),
                "num_vertices": data.get("num_vertices", np.nan),
                "residues": data.get("residues", []),
            }
        )
    return pd.DataFrame(pockets)


def run_apbs(
    pdb_path: str,
    pqr_path: Optional[str] = None,
    apbs_bin: str = "apbs",
    pdb2pqr_bin: str = "pdb2pqr30",
) -> str:
    workdir = Path(tempfile.mkdtemp(prefix="apbs_"))
    pdb_file = Path(pdb_path)

    if pqr_path is None:
        pqr_path = str(workdir / f"{pdb_file.stem}.pqr")
        cmd_pqr = [pdb2pqr_bin, "--ff=AMBER", pdb_path, pqr_path]
        result = subprocess.run(cmd_pqr, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"pdb2pqr failed:\n{result.stderr}")

    apbs_input = str(workdir / "apbs.in")
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
print elec pb pot dx {workdir / "pot.dx"}
quit""")

    cmd_apbs = [apbs_bin, str(apbs_input)]
    result = subprocess.run(cmd_apbs, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"APBS failed:\n{result.stderr}")
    return str(workdir)


def filter_cavities_by_charge(
    pockets_df: pd.DataFrame,
    charge_threshold: float = 0.0,
    charge_col: str = "mean_charge",
) -> pd.DataFrame:
    return pockets_df[pockets_df[charge_col] > charge_threshold].copy()


def calculate_surface_area_per_cavity(pockets_df: pd.DataFrame) -> pd.DataFrame:
    df = pockets_df.copy()
    df["surface_area"] = df["area"]
    return df


def plot_area_vs_s(
    pockets_df: pd.DataFrame,
    specificity_values: Optional[dict[str, float]] = None,
    group_labels: Optional[dict[str, str]] = None,
    title: str = "Area de cavidad vs Especificidad CO2/O2",
    save_path: Optional[str] = None,
) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=pockets_df,
        x="area",
        y="S_rel",
        hue="group" if "group" in pockets_df.columns else None,
        style="group" if "group" in pockets_df.columns else None,
        s=100,
        ax=ax,
    )
    ax.set_xlabel("Area de cavidad ($\AA^2$)")
    ax.set_ylabel("Especificidad CO$_2$/O$_2$ (S)")
    ax.set_title(title)
    ax.legend(title="Grupo")
    sns.despine()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def pipeline_cavidades_rubisco(
    pdb_path: str,
    specificity: Optional[float] = None,
    group: Optional[str] = None,
    charge_filter: bool = True,
    charge_threshold: float = 0.0,
) -> pd.DataFrame:
    fpocket_dir = run_fpocket(pdb_path)
    pockets = parse_fpocket_pockets(fpocket_dir)

    pockets = calculate_surface_area_per_cavity(pockets)

    if charge_filter:
        apbs_dir = run_apbs(pdb_path)
        pockets = filter_cavities_by_charge(pockets, charge_threshold)

    if specificity is not None:
        pockets["S_rel"] = specificity
    if group is not None:
        pockets["group"] = group

    return pockets
