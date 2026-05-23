# Poudel 2020 — Resumen Ejecutivo

**Paper:** Poudel, Pike, Raanan, et al. (2020) — PNAS, DOI: 10.1073/pnas.2018939117

---

## El problema
RuBisCO es la enzima más abundante de la Tierra, pero es lenta y poco selectiva: ~30% de las reacciones son con O₂ en vez de CO₂ (fotorrespiración).

## Hipótesis central
Los residuos **cercanos al sitio activo** (no los catalíticos directos) determinan la especificidad. Específicamente: **cavidades cargadas positivamente** que se extienden desde el sitio activo.

## Dataset
- 55 secuencias de RuBisCO con razón de especificidad S medida experimentalmente
- 11 estructuras cristalográficas de alta resolución (6 activas + 5 inactivas)
- Grupos: G-I (IB, IC, ID), G-II, G-III

## Métrica clave
- **S = (Vc/Kc) / (Vo/Ko)** — razón de especificidad CO₂/O₂
- Cavidades medidas con **CASTp** (probe 1.4 Å) + **APBS** (electrostática)
- Solo cavidades **cargadas positivamente** con solapamiento al sitio activo

## Hallazgo principal
**r² = 0.59 (P < 0.05)** entre área de cavidad positiva y S (n=11).

## Cambio topológico de cavidades

| Grupo | Morfología | Conectividad |
|-------|-----------|-------------|
| G-II (S~10-20) | Parches pequeños y aislados | Cada sitio activo con cavidad separada |
| G-IC, IB (S~40-80) | Parches más grandes | Empiezan a conectarse |
| G-ID (S~100-160) | **Canal continuo a lo largo del dímero** | Conecta ambos sitios activos |

La evolución no solo agrandó la cavidad — cambió su topología de **bolsas aisladas** a **túnel continuo**.

## Mecanismo: Electrostatic Steering
El CO₂ tiene momento **cuadrupolar** (C δ⁺, O δ⁻). Las cavidades positivas atraen los oxígenos del CO₂, actuando como **reservorio electrostático** que guía la molécula al sitio activo.

## Limitaciones
- n=11 estructuras → r² modesto, intervalo de confianza amplio
- **Grupo III no sigue la tendencia** — sugiere factores adicionales
- ~40% de varianza sin explicar

## Para el proyecto
- 44 estructuras AlphaFold sin analizar en cavidades
- Hipótesis: extender pipeline a n=55 y modificar residuos de cavidad para diseñar RuBisCO con mayor S
