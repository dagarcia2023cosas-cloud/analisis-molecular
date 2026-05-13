# PLAN DE APRENDIZAJE — analisismolecular

## Estructura: de lo más simple a lo más complejo

---

### Nivel 1 — Exploración y visualización (sin instalaciones pesadas)

| Sesión | Objetivo | Complejidad |
|--------|----------|:--:|
| **1.1** | Explorar código de AI.zymes — estructura modular, qué archivo hace qué, flujo PDB→PDB | ⭐ |
| **1.2** | Obtener PDBs de RuBisCO (G-I a G-IV), visualizar sitio activo con py3Dmol en Colab | ⭐ |
| **1.3** | *(con Francisco)* — Cruzar conocimiento: Diels-Alder ↔ AI.zymes | ⭐ |
| **1.4** | Conceptos de termo justos: ∆G‡, kcat, Km, ecuación de Michaelis-Menten aplicado a RuBisCO | ⭐ |

### Nivel 2 — Herramientas vía API (se corren directo en Colab)

| Sesión | Objetivo | Complejidad |
|--------|----------|:--:|
| **2.1** | ESMFold — predecir estructura desde secuencia, comparar con PDB experimental | ⭐⭐ |
| **2.2** | ProteinMPNN — diseñar secuencias para un scaffold de RuBisCO | ⭐⭐ |
| **2.3** | *(con Francisco)* — Él explica mutaciones clave en enzimas, vos mostrás predicción de estructura | ⭐⭐ |

### Nivel 3 — Análisis computacional (algoritmos en Python puro)

| Sesión | Objetivo | Complejidad |
|--------|----------|:--:|
| **3.1** | Selección Boltzmann — implementar desde cero, simular evolución de una población | ⭐⭐⭐ |
| **3.2** | Reproducir análisis de cavidades cargadas (Poudel et al.) — APBS/PyMOL, correlación r²=0.59 | ⭐⭐⭐ |
| **3.3** | Diseño evolutivo mínimo — unir Boltzmann + scoring simple en un ciclo iterativo | ⭐⭐⭐ |

### Nivel 4 — Herramientas pesadas (instalación + curva alta)

| Sesión | Objetivo | Complejidad |
|--------|----------|:--:|
| **4.1** | Rosetta — score functions, relax, qué hace cada protocolo | ⭐⭐⭐⭐ |
| **4.2** | RosettaDesign — modificar sitio activo de RuBisCO in silico | ⭐⭐⭐⭐ |
| **4.3** | Campos eléctricos catalíticos — FieldTools, relación campo↔kcat | ⭐⭐⭐⭐ |

### Nivel 5 — Integración y cierre

| Sesión | Objetivo | Complejidad |
|--------|----------|:--:|
| **5.1** | Pipeline completo — diseño de variantes RuBisCO con mejores cavidades cargadas | ⭐⭐⭐⭐⭐ |
| **5.2** | Documentación, bitácora final, preguntas abiertas, proyección a tesis | ⭐⭐⭐⭐ |

---

## Estructura de cada sesión

```
1. Concepto del día (5 min)       — Explicación de qué se trata
2. Manos a la obra (30-40 min)    — Implementación en Colab/VS Code
3. Cierre (5 min)                 — Bitácora: ¿qué aprendí? ¿qué no entendí? ¿qué sigue?
```

## Mecánicas fijas

- **Bitácora** en `docs/bitacora.md` — 3 líneas al final de cada sesión
- **Sesiones con Francisco** — Cada 3-4 sesiones, cruce de conocimiento
- **Termo intercalada** — Solo lo necesario, en el momento justo, no de golpe

## Progreso

| Sesión | Estado | Fecha |
|--------|--------|-------|
| 1.1 | ⬜ pendiente | |
| 1.2 | ⬜ pendiente | |
| 1.3 | ⬜ pendiente | |
| 1.4 | ⬜ pendiente | |
| 2.1 | ⬜ pendiente | |
| 2.2 | ⬜ pendiente | |
| 2.3 | ⬜ pendiente | |
| 3.1 | ⬜ pendiente | |
| 3.2 | ⬜ pendiente | |
| 3.3 | ⬜ pendiente | |
| 4.1 | ⬜ pendiente | |
| 4.2 | ⬜ pendiente | |
| 4.3 | ⬜ pendiente | |
| 5.1 | ⬜ pendiente | |
| 5.2 | ⬜ pendiente | |

---

*Plan creado: Mayo 2026*
