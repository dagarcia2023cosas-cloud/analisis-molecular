# Plan de Aprendizaje — analisismolecular + AI.zymes

## Estructura: de lo mas simple a lo mas complejo

### Nivel 1 — Exploracion y visualizacion
| Sesion | Objetivo | Notebook | Estado |
|--------|----------|----------|--------|
| **1.1** | Setup en Colab: clonar repo, instalar TODAS las deps (AI.zymes, CASTpFold, ESMFold, APBS) | `00_setup.ipynb` | ⬜ |
| **1.2** | Obtener PDBs de RuBisCO (G-I a G-IV), visualizar con py3Dmol | `01_intro.ipynb` | ⬜ |
| **1.3** | Flujo completo VS Code → GitHub → Colab → Drive | `02_workflow.ipynb` | ⬜ |

### Nivel 2 — Analisis de cavidades (CASTpFold)
| Sesion | Objetivo | Notebook | Estado |
|--------|----------|----------|--------|
| **2.1** | Correr CASTpFold sobre PDBs de RuBisCO, interpretar resultados | `03_cavidades.ipynb` | ⬜ |
| **2.2** | APBS: electrostatica de cavidades, filtrar por carga positiva | `03_cavidades.ipynb` | ⬜ |
| **2.3** | Correlacion area/volumen de cavidad vs S (reproducir Poudel) | `03_cavidades.ipynb` | ⬜ |

### Nivel 3 — Herramientas AI.zymes
| Sesion | Objetivo | Notebook | Estado |
|--------|----------|----------|--------|
| **3.1** | ESMFold: predecir estructura desde secuencia de RuBisCO | `04_esmfold.ipynb` | ⬜ |
| **3.2** | ProteinMPNN: rediseñar scaffold de RuBisCO | `05_proteinmpnn.ipynb` | ⬜ |
| **3.3** | FieldTools: campos electricos en sitio activo | `06_fieldtools.ipynb` | ⬜ |

### Nivel 4 — Integracion (pipeline AI.zymes)
| Sesion | Objetivo | Notebook | Estado |
|--------|----------|----------|--------|
| **4.1** | Seleccion de Boltzmann: implementar desde cero, multiobjetivo | `07_boltzmann.ipynb` | ⬜ |
| **4.2** | Diseño evolutivo minimo para RuBisCO (ciclos iterativos) | `07_boltzmann.ipynb` | ⬜ |
| **4.3** | Pipeline completo: ESMFold → CASTpFold → FieldTools → Boltzmann → ProteinMPNN | `08_pipeline.ipynb` | ⬜ |

### Nivel 5 — Cierre
| Sesion | Objetivo | Estado |
|--------|----------|--------|
| **5.1** | Documentacion final, bitacora, proyeccion a tesis | ⬜ |

---

## Dependencias por nivel

| Nivel | Dependencias clave |
|-------|-------------------|
| 1 | numpy, pandas, matplotlib, py3Dmol, biopython, prody |
| 2 | castpfoldpy, APBS, pdb2pqr, freesasa |
| 3 | fair-esm, torch, transformers, ProteinMPNN, aizymes (FieldTools) |
| 4 | aizymes, PyRosetta (opcional) |

## Flujo de trabajo

```
VS Code (interfaz)  →  Google Colab (GPU)  →  GitHub (respaldo)
   escribir codigo       correr analisis        versionado
   editar notebooks      visualizar resultados  portabilidad
```

## Mecanicas fijas

- **Bitacora:** 3 lineas al final de cada sesion en `bitacora.md`
- **Termo intercalada:** solo lo necesario, en el momento justo
- **Criterio de avance:** no pasar de nivel sin entender el anterior

---

*Plan actualizado: Mayo 2026 — Integracion con AI.zymes + CASTpFold*
