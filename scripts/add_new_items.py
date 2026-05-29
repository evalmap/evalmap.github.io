#!/usr/bin/env python3
"""
Adds three new evaluation items to all language versions (es, ca, en):
  - INS_CUAD_CAMPO  → instrumentos.json
  - INS_MICROVIDEO  → instrumentos.json
  - DIM_GAMIF       → dimensiones.json
Also updates back-references in existing items.
"""

import json
import os
import copy

BASE = os.path.join(os.path.dirname(__file__), "..", "data")

# ─────────────────────────────────────────────────────────────────────────────
# ITEM DEFINITIONS  (shared structure; text fields set per language below)
# ─────────────────────────────────────────────────────────────────────────────

SHARED_INS_CUAD_CAMPO = {
    "Código": "INS_CUAD_CAMPO",
    "Complejidad": "Media",
    "Fase": "Proceso",
    "Participación": "Docente/Alumno",
    "rel_tec": ["TEC_OBS_SIS", "TEC_PROD", "TEC_PROC_REFLEX"],
    "rel_her": ["HER_GUIA_CORR", "HER_LISTA", "HER_NOTAS_CAMPO", "HER_RUB_ANA"],
    "rel_dim": ["DIM_INDAG", "DIM_COMP", "DIM_FORM"],
    "rel_meta": {
        "rel_tec": {
            "TEC_OBS_SIS": "principal",
            "TEC_PROD": "complementaria",
            "TEC_PROC_REFLEX": "ocasional"
        },
        "rel_her": {
            "HER_GUIA_CORR": "principal",
            "HER_LISTA": "complementaria",
            "HER_NOTAS_CAMPO": "complementaria",
            "HER_RUB_ANA": "ocasional"
        },
        "rel_dim": {
            "DIM_INDAG": "principal",
            "DIM_COMP": "complementaria",
            "DIM_FORM": "complementaria"
        }
    },
    "tipo_entidad": "medio_evidencia",
    "Modalidad": "Presencial",
    "Resistencia IA": "Alta"
}

SHARED_INS_MICROVIDEO = {
    "Código": "INS_MICROVIDEO",
    "Complejidad": "Media",
    "Fase": "Final",
    "Participación": "Docente/Iguales",
    "rel_tec": ["TEC_PROD", "TEC_ORAL"],
    "rel_her": ["HER_RUB_ANA", "HER_RUB_PROD", "HER_LISTA", "HER_FICHA_COEV"],
    "rel_dim": ["DIM_DIG", "DIM_COMP", "DIM_DESEMP"],
    "rel_meta": {
        "rel_tec": {
            "TEC_PROD": "principal",
            "TEC_ORAL": "complementaria"
        },
        "rel_her": {
            "HER_RUB_ANA": "principal",
            "HER_RUB_PROD": "complementaria",
            "HER_LISTA": "complementaria",
            "HER_FICHA_COEV": "ocasional"
        },
        "rel_dim": {
            "DIM_DIG": "principal",
            "DIM_COMP": "complementaria",
            "DIM_DESEMP": "complementaria"
        }
    },
    "tipo_entidad": "medio_evidencia",
    "Modalidad": "Presencial / Online",
    "Resistencia IA": "Alta"
}

SHARED_DIM_GAMIF = {
    "Código": "DIM_GAMIF",
    "Categoría": "Contexto metodológico",
    "Fase": "Proceso/Final",
    "Participación": "Docente/Alumno/Iguales",
    "rel_ins": [
        "INS_ESCAPE",
        "INS_PROB",
        "INS_SIT_PROB",
        "INS_TAREA_COMP_INT",
        "INS_CUEST_DIG"
    ],
    "rel_her": [
        "HER_ESC_OBS",
        "HER_LISTA",
        "HER_RUB_COMP",
        "HER_ANALITICAS"
    ],
    "rel_meta": {
        "rel_ins": {
            "INS_ESCAPE": "principal",
            "INS_PROB": "complementaria",
            "INS_SIT_PROB": "complementaria",
            "INS_TAREA_COMP_INT": "complementaria",
            "INS_CUEST_DIG": "complementaria"
        },
        "rel_her": {
            "HER_ESC_OBS": "complementaria",
            "HER_LISTA": "complementaria",
            "HER_RUB_COMP": "complementaria",
            "HER_ANALITICAS": "complementaria"
        }
    },
    "tipo_entidad": "dimension",
    "Modalidad": "Presencial / Online",
    "Resistencia IA": "Media"
}

# ─────────────────────────────────────────────────────────────────────────────
# LANGUAGE-SPECIFIC TEXT
# ─────────────────────────────────────────────────────────────────────────────

LANG_DATA = {
    "es": {
        "INS_CUAD_CAMPO": {
            "Instrumento": "Cuaderno de campo",
            "Tipo": "Producción escrita/observacional",
            "Descripción breve": "Registro de observaciones, datos y reflexiones durante actividades en el exterior o entorno real.",
            "Técnicas asociadas": "Observación sistemática; Análisis de producciones; Análisis de procesos y reflexiones",
            "Evidencia": "Producción escrita",
            "Adecuado para": "Observación in situ; registro de datos; conexión con el entorno natural o social.",
            "Etiquetas": "campo; exterior; observacion; naturaleza",
            "Descripción detallada": (
                "El cuaderno de campo es el registro que elabora el alumno durante actividades realizadas fuera del aula: "
                "salidas de campo, visitas, estudios del entorno o actividades en espacios naturales. A diferencia del "
                "cuaderno de clase (INS_CUADERNO), documenta observaciones en tiempo real en contextos no controlados; "
                "a diferencia del informe de laboratorio (INS_INFO_LAB), no sigue una estructura experimental cerrada, "
                "sino que recoge notas, croquis, medidas y reflexiones sobre la marcha.\n\n"
                "Cómo usarlo para evaluar: el alumno registra observaciones directas, datos medidos, dibujos o croquis, "
                "preguntas emergentes y reflexiones iniciales. El docente evalúa la precisión y completitud de las "
                "observaciones, la capacidad de registrar datos relevantes y la calidad de la reflexión sobre lo observado. "
                "Una guía de corrección con los elementos esperados orienta la evaluación de forma coherente.\n\n"
                "Es especialmente útil en ciencias naturales, geografía, educación ambiental, historia local y cualquier "
                "materia que trabaje con el entorno como fuente de aprendizaje. Su valor radica en que la evidencia se "
                "genera en el lugar de los hechos, lo que aporta autenticidad y contextualización difícilmente "
                "reproducibles en el aula."
            ),
            "Dimensiones asociadas": "Indagación; Enfoque competencial; Finalidad formativa",
            "Instrumentos de evaluación recomendados": "Guía de corrección; Lista de cotejo o control; Notas de campo; Rúbrica analítica",
            "Lugar": "Exterior / Laboratorio / Aula",
            "Agrupamiento": "Individual / Grupo pequeño",
        },
        "INS_MICROVIDEO": {
            "Instrumento": "Microvídeo educativo",
            "Tipo": "Producción audiovisual",
            "Descripción breve": "Vídeo breve (60–90 s) que explica, divulga o argumenta sobre un tema.",
            "Técnicas asociadas": "Análisis de producciones; Intercambios orales",
            "Evidencia": "Producto audiovisual",
            "Adecuado para": "Síntesis; comunicación concisa; creatividad; competencia digital.",
            "Etiquetas": "video; corto; reel; divulgacion; digital",
            "Descripción detallada": (
                "El microvídeo educativo es una producción audiovisual de corta duración (habitualmente entre 60 y 90 "
                "segundos) en la que el alumno explica un concepto, argumenta una posición, resume un tema o comunica "
                "resultados de forma sintética y directa. Se diferencia del vídeo convencional (INS_VIDEO) por la "
                "exigencia de condensar el mensaje al máximo; y del videotutorial (INS_TUTORIAL) en que no sigue "
                "necesariamente una estructura procedimental paso a paso.\n\n"
                "Cómo usarlo para evaluar: se valoran la claridad y precisión del mensaje, la adecuación al "
                "destinatario, la estructura narrativa dentro del tiempo reducido, la corrección del contenido y la "
                "calidad técnica básica (imagen, sonido). Una rúbrica analítica que diferencie contenido y producción "
                "permite retroalimentación específica. La coevaluación entre compañeros es especialmente natural en "
                "este formato.\n\n"
                "Es motivador para alumnado que aprende mejor mediante formatos visuales y orales que escritos. "
                "Desarrolla la competencia digital, la comunicación y la capacidad de síntesis."
            ),
            "Dimensiones asociadas": "Evidencias digitales; Enfoque competencial; Evidencia de desempeño",
            "Instrumentos de evaluación recomendados": "Rúbrica analítica; Rúbrica de producto; Lista de cotejo o control; Ficha de coevaluación",
            "Lugar": "Aula / Virtual / Domicilio / Exterior",
            "Agrupamiento": "Individual / Parejas",
        },
        "DIM_GAMIF": {
            "Dimensión": "Evaluación gamificada",
            "Descripción breve": "Uso de mecánicas de juego para recoger evidencias de aprendizaje.",
            "Función pedagógica": "Aumentar motivación e implicación, y obtener retroalimentación inmediata sobre el aprendizaje.",
            "Evidencias habituales": "Retos, escape rooms, rondas cronometradas, insignias, marcadores, desafíos cooperativos.",
            "Cuándo conviene": "Cuando se quiere evaluar con alta motivación, consolidar aprendizajes o hacer evaluación diagnóstica de forma activa.",
            "Precauciones": "Las mecánicas de juego no deben distorsionar la evaluación; hay que distinguir entre participación y aprendizaje demostrado.",
            "Etiquetas": "gamificacion; juego; escape room; reto; insignias",
            "Descripción detallada": (
                "Esta dimensión describe el formato o situación didáctica en la que se genera la evidencia. Puede "
                "combinar varios procedimientos de recogida.\n\n"
                "La evaluación gamificada incorpora mecánicas propias del juego (retos, puntos, insignias, "
                "contrarreloj, cooperación o competición regulada) para recoger evidencias de aprendizaje en un "
                "entorno de alta motivación. No es sinónimo de un instrumento concreto como el escape room "
                "(INS_ESCAPE), sino el enfoque metodológico que engloba cualquier estrategia que usa el juego con "
                "propósito evaluativo.\n\n"
                "Cómo aplicarla: se diseñan tareas o retos con reglas claras, criterios de logro visibles y "
                "retroalimentación inmediata. Los puntos o insignias pueden usarse como evidencia del nivel alcanzado "
                "si están alineados con criterios de evaluación reales. Las analíticas de la plataforma gamificada "
                "(tiempo, intentos, aciertos) complementan la observación docente, pero no la sustituyen.\n\n"
                "Es especialmente adecuada para la evaluación formativa, la consolidación y la evaluación "
                "diagnóstica, ya que el contexto lúdico reduce la ansiedad evaluativa y favorece la participación "
                "de alumnado con dificultades de motivación."
            ),
            "Medios/evidencias asociados": "Escape room o reto gamificado; Resolución de problemas; Situación-problema; Tarea competencial integrada; Cuestionario digital",
            "Instrumentos de evaluación recomendados": "Escala de observación; Lista de cotejo o control; Rúbrica competencial; Analíticas de aprendizaje",
            "Lugar": "Aula / Virtual",
            "Agrupamiento": "Individual / Grupo pequeño / Gran grupo",
        }
    },
    "ca": {
        "INS_CUAD_CAMPO": {
            "Instrumento": "Quadern de camp",
            "Tipo": "Producció escrita/observacional",
            "Descripción breve": "Registre d'observacions, dades i reflexions durant activitats a l'exterior o entorn real.",
            "Técnicas asociadas": "Observació sistemàtica; Anàlisi de produccions; Anàlisi de processos i reflexions",
            "Evidencia": "Producció escrita",
            "Adecuado para": "Observació in situ; registre de dades; connexió amb l'entorn natural o social.",
            "Etiquetas": "camp; exterior; observacio; natura",
            "Descripción detallada": (
                "El quadern de camp és el registre que elabora l'alumne durant activitats realitzades fora de l'aula: "
                "sortides de camp, visites, estudis de l'entorn o activitats en espais naturals. A diferència del "
                "quadern de classe (INS_CUADERNO), documenta observacions en temps real en contextos no controlats; "
                "a diferència de l'informe de laboratori (INS_INFO_LAB), no segueix una estructura experimental "
                "tancada, sinó que recull notes, croquis, mesures i reflexions sobre la marxa.\n\n"
                "Com usar-lo per avaluar: l'alumne registra observacions directes, dades mesurades, dibuixos o "
                "croquis, preguntes emergents i reflexions inicials. El docent avalua la precisió i la completesa de "
                "les observacions, la capacitat de registrar dades rellevants i la qualitat de la reflexió sobre "
                "allò observat. Una guia de correcció amb els elements esperats orienta l'avaluació de forma coherent.\n\n"
                "És especialment útil en ciències naturals, geografia, educació ambiental, història local i qualsevol "
                "matèria que treballi amb l'entorn com a font d'aprenentatge. El seu valor rau en el fet que "
                "l'evidència es genera al lloc dels fets, cosa que aporta autenticitat i contextualització "
                "difícilment reproduïbles a l'aula."
            ),
            "Dimensiones asociadas": "Indagació; Enfocament competencial; Finalitat formativa",
            "Instrumentos de evaluación recomendados": "Guia de correcció; Llista de verificació o control; Notes de camp; Rúbrica analítica",
            "Lugar": "Exterior / Laboratori / Aula",
            "Agrupamiento": "Individual / Grup petit",
        },
        "INS_MICROVIDEO": {
            "Instrumento": "Microvídeo educatiu",
            "Tipo": "Producció audiovisual",
            "Descripción breve": "Vídeo breu (60–90 s) que explica, divulga o argumenta sobre un tema.",
            "Técnicas asociadas": "Anàlisi de produccions; Intercanvis orals",
            "Evidencia": "Producte audiovisual",
            "Adecuado para": "Síntesi; comunicació concisa; creativitat; competència digital.",
            "Etiquetas": "video; curt; reel; divulgacio; digital",
            "Descripción detallada": (
                "El microvídeo educatiu és una producció audiovisual de curta durada (habitualment entre 60 i 90 "
                "segons) en la qual l'alumne explica un concepte, argumenta una posició, resumeix un tema o comunica "
                "resultats de forma sintètica i directa. Es diferencia del vídeo convencional (INS_VIDEO) per "
                "l'exigència de condensar el missatge al màxim; i del videotutorial (INS_TUTORIAL) en el fet que no "
                "segueix necessàriament una estructura procedimental pas a pas.\n\n"
                "Com usar-lo per avaluar: es valoren la claredat i precisió del missatge, l'adequació al destinatari, "
                "l'estructura narrativa dins del temps reduït, la correcció del contingut i la qualitat tècnica "
                "bàsica (imatge, so). Una rúbrica analítica que diferenciï contingut i producció permet una "
                "retroalimentació específica. La coavaluació entre companys és especialment natural en aquest format.\n\n"
                "És motivador per a l'alumnat que aprèn millor mitjançant formats visuals i orals que escrits. "
                "Desenvolupa la competència digital, la comunicació i la capacitat de síntesi."
            ),
            "Dimensiones asociadas": "Evidències digitals; Enfocament competencial; Evidència de desempenys",
            "Instrumentos de evaluación recomendados": "Rúbrica analítica; Rúbrica de producte; Llista de verificació o control; Fitxa de coavaluació",
            "Lugar": "Aula / Virtual / Domicili / Exterior",
            "Agrupamiento": "Individual / Parelles",
        },
        "DIM_GAMIF": {
            "Dimensión": "Avaluació gamificada",
            "Descripción breve": "Ús de mecàniques de joc per recollir evidències d'aprenentatge.",
            "Función pedagógica": "Augmentar la motivació i la implicació, i obtenir retroalimentació immediata sobre l'aprenentatge.",
            "Evidencias habituales": "Reptes, escape rooms, rondes cronometrades, insígnies, marcadors, desafiaments cooperatius.",
            "Cuándo conviene": "Quan es vol avaluar amb alta motivació, consolidar aprenentatges o fer avaluació diagnòstica de forma activa.",
            "Precauciones": "Les mecàniques de joc no han de distorsionar l'avaluació; cal distingir entre participació i aprenentatge demostrat.",
            "Etiquetas": "gamificacio; joc; escape room; repte; insignies",
            "Descripción detallada": (
                "Aquesta dimensió descriu el format o situació didàctica en la qual es genera l'evidència. Pot "
                "combinar diversos procediments de recollida.\n\n"
                "L'avaluació gamificada incorpora mecàniques pròpies del joc (reptes, punts, insígnies, contrarellotge, "
                "cooperació o competició regulada) per recollir evidències d'aprenentatge en un entorn d'alta "
                "motivació. No és sinònim d'un instrument concret com l'escape room (INS_ESCAPE), sinó l'enfocament "
                "metodològic que engloba qualsevol estratègia que utilitza el joc amb propòsit avaluatiu.\n\n"
                "Com aplicar-la: es dissenyen tasques o reptes amb regles clares, criteris d'assoliment visibles i "
                "retroalimentació immediata. Els punts o insígnies es poden usar com a evidència del nivell assolit "
                "si estan alineats amb criteris d'avaluació reals. Les analítiques de la plataforma gamificada "
                "(temps, intents, encerts) complementen l'observació docent, però no la substitueixen.\n\n"
                "És especialment adequada per a l'avaluació formativa, la consolidació i l'avaluació diagnòstica, "
                "ja que el context lúdic redueix l'ansietat avaluativa i afavoreix la participació de l'alumnat "
                "amb dificultats de motivació."
            ),
            "Medios/evidencias asociados": "Escape room o repte gamificat; Resolució de problemes; Situació-problema; Tasca competencial integrada; Qüestionari digital",
            "Instrumentos de evaluación recomendados": "Escala d'observació; Llista de verificació o control; Rúbrica competencial; Analítiques d'aprenentatge",
            "Lugar": "Aula / Virtual",
            "Agrupamiento": "Individual / Grup petit / Grup gran",
        }
    },
    "en": {
        "INS_CUAD_CAMPO": {
            "Instrumento": "Field notebook",
            "Tipo": "Written/observational production",
            "Descripción breve": "Record of observations, data and reflections during outdoor or real-world activities.",
            "Técnicas asociadas": "Systematic observation; Analysis of productions; Analysis of processes and reflections",
            "Evidencia": "Written production",
            "Adecuado para": "In situ observation; data recording; connection with the natural or social environment.",
            "Etiquetas": "field notebook; outdoor; observation; nature",
            "Descripción detallada": (
                "The field notebook is the record produced by the student during activities carried out outside the "
                "classroom: field trips, visits, environmental studies or activities in natural spaces. Unlike the "
                "classroom notebook (INS_CUADERNO), it documents real-time observations in uncontrolled contexts; "
                "unlike the laboratory report (INS_INFO_LAB), it does not follow a closed experimental structure, "
                "but collects notes, sketches, measurements and on-the-spot reflections.\n\n"
                "How to use it for assessment: the student records direct observations, measured data, drawings or "
                "sketches, emerging questions and initial reflections. The teacher assesses the accuracy and "
                "completeness of observations, the ability to record relevant data, and the quality of reflection "
                "on what was observed. A correction guide listing the expected elements supports consistent assessment.\n\n"
                "It is especially useful in natural sciences, geography, environmental education, local history and "
                "any subject that uses the environment as a source of learning. Its value lies in the fact that "
                "evidence is generated on the spot, providing authenticity and contextualisation that are hard to "
                "replicate in the classroom."
            ),
            "Dimensiones asociadas": "Inquiry; Competency-based approach; Formative purpose",
            "Instrumentos de evaluación recomendados": "Correction guide; Checklist; Field notes; Analytical rubric",
            "Lugar": "Outdoors / Laboratory / Classroom",
            "Agrupamiento": "Individual / Small group",
        },
        "INS_MICROVIDEO": {
            "Instrumento": "Educational micro-video",
            "Tipo": "Audiovisual production",
            "Descripción breve": "Short video (60–90 s) that explains, communicates or argues about a topic.",
            "Técnicas asociadas": "Analysis of productions; Oral exchanges",
            "Evidencia": "Audiovisual product",
            "Adecuado para": "Synthesis; concise communication; creativity; digital competence.",
            "Etiquetas": "micro-video; short; reel; educational; digital",
            "Descripción detallada": (
                "An educational micro-video is a short audiovisual production (usually between 60 and 90 seconds) "
                "in which the student explains a concept, argues a position, summarises a topic or communicates "
                "results in a concise and direct way. It differs from a conventional video (INS_VIDEO) in that it "
                "requires maximum condensation of the message; and from a video tutorial (INS_TUTORIAL) in that it "
                "does not necessarily follow a step-by-step procedural structure.\n\n"
                "How to use it for assessment: clarity and accuracy of the message, suitability for the intended "
                "audience, narrative structure within the limited duration, correctness of content and basic "
                "technical quality (image, sound) are all assessed. An analytical rubric that distinguishes between "
                "content and production allows specific feedback. Peer assessment is particularly natural for "
                "this format.\n\n"
                "It is motivating for students who learn better through visual and oral formats than through "
                "writing. It develops digital competence, communication skills and the ability to synthesise."
            ),
            "Dimensiones asociadas": "Digital evidence; Competency-based approach; Performance evidence",
            "Instrumentos de evaluación recomendados": "Analytical rubric; Product rubric; Checklist; Peer assessment form",
            "Lugar": "Classroom / Virtual / Home / Outdoors",
            "Agrupamiento": "Individual / Pairs",
        },
        "DIM_GAMIF": {
            "Dimensión": "Gamified assessment",
            "Descripción breve": "Use of game mechanics to collect evidence of learning.",
            "Función pedagógica": "Increase motivation and engagement, and obtain immediate feedback on learning.",
            "Evidencias habituales": "Challenges, escape rooms, timed rounds, badges, leaderboards, cooperative quests.",
            "Cuándo conviene": "When high motivation is sought, when consolidating learning, or when conducting active diagnostic assessment.",
            "Precauciones": "Game mechanics must not distort assessment; participation must be distinguished from demonstrated learning.",
            "Etiquetas": "gamification; game-based; escape room; challenge; badges",
            "Descripción detallada": (
                "This dimension describes the didactic format or situation in which evidence is generated. It can "
                "combine several collection procedures.\n\n"
                "Gamified assessment incorporates game mechanics (challenges, points, badges, countdowns, regulated "
                "cooperation or competition) to collect evidence of learning in a highly motivating environment. It "
                "is not synonymous with a specific instrument such as an escape room (INS_ESCAPE), but rather the "
                "methodological approach that encompasses any strategy using games for assessment purposes.\n\n"
                "How to apply it: tasks or challenges are designed with clear rules, visible achievement criteria "
                "and immediate feedback. Points or badges can be used as evidence of the level reached if they are "
                "aligned with real assessment criteria. Analytics from the gamified platform (time, attempts, "
                "correct answers) complement the teacher's observation but do not replace it.\n\n"
                "It is especially suitable for formative assessment, consolidation and diagnostic assessment, as the "
                "playful context reduces assessment anxiety and encourages participation from students who struggle "
                "with motivation."
            ),
            "Medios/evidencias asociados": "Escape room or gamified challenge; Problem solving; Problem situation; Integrated competency task; Digital questionnaire",
            "Instrumentos de evaluación recomendados": "Observation scale; Checklist; Competency rubric; Learning analytics",
            "Lugar": "Classroom / Virtual",
            "Agrupamiento": "Individual / Small group / Whole class",
        }
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# BACK-REFERENCES TO ADD IN EXISTING ITEMS
# ─────────────────────────────────────────────────────────────────────────────

# Format: { filename: { código: { field: { key: value } } } }
# All languages share the same structure (codes/keys are identical).

BACKREF_INSTRUMENTOS = {
    # INS_ESCAPE → add DIM_GAMIF to rel_dim
    "INS_ESCAPE": {
        "rel_dim": {"DIM_GAMIF": "principal"},
        "rel_meta_dim": {"DIM_GAMIF": "principal"}
    },
    # INS_SIT_PROB → add DIM_GAMIF to rel_dim
    "INS_SIT_PROB": {
        "rel_dim": {"DIM_GAMIF": "complementaria"},
        "rel_meta_dim": {"DIM_GAMIF": "complementaria"}
    },
    # INS_TAREA_COMP_INT → add DIM_GAMIF to rel_dim
    "INS_TAREA_COMP_INT": {
        "rel_dim": {"DIM_GAMIF": "complementaria"},
        "rel_meta_dim": {"DIM_GAMIF": "complementaria"}
    },
}

BACKREF_TECNICAS = {
    # TEC_OBS_SIS → add INS_CUAD_CAMPO to rel_ins
    "TEC_OBS_SIS": {
        "rel_ins": {"INS_CUAD_CAMPO": "complementaria"},
        "rel_meta_ins": {"INS_CUAD_CAMPO": "complementaria"}
    },
    # TEC_PROD → add INS_CUAD_CAMPO and INS_MICROVIDEO
    "TEC_PROD": {
        "rel_ins": {"INS_CUAD_CAMPO": "complementaria", "INS_MICROVIDEO": "complementaria"},
        "rel_meta_ins": {"INS_CUAD_CAMPO": "complementaria", "INS_MICROVIDEO": "complementaria"}
    },
    # TEC_ORAL → add INS_MICROVIDEO
    "TEC_ORAL": {
        "rel_ins": {"INS_MICROVIDEO": "complementaria"},
        "rel_meta_ins": {"INS_MICROVIDEO": "complementaria"}
    },
}

BACKREF_HERRAMIENTAS = {
    # HER_GUIA_CORR → add INS_CUAD_CAMPO
    "HER_GUIA_CORR": {
        "rel_ins": {"INS_CUAD_CAMPO": "complementaria"},
        "rel_meta_ins": {"INS_CUAD_CAMPO": "complementaria"}
    },
    # HER_NOTAS_CAMPO → add INS_CUAD_CAMPO
    "HER_NOTAS_CAMPO": {
        "rel_ins": {"INS_CUAD_CAMPO": "principal"},
        "rel_meta_ins": {"INS_CUAD_CAMPO": "principal"}
    },
    # HER_RUB_ANA → add INS_MICROVIDEO
    "HER_RUB_ANA": {
        "rel_ins": {"INS_MICROVIDEO": "complementaria"},
        "rel_meta_ins": {"INS_MICROVIDEO": "complementaria"}
    },
    # HER_RUB_PROD → add INS_MICROVIDEO
    "HER_RUB_PROD": {
        "rel_ins": {"INS_MICROVIDEO": "complementaria"},
        "rel_meta_ins": {"INS_MICROVIDEO": "complementaria"}
    },
    # HER_ANALITICAS → add DIM_GAMIF
    "HER_ANALITICAS": {
        "rel_dim": {"DIM_GAMIF": "complementaria"},
        "rel_meta_dim": {"DIM_GAMIF": "complementaria"}
    },
}

BACKREF_DIMENSIONES = {
    # DIM_INDAG → add INS_CUAD_CAMPO
    "DIM_INDAG": {
        "rel_ins": {"INS_CUAD_CAMPO": "principal"},
        "rel_meta_ins": {"INS_CUAD_CAMPO": "principal"}
    },
    # DIM_COMP → add INS_CUAD_CAMPO and INS_MICROVIDEO
    "DIM_COMP": {
        "rel_ins": {"INS_CUAD_CAMPO": "complementaria", "INS_MICROVIDEO": "complementaria"},
        "rel_meta_ins": {"INS_CUAD_CAMPO": "complementaria", "INS_MICROVIDEO": "complementaria"}
    },
    # DIM_FORM → add INS_CUAD_CAMPO
    "DIM_FORM": {
        "rel_ins": {"INS_CUAD_CAMPO": "complementaria"},
        "rel_meta_ins": {"INS_CUAD_CAMPO": "complementaria"}
    },
    # DIM_DIG → add INS_MICROVIDEO
    "DIM_DIG": {
        "rel_ins": {"INS_MICROVIDEO": "principal"},
        "rel_meta_ins": {"INS_MICROVIDEO": "principal"}
    },
    # DIM_DESEMP → add INS_MICROVIDEO
    "DIM_DESEMP": {
        "rel_ins": {"INS_MICROVIDEO": "complementaria"},
        "rel_meta_ins": {"INS_MICROVIDEO": "complementaria"}
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {path}")

def build_item(shared, lang_text):
    item = copy.deepcopy(shared)
    item.update(lang_text)
    return item

def apply_backrefs(items, backrefs):
    """Apply back-references to a list of JSON items."""
    for item in items:
        code = item.get("Código")
        if code not in backrefs:
            continue
        refs = backrefs[code]

        for field, additions in refs.items():
            if field == "rel_meta_ins":
                item.setdefault("rel_meta", {}).setdefault("rel_ins", {}).update(additions)
                # Also add to rel_ins list if not present
                for k in additions:
                    if k not in item.get("rel_ins", []):
                        item.setdefault("rel_ins", []).append(k)
            elif field == "rel_meta_dim":
                item.setdefault("rel_meta", {}).setdefault("rel_dim", {}).update(additions)
                for k in additions:
                    if k not in item.get("rel_dim", []):
                        item.setdefault("rel_dim", []).append(k)
            elif field == "rel_ins":
                # handled above via rel_meta_ins
                pass
            elif field == "rel_dim":
                # handled above via rel_meta_dim
                pass

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def process_language(lang):
    print(f"\n── {lang.upper()} ──")
    lang_dir = os.path.join(BASE, lang)
    texts = LANG_DATA[lang]

    # ── instrumentos.json ──
    ins_path = os.path.join(lang_dir, "instrumentos.json")
    ins = load(ins_path)
    existing_codes = {i["Código"] for i in ins}

    # Add new instrument items if not already present
    for code in ["INS_CUAD_CAMPO", "INS_MICROVIDEO"]:
        if code not in existing_codes:
            shared = SHARED_INS_CUAD_CAMPO if code == "INS_CUAD_CAMPO" else SHARED_INS_MICROVIDEO
            ins.append(build_item(shared, texts[code]))
            print(f"  + Added {code}")
        else:
            print(f"  · {code} already exists, skipped")

    # Apply instrument back-references
    apply_backrefs(ins, BACKREF_INSTRUMENTOS)

    save(ins_path, ins)

    # ── tecnicas.json ──
    tec_path = os.path.join(lang_dir, "tecnicas.json")
    tec = load(tec_path)
    apply_backrefs(tec, BACKREF_TECNICAS)
    save(tec_path, tec)

    # ── herramientas.json ──
    her_path = os.path.join(lang_dir, "herramientas.json")
    her = load(her_path)
    apply_backrefs(her, BACKREF_HERRAMIENTAS)
    save(her_path, her)

    # ── dimensiones.json ──
    dim_path = os.path.join(lang_dir, "dimensiones.json")
    dim = load(dim_path)
    existing_dim_codes = {d["Código"] for d in dim}

    # Apply dimension back-references first
    apply_backrefs(dim, BACKREF_DIMENSIONES)

    # Add DIM_GAMIF if not present
    if "DIM_GAMIF" not in existing_dim_codes:
        dim.append(build_item(SHARED_DIM_GAMIF, texts["DIM_GAMIF"]))
        print(f"  + Added DIM_GAMIF")
    else:
        print(f"  · DIM_GAMIF already exists, skipped")

    save(dim_path, dim)


if __name__ == "__main__":
    for lang in ["es", "ca", "en"]:
        process_language(lang)
    print("\nDone.")
