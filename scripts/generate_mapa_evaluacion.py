#!/usr/bin/env python3
"""
Genera mapa_evaluacion.md a partir de los JSON de datos en data/es/.
Uso: python scripts/generate_mapa_evaluacion.py
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "es")
OUTPUT = os.path.join(BASE_DIR, "mapa_evaluacion.md")


def load(filename):
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as f:
        return json.load(f)


def sep(value):
    """Convierte lista separada por '; ' en lista separada por ', '."""
    if not value:
        return ""
    return value.replace("; ", ", ")


def field(label, value):
    """Devuelve una línea de campo markdown o cadena vacía si no hay valor."""
    if not value:
        return ""
    return f"**{label}:** {value}\n"


def tecnica_block(n, item):
    lines = []
    lines.append(f"### {n}. {item['Técnica']}\n")
    lines.append(f"_{item['Descripción breve']}_\n")
    lines.append(f"**Fase:** {item['Fase']} · **Participación:** {item['Participación']}\n")
    lines.append(f"{item['Descripción detallada']}\n")
    lines.append(field("Finalidad", item.get("Finalidad principal", "")))
    lines.append(field("Cuándo conviene", item.get("Cuándo conviene", "")))
    lines.append(field("Evidencias habituales", item.get("Evidencias habituales", "")))
    lines.append(field("Limitaciones", item.get("Limitaciones", "")))
    lines.append(field("Medios/evidencias asociados", sep(item.get("Medios/evidencias asociados", ""))))
    lines.append(field("Instrumentos de evaluación relacionados", sep(item.get("Instrumentos de evaluación recomendados", ""))))
    lines.append("---\n")
    return "\n".join(l for l in lines if l) + "\n"


def dimension_block(n, item):
    lines = []
    lines.append(f"### {n}. {item['Dimensión']}\n")
    lines.append(f"_{item['Descripción breve']}_\n")
    lines.append(f"**Categoría:** {item['Categoría']} · **Fase:** {item['Fase']} · **Participación:** {item['Participación']}\n")
    lines.append(f"{item['Descripción detallada']}\n")
    lines.append(field("Función pedagógica", item.get("Función pedagógica", "")))
    lines.append(field("Cuándo conviene", item.get("Cuándo conviene", "")))
    lines.append(field("Evidencias habituales", item.get("Evidencias habituales", "")))
    lines.append(field("Precauciones", item.get("Precauciones", "")))
    lines.append(field("Medios/evidencias asociados", sep(item.get("Medios/evidencias asociados", ""))))
    lines.append(field("Instrumentos de evaluación recomendados", sep(item.get("Instrumentos de evaluación recomendados", ""))))
    lines.append("---\n")
    return "\n".join(l for l in lines if l) + "\n"


def evidencia_block(n, item):
    lines = []
    lines.append(f"### {n}. {item['Instrumento']}\n")
    lines.append(f"_{item['Descripción breve']}_\n")
    meta = f"**Tipo:** {item['Tipo']} · **Fase:** {item['Fase']}"
    if item.get("Complejidad"):
        meta += f" · **Complejidad:** {item['Complejidad']}"
    meta += f" · **Participación:** {item['Participación']}"
    lines.append(meta + "\n")
    lines.append(f"{item['Descripción detallada']}\n")
    lines.append(field("Evidencia", item.get("Evidencia", "")))
    lines.append(field("Adecuado para", item.get("Adecuado para", "")))
    lines.append(field("Técnicas asociadas", sep(item.get("Técnicas asociadas", ""))))
    lines.append(field("Instrumentos de evaluación recomendados", sep(item.get("Instrumentos de evaluación recomendados", ""))))
    lines.append(field("Dimensiones asociadas", sep(item.get("Dimensiones asociadas", ""))))
    lines.append("---\n")
    return "\n".join(l for l in lines if l) + "\n"


def herramienta_block(n, item):
    lines = []
    lines.append(f"### {n}. {item['Herramienta']}\n")
    lines.append(f"_{item['Descripción breve']}_\n")
    meta = f"**Tipo:** {item['Tipo']} · **Fase:** {item['Fase']}"
    if item.get("Complejidad"):
        meta += f" · **Complejidad:** {item['Complejidad']}"
    meta += f" · **Participación:** {item['Participación']}"
    lines.append(meta + "\n")
    lines.append(f"{item['Descripción detallada']}\n")
    lines.append(field("Sirve para", item.get("Sirve para", "")))
    lines.append(field("Adecuada para", sep(item.get("Adecuada para", ""))))
    lines.append(field("Ventajas", item.get("Ventajas", "")))
    lines.append(field("Limitaciones", item.get("Limitaciones", "")))
    lines.append(field("Técnicas asociadas", sep(item.get("Técnicas asociadas", ""))))
    lines.append(field("Medios/evidencias compatibles", sep(item.get("Medios/evidencias compatibles", item.get("Medios/evidencias asociados", "")))))
    lines.append(field("Dimensiones asociadas", sep(item.get("Dimensiones asociadas", ""))))
    lines.append("---\n")
    return "\n".join(l for l in lines if l) + "\n"


def main():
    tecnicas = load("tecnicas.json")
    dimensiones = load("dimensiones.json")
    instrumentos = load("instrumentos.json")   # medio_evidencia (Evidencias evaluables)
    herramientas = load("herramientas.json")   # instrumento_evaluacion (Instrumentos de evaluación)

    out = []

    # Cabecera estática
    out.append("""# Mapa de Evaluación Educativa

> Guía de técnicas, dimensiones, evidencias evaluables e instrumentos de evaluación para diseñar evaluaciones educativas coherentes.

## Índice

1. [Técnicas de evaluación](#técnicas-de-evaluación)
2. [Dimensiones transversales](#dimensiones-transversales)
3. [Evidencias evaluables](#evidencias-evaluables)
4. [Instrumentos de evaluación](#instrumentos-de-evaluación)

## Marco Conceptual

Este mapa no pretende ofrecer una clasificación cerrada, sino una ayuda práctica para diseñar evaluaciones más coherentes, variadas y útiles en el aula. En evaluación educativa conviene distinguir entre lo que el alumnado hace o produce, cómo se recoge esa información, con qué criterios se interpreta y qué decisión docente se toma a partir de ella.

Las **técnicas** son procedimientos de recogida, análisis o contraste de evidencias de aprendizaje. Las **dimensiones transversales** sitúan pedagógicamente la evaluación según el agente, la finalidad, el momento, el enfoque curricular, el tipo de evidencia, el soporte y el contexto metodológico. Las **evidencias evaluables** son las tareas, actividades, productos, actuaciones o respuestas mediante las cuales el alumnado hace visible su aprendizaje. Los **instrumentos de evaluación** permiten registrar, valorar, retroalimentar, calificar o comunicar esas evidencias, aunque no todos los instrumentos tienen por qué usarse para calificar.

La utilidad pedagógica del mapa depende de su uso docente: las evidencias deben estar alineadas con los criterios de evaluación, ser suficientes y variadas, y tener en cuenta el contexto real del aula, la diversidad del alumnado y la carga de trabajo asumible. Una misma actividad puede cumplir funciones distintas según el momento y la finalidad: diagnóstica, formativa, sumativa, competencial, inclusiva o acreditativa.

Por tanto, las relaciones entre técnicas, dimensiones, evidencias e instrumentos deben entenderse como orientaciones para tomar decisiones, no como recetas automáticas. Evaluar bien implica seleccionar evidencias relevantes, interpretarlas con criterios claros, ofrecer retroalimentación útil y, cuando corresponda, traducirlas en una calificación justificable.

## Técnicas de Evaluación
""")

    for i, item in enumerate(tecnicas, 1):
        out.append(tecnica_block(i, item))

    out.append("## Dimensiones Transversales\n")
    for i, item in enumerate(dimensiones, 1):
        out.append(dimension_block(i, item))

    out.append("## Evidencias Evaluables\n")
    for i, item in enumerate(instrumentos, 1):
        out.append(evidencia_block(i, item))

    out.append("## Instrumentos de Evaluación\n")
    for i, item in enumerate(herramientas, 1):
        out.append(herramienta_block(i, item))

    content = "\n".join(out).rstrip() + "\n"

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generado: {OUTPUT}")
    print(f"  Técnicas:    {len(tecnicas)}")
    print(f"  Dimensiones: {len(dimensiones)}")
    print(f"  Evidencias:  {len(instrumentos)}")
    print(f"  Instrumentos:{len(herramientas)}")
    print(f"  Total ítems: {len(tecnicas) + len(dimensiones) + len(instrumentos) + len(herramientas)}")


if __name__ == "__main__":
    main()
