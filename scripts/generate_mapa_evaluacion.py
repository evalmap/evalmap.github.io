#!/usr/bin/env python3
"""
Genera los mapas Markdown a partir de los JSON de datos en data/{idioma}/.
Uso: python scripts/generate_mapa_evaluacion.py
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGS = {
    "es": {
        "output": "mapa_evaluacion.md",
        "title": "Mapa de Evaluación Educativa",
        "subtitle": "Guía de técnicas, dimensiones, evidencias evaluables e instrumentos de evaluación para diseñar evaluaciones educativas coherentes.",
        "toc": "Índice",
        "conceptual": "Marco Conceptual",
        "techniques": "Técnicas de Evaluación",
        "dimensions": "Dimensiones Transversales",
        "evidence": "Evidencias Evaluables",
        "tools": "Instrumentos de Evaluación",
        "intro": """Este mapa no pretende ofrecer una clasificación cerrada, sino una ayuda práctica para diseñar evaluaciones más coherentes, variadas y útiles en el aula. En evaluación educativa conviene distinguir entre lo que el alumnado hace o produce, cómo se recoge esa información, con qué criterios se interpreta y qué decisión docente se toma a partir de ella.

Las **técnicas** son procedimientos de recogida, análisis o contraste de evidencias de aprendizaje. Las **dimensiones transversales** sitúan pedagógicamente la evaluación según el agente, la finalidad, el momento, el enfoque curricular, el tipo de evidencia, el soporte y el contexto metodológico. Las **evidencias evaluables** son las tareas, actividades, productos, actuaciones o respuestas mediante las cuales el alumnado hace visible su aprendizaje. Los **instrumentos de evaluación** permiten registrar, valorar, retroalimentar, calificar o comunicar esas evidencias, aunque no todos los instrumentos tienen por qué usarse para calificar.

La utilidad pedagógica del mapa depende de su uso docente: las evidencias deben estar alineadas con los criterios de evaluación, ser suficientes y variadas, y tener en cuenta el contexto real del aula, la diversidad del alumnado y la carga de trabajo asumible. Una misma actividad puede cumplir funciones distintas según el momento y la finalidad: diagnóstica, formativa, sumativa, competencial, inclusiva o acreditativa.

Por tanto, las relaciones entre técnicas, dimensiones, evidencias e instrumentos deben entenderse como orientaciones para tomar decisiones, no como recetas automáticas. Evaluar bien implica seleccionar evidencias relevantes, interpretarlas con criterios claros, ofrecer retroalimentación útil y, cuando corresponda, traducirlas en una calificación justificable.""",
        "labels": {
            "phase": "Fase",
            "participation": "Participación",
            "purpose": "Finalidad",
            "when": "Cuándo conviene",
            "typical_evidence": "Evidencias habituales",
            "limitations": "Limitaciones",
            "associated_media": "Medios/evidencias asociados",
            "related_tools": "Instrumentos de evaluación relacionados",
            "recommended_tools": "Instrumentos de evaluación recomendados",
            "category": "Categoría",
            "pedagogical_function": "Función pedagógica",
            "precautions": "Precauciones",
            "type": "Tipo",
            "complexity": "Complejidad",
            "evidence_field": "Evidencia",
            "suitable_for": "Adecuado para",
            "associated_techniques": "Técnicas asociadas",
            "associated_dimensions": "Dimensiones asociadas",
            "serves_for": "Sirve para",
            "suitable_tool_for": "Adecuada para",
            "advantages": "Ventajas",
            "compatible_media": "Medios/evidencias compatibles",
            "_values": {},
        },
    },
    "ca": {
        "output": "mapa_avaluacio.md",
        "title": "Mapa d'Avaluació Educativa",
        "subtitle": "Guia de tècniques, dimensions, evidències avaluables i instruments d'avaluació per dissenyar avaluacions educatives coherents.",
        "toc": "Índex",
        "conceptual": "Marc Conceptual",
        "techniques": "Tècniques d'Avaluació",
        "dimensions": "Dimensions Transversals",
        "evidence": "Evidències Avaluables",
        "tools": "Instruments d'Avaluació",
        "intro": """Aquest mapa no pretén oferir una classificació tancada, sinó una ajuda pràctica per dissenyar avaluacions més coherents, variades i útils a l'aula. En avaluació educativa convé distingir entre allò que l'alumnat fa o produeix, com es recull aquesta informació, amb quins criteris s'interpreta i quina decisió docent es pren a partir d'ella.

Les **tècniques** són procediments de recollida, anàlisi o contrast d'evidències d'aprenentatge. Les **dimensions transversals** situen pedagògicament l'avaluació segons l'agent, la finalitat, el moment, l'enfocament curricular, el tipus d'evidència, el suport i el context metodològic. Les **evidències avaluables** són les tasques, activitats, productes, actuacions o respostes mitjançant les quals l'alumnat fa visible el seu aprenentatge. Els **instruments d'avaluació** permeten registrar, valorar, retroalimentar, qualificar o comunicar aquestes evidències, encara que no tots els instruments s'han d'utilitzar necessàriament per qualificar.

La utilitat pedagògica del mapa depèn del seu ús docent: les evidències han d'estar alineades amb els criteris d'avaluació, ser suficients i variades, i tenir en compte el context real de l'aula, la diversitat de l'alumnat i la càrrega de treball assumible. Una mateixa activitat pot complir funcions diferents segons el moment i la finalitat: diagnòstica, formativa, sumativa, competencial, inclusiva o acreditativa.

Per tant, les relacions entre tècniques, dimensions, evidències i instruments s'han d'entendre com orientacions per prendre decisions, no com receptes automàtiques. Avaluar bé implica seleccionar evidències rellevants, interpretar-les amb criteris clars, oferir retroalimentació útil i, quan correspongui, traduir-les en una qualificació justificable.""",
        "labels": {
            "phase": "Fase",
            "participation": "Participació",
            "purpose": "Finalitat",
            "when": "Quan convé",
            "typical_evidence": "Evidències habituals",
            "limitations": "Limitacions",
            "associated_media": "Mitjans/evidències associats",
            "related_tools": "Instruments d'avaluació relacionats",
            "recommended_tools": "Instruments d'avaluació recomanats",
            "category": "Categoria",
            "pedagogical_function": "Funció pedagògica",
            "precautions": "Precaucions",
            "type": "Tipus",
            "complexity": "Complexitat",
            "evidence_field": "Evidència",
            "suitable_for": "Adequat per a",
            "associated_techniques": "Tècniques associades",
            "associated_dimensions": "Dimensions associades",
            "serves_for": "Serveix per a",
            "suitable_tool_for": "Adequada per a",
            "advantages": "Avantatges",
            "compatible_media": "Mitjans/evidències compatibles",
            "_values": {
                "Diseño": "Disseny",
                "Inicial": "Inicial",
                "Proceso": "Procés",
                "Final": "Final",
                "Docente": "Docent",
                "Alumno": "Alumne",
                "Iguales": "Iguals",
                "Grupo": "Grup",
                "Equipo docente": "Equip docent",
                "Alta": "Alta",
                "Media": "Mitjana",
                "Baja": "Baixa",
                "Agente evaluador": "Agent avaluador",
                "Contexto metodológico": "Context metodològic",
                "Enfoque curricular": "Enfocament curricular",
                "Finalidad y momento": "Finalitat i moment",
                "Finalidad y uso": "Finalitat i ús",
                "Soporte de evidencias": "Suport d'evidències",
                "Tipo de evidencia": "Tipus d'evidència",
                "Trazabilidad": "Traçabilitat",
                "autoría": "autoria",
                "proceso": "procés",
            },
        },
    },
    "en": {
        "output": "assessment_map.md",
        "title": "Educational Assessment Map",
        "subtitle": "Guide to assessment techniques, cross-cutting dimensions, assessable evidence and assessment instruments for designing coherent educational assessment.",
        "toc": "Table of Contents",
        "conceptual": "Conceptual Framework",
        "techniques": "Assessment Techniques",
        "dimensions": "Cross-cutting Dimensions",
        "evidence": "Assessable Evidence",
        "tools": "Assessment Instruments",
        "intro": """This map is not intended as a closed classification, but as a practical aid for designing more coherent, varied and useful assessment in the classroom. In educational assessment, it is useful to distinguish between what students do or produce, how that information is gathered, which criteria are used to interpret it and which teaching decision is made from it.

**Techniques** are procedures for gathering, analysing or contrasting evidence of learning. **Cross-cutting dimensions** situate assessment pedagogically according to the agent, purpose, timing, curricular approach, type of evidence, medium and methodological context. **Assessable evidence** refers to the tasks, activities, products, performances or responses through which students make their learning visible. **Assessment instruments** make it possible to record, value, provide feedback on, grade or communicate that evidence, although not every instrument has to be used for grading.

The pedagogical usefulness of the map depends on how teachers use it: evidence should be aligned with assessment criteria, sufficient and varied, and should take into account the real classroom context, student diversity and a manageable workload. The same activity can serve different functions depending on timing and purpose: diagnostic, formative, summative, competency-based, inclusive or accrediting.

Therefore, the relationships between techniques, dimensions, evidence and instruments should be understood as guidance for decision-making, not as automatic recipes. Good assessment means selecting relevant evidence, interpreting it with clear criteria, providing useful feedback and, when appropriate, translating it into a justifiable grade.""",
        "labels": {
            "phase": "Phase",
            "participation": "Participation",
            "purpose": "Purpose",
            "when": "When to use",
            "typical_evidence": "Typical evidence",
            "limitations": "Limitations",
            "associated_media": "Associated media/evidence",
            "related_tools": "Related assessment instruments",
            "recommended_tools": "Recommended assessment instruments",
            "category": "Category",
            "pedagogical_function": "Pedagogical function",
            "precautions": "Precautions",
            "type": "Type",
            "complexity": "Complexity",
            "evidence_field": "Evidence",
            "suitable_for": "Suitable for",
            "associated_techniques": "Associated techniques",
            "associated_dimensions": "Associated dimensions",
            "serves_for": "Useful for",
            "suitable_tool_for": "Suitable for",
            "advantages": "Advantages",
            "compatible_media": "Compatible media/evidence",
            "_values": {
                "Diseño": "Design",
                "Inicial": "Initial",
                "Proceso": "Process",
                "Final": "Final",
                "Docente": "Teacher",
                "Alumno": "Student",
                "Iguales": "Peers",
                "Grupo": "Group",
                "Equipo docente": "Teaching team",
                "Alta": "High",
                "Media": "Medium",
                "Baja": "Low",
                "Agente evaluador": "Assessment agent",
                "Contexto metodológico": "Methodological context",
                "Enfoque curricular": "Curricular approach",
                "Finalidad y momento": "Purpose and timing",
                "Finalidad y uso": "Purpose and use",
                "Soporte de evidencias": "Evidence medium",
                "Tipo de evidencia": "Type of evidence",
                "Trazabilidad": "Traceability",
                "autoría": "authorship",
                "proceso": "process",
            },
        },
    },
}


def load(lang, filename):
    data_dir = os.path.join(BASE_DIR, "data", lang)
    with open(os.path.join(data_dir, filename), encoding="utf-8") as f:
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


def slug(text):
    """Genera anclas Markdown sencillas para los títulos del documento."""
    value = text.lower().strip().replace(" ", "-")
    return re.sub(r"[^\w\-]", "", value, flags=re.UNICODE)


def translated_value(value, labels):
    """Traduce metadatos normalizados que siguen guardados en castellano."""
    translations = labels.get("_values", {})
    if not value or not translations:
        return value
    return "/".join(translations.get(part, part) for part in str(value).split("/"))


def relation_text(item, rel_key, names_by_code, fallback=""):
    """Devuelve nombres traducidos desde relaciones por código, o un campo heredado."""
    codes = item.get(rel_key) or []
    names = [names_by_code[code] for code in codes if code in names_by_code]
    if names:
        return ", ".join(names)
    return sep(item.get(fallback, "")) if fallback else ""


def tecnica_block(n, item, labels, names):
    lines = []
    lines.append(f"### {n}. {item['Técnica']}\n")
    lines.append(f"_{item['Descripción breve']}_\n")
    lines.append(f"**{labels['phase']}:** {translated_value(item['Fase'], labels)} · **{labels['participation']}:** {translated_value(item['Participación'], labels)}\n")
    lines.append(f"{item['Descripción detallada']}\n")
    lines.append(field(labels["purpose"], item.get("Finalidad principal", "")))
    lines.append(field(labels["when"], item.get("Cuándo conviene", "")))
    lines.append(field(labels["typical_evidence"], item.get("Evidencias habituales", "")))
    lines.append(field(labels["limitations"], item.get("Limitaciones", "")))
    lines.append(field(labels["associated_media"], relation_text(item, "rel_ins", names["instrumentos"], "Medios/evidencias asociados")))
    lines.append(field(labels["related_tools"], relation_text(item, "rel_her", names["herramientas"], "Instrumentos de evaluación recomendados")))
    lines.append("---\n")
    return "\n".join(l for l in lines if l) + "\n"


def dimension_block(n, item, labels, names):
    lines = []
    lines.append(f"### {n}. {item['Dimensión']}\n")
    lines.append(f"_{item['Descripción breve']}_\n")
    lines.append(f"**{labels['category']}:** {translated_value(item['Categoría'], labels)} · **{labels['phase']}:** {translated_value(item['Fase'], labels)} · **{labels['participation']}:** {translated_value(item['Participación'], labels)}\n")
    lines.append(f"{item['Descripción detallada']}\n")
    lines.append(field(labels["pedagogical_function"], item.get("Función pedagógica", "")))
    lines.append(field(labels["when"], item.get("Cuándo conviene", "")))
    lines.append(field(labels["typical_evidence"], item.get("Evidencias habituales", "")))
    lines.append(field(labels["precautions"], item.get("Precauciones", "")))
    lines.append(field(labels["associated_media"], relation_text(item, "rel_ins", names["instrumentos"], "Medios/evidencias asociados")))
    lines.append(field(labels["recommended_tools"], relation_text(item, "rel_her", names["herramientas"], "Instrumentos de evaluación recomendados")))
    lines.append("---\n")
    return "\n".join(l for l in lines if l) + "\n"


def evidencia_block(n, item, labels, names):
    lines = []
    lines.append(f"### {n}. {item['Instrumento']}\n")
    lines.append(f"_{item['Descripción breve']}_\n")
    meta = f"**{labels['type']}:** {translated_value(item['Tipo'], labels)} · **{labels['phase']}:** {translated_value(item['Fase'], labels)}"
    if item.get("Complejidad"):
        meta += f" · **{labels['complexity']}:** {translated_value(item['Complejidad'], labels)}"
    meta += f" · **{labels['participation']}:** {translated_value(item['Participación'], labels)}"
    lines.append(meta + "\n")
    lines.append(f"{item['Descripción detallada']}\n")
    lines.append(field(labels["evidence_field"], item.get("Evidencia", "")))
    lines.append(field(labels["suitable_for"], item.get("Adecuado para", "")))
    lines.append(field(labels["associated_techniques"], relation_text(item, "rel_tec", names["tecnicas"], "Técnicas asociadas")))
    lines.append(field(labels["recommended_tools"], relation_text(item, "rel_her", names["herramientas"], "Instrumentos de evaluación recomendados")))
    lines.append(field(labels["associated_dimensions"], relation_text(item, "rel_dim", names["dimensiones"], "Dimensiones asociadas")))
    lines.append("---\n")
    return "\n".join(l for l in lines if l) + "\n"


def herramienta_block(n, item, labels, names):
    lines = []
    lines.append(f"### {n}. {item['Herramienta']}\n")
    lines.append(f"_{item['Descripción breve']}_\n")
    meta = f"**{labels['type']}:** {translated_value(item['Tipo'], labels)} · **{labels['phase']}:** {translated_value(item['Fase'], labels)}"
    if item.get("Complejidad"):
        meta += f" · **{labels['complexity']}:** {translated_value(item['Complejidad'], labels)}"
    meta += f" · **{labels['participation']}:** {translated_value(item['Participación'], labels)}"
    lines.append(meta + "\n")
    lines.append(f"{item['Descripción detallada']}\n")
    lines.append(field(labels["serves_for"], item.get("Sirve para", "")))
    lines.append(field(labels["suitable_tool_for"], sep(item.get("Adecuada para", ""))))
    lines.append(field(labels["advantages"], item.get("Ventajas", "")))
    lines.append(field(labels["limitations"], item.get("Limitaciones", "")))
    lines.append(field(labels["associated_techniques"], relation_text(item, "rel_tec", names["tecnicas"], "Técnicas asociadas")))
    lines.append(field(labels["compatible_media"], relation_text(item, "rel_ins", names["instrumentos"], "Medios/evidencias compatibles")))
    lines.append(field(labels["associated_dimensions"], relation_text(item, "rel_dim", names["dimensiones"], "Dimensiones asociadas")))
    lines.append("---\n")
    return "\n".join(l for l in lines if l) + "\n"


def header(cfg):
    return f"""# {cfg['title']}

> {cfg['subtitle']}

## {cfg['toc']}

1. [{cfg['techniques']}](#{slug(cfg['techniques'])})
2. [{cfg['dimensions']}](#{slug(cfg['dimensions'])})
3. [{cfg['evidence']}](#{slug(cfg['evidence'])})
4. [{cfg['tools']}](#{slug(cfg['tools'])})

## {cfg['conceptual']}

{cfg['intro']}

## {cfg['techniques']}
"""


def generate(lang, cfg):
    labels = cfg["labels"]
    tecnicas = load(lang, "tecnicas.json")
    dimensiones = load(lang, "dimensiones.json")
    instrumentos = load(lang, "instrumentos.json")   # medio_evidencia (Evidencias evaluables)
    herramientas = load(lang, "herramientas.json")   # instrumento_evaluacion (Instrumentos de evaluación)
    names = {
        "tecnicas": {item["Código"]: item["Técnica"] for item in tecnicas},
        "dimensiones": {item["Código"]: item["Dimensión"] for item in dimensiones},
        "instrumentos": {item["Código"]: item["Instrumento"] for item in instrumentos},
        "herramientas": {item["Código"]: item["Herramienta"] for item in herramientas},
    }

    out = []
    out.append(header(cfg))

    for i, item in enumerate(tecnicas, 1):
        out.append(tecnica_block(i, item, labels, names))

    out.append(f"## {cfg['dimensions']}\n")
    for i, item in enumerate(dimensiones, 1):
        out.append(dimension_block(i, item, labels, names))

    out.append(f"## {cfg['evidence']}\n")
    for i, item in enumerate(instrumentos, 1):
        out.append(evidencia_block(i, item, labels, names))

    out.append(f"## {cfg['tools']}\n")
    for i, item in enumerate(herramientas, 1):
        out.append(herramienta_block(i, item, labels, names))

    content = "\n".join(out).rstrip() + "\n"
    output = os.path.join(BASE_DIR, cfg["output"])

    with open(output, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generado ({lang}): {output}")
    print(f"  Técnicas:    {len(tecnicas)}")
    print(f"  Dimensiones: {len(dimensiones)}")
    print(f"  Evidencias:  {len(instrumentos)}")
    print(f"  Instrumentos:{len(herramientas)}")
    print(f"  Total ítems: {len(tecnicas) + len(dimensiones) + len(instrumentos) + len(herramientas)}")


def main():
    for lang, cfg in LANGS.items():
        generate(lang, cfg)


if __name__ == "__main__":
    main()
