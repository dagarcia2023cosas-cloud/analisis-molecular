# Project Context for AI Agents

## Project

- **Name:** analisismolecular
- **Package:** libreria_analisismolecular
- **Type:** Computational chemistry / molecular analysis
- **Colab integration:** Native support for Google Colab

## Structure

- `src/libreria_analisismolecular/` — Main package
- `notebooks/` — Colab-ready Jupyter notebooks
- `colab/` — Standalone Colab setup scripts
- `data/raw/`, `data/processed/`, `data/external/` — Data directories
- `tests/` — Pytest tests

## Key Dev Commands

- Install: `pip install -e .`
- Full env: `conda env create -f environment.yml`
- Tests: `pytest tests/`
- If npm is needed ALWAYS use pnpm
- No linter/typecheck configured yet

## Dependencies

- rdkit, openbabel (cheminformatics)
- py3Dmol, nglview (3D visualization)
- mdanalysis, prody, biopython (MD analysis)
- numpy, scipy, pandas, matplotlib, seaborn, scikit-learn
- torch (optional ML)
