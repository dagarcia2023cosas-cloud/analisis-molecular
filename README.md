# analisismolecular

Proyecto de análisis molecular computacional con integración nativa para Google Colab.

## Estructura del proyecto

```
analisismolecular/
├── src/
│   └── libreria_analisismolecular/   # Paquete principal
│       ├── __init__.py
│       ├── utils.py                  # Utilidades generales
│       └── colab/                    # Integración con Google Colab
│           ├── __init__.py
│           ├── setup.py              # Configuración del entorno Colab
│           ├── drive_utils.py        # Montaje y uso de Google Drive
│           └── visualization.py      # Visualización molecular 3D
├── colab/
│   └── setup_colab.py               # Script autónomo para Colab
├── notebooks/
│   ├── 00_colab_setup.ipynb          # Setup inicial para Colab
│   └── 01_molecular_analysis_intro.ipynb  # Introducción al análisis
├── data/
│   ├── raw/                          # Datos crudos
│   ├── processed/                    # Datos procesados
│   └── external/                     # Datos externos
├── tests/
│   └── test_colab.py
├── requirements.txt
├── environment.yml
├── pyproject.toml
└── .gitignore
```

## Uso en Google Colab

### Opción 1: Notebook de setup (recomendada)

1. Sube el notebook `notebooks/00_colab_setup.ipynb` a Google Colab
2. Ejecuta las celdas en orden

### Opción 2: Script directo

En una celda de Colab:

```python
!wget -q https://raw.githubusercontent.com/tu-usuario/analisismolecular/main/colab/setup_colab.py
from setup_colab import setup
setup(install_full=True)
```

### Opción 3: Instalación manual

```python
!git clone https://github.com/tu-usuario/analisismolecular.git /content/analisismolecular
%cd /content/analisismolecular
!pip install -q -e .
!pip install -q py3Dmol nglview plotly ipywidgets prody biopython rdkit-pypi
```

## Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/analisismolecular.git
cd analisismolecular

# Opción 1: pip
pip install -e .

# Opción 2: conda (recomendada para RDKit)
conda env create -f environment.yml
conda activate analisismolecular
```

## Dependencias principales

- **RDKit** — Cheminformatics y química computacional
- **OpenBabel** — Interconversión de formatos moleculares
- **py3Dmol / nglview** — Visualización 3D de moléculas
- **MDAnalysis / ProDy** — Análisis de dinámica molecular
- **PyTorch** — Deep learning (opcional)
- **NumPy, SciPy, Pandas** — Cómputo científico
- **Matplotlib, Seaborn, Plotly** — Visualización de datos

## Licencia

MIT
