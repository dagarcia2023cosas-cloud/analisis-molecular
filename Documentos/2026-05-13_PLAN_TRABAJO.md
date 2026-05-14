---
nombre: Plan de trabajo — proyecto RuBisCO
fecha: 2026-05-13
tags: [rubisco, proyecto-rubisco, plan]
estado: activo
---

# Plan de trabajo — proyecto RuBisCO

> Secuencia de fases basada en el análisis de Poudel 2020 y las herramientas disponibles en repo-lab-qm-modelamiento-molecular.

---

## Fase 1 — Reproducir a Poudel

**Objetivo:** Validar que el pipeline fpocket + APBS replica la correlación r² ~0.59 en las 11 estructuras cristalográficas.

Pasos:
1. Instalar fpocket, freesasa, APBS, pdb2pqr
2. Descargar las 11 PDB cristalográficas (usar MCP PDB)
3. Correr fpocket sobre cada estructura → detectar cavidades
4. Correr APBS → filtrar cavidades por potencial positivo
5. Filtrar por solapamiento con sitio activo
6. Medir área superficial de cavidades filtradas
7. Graficar área vs S → verificar r² ~0.59

**Entregable:** Scatter plot área cavidad positiva vs S (n=11)

---

## Fase 2 — Escalar a 55

**Objetivo:** Ver si la correlación se mantiene, mejora o se rompe al incluir las 44 AF.

Pasos:
1. Verificar calidad de las 44 AF: pLDDT en regiones de cavidad
2. Correr fpocket + APBS sobre las 44 AF
3. Repetir análisis de correlación con n=55
4. Analizar G-III por separado (no sigue la tendencia general)

**Escenarios posibles:**
| Resultado | Implicancia |
|-----------|-------------|
| r² ≥ 0.59 con n=55 | Validación robusta del método |
| r² < 0.3 | Problema de calidad AF o la hipótesis no escala |
| Se mantiene parcial pero G-III es contraejemplo | Publicación sobre límites del modelo |

**Entregable:** Scatter plot área vs S (n=55) + análisis por grupo

---

## Fase 3 — Ingeniería de cavidades

**Objetivo:** Identificar mutaciones que conviertan cavidades de baja/media S en túneles continuos tipo G-ID.

Pasos:
1. Identificar residuos específicos de cavidad (output de fpocket) en cada grupo
2. Comparar perfiles de residuos entre G-IC, G-IB vs G-ID
3. Proponer mutaciones G-IC → G-ID para crear túnel continuo
4. Conectar con AI.zymes (David) para diseño evolutivo

**Nivel 1:** Mutar residuos de cavidad G-IC para parecerse a G-ID → probar si S sube
**Nivel 2:** Diseñar cavidades con topología de túnel continuo que no existen en naturaleza

**Entregable:** Lista de mutaciones candidatas + pipeline de validación in silico

---

## Stack tecnológico

| Herramienta | Rol en el pipeline |
|-------------|--------------------|
| **fpocket** | Detección de cavidades (reemplaza CASTp) |
| **freesasa** | Cálculo de área superficial |
| **pdb2pqr** | Preparación de estructuras para APBS |
| **APBS** | Potencial electrostático Poisson-Boltzmann |
| **Biopython** | Parseo de PDB, manipulación de estructuras |
| **Python + matplotlib** | Análisis y visualización |
| **PDB MCP** | Descarga de estructuras cristalográficas |
| **PubChem MCP** | Sustratos, inhibidores, ligandos |
