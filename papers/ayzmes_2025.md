# AI.zymes — Resumen Ejecutivo

**Paper:** Merlicek et al. (2025) — Angew. Chem. Int. Ed., DOI: 10.1002/anie.202507031
**Código:** https://github.com/bunzela/AIzymes

---

## ¿Qué es?
Plataforma modular para **diseño evolutivo computacional de enzimas**. Integra Rosetta, ESMFold, ProteinMPNN y FieldTools en ciclos iterativos de diseño y selección.

## ¿Cómo funciona? (6 pasos)
1. **Generar** variantes iniciales de una proteína
2. **Seleccionar** las mejores → selección de Boltzmann multiobjetivo (afinidad al TS + estabilidad + campo eléctrico)
3. **Predecir** estructura 3D con **ESMFold**
4. **Relajar** estructura con **RosettaRelax**
5. **Rediseñar**: RosettaDesign (70%, sitio activo) + ProteinMPNN (30%, scaffold)
6. **Iterar** — las variantes rediseñadas vuelven al pool

**Clave modular:** todas las herramientas se comunican mediante archivos **PDB**.

## Resultado principal
- **7.7x** mejora de actividad (KSI Kemp eliminasa)
- Solo **7 variantes** testeadas experimentalmente
- K3: monomérica, termoestable hasta **95 °C**

## Lección para RuBisCO
> AI.zymes puede optimizar cualquier propiedad siempre que exista una **métrica cuantificable** para la selección de Boltzmann. Si definimos una puntuación de discriminación CO₂/O₂, podemos optimizarla evolutivamente sin necesitar algoritmos que "entiendan" la discriminación.

## Herramientas usables ya

| Herramienta | Para qué en RuBisCO |
|-------------|---------------------|
| **ESMFold** | Predecir estructuras desde secuencia (API gratuita) |
| **ProteinMPNN** | Rediseñar scaffold, mejorar termoestabilidad |
| **FieldTools** | Calcular campos eléctricos en sitio activo |
| **MD corta (10 ns)** | Filtrar variantes no productivas |

## Conceptos clave

- **Diseño evolutivo:** ciclos repetidos de diseñar→evaluar→seleccionar→rediseñar
- **Selección de Boltzmann:** selección probabilística con temperatura que baja gradualmente (explorar → explotar)
- **Campos eléctricos catalíticos:** el campo que la enzima genera para estabilizar el estado de transición
- **Optimización forward-looking:** selecciona variantes por el potencial promedio de ellas y sus descendientes
