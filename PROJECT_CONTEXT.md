# Contexto General del Proyecto: analisismolecular

## Visión General

Plataforma de análisis molecular computacional que integra desarrollo local en **VS Code** con ejecución en **Google Colab** (GPU/TPU), sincronizado vía **GitHub**.

El objetivo es tener un entorno donde:
- Se desarrolla el código localmente (VS Code)
- Se ejecutan análisis pesados en la nube (Colab)
- Los datos y resultados persisten (Google Drive + GitHub)
- Todo está documentado para cualquier agente IA o colaborador

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.10+ |
| Paquete | `libreria_analisismolecular` |
| Química computacional | RDKit, OpenBabel, py3Dmol, MDAnalysis |
| Visualización | py3Dmol, nglview, matplotlib, seaborn, plotly |
| ML (opcional) | PyTorch, scikit-learn |
| Editor | VS Code con extensiones recomendadas |
| Nube | Google Colab + Google Drive |
| Control de versiones | GitHub |
| CI/CD | Por definir (GitHub Actions) |

## Estructura del Proyecto

```
analisismolecular/
├── src/libreria_analisismolecular/   # Paquete Python principal
│   ├── utils.py                      # Utilidades generales
│   └── colab/                        # Módulo de integración Colab
│       ├── setup.py                  # Detectar Colab, instalar deps
│       ├── drive_utils.py            # Montar Drive, guardar/cargar
│       └── visualization.py          # Visualización 3D de moléculas
├── notebooks/                        # Notebooks listos para Colab
│   ├── 00_colab_setup.ipynb          # Setup inicial
│   ├── 01_molecular_analysis_intro.ipynb  # Intro al análisis
│   └── 02_vscode_colab_workflow.ipynb     # Flujo completo VS Code+Colab
├── colab/                            # Scripts standalone para Colab
│   └── setup_colab.py                # Configuración autónoma
├── scripts/                          # Utilidades de desarrollo
│   ├── sync_to_colab.py              # Genera celdas para Colab
│   └── dev_setup.ps1                 # Setup local automático
├── uploads/                          # Archivos que sube el usuario
├── data/                             # Datos del proyecto
│   ├── raw/                          # Datos crudos (ignorados por git)
│   ├── processed/                    # Datos procesados
│   └── external/                     # Datos externos de referencia
├── tests/                            # Tests unitarios (pytest)
├── .vscode/                          # Config de VS Code compartida
├── docs/                             # Documentación
│   └── WORKFLOW.md                   # Flujo de trabajo detallado
├── .agents/AGENTS.md                 # Contexto para agentes IA
├── pyproject.toml                    # Config del paquete
├── requirements.txt                  # Dependencias pip
├── environment.yml                   # Entorno conda completo
└── PROJECT_CONTEXT.md                # Este archivo
```

## Lo que ya tenemos (MVP)

- [x] Paquete Python instalable (`libreria_analisismolecular`)
- [x] Integración con Colab (setup, Drive, visualización)
- [x] Config de VS Code (settings, tasks, debug, extensions)
- [x] Scripts de sincronización local ↔ Colab
- [x] Notebooks de ejemplo listos para Colab
- [x] Proyecto en GitHub
- [x] `.agents/AGENTS.md` con contexto para IA

## Lo que sigue (Roadmap)

### Fase 1 — Análisis molecular básico
- [ ] Carga y visualización de moléculas (SDF, PDB, MOL)
- [ ] Cálculo de descriptores moleculares (MW, LogP, HBA, HBD, etc.)
- [ ] Generación de huellas (fingerprints) Morgan, MACCS
- [ ] Similitud molecular (Tanimoto, Dice)

### Fase 2 — Análisis avanzado
- [ ] Alineamiento molecular
- [ ] Docking molecular (con AutoDock Vina u OpenBabel)
- [ ] Dinámica molecular (MDAnalysis)
- [ ] Visualización 3D interactiva en notebooks

### Fase 3 — Machine Learning
- [ ] Modelos QSAR/QSPR con scikit-learn
- [ ] Redes neuronales con PyTorch
- [ ] Embeddings moleculares
- [ ] Clustering de compuestos

### Fase 4 — Producción
- [ ] GitHub Actions (tests automáticos, linting)
- [ ] Documentación con Sphinx o MkDocs
- [ ] PyPI (publicar el paquete)

## Flujo de Trabajo

```
┌─────────────────────────────────────────────────────┐
│                   VS Code (local)                    │
│  Editar código → Correr tests → Commit + Push       │
└──────────────────────┬──────────────────────────────┘
                       │ git push
                       ▼
┌─────────────────────────────────────────────────────┐
│                   GitHub                             │
│  Repositorio central del proyecto                   │
└──────────────────────┬──────────────────────────────┘
                       │ git clone / git pull
                       ▼
┌─────────────────────────────────────────────────────┐
│                Google Colab (nube)                   │
│  Clonar repo → Instalar deps → Ejecutar análisis    │
│  Guardar resultados en Drive o subir a GitHub       │
└─────────────────────────────────────────────────────┘
```

## Cómo usar este proyecto

### Local (VS Code)
```bash
code C:\PROYECTOS_UDEC\analisismolecular
.venv\Scripts\Activate.ps1
pytest tests/ -v
```

### Colab
Subir `notebooks/00_colab_setup.ipynb` a Colab y ejecutar.

### Subir archivos para procesar
Poner los archivos en la carpeta `uploads/` y pedir su procesamiento.

---

*Última actualización: Mayo 2026*
