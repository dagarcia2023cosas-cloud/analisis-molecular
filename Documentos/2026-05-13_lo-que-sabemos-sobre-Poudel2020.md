---
nombre: LO QUE SABEMOS — Resumen vivo del proyecto RuBisCO
fecha: 2026-05-13
tags: [rubisco, proyecto-rubisco, resumen]
estado: activo
ultima_actualizacion: 2026-05-13
---

# LO QUE SABEMOS — RuBisCO

> Este archivo se actualiza a medida que comprendemos mejor el proyecto. Nada está escrito en piedra.

## El problema

RuBisCO es la enzima más abundante de la Tierra, pero es lenta y poco selectiva: en plantas C3, ~30% de las reacciones son con O₂ en vez de CO₂ (fotorrespiración). Entender qué determina su especificidad por CO₂ vs O₂ es el objetivo del laboratorio del Dr. Recabarren.

## Lo que dice Poudel et al. 2020

### Hipótesis central
Los residuos **cercanos al sitio activo** (no los catalíticos directos) son los que determinan la especificidad. Específicamente: **cavidades cargadas positivamente** que se extienden desde el sitio activo.

### Dataset
- 55 secuencias de RuBisCO con razón de especificidad S medida experimentalmente
- 11 estructuras cristalográficas de alta resolución (6 activas + 5 inactivas)
- Grupos cubiertos: G-I (IB, IC, ID), G-II, G-III
- Análisis exclusivo de la subunidad large (catalítica)

### Métrica clave
- **S = (Vc/Kc) / (Vo/Ko)** — razón de especificidad CO₂/O₂ (ratio de eficiencias catalíticas)
  - Vc/Kc = eficiencia de carboxilación; Vo/Ko = eficiencia de oxidación
  - A mayor S, mejor discrimina CO₂ de O₂
- Cavidades medidas con **CASTp** (probe radius 1.4 Å) + **APBS** (electrostática)
- Solo cavidades **cargadas positivamente** y con solapamiento al sitio activo

### Hallazgo principal
**r² = 0.59 (P < 0.05)** entre área de cavidad positiva y S, sobre las 11 estructuras.

#### Cambio topológico de las cavidades
No solo cambia el área — la **topología** de las cavidades es distinta entre grupos:

| Grupo | Morfología | Conectividad |
|-------|-----------|-------------|
| G-II (S~10-20) | Parches pequeños y aislados | Cada sitio activo con cavidad separada |
| G-IC, IB (S~40-80) | Parches más grandes | Empiezan a conectarse |
| G-ID (S~100-160) | **Canal continuo a lo largo del dímero** | Conecta ambos sitios activos en un solo embudo |

La evolución no solo agrandó la cavidad — cambió su topología de **bolsas aisladas** a **túnel continuo**. Esto crea un reservorio más grande de CO₂, aumentando la probabilidad de carboxilación vs oxidación.

#### Análisis de la correlación
**n=11 puntos. G-III pesa mucho.** Con tan pocos datos, los ~2-3 puntos de G-III pueden arrastrar el r² significativamente hacia abajo.

- **Si sacamos G-III** (quedan ~8-9 pts de G-I + G-II), la tendencia visual es bastante lineal. El r² posiblemente subiría a ~0.75-0.85.
- **La correlación funciona dentro de Forma I** y entre Forma I vs II.
- **G-III es otro mundo**: las RuBisCO de arqueas tienen estructura distinta (dímero B₂ vs L₈S₈, loops diferentes). El mecanismo de especificidad probablemente es otro.

Dos preguntas que nos quedan:
1. **¿Reportar como: "Funciona para G-I y G-II; G-III requiere otro modelo"?** — sería un hallazgo válido y publicable.
2. **¿O explorar qué tienen las cavidades de G-III?** — ¿tamaño, carga, posición de los parches positivos? Tal vez el predictor (área de cavidad) falla en G-III porque ni siquiera tienen el mismo tipo de cavidad.

#### Residuos que forman las cavidades
Las cavidades no vienen de 1-2 residuos "mágicos": son el efecto colectivo de ~15-20 residuos (Loop 6, C-terminal, β-hairpin, α-hélice 6) que bordean el sitio activo. **Cada grupo usa una combinación distinta de estos residuos**, lo que genera cavidades de distinta forma y tamaño. Esto explica por qué el sitio activo es casi idéntico pero la especificidad difiere.

### Mapas electrostáticos 2D (APBS)
Poudel visualiza cortes 2D del potencial electrostático a través del sitio activo:
- **G-II**: parches positivos (azul) pequeños y desconectados
- **G-IC, IB**: parches más grandes, tienden a fusionarse
- **G-ID**: canal azul continuo conectando ambos monómeros — un "embudo electrostático"

### Análisis de secuencia (44 AF)
Las 44 AF **no se usaron para cavidades**, solo para análisis de secuencia:
- Los residuos de cavidad tienen **alta conservación intragrupo, baja intergrupo**
- Los residuos catalíticos son 100% conservados entre todos los grupos
- **Conclusión**: la evolución de S no muta el sitio activo (intocable), sino los residuos alrededor que definen la forma y carga de la cavidad

### Mecanismo propuesto
"**Electrostatic steering**" — el CO₂ tiene momento **cuadrupolar** (C δ⁺, O δ⁻). Las cavidades cargadas positivamente atraen los oxígenos parcialmente negativos del CO₂, actuando como un **reservorio electrostático** que guía la molécula hacia el sitio activo. A mayor área de cavidad positiva → mejor guía electrostática → mayor probabilidad de carboxilación vs oxidación → mayor S.

### Limitaciones importantes
- n = 11 solo estructuras → r² modesto y con intervalo de confianza amplio
- No hay validación experimental de la hipótesis de ingeniería
- Probe radius no se varía para probar robustez
- r² = 0.59 deja ~40% de varianza sin explicar
- **Grupo III no sigue la tendencia** — la correlación cavidad-S se debilita o desaparece en este grupo, lo que sugiere que hay factores adicionales más allá de las cavidades

### Notas sobre la metodología (discusión nuestra)
- **Probe radius**: habría que probar radios más grandes para ver cómo varían las áreas calculadas. Por ahora partiremos con 1.4 Å (el estándar).
- **Dinámica molecular**: meter dinámica en este pipeline es prematuro. Poudel usó estructuras estáticas y nosotros haremos lo mismo por ahora.
- **Constantes dieléctricas (APBS)**: habrá que evaluar si cambiarlas altera significativamente los resultados. Si la variación es mínima, los valores por defecto están bien.

## Lo que sabemos del laboratorio

- Dr. Rodrigo Recabarren, Lab de Química Cuántica y Modelamiento Molecular, UdeC
- El dataset del lab **es el mismo de Poudel 2020** (n=55, 11 cristal + 44 AlphaFold)
- Stack: ChimeraX, PyMOL+APBS, CASTp, Jupyter/Python
- En transición hacia modelos LLM (tesis de un estudiante de Matemáticas)
- David García trabaja en AI.zymes (Merlicek 2025) — pipeline evolutivo computacional

## Hipótesis del proyecto

> Especulación de Francisco — pendiente de validar con David o el Dr. Recabarren.

1. **Extender el pipeline de Poudel a las 44 estructuras AlphaFold.** Si el lab ya tiene las 55 estructuras (11 cristal + 44 AF), correr CASTp + APBS sobre todas y ver si la correlación área de cavidad vs S se mantiene, mejora o se rompe al pasar de n=11 a n=55.
   - Si r² ≥ 0.59 → validación robusta del método
   - Si r² < 0.3 → problema de calidad AF o la hipótesis no escala
   - Si se mantiene parcial pero Grupo III es contraejemplo → publicación sobre límites del modelo

2. **Modificar residuos de cavidad para crear un túnel continuo → aumentar S.** Si la topología de cavidad (bolsas aisladas → canal continuo) correlaciona con S, entonces modificar los ~15-20 residuos que bordean la cavidad en una RuBisCO de baja/media S para parecerse a G-ID debería aumentar su especificidad.
   - **Nivel 1**: cambiar residuos de cavidad en G-IC para que se parezcan a G-ID → probar si S sube
   - **Nivel 2**: diseñar cavidades con topología de túnel continuo que no existen en la naturaleza

## Preguntas que nos quedan abiertas

- ¿Por qué r² = 0.59 y no más? ¿Qué explica el 40% restante?
- ¿El probe radius de CASTp cambia los resultados?
- ¿Las 44 estructuras AlphaFold pasan filtros de calidad (pLDDT) en las regiones de cavidad?
- ¿Podemos reproducir el análisis de Poudel con ChimeraX (en vez de PyMOL)?
- ¿Cómo se conecta esto con AI.zymes?

## Resumen general — Poudel 2020

1. **Paradoja**: sitio activo idéntico, S varía 10× entre RuBisCOs
2. **Hipótesis**: la diferencia está en cavidades cargadas positivamente alrededor del sitio activo, no en los residuos catalíticos
3. **Pipeline**: CASTp → APBS → filtrar por solapamiento → medir área vs S
4. **Hallazgo**: r² = 0.59 área cavidad-S (n=11). G-III no sigue la tendencia. Las cavidades evolucionaron de parches aislados (G-II) a túnel continuo (G-ID)
5. **Mecanismo**: electrostatic steering — cuadrupolo del CO₂ guiado por cavidades positivas
6. **Para el lab**: 44 AF sin analizar en cavidades. Hipótesis: extender pipeline a n=55 y modificar residuos de cavidad para diseñar RuBisCO con mayor S

---

*Próxima actualización: cuando avancemos tema por tema en los archivos específicos.*
