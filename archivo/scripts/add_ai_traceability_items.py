#!/usr/bin/env python3
"""
Adds AI-context evaluation items to all language versions:
  - DIM_TRAZ_IA  -> dimensiones.json
  - INS_BIT_IA   -> instrumentos.json
  - HER_DECL_IA  -> herramientas.json

The script is idempotent and updates selected back-references.
"""

import copy
import json
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "data")

DIM_CODE = "DIM_TRAZ_IA"
INS_CODE = "INS_BIT_IA"
HER_CODE = "HER_DECL_IA"

TRACEABLE_INS = {
    "INS_DIARIO": "principal",
    "INS_PORT": "principal",
    "INS_INFO_INV": "principal",
    "INS_MONO": "principal",
    "INS_ENSAYO": "principal",
    "INS_ART_DIV": "principal",
    "INS_MEM_PROY": "principal",
    "INS_PLAN_TRAB": "principal",
    "INS_DOC_COL": "principal",
    "INS_PORT_DIG": "principal",
    "INS_BIT": "principal",
    "INS_CUAD_DIG": "principal",
    "INS_EPORT_SEL": "principal",
    "INS_PRESENT_DIG": "principal",
    "INS_WEB": "principal",
    "INS_BLOG": "principal",
    "INS_VIDEO": "principal",
    "INS_TUTORIAL": "principal",
    "INS_MICROVIDEO": "principal",
    "INS_COM_TEXT": "complementaria",
    "INS_COM_GRAF": "complementaria",
    "INS_RESEÑA": "complementaria",
    "INS_PROB": "complementaria",
    "INS_CASO": "complementaria",
    "INS_PR_COMP": "complementaria",
    "INS_INFOG": "complementaria",
    "INS_POSTER": "complementaria",
    "INS_PODCAST": "complementaria",
    "INS_MODELO_DIG": "complementaria",
    "INS_FORO": "complementaria",
    "INS_BORR": "complementaria",
    "INS_ENT_PAR": "complementaria",
    "INS_REV_PARES": "complementaria",
    "INS_CUAD_CAMPO": "complementaria",
    "INS_RESUMEN": "ocasional",
    "INS_ESQUEMA": "ocasional",
    "INS_MAP_CONC": "ocasional",
    "INS_MAP_MENT": "ocasional",
    "INS_LINEA": "ocasional",
    "INS_GLOS": "ocasional",
    "INS_FICHA_LECT": "ocasional",
    "INS_ACTA": "ocasional",
    "INS_F_REFLEX": "ocasional",
    "INS_AUTOINF": "ocasional",
    "INS_TAREA_COMP_INT": "ocasional",
    "INS_SIT_PROB": "ocasional",
}

DIM_TOOLS = {
    HER_CODE: "principal",
    "HER_HIST_REV": "principal",
    "HER_MAP_EVID": "principal",
    "HER_BANCO_EVID": "complementaria",
    "HER_RUB_PROC": "complementaria",
    "HER_FICHA_RETRO": "complementaria",
    "HER_ANALITICAS": "ocasional",
}

BIT_TOOLS = {
    HER_CODE: "principal",
    "HER_HIST_REV": "principal",
    "HER_MAP_EVID": "complementaria",
    "HER_RUB_PROC": "complementaria",
    "HER_FICHA_RETRO": "complementaria",
    "HER_BANCO_EVID": "ocasional",
}

BIT_TECHNIQUES = {
    "TEC_PROC_REFLEX": "principal",
    "TEC_ANAL_DOC": "principal",
    "TEC_INTER_DIG": "complementaria",
    "TEC_TRIANG": "ocasional",
}

BIT_DIMS = {
    DIM_CODE: "principal",
    "DIM_DIG": "principal",
    "DIM_FORM": "complementaria",
    "DIM_FEED": "complementaria",
    "DIM_COMP": "ocasional",
}

DECL_TECHNIQUES = {
    "TEC_PROC_REFLEX": "principal",
    "TEC_ANAL_DOC": "principal",
    "TEC_TRIANG": "complementaria",
}

DECL_DIMS = {
    DIM_CODE: "principal",
    "DIM_DIG": "complementaria",
    "DIM_CRIT": "complementaria",
    "DIM_FEED": "ocasional",
}

SHARED_DIM = {
    "Código": DIM_CODE,
    "Categoría": "Soporte de evidencias",
    "Fase": "Proceso/Final",
    "Participación": "Docente/Alumno",
    "rel_ins": list(TRACEABLE_INS.keys()) + [INS_CODE],
    "rel_her": list(DIM_TOOLS.keys()),
    "rel_meta": {
        "rel_ins": {**TRACEABLE_INS, INS_CODE: "principal"},
        "rel_her": DIM_TOOLS,
    },
    "tipo_entidad": "dimension",
    "Modalidad": "Presencial / Online",
    "Lugar": "Aula / Virtual / Domicilio",
    "Agrupamiento": "Individual / Grupo pequeño",
    "Resistencia IA": "Alta",
}

SHARED_INS = {
    "Código": INS_CODE,
    "Tipo": "Digital/proceso",
    "Complejidad": "Media",
    "Fase": "Proceso/Final",
    "Participación": "Docente/Alumno",
    "rel_tec": list(BIT_TECHNIQUES.keys()),
    "rel_dim": list(BIT_DIMS.keys()),
    "rel_her": list(BIT_TOOLS.keys()),
    "rel_meta": {
        "rel_tec": BIT_TECHNIQUES,
        "rel_dim": BIT_DIMS,
        "rel_her": BIT_TOOLS,
    },
    "tipo_entidad": "medio_evidencia",
    "Modalidad": "Presencial / Online",
    "Lugar": "Aula / Virtual / Domicilio",
    "Agrupamiento": "Individual",
    "Resistencia IA": "Alta",
}

SHARED_HER = {
    "Código": HER_CODE,
    "Tipo": "Trazabilidad/autoría",
    "Complejidad": "Baja/Media",
    "Fase": "Proceso/Final",
    "Participación": "Alumno/Docente",
    "rel_ins": list(TRACEABLE_INS.keys()) + [INS_CODE],
    "rel_dim": list(DECL_DIMS.keys()),
    "rel_tec": list(DECL_TECHNIQUES.keys()),
    "rel_meta": {
        "rel_ins": {**TRACEABLE_INS, INS_CODE: "principal"},
        "rel_dim": DECL_DIMS,
        "rel_tec": DECL_TECHNIQUES,
    },
    "tipo_entidad": "instrumento_evaluacion",
    "Modalidad": "Presencial / Online",
    "Lugar": "Aula / Virtual",
    "Agrupamiento": "Individual / Grupo pequeño",
    "Resistencia IA": "Alta",
}

LANG_DATA = {
    "es": {
        DIM_CODE: {
            "Dimensión": "Trazabilidad, autoría y uso de IA",
            "Descripción breve": "Documentación del proceso, las fuentes, las ayudas externas y el uso de IA en una evidencia.",
            "Función pedagógica": "Hacer visible cómo se ha elaborado una producción y distinguir el aprendizaje demostrado de las ayudas utilizadas.",
            "Evidencias habituales": "Versiones, prompts, fuentes, historial de revisión, decisiones justificadas, declaración de uso de IA.",
            "Cuándo conviene": "Cuando una tarea permite ayuda externa, edición digital, trabajo fuera del aula o uso de IA generativa.",
            "Precauciones": "No debe convertirse en burocracia; la trazabilidad debe aportar evidencias reales sobre decisiones, revisión y autoría.",
            "Etiquetas": "ia; autoria; trazabilidad; fuentes; proceso",
            "Descripción detallada": (
                "Esta dimensión sitúa la evaluación en contextos donde el proceso de elaboración puede quedar oculto o apoyarse en herramientas externas, incluida la IA generativa.\n\n"
                "Cómo aplicarla: el alumnado documenta qué fuentes, ayudas, herramientas o sistemas de IA ha usado, para qué los ha usado y qué decisiones propias ha tomado. Puede conservar versiones, prompts relevantes, cambios realizados, comprobaciones de fuentes y justificaciones breves. El docente valora la calidad del proceso, la revisión crítica y la correspondencia entre la producción final y el aprendizaje demostrado.\n\n"
                "Es especialmente útil en trabajos de investigación, proyectos, documentos colaborativos, portfolios, productos digitales y tareas realizadas parcialmente fuera del aula. No pretende penalizar el uso de IA, sino hacerlo transparente y evaluable."
            ),
            "Medios/evidencias asociados": "Bitácora de proceso con IA; Diario de aprendizaje; Porfolio; Informe de investigación; Monografía; Ensayo; Memoria de proyecto; Documento colaborativo; Portfolio digital; Presentación digital; Página web; Entrada de blog; Vídeo; Microvídeo educativo",
            "Instrumentos de evaluación recomendados": "Declaración de uso de IA y fuentes; Historial de revisión; Mapa de evidencias por criterio; Banco digital de evidencias; Rúbrica de proceso; Ficha de retroalimentación",
        },
        INS_CODE: {
            "Instrumento": "Bitácora de proceso con IA",
            "Descripción breve": "Registro del proceso de trabajo, uso de IA, fuentes, versiones y decisiones tomadas.",
            "Técnicas asociadas": "Análisis de procesos y reflexiones; Análisis documental; Análisis de interacciones digitales; Triangulación de evidencias",
            "Evidencia": "Registro de proceso",
            "Adecuado para": "Proyectos; investigaciones; producciones digitales; tareas con ayuda de IA; trabajo fuera del aula.",
            "Etiquetas": "ia; prompts; proceso; autoria; fuentes; versiones",
            "Descripción detallada": (
                "La bitácora de proceso con IA es una evidencia en la que el alumno documenta cómo ha elaborado una tarea cuando ha podido usar herramientas digitales, fuentes externas o IA generativa. Recoge el recorrido de trabajo, no solo el producto final.\n\n"
                "Cómo usarla para evaluar: se pide al alumnado que registre los pasos relevantes, fuentes consultadas, prompts o instrucciones usadas, respuestas aprovechadas o descartadas, cambios entre versiones, comprobaciones realizadas y decisiones propias. No es necesario guardar todo, sino las evidencias suficientes para explicar el proceso.\n\n"
                "Permite valorar autoría, pensamiento crítico, revisión, mejora y uso responsable de la IA. Conviene vincularla a criterios concretos para que no se reduzca a una declaración formal sin valor evaluativo."
            ),
            "Dimensiones asociadas": "Trazabilidad, autoría y uso de IA; Evidencias digitales; Finalidad formativa; Retroalimentación y feedforward; Enfoque competencial",
            "Instrumentos de evaluación recomendados": "Declaración de uso de IA y fuentes; Historial de revisión; Mapa de evidencias por criterio; Rúbrica de proceso; Ficha de retroalimentación; Banco digital de evidencias",
        },
        HER_CODE: {
            "Herramienta": "Declaración de uso de IA y fuentes",
            "Descripción breve": "Plantilla para declarar ayudas, fuentes, herramientas de IA y decisiones propias en una tarea.",
            "Sirve para": "Documentar autoría, uso de IA, verificación de fuentes y responsabilidad sobre la producción final.",
            "Adecuada para": "Producciones escritas, proyectos, portfolios, productos digitales y tareas realizadas fuera del aula.",
            "Ventajas": "Hace transparente el proceso y facilita conversaciones de retroalimentación sobre autoría y calidad del trabajo.",
            "Limitaciones": "Depende de la honestidad del alumnado y debe combinarse con revisión del proceso o defensa oral cuando sea necesario.",
            "Etiquetas": "ia; autoria; fuentes; declaracion; trazabilidad",
            "Descripción detallada": (
                "La declaración de uso de IA y fuentes es una plantilla breve que acompaña a una tarea para explicar qué apoyos externos se han utilizado y qué parte del trabajo corresponde a decisiones propias del alumno.\n\n"
                "Cómo usarla: puede incluir apartados sobre fuentes consultadas, herramientas de IA empleadas, finalidad de cada ayuda, fragmentos revisados, errores detectados, cambios realizados y responsabilidad final sobre el contenido. Es más útil si se pide junto con borradores, historial de revisión o una breve defensa del trabajo.\n\n"
                "No sustituye a una rúbrica ni demuestra por sí sola el aprendizaje, pero ayuda a convertir el uso de IA en una práctica transparente, revisable y educativamente aprovechable."
            ),
            "Dimensiones asociadas": "Trazabilidad, autoría y uso de IA; Evidencias digitales; Evaluación criterial; Retroalimentación y feedforward",
            "Medios/evidencias compatibles": "Bitácora de proceso con IA; Informe de investigación; Monografía; Ensayo; Artículo divulgativo; Memoria de proyecto; Documento colaborativo; Portfolio digital; Presentación digital; Página web; Entrada de blog; Vídeo; Microvídeo educativo",
            "Medios/evidencias asociados": "Bitácora de proceso con IA; Informe de investigación; Monografía; Ensayo; Artículo divulgativo; Memoria de proyecto; Documento colaborativo; Portfolio digital; Presentación digital; Página web; Entrada de blog; Vídeo; Microvídeo educativo",
            "Técnicas asociadas": "Análisis de procesos y reflexiones; Análisis documental; Triangulación de evidencias",
        },
    },
    "ca": {
        DIM_CODE: {
            "Dimensión": "Traçabilitat, autoria i ús d'IA",
            "Descripción breve": "Documentació del procés, les fonts, les ajudes externes i l'ús d'IA en una evidència.",
            "Función pedagógica": "Fer visible com s'ha elaborat una producció i distingir l'aprenentatge demostrat de les ajudes utilitzades.",
            "Evidencias habituales": "Versions, prompts, fonts, historial de revisió, decisions justificades, declaració d'ús d'IA.",
            "Cuándo conviene": "Quan una tasca permet ajuda externa, edició digital, treball fora de l'aula o ús d'IA generativa.",
            "Precauciones": "No s'ha de convertir en burocràcia; la traçabilitat ha d'aportar evidències reals sobre decisions, revisió i autoria.",
            "Etiquetas": "ia; autoria; tracabilitat; fonts; proces",
            "Descripción detallada": (
                "Aquesta dimensió situa l'avaluació en contextos on el procés d'elaboració pot quedar ocult o rebre suport d'eines externes, inclosa la IA generativa.\n\n"
                "Com aplicar-la: l'alumnat documenta quines fonts, ajudes, eines o sistemes d'IA ha utilitzat, per a què els ha utilitzat i quines decisions pròpies ha pres. Pot conservar versions, prompts rellevants, canvis realitzats, comprovacions de fonts i justificacions breus. El docent valora la qualitat del procés, la revisió crítica i la correspondència entre la producció final i l'aprenentatge demostrat.\n\n"
                "És especialment útil en treballs de recerca, projectes, documents col·laboratius, portfolios, productes digitals i tasques realitzades parcialment fora de l'aula. No pretén penalitzar l'ús d'IA, sinó fer-lo transparent i avaluable."
            ),
            "Medios/evidencias asociados": "Bitàcola de procés amb IA; Diari d'aprenentatge; Portafolis; Informe de recerca; Monografia; Assaig; Memòria de projecte; Document col·laboratiu; Portfolio digital; Presentació digital; Pàgina web; Entrada de blog; Vídeo; Microvídeo educatiu",
            "Instrumentos de evaluación recomendados": "Declaració d'ús d'IA i fonts; Historial de revisió; Mapa d'evidències per criteri; Banc digital d'evidències; Rúbrica de procés; Fitxa de retroalimentació",
        },
        INS_CODE: {
            "Instrumento": "Bitàcola de procés amb IA",
            "Descripción breve": "Registre del procés de treball, ús d'IA, fonts, versions i decisions preses.",
            "Técnicas asociadas": "Anàlisi de processos i reflexions; Anàlisi documental; Anàlisi d'interaccions digitals; Triangulació d'evidències",
            "Evidencia": "Registre de procés",
            "Adecuado para": "Projectes; recerques; produccions digitals; tasques amb ajuda d'IA; treball fora de l'aula.",
            "Etiquetas": "ia; prompts; proces; autoria; fonts; versions",
            "Descripción detallada": (
                "La bitàcola de procés amb IA és una evidència en què l'alumne documenta com ha elaborat una tasca quan ha pogut usar eines digitals, fonts externes o IA generativa. Recull el recorregut de treball, no només el producte final.\n\n"
                "Com usar-la per avaluar: es demana a l'alumnat que registri els passos rellevants, fonts consultades, prompts o instruccions usades, respostes aprofitades o descartades, canvis entre versions, comprovacions realitzades i decisions pròpies. No cal guardar-ho tot, sinó les evidències suficients per explicar el procés.\n\n"
                "Permet valorar autoria, pensament crític, revisió, millora i ús responsable de la IA. Convé vincular-la a criteris concrets perquè no es redueixi a una declaració formal sense valor avaluatiu."
            ),
            "Dimensiones asociadas": "Traçabilitat, autoria i ús d'IA; Evidències digitals; Finalitat formativa; Retroalimentació i feedforward; Enfocament competencial",
            "Instrumentos de evaluación recomendados": "Declaració d'ús d'IA i fonts; Historial de revisió; Mapa d'evidències per criteri; Rúbrica de procés; Fitxa de retroalimentació; Banc digital d'evidències",
        },
        HER_CODE: {
            "Herramienta": "Declaració d'ús d'IA i fonts",
            "Descripción breve": "Plantilla per declarar ajudes, fonts, eines d'IA i decisions pròpies en una tasca.",
            "Sirve para": "Documentar autoria, ús d'IA, verificació de fonts i responsabilitat sobre la producció final.",
            "Adecuada para": "Produccions escrites, projectes, portfolios, productes digitals i tasques realitzades fora de l'aula.",
            "Ventajas": "Fa transparent el procés i facilita converses de retroalimentació sobre autoria i qualitat del treball.",
            "Limitaciones": "Depèn de l'honestedat de l'alumnat i s'ha de combinar amb revisió del procés o defensa oral quan calgui.",
            "Etiquetas": "ia; autoria; fonts; declaracio; tracabilitat",
            "Descripción detallada": (
                "La declaració d'ús d'IA i fonts és una plantilla breu que acompanya una tasca per explicar quins suports externs s'han utilitzat i quina part del treball correspon a decisions pròpies de l'alumne.\n\n"
                "Com usar-la: pot incloure apartats sobre fonts consultades, eines d'IA emprades, finalitat de cada ajuda, fragments revisats, errors detectats, canvis realitzats i responsabilitat final sobre el contingut. És més útil si es demana juntament amb esborranys, historial de revisió o una breu defensa del treball.\n\n"
                "No substitueix una rúbrica ni demostra per si sola l'aprenentatge, però ajuda a convertir l'ús d'IA en una pràctica transparent, revisable i educativament aprofitable."
            ),
            "Dimensiones asociadas": "Traçabilitat, autoria i ús d'IA; Evidències digitals; Avaluació criterial; Retroalimentació i feedforward",
            "Medios/evidencias compatibles": "Bitàcola de procés amb IA; Informe de recerca; Monografia; Assaig; Article divulgatiu; Memòria de projecte; Document col·laboratiu; Portfolio digital; Presentació digital; Pàgina web; Entrada de blog; Vídeo; Microvídeo educatiu",
            "Medios/evidencias asociados": "Bitàcola de procés amb IA; Informe de recerca; Monografia; Assaig; Article divulgatiu; Memòria de projecte; Document col·laboratiu; Portfolio digital; Presentació digital; Pàgina web; Entrada de blog; Vídeo; Microvídeo educatiu",
            "Técnicas asociadas": "Anàlisi de processos i reflexions; Anàlisi documental; Triangulació d'evidències",
        },
    },
    "en": {
        DIM_CODE: {
            "Dimensión": "Traceability, authorship and AI use",
            "Descripción breve": "Documentation of the process, sources, external support and AI use behind a piece of evidence.",
            "Función pedagógica": "Make the production process visible and distinguish demonstrated learning from the support used.",
            "Evidencias habituales": "Versions, prompts, sources, revision history, justified decisions, AI-use declaration.",
            "Cuándo conviene": "When a task allows external help, digital editing, work outside the classroom or generative AI use.",
            "Precauciones": "It should not become bureaucracy; traceability must provide real evidence about decisions, review and authorship.",
            "Etiquetas": "ai; authorship; traceability; sources; process",
            "Descripción detallada": (
                "This dimension places assessment in contexts where the production process may be hidden or supported by external tools, including generative AI.\n\n"
                "How to apply it: students document which sources, supports, tools or AI systems they used, what they used them for and which decisions were their own. They may keep versions, relevant prompts, changes made, source checks and brief justifications. The teacher assesses the quality of the process, critical review and the match between the final product and the learning demonstrated.\n\n"
                "It is especially useful in research tasks, projects, collaborative documents, portfolios, digital products and tasks completed partly outside the classroom. Its purpose is not to penalise AI use, but to make it transparent and assessable."
            ),
            "Medios/evidencias asociados": "AI process log; Learning journal; Portfolio; Research report; Monograph; Essay; Project report; Collaborative document; Digital portfolio; Digital presentation; Web page; Blog post; Video; Educational microvideo",
            "Instrumentos de evaluación recomendados": "AI and sources use declaration; Revision history; Evidence map by criterion; Digital evidence bank; Process rubric; Feedback/feedforward template",
        },
        INS_CODE: {
            "Instrumento": "AI process log",
            "Descripción breve": "Record of the work process, AI use, sources, versions and decisions made.",
            "Técnicas asociadas": "Analysis of processes and reflections; Document analysis; Analysis of digital interactions; Triangulation of evidence",
            "Evidencia": "Process record",
            "Adecuado para": "Projects; research tasks; digital productions; AI-supported tasks; work outside the classroom.",
            "Etiquetas": "ai; prompts; process; authorship; sources; versions",
            "Descripción detallada": (
                "The AI process log is evidence in which the student documents how they produced a task when digital tools, external sources or generative AI could be used. It records the work journey, not only the final product.\n\n"
                "How to use it for assessment: students record relevant steps, sources consulted, prompts or instructions used, responses used or discarded, changes between versions, checks carried out and their own decisions. They do not need to keep everything, only enough evidence to explain the process.\n\n"
                "It supports assessment of authorship, critical thinking, revision, improvement and responsible AI use. It should be linked to specific criteria so that it does not become a formal declaration with no assessment value."
            ),
            "Dimensiones asociadas": "Traceability, authorship and AI use; Digital evidence; Formative purpose; Feedback and feedforward; Competency-based approach",
            "Instrumentos de evaluación recomendados": "AI and sources use declaration; Revision history; Evidence map by criterion; Process rubric; Feedback/feedforward template; Digital evidence bank",
        },
        HER_CODE: {
            "Herramienta": "AI and sources use declaration",
            "Descripción breve": "Template for declaring support, sources, AI tools and personal decisions in a task.",
            "Sirve para": "Document authorship, AI use, source checking and responsibility for the final production.",
            "Adecuada para": "Written productions, projects, portfolios, digital products and tasks completed outside the classroom.",
            "Ventajas": "Makes the process transparent and supports feedback conversations about authorship and work quality.",
            "Limitaciones": "It depends on student honesty and should be combined with process review or oral defence when needed.",
            "Etiquetas": "ai; authorship; sources; declaration; traceability",
            "Descripción detallada": (
                "The AI and sources use declaration is a short template that accompanies a task to explain which external supports were used and which part of the work reflects the student's own decisions.\n\n"
                "How to use it: it can include sections on sources consulted, AI tools used, the purpose of each support, revised fragments, errors found, changes made and final responsibility for the content. It is more useful when requested together with drafts, revision history or a short defence of the work.\n\n"
                "It does not replace a rubric or prove learning by itself, but it helps turn AI use into a transparent, reviewable and educationally useful practice."
            ),
            "Dimensiones asociadas": "Traceability, authorship and AI use; Digital evidence; Criterion-referenced assessment; Feedback and feedforward",
            "Medios/evidencias compatibles": "AI process log; Research report; Monograph; Essay; Popular science article; Project report; Collaborative document; Digital portfolio; Digital presentation; Web page; Blog post; Video; Educational microvideo",
            "Medios/evidencias asociados": "AI process log; Research report; Monograph; Essay; Popular science article; Project report; Collaborative document; Digital portfolio; Digital presentation; Web page; Blog post; Video; Educational microvideo",
            "Técnicas asociadas": "Analysis of processes and reflections; Document analysis; Triangulation of evidence",
        },
    },
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {path}")


def build_item(shared, text):
    item = copy.deepcopy(shared)
    item.update(text)
    return item


def upsert(items, code, item):
    for idx, existing in enumerate(items):
        if existing.get("Código") == code:
            items[idx] = item
            print(f"  ↻ Updated {code}")
            return
    items.append(item)
    print(f"  + Added {code}")


def add_relation(item, rel_field, target_code, kind):
    rels = item.setdefault(rel_field, [])
    if target_code not in rels:
        rels.append(target_code)
    item.setdefault("rel_meta", {}).setdefault(rel_field, {})[target_code] = kind


def update_item_relations(items, rels_by_code, rel_field, target_code):
    for item in items:
        code = item.get("Código")
        if code in rels_by_code:
            add_relation(item, rel_field, target_code, rels_by_code[code])


def process_language(lang):
    print(f"\n── {lang.upper()} ──")
    lang_dir = os.path.join(BASE, lang)
    texts = LANG_DATA[lang]

    ins_path = os.path.join(lang_dir, "instrumentos.json")
    ins = load(ins_path)
    update_item_relations(ins, TRACEABLE_INS, "rel_dim", DIM_CODE)
    update_item_relations(ins, TRACEABLE_INS, "rel_her", HER_CODE)
    upsert(ins, INS_CODE, build_item(SHARED_INS, texts[INS_CODE]))
    save(ins_path, ins)

    her_path = os.path.join(lang_dir, "herramientas.json")
    her = load(her_path)
    for tool_code, kind in DIM_TOOLS.items():
        for item in her:
            if item.get("Código") == tool_code and tool_code != HER_CODE:
                add_relation(item, "rel_dim", DIM_CODE, kind)
                add_relation(item, "rel_ins", INS_CODE, BIT_TOOLS.get(tool_code, "complementaria"))
    upsert(her, HER_CODE, build_item(SHARED_HER, texts[HER_CODE]))
    save(her_path, her)

    tec_path = os.path.join(lang_dir, "tecnicas.json")
    tec = load(tec_path)
    for item in tec:
        code = item.get("Código")
        if code in BIT_TECHNIQUES:
            add_relation(item, "rel_ins", INS_CODE, BIT_TECHNIQUES[code])
        if code in DECL_TECHNIQUES:
            add_relation(item, "rel_her", HER_CODE, DECL_TECHNIQUES[code])
    save(tec_path, tec)

    dim_path = os.path.join(lang_dir, "dimensiones.json")
    dim = load(dim_path)
    for item in dim:
        code = item.get("Código")
        if code in BIT_DIMS and code != DIM_CODE:
            add_relation(item, "rel_ins", INS_CODE, BIT_DIMS[code])
        if code in DECL_DIMS and code != DIM_CODE:
            add_relation(item, "rel_her", HER_CODE, DECL_DIMS[code])
    upsert(dim, DIM_CODE, build_item(SHARED_DIM, texts[DIM_CODE]))
    save(dim_path, dim)


if __name__ == "__main__":
    for language in ["es", "ca", "en"]:
        process_language(language)
    print("\nDone.")
