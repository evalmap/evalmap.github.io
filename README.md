# Mapa de Evaluación

Aplicación web para explorar y relacionar técnicas, evidencias evaluables, instrumentos de evaluación y dimensiones transversales de la evaluación educativa, incluyendo trazabilidad, autoría y uso de IA.

## Cómo ejecutar

```bash
# Desde la carpeta del proyecto:
python3 -m http.server 8080
# Luego abrir: http://localhost:8080
```

> No abrir `index.html` directamente desde el sistema de archivos (los JSON no cargarán por restricciones CORS).

## Estructura del proyecto

```
/
├── index.html                  # Aplicación principal
├── mapa_evaluacion.md          # Mapa completo generado en Markdown
├── css/
│   └── styles.css              # Estilos (modo claro/oscuro/sistema)
├── src/
│   ├── app.js                  # Lógica principal: catálogo, grafo, filtros y planificador
│   ├── i18n.js                 # Textos de interfaz en castellano, catalán e inglés
│   └── legacy/                 # Motor, parser, generador y exportación antiguos
├── data/
│   ├── es/                     # Datos principales en castellano
│   ├── ca/                     # Datos traducidos al catalán
│   └── en/                     # Datos traducidos al inglés
└── scripts/
    ├── generate_mapa_evaluacion.py  # Genera mapa_evaluacion.md desde data/es/
    └── *.py                         # Scripts auxiliares de mantenimiento de datos
```

Los catálogos principales están en `data/es/`:

- `tecnicas.json`: técnicas de evaluación (12 registros)
- `dimensiones.json`: dimensiones transversales de evaluación (22 registros)
- `instrumentos.json`: evidencias evaluables (86 registros)
- `herramientas.json`: instrumentos de evaluación (58 registros)

## Generar el mapa en Markdown

`mapa_evaluacion.md` se genera a partir de los JSON en castellano:

```bash
python3 scripts/generate_mapa_evaluacion.py
```

La introducción y la estructura general del Markdown están definidas en ese script; el contenido de cada ficha sale de `data/es/`.

## Vistas de la aplicación

### Inicio
Mapa visual de las cuatro categorías con acceso directo a cada catálogo.

### Catálogo
Vista de dos paneles: lista filtrable a la izquierda y detalle con grafo de relaciones a la derecha.

- **Categorías**: Técnicas, Evidencias evaluables, Instrumentos de evaluación y Dimensiones transversales, incluida la trazabilidad del proceso y uso de IA.
- **Filtros**: búsqueda por texto y chips de filtrado por atributos específicos de cada categoría.
- **Grafo de relaciones**: al seleccionar un elemento se genera un grafo interactivo que muestra sus conexiones. Las dimensiones transversales aparecen siempre a la izquierda del nodo central.
  - **Expandir relaciones**: muestra conexiones de segundo nivel.
  - **Modo: esenciales / todas**: filtra por tipo de relación (principal + complementaria, u ocasional también).
  - **Ver**: activa/desactiva categorías en el grafo (Técnicas, Evidencias evaluables, Instrumentos de evaluación, Dimensiones).
  - **Tipos de relación**: principal, complementaria, ocasional y transversal (dimensiones).
- **Panel de detalle**: ficha completa del elemento con descripción, relaciones agrupadas y acciones de copiar (Markdown) e imprimir.

## Categorías y relaciones

| Categoría | Registros | Descripción |
|---|---|---|
| Técnicas | 12 | Procedimientos para recoger evidencias del aprendizaje |
| Evidencias evaluables | 86 | Tareas, actividades y producciones mediante las que el alumnado hace visible su aprendizaje |
| Instrumentos de evaluación | 58 | Rúbricas, escalas, listas, registros y declaraciones para valorar y retroalimentar evidencias |
| Dimensiones | 22 | Ejes transversales que contextualizan la evaluación: finalidad, agente, enfoque, trazabilidad, etc. |

Las relaciones entre categorías tienen tres intensidades: **principal**, **complementaria** y **ocasional**.
