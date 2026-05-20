# AI.zymes: Una Plataforma Modular para el Diseño Evolutivo de Enzimas

**Referencia completa:** Merlicek, L. P., Neumann, J., Lear, A., Degiorgi, V., de Waal, M. M., Cotet, T.-S., Mulholland, A. J., & Bunzel, H. A. (2025). *AI.zymes: A Modular Platform for Evolutionary Enzyme Design*. **Angewandte Chemie International Edition**, *64*, e202507031.

**DOI:** [10.1002/anie.202507031](https://doi.org/10.1002/anie.202507031)

**Afiliaciones:** ETH Zurich (Biosystems Science and Engineering) y University of Bristol (Centre for Computational Chemistry).

**Financiamiento:** Swiss National Science Foundation (Ambizione PZ00P3_208691) y ERC Advanced Grant (PREDACTED, 101021207).

---

## 1. Resumen (Abstract)

La capacidad de crear enzimas completamente nuevas (*new-to-nature*) impulsaría sustancialmente la bioingeniería, la medicina y la industria química. A pesar de los avances recientes en diseño de proteínas y predicción de estructuras, diseñar biocatalizadores novedosos sigue siendo un desafío. En este trabajo presentamos **AI.zymes**, una plataforma modular que integra algoritmos de vanguardia en ingeniería de proteínas dentro de un marco evolutivo. AI.zymes combina herramientas bioinformáticas como **Rosetta**, **ESMFold**, **ProteinMPNN** y **FieldTools** en rondas iterativas de diseño y selección, permitiendo optimizar un amplio rango de propiedades catalíticamente relevantes. Además de mejorar la afinidad por el estado de transición y la estabilidad proteica, AI.zymes también puede optimizar propiedades que no son directamente abordadas por los algoritmos de diseño empleados. Por ejemplo, AI.zymes logra potenciar la catálisis electrostática mediante la selección iterativa de variantes con campos eléctricos catalíticos más intensos. Al evaluar AI.zymes sobre la actividad Kemp eliminasa promiscua de la ketosteroide isomerasa (KSI), se obtuvo un aumento de actividad de **7.7 veces** tras probar experimentalmente solo **7 variantes**. Gracias a su modularidad, AI.zymes puede incorporar fácilmente nuevos algoritmos de diseño, allanando el camino hacia un marco unificador para el diseño de enzimas.

---

## 2. Introducción

Las enzimas son los catalizadores de la naturaleza: facilitan reacciones químicas con una especificidad y eficiencia notables. Poder crear enzimas a medida tiene un potencial inmenso para la biotecnología, la medicina y la industria química. Sin embargo, la inmensidad del espacio de secuencias y la compleja relación entre estructura y función convierten el diseño y la ingeniería de enzimas en un desafío formidable.

### 2.1 Evolución dirigida vs. diseño computacional

- **Evolución dirigida experimental:** método potente para navegar el espacio de secuencias y optimizar la actividad enzimática mediante rondas iterativas de mutagénesis y selección. Sin embargo, consume mucho tiempo y tiene dificultades para acceder a regiones distantes del paisaje de aptitud (*fitness landscape*).

- **Diseño computacional de proteínas:** alternativa a la evolución dirigida. Típicamente introduce mutaciones sobre un conjunto fijo de estructuras de entrada, lo que limita la diversidad y el acceso a variantes funcionales lejanas.

- **Diseño evolutivo computacional:** supera la limitación anterior iterando a través de ciclos de diseño y selección, utilizando las mejores variantes como plantillas para optimización posterior. Al variar continuamente la estructura de entrada, los enfoques evolutivos pueden acceder a secuencias inaccesibles en un solo ciclo de diseño.

### 2.2 Limitaciones actuales

- La mayoría de los algoritmos de diseño de proteínas se desarrollaron para mejorar la **estabilidad** más que para optimizar propiedades biocatalíticas.
- El diseño computacional suele priorizar la estabilidad del sitio activo, descuidando factores **electrostáticos** y **dinámicos** esenciales para la biocatálisis.
- Efectos como la **catálisis electrostática** y la **dinámica conformacional** típicamente se abordan solo *después* del diseño, como filtros, en lugar de integrarse durante el proceso.
- Esta brecha metodológica probablemente contribuye a los bajos valores de **k~cat~** observados en enzimas diseñadas *de novo*.

### 2.3 Solución propuesta: AI.zymes

Para cerrar esta brecha, los autores desarrollaron **AI.zymes**, una plataforma modular para diseño evolutivo que integra múltiples herramientas bioinformáticas (Rosetta, ESMFold, ProteinMPNN, FieldTools) en un flujo de trabajo coherente, permitiendo la **optimización multiobjetivo** que incluye propiedades biocatalíticas desde el inicio del proceso de diseño.

---

## 3. Resultados y Discusión

### 3.1 ¿Cómo funciona AI.zymes?

AI.zymes opera sobre un **pool de variantes en continua expansión**, seleccionando y rediseñando variantes independientemente de su generación (a diferencia de los enfoques basados en "rondas" discretas).

#### 3.1.1 Flujo de trabajo completo

El proceso de diseño evolutivo de AI.zymes sigue estos pasos:

1. **Generación de variantes iniciales:** a partir de una estructura de entrada fija se genera un pool inicial de variantes (similar al diseño no evolutivo).

2. **Selección (Boltzmann):**
   - Primero se **eliminan variantes** que no alinean con la geometría objetivo entre el estado de transición químico y los residuos catalíticos (filtro geométrico).
   - Luego se aplica **selección de Boltzmann multiobjetivo** basada en tres puntuaciones:
     - **Interface score:** fuerza de interacción ligando-proteína (afinidad por el estado de transición).
     - **Stability score:** estabilidad proteica.
     - **Campo eléctrico:** magnitud de la catálisis electrostática.
   - La selección es **forward-looking** (prospectiva): evalúa el **potencial** de cada variante como el promedio de su propia puntuación y las puntuaciones de sus descendientes inmediatos.
   - La **temperatura de Boltzmann** se ajusta gradualmente: comienza alta (fase de **exploración**, selección más aleatoria) y desciende progresivamente (fase de **explotación**, altamente selectiva hacia las variantes más prometedoras).

3. **Predicción de estructura con ESMFold:** las variantes seleccionadas son sometidas a predicción estructural mediante el modelo de lenguaje de proteínas ESMFold.

4. **Relajación con RosettaRelax:** las estructuras predichas se relajan para evaluar estabilidad conformacional y desplazamientos del esqueleto proteico (*backbone*).

5. **Rediseño (dos algoritmos complementarios):**
   - **RosettaDesign** (70% de probabilidad): optimiza los residuos del **sitio activo**. Puede modelar ligandos químicos explícitamente.
   - **ProteinMPNN** (30% de probabilidad): rediseña el **andamiaje proteico** (*scaffold*). Excelente generando proteínas termoestables.
   - Esta división aprovecha las fortalezas de cada algoritmo.

6. **Iteración:** las variantes rediseñadas se incorporan al pool y el ciclo continúa.

#### 3.1.2 Control de la carga mutacional

Para explorar el espacio de secuencias de forma gradual, AI.zymes restringe la **carga mutacional por paso de diseño**:

- Demasiadas mutaciones por paso borrarían la información evolutiva contenida en la secuencia.
- Muy pocas mutaciones limitan la eficiencia del diseño.
- En **RosettaDesign**: se añade un peso que penaliza las mutaciones respecto a la estructura de entrada.
- En **ProteinMPNN**: se añade un sesgo (*bias*) hacia la secuencia de entrada.

**Parámetros clave ajustables:** tasa de mutación, temperatura de selección de Boltzmann y estrategia de diseño.

#### 3.1.3 Modularidad basada en PDB

AI.zymes es **altamente modular**: todos los módulos utilizan archivos **PDB como entrada y salida**. Esto significa que cada algoritmo opera de forma independiente y se comunica con los demás exclusivamente mediante estructuras en formato PDB:

- Para ProteinMPNN (que trabaja sobre secuencia), la modularidad se logra acoplando la secuencia diseñada → predicción de estructura → relajación, y el resultado es un PDB.
- Esta arquitectura facilita la **integración de nuevos métodos de diseño** y asegura la aplicabilidad continua de AI.zymes en el campo rápidamente cambiante del diseño computacional de proteínas.

```
[Algoritmo A] → PDB → [Algoritmo B] → PDB → [Algoritmo C] → ...
```

### 3.2 Diseño evolutivo vs. diseño no evolutivo

Se utilizó como banco de pruebas la **actividad Kemp eliminasa promiscua de la ketosteroide isomerasa (KSI)** de *Comamonas testosteroni*.

**Reacción de referencia:** la eliminación de Kemp es la desprotonación C─H catalizada por base de benzisoxazoles. Es un punto de referencia establecido para enzimas *de novo*.

**Variante de partida (WT):** KSI con mutación **D38N** (elimina uno de los dos aspartatos del sitio activo que podrían actuar como base catalítica, dejando D99 como base). Formaba una mezcla oligomérica. Objetivo: mejorar actividad + crear enzima termoestable y monomérica.

**Resultados de la comparación (Figura 2):**

| Métrica | Diseño no evolutivo | Diseño evolutivo (solo Rosetta) | Diseño evolutivo (Rosetta + ProteinMPNN) |
|---------|---------------------|--------------------------------|-------------------------------------------|
| Interface score | Base | Mejor | - |
| Stability score | Base | Mejor | **Aún mejor** |
| Espacio de secuencias explorado | Limitado | Amplio | **Muy amplio** |
| Diversidad (tSNE de embeddings ESM2) | Baja | Alta | **Máxima** |

La integración de **ProteinMPNN** mejoró adicionalmente los diseños al aumentar el stability score y expandir el espacio de secuencias explorado.

**Árbol filogenético:** AI.zymes registra el historial evolutivo completo, permitiendo construir un árbol filogenético que rastrea ancestros y descendientes, visualizando las mejoras incrementales logradas durante el diseño (Figura 2e).

### 3.3 Diseño evolutivo de campos eléctricos

#### 3.3.1 ¿Por qué son importantes los campos eléctricos?

Los **campos eléctricos catalíticos** son críticos para estabilizar los estados de transición y promover la actividad enzimática. La enzima orienta cargas y dipolos en su sitio activo para generar un campo eléctrico que facilita la ruptura/formación de enlaces.

A pesar de algunos éxitos puntuales, el diseño computacional de campos eléctricos catalíticos ha sido históricamente difícil. Los bajos valores de k~cat~ de las enzimas diseñadas probablemente se deben en parte a la **negligencia de la catálisis electrostática** durante el diseño.

#### 3.3.2 Integración de FieldTools

Los autores integraron **FieldTools** (herramienta desarrollada previamente por el mismo grupo para evaluar campos eléctricos a partir de trayectorias de dinámica molecular, MD) dentro de AI.zymes. El diseño del campo eléctrico se orientó a mejorar el **campo efectivo a lo largo del enlace C─H escindible** (el enlace que se rompe en la eliminación de Kemp).

#### 3.3.3 Resultado clave

**Ni RosettaDesign ni ProteinMPNN pueden diseñar campos eléctricos catalíticos de forma explícita.** Sin embargo, AI.zymes logra la **optimización del campo eléctrico combinando**:

- Algoritmos de diseño de proteínas (que desconocen los campos eléctricos)
- Selección de Boltzmann que favorece variantes con **campos catalíticos más intensos**

Los campos más efectivos surgieron de diseños que combinaban **Rosetta + ProteinMPNN**, no de Rosetta solo. Esto resalta la importancia de las **mutaciones remotas en el andamiaje proteico** (más allá del sitio activo) para modular el campo eléctrico.

> **Conclusión clave:** La optimización de campos eléctricos —un avance significativo en diseño de enzimas— puede lograrse con métodos de diseño **no diseñados específicamente para efectos de campo**, siempre que exista una puntuación cuantificable que la selección de Boltzmann pueda usar como criterio.

### 3.4 Cribado por Dinámica Molecular (MD Screening)

Antes de la validación experimental, se realizó un **cribado por simulaciones cortas de dinámica molecular** (10 ns) de los 96 mejores diseños.

**Objetivo del cribado MD:** No identificar los *mejores* diseños, sino **descartar variantes malas** que adoptan rápidamente conformaciones no productivas.

**Criterios de filtrado (5 métricas):**

1. **Flexibilidad del ligando:** ¿permanece el ligando en una conformación productiva?
2. **Distancia ligando-base catalítica:** ¿se mantiene la proximidad geométrica necesaria?
3. **Intensidad del campo eléctrico:** ¿se sostiene el campo catalítico en la simulación?
4. **Preorganización del estado apo:** ¿la conformación sin ligando es favorable?
5. **Hidratación del sitio activo:** ¿hay agua interfiriendo?

**Resultado del cribado:** De 96 variantes, 23 pasaron los filtros MD. Tras inspección visual de la geometría del sitio activo, se seleccionaron **7 variantes** para prueba experimental.

### 3.5 Validación experimental

#### 3.5.1 Resultados de actividad

| Métrica | WT (KSI D38N) | Variante K3 |
|---------|---------------|-------------|
| **(k~cat~/K~M~)~max~** | 1,200 ± 200 M⁻¹s⁻¹ | **9,200 ± 1,800 M⁻¹s⁻¹** |
| **pK~a~ de la base general** | 8.1 ± 0.1 | 8.4 ± 0.1 |
| **Mejora de actividad** | 1× | **7.7×** |

- De las 7 variantes probadas, solo **K3** superó la actividad de WT.
- Las mejoras fueron impulsadas principalmente por aumentos en **k~cat~** (mayor tasa de recambio), no por cambios en K~M~ (la cinética de Michaelis-Menten a pH 7.0 mostró que las mejoras de velocidad se debieron casi enteramente a mayores tasas de recambio).
- El cambio en el pK~a~ de 8.1 a 8.4 sugiere una alteración en el entorno electrostático de la base catalítica D99.

#### 3.5.2 Logros estructurales

| Propiedad | WT | K3 |
|-----------|-----|-----|
| Estado oligomérico | Mezcla oligomérica | **Monomérico** |
| Temperatura de desnaturalización (T~m~) | 49.8 °C | **>95 °C** (no se desnaturaliza) |
| Señal CD | Base | **Más intensa** (mejor plegamiento) |

- **Monomerización:** lograda reemplazando residuos hidrofóbicos por hidrofílicos en la interfaz del dímero de KSI.
- **Termoestabilidad extrema:** K3 permanece plegada hasta 95 °C (límite del experimento).
- **AlphaFold3** corroboró la predicción: K3 se predice como monómero estable, mientras que WT puede adoptar múltiples formas oligoméricas.

#### 3.5.3 Eficiencia del diseño

Aunque el diseño evolutivo alteró entre el **45% y 55%** de la secuencia proteica, solo fue necesario probar **7 variantes** para encontrar una con actividad mejorada. Esto contrasta fuertemente con campañas típicas de ingeniería enzimática asistida por computación o machine learning, que usualmente requieren cribado experimental masivo.

### 3.6 Análisis de la optimización del campo eléctrico en K3

#### 3.6.1 Origen molecular de las mejoras

La inspección de las mutaciones entre WT y K3 reveló que las mejoras en el campo eléctrico total surgieron de **numerosas contribuciones pequeñas** distribuidas por toda la proteína:

| Mutación | Efecto sobre el campo eléctrico | Mecanismo |
|----------|-------------------------------|-----------|
| **L115D** | Aumenta | Introduce carga negativa que **favorece** la desprotonación |
| **R113V** | Aumenta | Elimina carga positiva **anticatalítica** presente en WT |
| **N38V** | Disminuye | Reduce el campo local pero **aumenta la hidrofobicidad** del sitio de unión, mejorando la unión del sustrato |

Este último caso (N38V) es particularmente interesante: AI.zymes introdujo una mutación que *perjudica* el campo eléctrico localmente pero *beneficia* la unión del sustrato. Esto demuestra que la plataforma realiza **compromisos multiobjetivo** automáticamente.

#### 3.6.2 Efectos dinámicos

- El campo eléctrico calculado sobre estructuras **estáticas** mostró una mejora de **23 MV cm⁻¹** en K3 respecto a WT.
- Simulaciones MD de **10 ns** mostraron una mejora de **19 MV cm⁻¹**: ligeramente menor, lo que subraya la importancia de incluir efectos dinámicos.
- Ocho réplicas de simulaciones de **1 µs** mostraron que en K3 el ligando permanece establemente unido en *todas* las trayectorias, mientras que en varias réplicas de WT el ligando adoptó conformaciones alternativas o se disoció.

> **Implicación:** Incluir los efectos de la dinámica en *todas* las puntuaciones calculadas (no solo en el cribado post-diseño) podría mejorar aún más los resultados.

#### 3.6.3 Principio general demostrado

AI.zymes optimizó campos eléctricos sin usar herramientas diseñadas para ese fin. Esto sugiere un principio general:

> **AI.zymes puede optimizar cualquier aspecto de la función enzimática —incluso aquellos que no pueden ser directamente abordados por los algoritmos de diseño— siempre que el rasgo deseado pueda ser cuantificado (*scored*) y utilizado en la selección de Boltzmann.**

---

## 4. Conclusión

1. **AI.zymes** es una plataforma modular que avanza el diseño de enzimas mediante **optimización evolutiva multiobjetivo**.

2. Se logró un aumento de actividad de **7.7 veces** en la Kemp eliminasa de KSI tras probar solo **7 variantes experimentales**, optimizando simultáneamente:
   - Reconocimiento del estado de transición
   - Geometría catalítica
   - Campos eléctricos
   - Estabilidad proteica

3. **Ventaja clave del diseño evolutivo:** dirige la mutagénesis hacia regiones funcionales del espacio de secuencias, aumentando la eficiencia respecto a métodos no evolutivos. Esto es valioso tanto para proyectos a gran escala (millones de diseños) como para esfuerzos pequeños con recursos computacionales limitados.

4. **La selección de Boltzmann sobre todo el pool** maximiza la utilización de recursos al ejecutar continuamente un número fijo de diseños sin esperar a que termine una ronda para comenzar la siguiente.

5. **Optimización multiobjetivo para rasgos no directamente diseñables:** AI.zymes puede mejorar propiedades (como la catálisis electrostática) sin aumentar el costo computacional, siempre que exista una función de puntuación.

### Perspectivas futuras (Outlook)

- **Integración de nuevas herramientas:** LigandMPNN, RFdiffusionAA, AlphaFold3 (que pueden modelar ligandos no proteicos) y herramientas de deep learning como ChemNet.
- **Descripción más refinada de la electrostática:** incluir la reorganización del campo eléctrico a lo largo de todos los enlaces y de la coordenada de reacción completa.
- **Integración con machine learning reforzado:** para guiar la exploración hacia regiones más activas del paisaje de aptitud.
- **Interfaz con diseño *de novo*:** usar AI.zymes para optimizar evolutivamente enzimas generadas desde cero mediante enfoques de teozima.
- **Cribado MD:** simulaciones cortas (≤10 ns) pueden eliminar efectivamente diseños con conformaciones no productivas, siendo computacionalmente viables para pools de ~100 diseños.

---

## 5. Herramientas clave utilizadas en AI.zymes

| Herramienta | Tipo | Función en AI.zymes | Referencia |
|-------------|------|---------------------|------------|
| **ESMFold** | Predicción de estructura (deep learning) | Predecir estructuras 3D a partir de secuencias diseñadas; evaluar estabilidad conformacional | Lin et al., *Science* 2023 |
| **RosettaDesign** | Diseño de proteínas (física + estadística) | Optimizar residuos del **sitio activo**; modela ligandos químicos explícitamente | Richter et al., *PLoS One* 2011 |
| **RosettaRelax** | Relajación estructural | Relajar estructuras predichas para evaluar estabilidad y desplazamientos del backbone | Khatib et al., *PNAS* 2011; Maguire et al., *Proteins* 2021 |
| **ProteinMPNN** | Diseño de proteínas (deep learning, modelo generativo) | Rediseñar el **andamiaje proteico** completo; excelente generando proteínas termoestables | Dauparas et al., *Science* 2022 |
| **FieldTools** | Análisis de campos eléctricos | Calcular y evaluar campos eléctricos catalíticos a partir de trayectorias MD | Jabeen et al., *ACS Catal.* 2024 |
| **ESM2** | Modelo de lenguaje de proteínas (embeddings) | Generar representaciones vectoriales (embeddings) de secuencias para análisis tSNE de diversidad | Lin et al., *Science* 2023 |
| **AlphaFold3** | Predicción de estructura (deep learning) | Validar estado oligomérico de variantes finales (K3 monomérico vs. WT multimérico) | Abramson et al., *Nature* 2024 |
| **Dinámica Molecular (MD)** | Simulación atomística | Cribado de 10 ns para descartar variantes no productivas; simulaciones de 1 µs para validación | Amber, Gaussian 16 |

---

## 6. Conceptos clave explicados de forma sencilla

### 6.1 Diseño evolutivo computacional

A diferencia del diseño tradicional (que parte de una estructura fija e introduce mutaciones), el **diseño evolutivo** realiza múltiples ciclos de: diseñar variantes → evaluarlas (scoring) → seleccionar las mejores → usarlas como punto de partida para la siguiente iteración.

**Analogía:** Es como la evolución natural, pero en la computadora. En lugar de que la naturaleza seleccione a los más aptos, AI.zymes usa funciones de puntuación (scores) para decidir qué variantes "sobreviven" y se usan como padres de la siguiente generación.

**Ventaja:** Al variar continuamente la estructura de entrada (no partir siempre del mismo molde), se pueden explorar regiones del espacio de secuencias que serían inaccesibles en un solo ciclo de diseño.

### 6.2 Selección de Boltzmann

Es un método de selección probabilística inspirado en la distribución de Boltzmann de la física estadística:

- A cada variante se le asigna una **probabilidad de ser seleccionada** proporcional a `exp(-score / T)`, donde `T` es la **temperatura de Boltzmann**.
- A **T alta** (fase de exploración): las probabilidades son más uniformes → se seleccionan variantes diversas, incluso algunas sub-óptimas.
- A **T baja** (fase de explotación): las probabilidades se concentran en las mejores variantes → selección altamente elitista.
- AI.zymes reduce `T` gradualmente, pasando de explorar ampliamente el espacio a refinar las mejores soluciones.

### 6.3 Campos eléctricos catalíticos

Las enzimas aceleran reacciones no solo por proximidad física, sino también mediante **efectos electrostáticos**: los residuos del sitio activo y del andamiaje generan un **campo eléctrico orientado** que estabiliza el estado de transición de la reacción.

- Este campo se mide en **MV cm⁻¹** (megavoltios por centímetro).
- En la eliminación de Kemp, el campo relevante es el que actúa a lo largo del **enlace C─H que se rompe**.
- AI.zymes logra optimizar este campo *sin que los algoritmos de diseño sepan qué es un campo eléctrico*: simplemente puntúa las variantes por la intensidad del campo y la selección de Boltzmann favorece aquellas con campos más fuertes.

### 6.4 Optimización multiobjetivo

En lugar de optimizar una sola propiedad (ej. estabilidad), AI.zymes considera **simultáneamente** múltiples objetivos:

1. Afinidad por el estado de transición (interface score)
2. Estabilidad proteica (stability score)
3. Campo eléctrico catalítico (electric field score)

La **puntuación combinada** es la **media estandarizada** de los potenciales de cada objetivo. Esto permite obtener variantes que son buenas en *todos* los aspectos, no solo en uno.

### 6.5 Modularidad PDB

Cada herramienta en AI.zymes es un **módulo independiente** que:

- **Recibe** uno o más archivos PDB (estructura 3D de la proteína)
- **Procesa** (diseña, predice, relaja, evalúa)
- **Devuelve** uno o más archivos PDB

Esta arquitectura permite:
- Intercambiar herramientas fácilmente (ej. cambiar RosettaDesign por otra herramienta de diseño).
- Agregar nuevos módulos sin modificar los existentes.
- Ejecutar módulos en paralelo o en diferentes órdenes.
- Adaptarse rápidamente a nuevos avances en el campo.

---

## 7. Repositorio y disponibilidad de datos

- **Código fuente (GitHub):** [https://github.com/bunzela/AIzymes](https://github.com/bunzela/AIzymes)
- **Repositorio de datos (University of Bristol):** [https://data.bris.ac.uk/data/dataset/fvbvxg89ldwn2kv5ecxba9b7m](https://data.bris.ac.uk/data/dataset/fvbvxg89ldwn2kv5ecxba9b7m)
- **Información suplementaria:** Disponible en línea junto al artículo en Angewandte Chemie.

---

## 8. Relevancia para el proyecto RuBisCO

Los siguientes conceptos y herramientas del artículo de AI.zymes son **directamente aplicables** al análisis y posible ingeniería de RuBisCO:

### 8.1 Conceptos transferibles

| Concepto de AI.zymes | Aplicación potencial en RuBisCO |
|----------------------|--------------------------------|
| **Diseño evolutivo computacional** | Explorar variantes de RuBisCO que mejoren la discriminación CO₂/O₂ o la eficiencia catalítica, partiendo de estructuras existentes (ej. PDB de *Rhodospirillum rubrum* u otras). |
| **Selección de Boltzmann multiobjetivo** | Optimizar simultáneamente: (a) afinidad por el estado de transición de carboxilación, (b) estabilidad del complejo enzima-sustrato, (c) campo eléctrico en el sitio activo. |
| **Campos eléctricos catalíticos (FieldTools)** | Analizar y optimizar el campo eléctrico en el sitio activo de RuBisCO para favorecer la carboxilación sobre la oxigenación (discriminación CO₂/O₂). La orientación del campo podría estabilizar diferencialmente el estado de transición de carboxilación. |
| **Cribado por MD corta (≤10 ns)** | Descartar variantes de RuBisCO que no mantengan la geometría productiva del complejo enzima-RuBP-CO₂/Mg²⁺ durante simulaciones cortas, antes de invertir en simulaciones largas o pruebas experimentales. |
| **Modularidad PDB** | Integrar herramientas existentes en el proyecto (análisis de cavidades, docking, MD) en un pipeline automatizado donde la salida de cada paso alimente al siguiente mediante archivos PDB. |
| **ProteinMPNN para termoestabilidad** | Rediseñar el andamiaje de RuBisCO para mejorar su termoestabilidad sin alterar los residuos catalíticos del sitio activo, un enfoque directamente análogo al usado en KSI. |
| **ESMFold para predicción estructural** | Validar rápidamente si las variantes diseñadas de RuBisCO pliegan correctamente antes de realizar costosas simulaciones MD o expresión experimental. |

### 8.2 Flujo de trabajo adaptable a RuBisCO

```
[Estructura PDB inicial de RuBisCO]
         │
         ▼
[Generación de variantes con RosettaDesign (sitio activo) + ProteinMPNN (andamiaje)]
         │
         ▼
[Predicción de estructura: ESMFold]
         │
         ▼
[Relajación: RosettaRelax]
         │
         ▼
[Evaluación multiobjetivo:]
  • Interface score (afinidad CO₂ / RuBP)
  • Stability score
  • Campo eléctrico en el sitio activo (FieldTools)
  • Geometría del complejo Mg²⁺-CO₂-RuBP
         │
         ▼
[Selección de Boltzmann → iterar]
         │
         ▼
[Cribado MD corto (10 ns)]
         │
         ▼
[Variantes candidatas para validación experimental]
```

### 8.3 Herramientas inmediatamente utilizables

De la caja de herramientas de AI.zymes, las siguientes son de código abierto y podrían integrarse en los flujos de trabajo actuales del proyecto:

- **FieldTools:** para calcular campos eléctricos en trayectorias MD de RuBisCO ya existentes.
- **ProteinMPNN:** para rediseñar regiones del andamiaje de RuBisCO preservando el sitio activo.
- **ESMFold:** para predicción rápida de estructuras sin necesidad de instalar AlphaFold.

### 8.4 Lección metodológica central

El hallazgo más relevante para el proyecto RuBisCO es el **principio de optimización indirecta**: AI.zymes demostró que se puede optimizar una propiedad (campo eléctrico catalítico) incluso cuando los algoritmos de diseño no la consideran explícitamente, siempre que exista una **métrica cuantificable** que la selección de Boltzmann pueda utilizar. Para RuBisCO, esto significa que:

> Si podemos definir una **puntuación de discriminación CO₂/O₂** (basada en geometría del sitio activo, campos eléctricos, energías de unión diferenciales, o simulaciones MD), AI.zymes podría optimizarla evolutivamente, **incluso sin tener un algoritmo de diseño que "entienda" la discriminación CO₂/O₂**.

---

*Documento generado a partir de: Merlicek et al. (2025) Angew. Chem. Int. Ed. 64, e202507031. Traducción y análisis conceptual para el proyecto de análisis molecular — Universidad de Concepción.*
