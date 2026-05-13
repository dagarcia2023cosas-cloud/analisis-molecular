# Flujo de Trabajo: VS Code + Google Colab + GitHub

## Arquitectura del entorno integrado

```
┌──────────────────────────────────────────────────────────────┐
│                     VS Code (Local)                          │
│  ┌─────────────┐  ┌──────────┐  ┌────────────────────────┐ │
│  │  Editar      │  │  Depurar  │  │  Jupyter Notebooks    │ │
│  │  *.py / *.md │  │  F5      │  │  (local o remoto)     │ │
│  └──────┬───────┘  └──────────┘  └──────────┬─────────────┘ │
│         │                                    │               │
└─────────┼────────────────────────────────────┼───────────────┘
          │ git add + commit + push            │
          ▼                                    ▼
┌──────────────────────────────────────────────────────────────┐
│                     GitHub                                    │
│              github.com/dagarcia2023cosas-cloud/              │
│                    analisismolecular                          │
└────────────────────────────┬─────────────────────────────────┘
                             │ git clone / git pull
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                  Google Colab (GPU/TPU)                      │
│  ┌─────────────────────┐  ┌──────────────────────────────┐  │
│  │  Notebooks de       │  │  Google Drive (datos,       │  │
│  │  análisis molecular  │  │  resultados, modelos)       │  │
│  └─────────────────────┘  └──────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Flujo diario

### 1. Desarrollo local (VS Code)

```bash
# Abrir el proyecto
code C:\PROYECTOS_UDEC\analisismolecular

# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Editar código, correr tests
pytest tests/ -v
```

**VS Code features:**
- `F5` — Debug Python
- `Ctrl+Shift+P` → "Python: Run All Tests"
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Run all tests"
- Extensiones recomendadas se instalan automáticamente al abrir el proyecto

### 2. Subir cambios a GitHub

```bash
git add -A
git commit -m "descripcion del cambio"
git push
```

### 3. Ejecutar en Colab

Abrir `notebooks/00_colab_setup.ipynb` en Colab y ejecutar la primera celda.
Esto clona el repo, instala dependencias y deja todo listo.

### 4. Sincronizar resultados

Los resultados se guardan en Google Drive via `drive_utils.save_to_drive()`.
Desde VS Code se pueden descargar o acceder via el repo.

## Atajos de VS Code

| Acción | Atajo |
|--------|-------|
| Debug Python | `F5` |
| Run test file | `Ctrl+F5` |
| Tasks | `Ctrl+Shift+P` → "Tasks" |
| Formatear código | `Shift+Alt+F` |
| Terminal | `` Ctrl+` `` |
| Git: commit | `Ctrl+Shift+P` → "Git: Commit" |

## Estructura de ramas recomendada

- `master` — código estable y funcional
- `dev` — desarrollo activo
- `experimentos/` — notebooks y scripts experimentales
