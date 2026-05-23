# Contexto — Proyecto RuBisCO

## Objetivo
Estudiar las variables que afectan la eficiencia enzimatica de las familias de RuBisCO, usando el pipeline de AIzymes como base metodologica. Meta a largo plazo: potencial tesis.

## Estado actual
**Integracion con AIzymes.** Setup simplificado (solo pip, sin condacolab). Dos pipelines alternativos: CASTpFold vs fpocket.

## Estructura

```
rubisco/
├── README.md
├── PLAN.md
├── bitacora.md
├── contexto.md
│
├── papers/
│   ├── ayzmes_2025.md         ← AIzymes (Merlicek 2025)
│   └── poudel_2020.md         ← Poudel 2020 (cavidades)
│
├── src/libreria_analisismolecular/
│   ├── __init__.py
│   ├── castpfold.py           ← CASTpFold wrapper (requests directo)
│   ├── cavidades.py           ← Legacy: fpocket + APBS
│   ├── utils.py
│   └── colab/
│       ├── __init__.py
│       ├── drive.py
│       └── viz.py
│
├── notebooks/
│   ├── 00_setup.ipynb         ← Setup: AIzymes + nuestro repo (solo pip)
│   ├── 01_pipeline_castpfold.ipynb ← Pipeline con CASTpFold
│   ├── 01_pipeline_fpocket.ipynb   ← Pipeline con fpocket
│   └── legacy/                ← Notebooks viejos (respaldo)
│
├── pyproject.toml             ← Dependencias simplificadas
├── requirements.txt
└── .gitignore
```

## Pipeline AIzymes + CASTpFold/fpocket

```
Secuencia → ESMFold → cavidades → FieldTools → Boltzmann → ProteinMPNN → (iterar x5)
```

| Herramienta | Fuente |
|---|---|
| ESMFold | `aizymes.design_ESMfold_001` (AIzymes) |
| CASTpFold | `castpfold.py` (nuestro, via requests) |
| fpocket | conda forge (alternativo) |
| FieldTools | `aizymes.FieldTools` (AIzymes) |
| Boltzmann | Implementacion propia (algoritmo) |
| ProteinMPNN | `aizymes.design_MPNN_001` (AIzymes) |

## Dos pipelines alternativos

| Notebook | Cavidades | Instalacion |
|---|---|---|
| `01_pipeline_castpfold.ipynb` | CASTpFold | Solo pip |
| `01_pipeline_fpocket.ipynb` | fpocket | pip + condacolab |

## Proximos pasos
- Ejecutar `00_setup.ipynb` en Colab
- Correr uno de los dos pipelines (CASTpFold recomendado)
- Comparar metricas de cavidades (CASTpFold vs fpocket vs Poudel 2020)

---

*Ultima actualizacion: 23/05/2026 — AIzymes real + CASTpFold/fpocket*
