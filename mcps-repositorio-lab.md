# MCPs para Modelado Molecular — Laboratorio Recabarren

> Repositorio de MCPs (Model Context Protocol) utiles para el proyecto RuBisCO y quimica computacional en general.

---

## 1. PDB MCP

| Campo       | Detalle                                                                |
| ----------- | ---------------------------------------------------------------------- |
| **Que hace**| Buscar y descargar estructuras del Protein Data Bank, metricas de calidad RSRZ/Clashscore, informacion de ligandos |
| **API**     | RCSB PDB Search API (publica, sin key)                                 |
| **Costo**   | Gratis                                                                 |
| **Repo**    | Buscar `pdb-mcp` en GitHub o npm                                       |

**Uso en RuBisCO:** Descargar estructuras cristalograficas de RuBisCO (ej. 1IR1, 1RBO, 4RUB), analizar calidad del modelo, extraer ligandos unidos.

---

## 2. PDBe MCP

| Campo       | Detalle                                                                        |
| ----------- | ------------------------------------------------------------------------------ |
| **Que hace**| Acceso a PDBe API: grafo de conocimiento, busqueda avanzada de proteinas, secuencias, go-terms, estructuras similares |
| **API**     | PDBe GraphQL API (publica)                                                     |
| **Costo**   | Gratis                                                                         |
| **Repo**    | Buscar `pdbe-mcp` en GitHub                                                    |

**Uso en RuBisCO:** Encontrar estructuras de RuBisCO de diferentes organismos, comparar sitios activos, obtener anotaciones GO y UniProt.

---

## 3. PubChem MCP

| Campo       | Detalle                                                                       |
| ----------- | ----------------------------------------------------------------------------- |
| **Que hace**| Buscar compuestos (110M+), obtener propiedades fisicoquimicas, bioensayos, similitud molecular, CID/InChI/SMILES |
| **API**     | PubChem PUG REST (publica, rate-limited)                                      |
| **Costo**   | Gratis                                                                        |
| **Repo**    | Buscar `pubchem-mcp` en GitHub                                                |

**Uso en RuBisCO:** Buscar sustratos (RuBP, CO2), inhibidores conocidos, aniones estabilizadores, propiedades de ligandos candidatos para docking.

---

## 4. RDKit MCP 3D

| Campo       | Detalle                                                                 |
| ----------- | ----------------------------------------------------------------------- |
| **Que hace**| Convertir SMILES a estructura 3D, generar conformeros, SDF, visualizacion molecular |
| **Libreria**| RDKit (open-source, BSD license)                                        |
| **Costo**   | Gratis                                                                  |
| **Repo**    | Buscar `rdkit-mcp` en GitHub                                            |

**Uso en RuBisCO:** Generar conformaciones 3D de inhibidores/sustratos, preparar ligandos para docking, visualizar moleculas.

---

## 5. ChEMBL MCP

| Campo       | Detalle                                                                    |
| ----------- | -------------------------------------------------------------------------- |
| **Que hace**| Acceder a 2.4M compuestos bioactivos, datos de actividad (IC50/EC50/Ki), farmacos aprobados, blancos |
| **API**     | ChEMBL API (publica, con key opcional)                                     |
| **Costo**   | Gratis                                                                     |
| **Repo**    | Buscar `chembl-mcp` en GitHub                                              |

**Uso en RuBisCO:** Obtener datos de actividad de inhibidores de RuBisCO reportados, comparar potencias, identificar farmacos que cross-reaccionan.

---

## 6. Rosetta MCP

| Campo       | Detalle                                                                  |
| ----------- | ------------------------------------------------------------------------ |
| **Que hace**| Docking molecular, mutaciones in silico, calculo de ΔΔG, diseno de proteinas |
| **Software**| Rosetta Commons (licencia academica disponible)                           |
| **Costo**   | Demo gratis / Licencia academica gratuita                                |
| **Repo**    | Buscar `rosetta-mcp` en GitHub                                           |

**Uso en RuBisCO:** Mutaciones en el sitio activo, docking de ligandos, calculo de energia de union, diseno de variantes.

---

## 7. Open Babel MCP (propuesto)

| Campo       | Detalle                                                            |
| ----------- | ------------------------------------------------------------------ |
| **Que hace**| Conversion entre formatos (PDB, XYZ, MOL2, SDF, SMILES, etc.), filtrado molecular |
| **Libreria**| Open Babel (GPL)                                                   |
| **Costo**   | Gratis                                                             |
| **Repo**    | Buscar `openbabel-mcp` en GitHub                                   |

**Uso en RuBisCO:** Convertir ligandos entre formatos, preparar archivos de entrada para Gaussian/ORCA.

---

## 8. Gaussian MCP (propuesto)

| Campo       | Detalle                                                                 |
| ----------- | ----------------------------------------------------------------------- |
| **Que hace**| Generar inputs de Gaussian (.gjf), analizar outputs, extraer energia/geometria/frecuencias |
| **Software**| Gaussian 16 (licencia del laboratorio)                                   |
| **Costo**   | Requiere licencia Gaussian                                              |
| **Repo**    | Buscar `gaussian-mcp` en GitHub                                         |

**Uso en RuBisCO:** Preparar calculos QM del sitio activo, analizar optimizaciones de geometria, calcular energias de union.

---

## Resumen para priorizar

| Prioridad | MCP            | Justificacion RuBisCO                             |
| --------- | -------------- | ------------------------------------------------- |
| 🔴 Alta   | PDB MCP        | Estructuras cristalograficas de partida           |
| 🔴 Alta   | PubChem MCP    | Sustratos, inhibidores, ligandos                  |
| 🔴 Alta   | RDKit MCP 3D   | Modelado 3D de ligandos, conformeros              |
| 🟡 Media  | PDBe MCP       | Busqueda avanzada de estructuras homologas        |
| 🟡 Media  | ChEMBL MCP     | Datos de actividad biologica reportados           |
| 🟡 Media  | Rosetta MCP    | Docking y mutaciones (si el lab trabaja con el)   |
| 🟢 Baja   | Open Babel MCP | Conversion de formatos (util pero trivial)        |
| 🟢 Baja   | Gaussian MCP   | Solo si se automatizan calculos QM en batch       |

---

> **Nota:** Algunos MCPs listados aun no existen como paquetes publicos. Para esos, habra que desarrollarlos internamente en el laboratorio. Los priorizados (PDB, PubChem, RDKit) si tienen implementaciones disponibles.
