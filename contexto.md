# Contexto — Proyecto RuBisCO

## Objetivo
Estudiar las variables que afectan la eficiencia enzimatica de las distintas familias de RuBisCO, utilizando el pipeline de AI.zymes como referencia metodologica. Meta a largo plazo: potencial tesis.

## Estado actual
**Reestructurado el 23/05/2026.** Integracion con AI.zymes + CASTpFold. 9 notebooks listos (00-08).

## Estructura del proyecto

```
rubisco/
├── README.md              ← Que es, flujo VS Code→Colab→GitHub, 3 pasos para empezar
├── PLAN.md                ← Plan de aprendizaje (5 niveles, vinculado a notebooks)
├── bitacora.md            ← Registro de sesiones
├── contexto.md            ← Este archivo
│
├── papers/
│   ├── ayzmes_2025.md     ← Resumen AI.zymes (Merlicek 2025)
│   └── poudel_2020.md     ← Resumen Poudel 2020 (cavidades cationicas)
│
├── src/libreria_analisismolecular/
│   ├── __init__.py
│   ├── cavidades.py       ← APBS, electrostatica (fpocket legacy)
│   ├── castpfold.py       ← CASTpFold: analisis de cavidades (nuevo)
│   ├── ai_zymes.py        ← ESMFold, Boltzmann, FieldTools (nuevo)
│   ├── utils.py           ← utilidades generales
│   └── colab/
│       ├── __init__.py
│       ├── drive.py       ← montar Drive, guardar/cargar resultados
│       └── viz.py         ← visualizacion molecular 3D
│
├── notebooks/
│   ├── 00_setup.ipynb     ← Setup completo: AI.zymes + CASTpFold + ESMFold + APBS
│   ├── 01_intro.ipynb     ← PDBs de RuBisCO, visualizacion py3Dmol
│   ├── 02_workflow.ipynb  ← Flujo VS Code→Colab→GitHub→Drive
│   ├── 03_cavidades.ipynb ← CASTpFold: cavidades vs S (Poudel)
│   ├── 04_esmfold.ipynb   ← ESMFold: prediccion de estructura
│   ├── 05_proteinmpnn.ipynb ← ProteinMPNN: rediseño de scaffold
│   ├── 06_fieldtools.ipynb ← FieldTools: campos electricos
│   ├── 07_boltzmann.ipynb ← Seleccion de Boltzmann multiobjetivo
│   └── 08_pipeline.ipynb  ← Pipeline completo AI.zymes
│
├── scripts/
│   ├── dev_setup.ps1
│   └── sync_to_colab.py
│
├── tests/
│   ├── __init__.py
│   └── test_colab.py
│
├── pyproject.toml
├── requirements.txt
├── environment.yml
├── opencode.json
└── .gitignore
```

## Papers base

| Paper | Resumen | Relevancia |
|---|---|---|
| AI.zymes (Merlicek 2025) | `papers/ayzmes_2025.md` | Pipeline de diseño evolutivo de enzimas |
| Poudel 2020 | `papers/poudel_2020.md` | Cavidades cationicas y especificidad en RuBisCO |
| CASTpFold (Ye 2024) | NAR, 52(W1), W194-W199 | Analisis de cavidades (reemplaza fpocket) |

## Flujo de trabajo

```
VS Code (interfaz)  →  Google Colab (GPU)  →  GitHub (respaldo)
   escribir codigo       correr analisis        versionado
   editar notebooks      visualizar resultados  portabilidad
```

## Pipeline AI.zymes

```
Secuencia → ESMFold → CASTpFold → FieldTools → Boltzmann → ProteinMPNN → (iterar)
```

| Herramienta | Funcion |
|---|---|
| ESMFold | Prediccion de estructura desde secuencia |
| CASTpFold | Analisis de cavidades y bolsillos |
| FieldTools | Campos electricos en sitio activo |
| Boltzmann | Seleccion multiobjetivo (afinidad + estabilidad + campo E) |
| ProteinMPNN | Rediseño de scaffold |
| PyRosetta | RosettaRelax/Design (opcional, pesado) |

## Plan de aprendizaje

5 niveles (ver `PLAN.md`):
1. Exploracion y visualizacion (notebooks 00-02)
2. Analisis de cavidades con CASTpFold (notebook 03)
3. Herramientas AI.zymes: ESMFold, ProteinMPNN, FieldTools (notebooks 04-06)
4. Integracion: Boltzmann + pipeline completo (notebooks 07-08)
5. Cierre (documentacion, proyeccion a tesis)

## Ultimo trabajo realizado
Actualizacion completa del proyecto (23/05/2026):
- Integracion con pipeline AI.zymes
- CASTpFold reemplaza a fpocket para analisis de cavidades
- 9 notebooks (00-08) con flujo completo
- Nuevos modulos: `castpfold.py`, `ai_zymes.py`
- `pyproject.toml` actualizado con dependencias AI.zymes
- PLAN.md reescrito con 5 niveles

## Proximos pasos
- Iniciar Sesion 1.1: Setup en Colab con `00_setup.ipynb`
- Completar Nivel 1: exploracion y visualizacion
- Ir desarrollando notebooks para Nivel 2 (cavidades con CASTpFold)

---

*Ultima actualizacion: 23/05/2026 — Integracion AI.zymes + CASTpFold*
