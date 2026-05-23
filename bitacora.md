# Bitacora de Aprendizaje — analisismolecular

## Formato
```
### Sesion X.X — [titulo] — [fecha]
**Aprendi:** 
**No entendi:** 
**Sigue:** 
```

---

### Sesion 1.0 — Setup y reestructuracion con AIzymes real + CASTpFold/fpocket — 23/05/2026

**Objetivo de la sesion:** Configurar el entorno en Google Colab para que el pipeline de diseño evolutivo de RuBisCO funcione con pocos ciclos (5-10). Basarnos en el codigo real de AIzymes (Merlicek 2025) y comparar dos herramientas de cavidades: CASTpFold y fpocket.

---

#### Lo que se hizo

1. **Setup inicial con dependencias (muchos intentos fallidos):**
   - El notebook `00_setup.ipynb` original intentaba instalar todo con `pip install -e .` (leyendo `pyproject.toml`) mas paquetes extras.
   - **Problemas encontrados y resueltos uno por uno:**
     - `castpfoldpy>=3.0` no existe en PyPI. La version real es `0.1.2`.
     - `rdkit-pypi` fue renombrado a `rdkit` (directamente desde pip).
     - `pandas>=2.0` instalaba pandas 3.0.3, que es incompatible con `google-colab` (requiere `pandas==2.2.2` exacto). Solucion: sacar pandas de las dependencias — Colab ya lo trae instalado.
     - `castpfoldpy` requiere Python >=3.12, pero Colab con GPU T4 usa Python 3.10/3.11. Solucion: **reescribir `castpfold.py`** para llamar a la API web de CASTpFold directamente con `requests`, sin depender del paquete `castpfoldpy`.
     - `condacolab` (necesario para instalar APBS/pdb2pqr/freesasa via conda) tenia conflictos de version de Python. APBS y pdb2pqr se lograron instalar. freesasa resulto ser un modulo Python sin binario CLI (`import freesasa`), no un ejecutable. No es critico.

2. **Descubrimiento clave: AIzymes NO es un notebook paso a paso.**
   - Al examinar el repositorio real `bunzela/AIzymes` y su `Example_KSI.ipynb`, entendimos que AIzymes es un **orquestador de cluster HPC**:
     - Usa `AIzymes_MAIN` + `submit_controller()` para enviar cientos de trabajos a SLURM.
     - Requiere 4 GPUs, 450 GB RAM, Rosetta con licencia.
     - **No se puede ejecutar completo en Google Colab** (1 GPU T4, 12 GB RAM, sin SLURM).
   - **Pero sus modulos individuales SI funcionan en Colab:**
     - `design_ESMfold_001` → prediccion de estructura (ESMFold, fair-esm)
     - `design_MPNN_001` → rediseño de scaffold (ProteinMPNN)
     - `FieldTools` → campos electricos en sitio activo
     - `scoring_efields_001` → scoring para seleccion de Boltzmann

3. **Que es condacolab y cuando se necesita:**
   - `condacolab` instala el gestor de paquetes `conda` dentro de Google Colab.
   - Colab normalmente solo tiene `pip`. Con condacolab, ademas podes instalar paquetes de `conda-forge`.
   - **NO es necesario para AIzymes** (se instala con pip).
   - **SI es necesario para fpocket, APBS, pdb2pqr, freesasa** (no existen en pip, solo en conda-forge).
   - Nuestro pipeline con CASTpFold **no necesita condacolab**. El pipeline con fpocket **si**.

4. **Reestructuracion final del proyecto:**

   **Notebooks nuevos (activos):**
   | Archivo | Que hace | Requiere |
   |---|---|---|
   | `00_setup.ipynb` | Clona AIzymes + nuestro repo. Instala todo con pip. | Ninguno |
   | `01_pipeline_castpfold.ipynb` | Pipeline 5 ciclos: ESMFold → CASTpFold → FieldTools → Boltzmann → ProteinMPNN | Solo pip |
   | `01_pipeline_fpocket.ipynb` | Pipeline 5 ciclos: igual pero con fpocket en vez de CASTpFold | pip + condacolab |

   **Notebooks viejos movidos a `legacy/`** (respaldo, no se usan mas): 00 al 08 originales.

   **Libreria (`src/libreria_analisismolecular/`):**
   | Archivo | Estado |
   |---|---|
   | `castpfold.py` | **Activo** — wrapper CASTpFold via requests (sin dependencias externas) |
   | `cavidades.py` | **Legacy** — viejo wrapper de fpocket + APBS (conservado por referencia) |
   | `colab/` | **Activo** — drive.py, viz.py |
   | `utils.py` | **Activo** |
   | `ai_zymes.py` | **Eliminado** — reemplazado por `aizymes` real de bunzela/AIzymes |
   | `__init__.py` | Simplificado — solo importa castpfold, utils, colab |

   **Configuracion:**
   - `pyproject.toml` simplificado: solo dependencias core (numpy, scipy, matplotlib, seaborn, scikit-learn, tqdm, requests, biopython, prody). Sin pandas, sin fair-esm, sin torch — todo eso lo maneja AIzymes.
   - `requirements.txt` actualizado.
   - `contexto.md` reescrito con la estructura nueva.
   - `PLAN.md` actualizado.

---

#### Pipeline (ambos notebooks siguen el mismo flujo)

```
Secuencia de RuBisCO (4RUB)
  │
  ├─ Paso 1: ESMFold → predecir estructura 3D (aizymes.design_ESMfold_001)
  ├─ Paso 2a: CASTpFold → metricas de cavidades (nuestro castpfold.py)
  ├─ Paso 2b: fpocket → metricas de cavidades (conda-forge, alternativa)
  ├─ Paso 3: FieldTools → campo electrico en sitio activo (aizymes.FieldTools)
  ├─ Paso 4: Score combinado (cavidades + campo E + afinidad + estabilidad)
  ├─ Paso 5: Seleccion de Boltzmann (temperatura decreciente)
  ├─ Paso 6: ProteinMPNN → rediseñar scaffold (aizymes.design_MPNN_001)
  │
  └─ Repetir x5 ciclos (en vez de 1000 del paper original)
```

**Metrica de cavidades en el Boltzmann score:** Segun Poudel 2020, cavidades mas grandes (mayor volumen/area) correlacionan con mayor especificidad CO2/O2. La metrica `cavity_score = log1p(volumen_total) * 0.1` se suma al score multiobjetivo con peso 0.3.

---

#### Lecciones aprendidas

- AIzymes es un orquestador de cluster, no un notebook ejecutable en Colab. Pero sus modulos individuales son funciones de Python que si funcionan en Colab.
- Las dependencias en `pyproject.toml` afectan a `pip install -e .`. Si una dependencia es incompatible con Colab (ej: pandas 3.x), rompe todo.
- `castpfoldpy` es incompatible con Python <3.12. Llamar a la API web directamente con `requests` es mas simple y portable.
- Google Colab con GPU T4 usa Python 3.10 o 3.11. Siempre verificar `requires-python` de los paquetes.
- Condacolab es util pero fragil — solo usarlo cuando el paquete no existe en pip (ej: fpocket, APBS).

---

#### Proximos pasos

- Ejecutar `00_setup.ipynb` en Colab (deberia funcionar a la primera, sin condacolab).
- Correr `01_pipeline_castpfold.ipynb` (recomendado: sin dependencias extra).
- Correr `01_pipeline_fpocket.ipynb` (alternativo: comparar metricas de cavidades).
- Comparar resultados de CASTpFold vs fpocket vs datos de Poudel 2020.
- Si se consigue acceso a un cluster (NLHPC via Dr. Recabarren), probar AIzymes completo con `AIzymes_MAIN`.

---

### Sesion 1.1 — [pendiente] — [fecha]

**Aprendi:**
**No entendi:**
**Sigue:**

---

*Ultima actualizacion: 23/05/2026 — Sesion 1.0 completada*
