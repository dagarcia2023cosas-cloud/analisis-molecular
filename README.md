# analisismolecular

Proyecto de analisis molecular computacional — RuBisCO.
Universidad de Concepcion, Laboratorio de Quimica Cuantica y Modelamiento Molecular.

## Flujo de trabajo

```
VS Code (interfaz)  →  Google Colab (GPU)  →  GitHub (respaldo)
   escribir codigo       correr analisis        versionado
   editar notebooks      visualizar resultados  portabilidad
```

## Estructura

```
rubisco/
├── papers/              ← Resumenes de papers base (AI.zymes, Poudel 2020)
├── src/                 ← Codigo Python (libreria analisismolecular)
├── notebooks/           ← Notebooks para abrir en Colab
├── scripts/             ← Scripts de automatizacion
├── tests/               ← Tests unitarios
├── PLAN.md              ← Plan de aprendizaje
├── bitacora.md          ← Registro de sesiones
├── pyproject.toml       ← Config del paquete
└── requirements.txt     ← Dependencias
```

## Empezar en 3 pasos

### 1. Local (VS Code)
```bash
cd investigacion/rubisco
pip install -e .
```

### 2. Colab (GPU)
Abrir `notebooks/00_setup.ipynb` en Google Colab y ejecutar las celdas en orden.

### 3. GitHub (respaldo)
```bash
git add -A
git commit -m "descripcion"
git push
```

## Papers base

- **AI.zymes** (Merlicek 2025): `papers/ayzmes_2025.md` — diseño evolutivo de enzimas
- **Poudel 2020**: `papers/poudel_2020.md` — cavidades catiónicas en RuBisCO

## Plan de aprendizaje

Ver `PLAN.md` para las sesiones ordenadas por nivel.

---

*Ultima actualizacion: Mayo 2026*
