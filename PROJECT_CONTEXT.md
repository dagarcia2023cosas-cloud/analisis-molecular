# Contexto General del Proyecto: analisismolecular

## Identidad del Proyecto

**Laboratorio:** Análisis Molecular — Universidad de Concepción (UdeC)
**Equipo:**
- **David** — Ayudante, enfoque en AI.zymes y herramientas computacionales
- **Francisco** — Ayudante, experiencia en enzimas Diels-Alder, mismo objetivo general

**Objetivo principal:** Estudiar las variables que afectan la eficiencia enzimática de las distintas familias de RuBisCO, utilizando el pipeline de AI.zymes como referencia metodológica.

**Meta de aprendizaje:** No hay fecha límite ni entregable forzoso. El foco es aprender y dominar las herramientas para potencialmente usarlas en una tesis futura.

---

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.10+ |
| Paquete | `libreria_analisismolecular` |
| Pipeline referencia | AI.zymes (Rosetta, ESMFold, ProteinMPNN, FieldTools) |
| Química computacional | RDKit, OpenBabel, py3Dmol, MDAnalysis |
| Análisis de cavidades | fpocket, CASTp (referencia) |
| Electroestática | APBS, pdb2pqr, freesasa |
| Visualización | py3Dmol, nglview, matplotlib, seaborn, plotly |
| ML (opcional) | PyTorch, scikit-learn |
| Editor | VS Code con extensiones recomendadas |
| Nube | Google Colab + Google Drive (GPU/TPU) |
| Control de versiones | GitHub |
| Guía IA | opencode (asistente + director de aprendizaje) |

---

## Papers Base

### Paper 1: AI.zymes — A Modular Platform for Evolutionary Enzyme Design
- **Autores:** Merlicek, Neumann, Lear, et al. (2025)
- **Publicado en:** Angew. Chem. Int. Ed.
- **DOI:** 10.1002/anie.202507031
- **Código:** https://github.com/bunzela/AIzymes

**Resumen:** Plataforma modular que integra múltiples herramientas de bioingeniería (Rosetta, ESMFold, ProteinMPNN, FieldTools) en ciclos iterativos de diseño evolutivo. Optimiza afinidad al estado de transición, estabilidad proteica y campos eléctricos catalíticos. Benchmark en KSI (Kemp eliminasa): 7.7x mejora con solo 7 variantes.

**Herramientas clave del pipeline:**
| Herramienta | Función |
|-------------|---------|
| **ESMFold** | Predicción de estructura proteica |
| **RosettaRelax** | Relajación y evaluación de estabilidad conformacional |
| **RosettaDesign** | Optimización de residuos del sitio activo (considera ligandos) |
| **ProteinMPNN** | Rediseño del scaffold proteico (estabilidad termal) |
| **FieldTools** | Evaluación de campos eléctricos catalíticos desde MD |

**Conceptos clave:**
- Diseño evolutivo vs. no-evolutivo
- Selección Boltzmann multiobjetivo
- Optimización forward-looking (selecciona variantes por su "potencial")
- Modularidad (input/output en formato PDB)

### Paper 2: Biophysical Analysis of the Structural Evolution of Substrate Specificity in RuBisCO
- **Autores:** Poudel, Pike, Raanan, et al. (2020)
- **Publicado en:** PNAS
- **DOI:** 10.1073/pnas.2018939117

**Resumen:** Análisis genómico y estructural de 55 variantes de RuBisCO. Identifica que cavidades con carga positiva alrededor del sitio activo se expandieron durante la evolución, correlacionando con mayor especificidad por CO₂ sobre O₂ (r² = 0.59).

**Grupos filogenéticos de RuBisCO:**
| Grupo | Características | Especificidad CO₂ |
|-------|----------------|-------------------|
| G-IV | RuBisCO-like protein (parálogo), no cataliza O₂/CO₂ | — |
| G-II | Ancestral, metanógenos anaeróbicos | Baja |
| G-III | Arqueas | Baja-Media |
| G-I (IA, IB, IC, ID) | Moderna, bacterias + eucariotas + plantas | Media-Alta (hasta >90) |

**Hallazgo principal:** La expansión de cavidades catiónicas favorece el cuadrupolo de CO₂ sobre el enlace O-O de O₂, creando un mecanismo de secuestro electrostático.

**Conclusiones de nuestra discusión:**
- **Grupo III no sigue la tendencia:** A pesar de tener cavidades catiónicas expandidas, G-III no muestra correlación positiva con especificidad. Esto sugiere que el tamaño de cavidad por sí solo no explica la eficiencia.
- **Cambio topológico de cavidades:** La evolución de G-II → G-I no solo agrandó cavidades, sino que transformó su geometría: de bolsas discretas y aisladas en G-II/G-III hacia un **túnel continuo** en G-I que conecta el sitio activo con la superficie de la proteína.
- **Electrostatic steering:** El túnel catiónico en G-I funciona como un "embudo electrostático" que orienta y concentra CO₂ hacia el sitio activo, explicando la mayor especificidad.
- **Implicancia directa:** Para diseño racional, no basta con agrandar cavidades — hay que asegurar conectividad topológica y gradiente electrostático direccional.

**Métodos usados en el paper:**
- Alineamiento múltiple (Clustal Omega)
- Árbol filogenético (RAxML, LG substitution matrix)
- Electrostatic surface potential (APBS + PyMOL)
- Análisis de cavidades (CASTp)
- Distancia de Hamming para diversidad de secuencia
- Programas: protCAD, APBS, PyMOL, R

---

## Plan de Trabajo y Aprendizaje

### Fase 0: Fundamentos (ahora)
- [x] Proyecto estructurado (VS Code + GitHub + Colab)
- [x] Papers leídos y contextualizados
- [ ] Configurar AI.zymes localmente o entender su pipeline
- [ ] Repasar termodinámica básica de enzimas (si es necesario)

### Fase 1: Entender las herramientas de AI.zymes
- [ ] ¿Qué hace cada herramienta? (ESMFold, Rosetta, ProteinMPNN, FieldTools)
- [ ] ¿Cómo se conectan? (formato PDB como interfaz)
- [ ] ¿Cómo implementar algo similar en Colab?
- [ ] Probar el código de AI.zymes en GitHub

### Fase 2: Aplicar a RuBisCO
- [ ] Obtener estructuras PDB de RuBisCO de los grupos G-I a G-IV
- [ ] Pipeline de análisis: fpocket → freesasa → APBS → Python
- [ ] Reproducir análisis de cavidades cargadas (como Poudel et al.)
- [ ] Calcular campos eléctricos catalíticos
- [ ] Correlacionar estructura con especificidad

### Fase 3: Diseño evolutivo
- [ ] Implementar ciclo de diseño inspirado en AI.zymes para RuBisCO
- [ ] Optimizar cavidades cargadas in silico
- [ ] Predecir variantes con mejor especificidad CO₂/O₂

### Fase 4: Proyección a tesis
- [ ] Consolidar pipeline completo
- [ ] Documentar metodología
- [ ] Identificar preguntas abiertas para investigación futura

---

## Rol de opencode (yo)

Actúo como:
1. **Guía** — Explico conceptos, sugiero qué aprender y en qué orden
2. **Asistente técnico** — Escribo código, configuro entornos, debuggeo
3. **Documentador** — Mantengo el contexto del proyecto actualizado

**Dinámica:** Vos me decís qué querés hacer o qué no entendés, y yo te llevo paso a paso. No hay preguntas tontas.

---

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
│  https://github.com/dagarcia2023cosas-cloud/         │
│                  analisismolecular                   │
└──────────────────────┬──────────────────────────────┘
                       │ git clone / git pull
                       ▼
┌─────────────────────────────────────────────────────┐
│                Google Colab (nube)                   │
│  Clonar repo → Instalar deps → Ejecutar análisis    │
│  Guardar resultados en Drive o subir a GitHub       │
└─────────────────────────────────────────────────────┘
```

---

*Última actualización: Mayo 2026*
