# Mapa de Evaluación

Aplicación web para explorar y relacionar técnicas, instrumentos, herramientas y dimensiones transversales de evaluación educativa.

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
├── index.html              # Aplicación principal
├── css/
│   └── styles.css          # Estilos (modo claro/oscuro/sistema)
├── src/
│   ├── app.js              # Lógica principal: catálogo, grafo de relaciones, filtros
│   ├── recommendationEngine.js  # Motor de recomendación
│   ├── generator.js        # Generador de herramientas
│   ├── parser.js           # Parser de texto libre
│   └── export.js           # Exportación de resultados
└── data/
    ├── tecnicas.json        # Catálogo de técnicas (12 registros)
    ├── instrumentos.json    # Catálogo de instrumentos (83 registros)
    ├── herramientas.json    # Catálogo de herramientas (57 registros)
    └── dimensiones.json     # Dimensiones transversales de evaluación (20 registros)
```

## Vistas de la aplicación

### Inicio
Mapa visual de las cuatro categorías con acceso directo a cada catálogo.

### Catálogo
Vista de dos paneles: lista filtrable a la izquierda y detalle con grafo de relaciones a la derecha.

- **Categorías**: Técnicas, Instrumentos, Herramientas y Dimensiones transversales.
- **Filtros**: búsqueda por texto y chips de filtrado por atributos específicos de cada categoría.
- **Grafo de relaciones**: al seleccionar un elemento se genera un grafo interactivo que muestra sus conexiones. Las dimensiones transversales aparecen siempre a la izquierda del nodo central.
  - **Expandir relaciones**: muestra conexiones de segundo nivel.
  - **Modo: esenciales / todas**: filtra por tipo de relación (principal + complementaria, u ocasional también).
  - **Ver**: activa/desactiva categorías en el grafo (Técnicas, Instrumentos, Herramientas, Dimensiones).
  - **Tipos de relación**: principal, complementaria, ocasional y transversal (dimensiones).
- **Panel de detalle**: ficha completa del elemento con descripción, relaciones agrupadas y acciones de copiar (Markdown) e imprimir.

## Categorías y relaciones

| Categoría | Registros | Descripción |
|---|---|---|
| Técnicas | 12 | Procedimientos para recoger evidencias del aprendizaje |
| Instrumentos | 83 | Actividades, productos o situaciones que generan evidencias |
| Herramientas | 57 | Recursos, plantillas y registros de apoyo a la evaluación |
| Dimensiones | 20 | Dimensiones transversales que atraviesan técnicas e instrumentos |

Las relaciones entre categorías tienen tres intensidades: **principal**, **complementaria** y **ocasional**.
