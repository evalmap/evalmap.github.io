#!/usr/bin/env python3
"""Añade 'Descripción detallada' a instrumentos.json"""
import json

instrumentos_desc = {
"Trabajo individual en aula": (
    "El trabajo individual en aula es una actividad que el alumno realiza de forma autónoma durante la clase, "
    "sin apoyo directo de compañeros. Permite al docente observar en directo el nivel de autonomía, la "
    "organización y la capacidad de resolución de cada alumno.\n\n"
    "Cómo usarlo para evaluar: mientras el alumnado trabaja, el docente circula por el aula y observa con "
    "una escala de observación o lista de cotejo. Registra quién avanza con soltura, quién se bloquea y en "
    "qué punto. También puede recoger el resultado final (ejercicio, tarea, esquema) y valorarlo con una "
    "guía de corrección.\n\n"
    "Es uno de los instrumentos más habituales porque permite información tanto del proceso como del "
    "resultado, en condiciones controladas y sin interferencia de otros alumnos."
),
"Trabajo cooperativo": (
    "El trabajo cooperativo es una actividad grupal en la que los alumnos comparten responsabilidades, "
    "distribuyen tareas y construyen un resultado común. Permite evaluar colaboración, comunicación, "
    "responsabilidad individual y capacidad de integrar distintas aportaciones.\n\n"
    "Cómo usarlo para evaluar: conviene combinar la valoración del producto grupal con la del proceso "
    "y la contribución individual. Una rúbrica de trabajo cooperativo, un registro de grupo y la "
    "autoevaluación de cada miembro ofrecen una imagen completa. El docente puede observar el "
    "funcionamiento del grupo con una escala de observación.\n\n"
    "Para que la evaluación sea justa, no debe reducirse al producto final: dos grupos pueden entregar "
    "trabajos similares pero con procesos de colaboración muy distintos."
),
"Participación en clase": (
    "La participación en clase incluye las intervenciones orales del alumnado: respuestas a preguntas, "
    "aportaciones espontáneas, preguntas propias, comentarios y contribuciones al debate colectivo.\n\n"
    "Cómo usarla para evaluar: es necesario un registro sistemático para que no dependa de la memoria "
    "del docente. Un registro de participación con nombre y tipo de intervención (respuesta, pregunta, "
    "aportación) permite valorar frecuencia y calidad. Una escala de observación ayuda a no reducirlo "
    "a si levanta la mano o no.\n\n"
    "Debe valorarse la calidad de las aportaciones, no solo la cantidad. Un alumno que interviene poco "
    "pero con ideas precisas merece reconocimiento; uno que interviene mucho pero sin escuchar no "
    "debería ser premiado por eso."
),
"Debate": (
    "El debate es una discusión reglada en la que el alumnado defiende posiciones con argumentos, "
    "escucha las posiciones contrarias y responde a ellas. Puede ser espontáneo o preparado, formal "
    "o informal, con roles asignados o libre.\n\n"
    "Cómo usarlo para evaluar: el docente (u otros alumnos como coevaluadores) usa una rúbrica oral "
    "o escala de observación para valorar la calidad de los argumentos, el uso de evidencias, la "
    "escucha activa y el respeto a los turnos. Si el grupo es grande, puede grabarse o valorarse "
    "por turnos.\n\n"
    "El debate permite evaluar competencias que no son visibles en pruebas escritas: argumentación, "
    "pensamiento crítico, comunicación oral y capacidad de rebatir con respeto."
),
"Coloquio": (
    "El coloquio es una conversación estructurada pero más abierta que el debate, donde el alumnado "
    "intercambia ideas, opiniones e interpretaciones sobre un tema. No hay posiciones enfrentadas, "
    "sino construcción colectiva de significado.\n\n"
    "Cómo usarlo para evaluar: el docente modera y observa con una escala o rúbrica oral, prestando "
    "atención a la profundidad de las aportaciones, la capacidad de relacionar ideas y la escucha "
    "activa. Es más difícil de registrar que el debate porque las intervenciones son más fluidas.\n\n"
    "Es especialmente adecuado para evaluar comprensión lectora, análisis de textos, interpretación "
    "histórica y reflexión filosófica o ética."
),
"Asamblea": (
    "La asamblea es una reunión del grupo-clase donde se toman decisiones colectivas, se comparten "
    "experiencias o se debaten normas y conflictos. En contextos educativos, se usa especialmente en "
    "Infantil y Primaria, aunque también en tutoría y proyectos de convivencia.\n\n"
    "Cómo usarla para evaluar: permite observar competencias sociales y comunicativas: respeto al "
    "turno, escucha, argumentación, propuesta de soluciones. Un registro anecdótico o una escala "
    "de participación recogen las evidencias más significativas.\n\n"
    "No es un instrumento de evaluación académica en sentido estricto, pero sí permite evaluar "
    "competencias cívicas, de comunicación y de resolución de conflictos."
),
"Práctica de laboratorio": (
    "La práctica de laboratorio es una actividad experimental en la que el alumnado aplica "
    "procedimientos científicos para observar fenómenos, comprobar hipótesis o desarrollar "
    "habilidades técnicas. Requiere planificación, uso de materiales específicos y registro de resultados.\n\n"
    "Cómo usarla para evaluar: permite evaluar tanto el proceso (cómo aplica el protocolo, cómo "
    "maneja el material, cómo registra observaciones) como el producto (informe de laboratorio). "
    "El docente observa con una lista de cotejo de proceso y después valora el informe con una rúbrica.\n\n"
    "Es uno de los instrumentos más ricos para la evaluación competencial en ciencias, ya que integra "
    "conocimientos, procedimientos y actitudes en una sola actividad."
),
"Taller": (
    "El taller es una actividad práctica en la que el alumnado aplica habilidades, técnicas o "
    "conocimientos en un contexto de trabajo activo. Puede ser artístico, tecnológico, lingüístico, "
    "culinario, etc. El resultado suele ser un producto físico o una habilidad demostrable.\n\n"
    "Cómo usarlo para evaluar: el docente observa el proceso con una lista de cotejo o escala de "
    "observación y valora el producto con una rúbrica o ficha de valoración. En talleres colectivos, "
    "puede combinarse la valoración individual y grupal.\n\n"
    "Es especialmente adecuado para evaluar procedimientos, creatividad y aplicación práctica de "
    "conocimientos, aspectos que no son visibles en una prueba escrita."
),
"Simulación": (
    "La simulación recrea una situación verosímil (histórica, profesional, social o científica) en "
    "la que el alumnado actúa como si fuera real, tomando decisiones y resolviendo problemas en "
    "ese contexto ficticio.\n\n"
    "Cómo usarla para evaluar: el docente observa con una rúbrica de desempeño o registro anecdótico "
    "mientras la simulación transcurre. También puede valorarse la reflexión posterior (qué decisiones "
    "tomé, qué habría cambiado, qué aprendí). Un informe post-simulación aporta evidencia escrita.\n\n"
    "Permite evaluar habilidades difíciles de observar en otras situaciones: toma de decisiones bajo "
    "presión, comunicación en roles profesionales, resolución de conflictos y aplicación de protocolos."
),
"Juego de rol": (
    "En el juego de rol, cada alumno asume un papel con características, objetivos e información "
    "propios, e interactúa con otros roles para resolver una situación o alcanzar un objetivo.\n\n"
    "Cómo usarlo para evaluar: el docente observa la actuación con una rúbrica de desempeño o "
    "escala de observación, valorando la adecuación al rol, la argumentación, la comunicación y "
    "la colaboración. Un diario reflexivo posterior permite al alumno analizar su propia actuación.\n\n"
    "Es especialmente útil en historia, ciencias sociales, ética, idiomas y educación para la "
    "ciudadanía, donde es importante entender perspectivas distintas a la propia."
),
"Dramatización": (
    "La dramatización es la representación escénica de una situación, texto o historia. El alumnado "
    "interpreta personajes, ensaya y presenta ante el grupo. Puede ser improvisada o preparada.\n\n"
    "Cómo usarla para evaluar: se valora la expresión oral y corporal, la comprensión del texto "
    "o situación representada, la memorización, la cooperación en el ensayo y la calidad de la "
    "presentación. Una rúbrica oral y de desempeño, aplicada por el docente o como coevaluación, "
    "recoge estas dimensiones.\n\n"
    "Es un instrumento especialmente rico para lengua y literatura, idiomas extranjeros y educación "
    "artística, ya que integra comprensión, expresión, creatividad y trabajo en equipo."
),
"Exposición oral": (
    "La exposición oral es una presentación estructurada en la que el alumno comunica al grupo "
    "información, resultados o ideas sobre un tema, de forma ordenada y con apoyo visual opcional.\n\n"
    "Cómo usarla para evaluar: el docente usa una rúbrica oral que valora estructura, contenido, "
    "claridad, vocabulario, comunicación no verbal y gestión de preguntas. Puede completarse con "
    "autoevaluación del propio alumno y coevaluación de los compañeros. Si el grupo es grande, "
    "puede grabarse para valorar después.\n\n"
    "Permite evaluar competencia comunicativa oral, capacidad de síntesis y dominio del contenido, "
    "dimensiones que no son visibles en producciones escritas."
),
"Defensa de proyecto": (
    "La defensa de proyecto es una presentación oral en la que el alumno o equipo explica su "
    "proyecto ante una audiencia (clase, tribunal, familias) y responde a preguntas. Es el cierre "
    "habitual de un proyecto de investigación o trabajo de síntesis.\n\n"
    "Cómo usarla para evaluar: se valoran por separado el contenido del proyecto (ya evaluado antes) "
    "y la calidad de la defensa: claridad, respuesta a preguntas, distribución de roles en el equipo. "
    "Una rúbrica de defensa específica permite hacerlo de forma estructurada.\n\n"
    "Añade valor al proyecto porque obliga al alumnado a comprender realmente lo que han hecho y "
    "a poder explicarlo con sus propias palabras ante preguntas inesperadas."
),
"Entrevista": (
    "La entrevista es una conversación estructurada entre el docente y el alumno (o entre pares) "
    "con el objetivo de explorar su comprensión, reflexión o proceso de aprendizaje de forma "
    "más profunda que en una prueba escrita.\n\n"
    "Cómo usarla para evaluar: el docente prepara un guion de preguntas abiertas y registra las "
    "respuestas con un formulario o grabación. Las preguntas deben ir más allá de la reproducción "
    "de información y explorar el razonamiento ('¿por qué crees eso?', '¿cómo lo harías diferente?').\n\n"
    "Es especialmente útil para alumnos con dificultades de expresión escrita o cuando se quiere "
    "verificar el nivel real de comprensión, sin el apoyo de apuntes o compañeros."
),
"Pregunta oral estructurada": (
    "La pregunta oral estructurada es una pregunta planificada y dirigida individualmente o al "
    "grupo durante la clase, con el objetivo de comprobar comprensión o estimular el razonamiento.\n\n"
    "Cómo usarla para evaluar: el docente formula la pregunta, da tiempo de reflexión (no responder "
    "inmediatamente) y escucha la respuesta con atención, registrando la calidad con una nota breve. "
    "Las técnicas como 'pizarras individuales', 'pensar-compartir' o 'kahoot' estructuran el proceso.\n\n"
    "Es una de las formas más inmediatas y frecuentes de evaluación formativa: permite ajustar la "
    "enseñanza en tiempo real según las respuestas del grupo."
),
"Cuaderno de clase": (
    "El cuaderno de clase es el registro personal del alumno del trabajo realizado en el aula: "
    "apuntes, ejercicios, esquemas, correcciones y reflexiones. Refleja el proceso de aprendizaje "
    "día a día.\n\n"
    "Cómo usarlo para evaluar: el docente puede revisarlo periódicamente con una lista de cotejo "
    "(¿está completo?, ¿está ordenado?, ¿recoge las correcciones?) o con una rúbrica que valore "
    "también la calidad de los apuntes y la organización. También puede revisarse en tutorías "
    "individuales.\n\n"
    "Es una ventana al proceso de aprendizaje del alumno que no dejan otras evidencias. Un cuaderno "
    "bien llevado refleja implicación, organización y capacidad de síntesis."
),
"Diario de aprendizaje": (
    "El diario de aprendizaje es un registro personal donde el alumno anota periódicamente qué ha "
    "aprendido, qué le ha costado, qué preguntas tiene y cómo se siente respecto al proceso. "
    "Tiene una dimensión reflexiva y metacognitiva que va más allá del cuaderno de clase.\n\n"
    "Cómo usarlo para evaluar: el docente puede proporcionar preguntas guía ('¿qué aprendí hoy?', "
    "'¿qué todavía no entiendo bien?', '¿qué cambiaría de cómo estudié?'). Se valora la profundidad "
    "de la reflexión, la honestidad y la conexión entre lo aprendido y la experiencia personal.\n\n"
    "Es un instrumento poderoso para el desarrollo de la metacognición y la autonomía. Su "
    "evaluación debe valorar la reflexión, no la calidad de redacción ni si las respuestas "
    "son 'correctas'."
),
"Porfolio": (
    "El porfolio es una colección organizada de trabajos y reflexiones del alumno que documenta su "
    "proceso de aprendizaje a lo largo de un periodo. No es una carpeta de todos los trabajos, sino "
    "una selección razonada con reflexión sobre cada pieza.\n\n"
    "Cómo usarlo para evaluar: el alumno selecciona las evidencias que mejor muestran su aprendizaje "
    "y escribe una reflexión sobre cada una ('elegí este trabajo porque…', 'demuestra que sé…', "
    "'lo que mejoraría es…'). El docente valora tanto la calidad de las evidencias como la profundidad "
    "de las reflexiones.\n\n"
    "Permite una evaluación longitudinal y auténtica. Desarrolla la autonomía, la reflexión y la "
    "capacidad de presentar el propio aprendizaje. Es la base de la evaluación por competencias "
    "en muchos sistemas educativos."
),
"Informe de laboratorio": (
    "El informe de laboratorio es el documento escrito que recoge el proceso y resultados de una "
    "práctica experimental: objetivos, hipótesis, materiales, procedimiento, observaciones, "
    "resultados y conclusiones.\n\n"
    "Cómo usarlo para evaluar: se valora con una rúbrica o guía de corrección que contemple todas "
    "las secciones del informe. Especial atención a la coherencia entre los datos registrados y las "
    "conclusiones, y a si el alumno interpreta los resultados o simplemente los describe.\n\n"
    "Combina la evaluación del proceso (qué hicieron en el laboratorio) con la del producto escrito "
    "(qué son capaces de comunicar sobre lo que hicieron). Desarrolla el pensamiento científico y "
    "la escritura académica."
),
"Informe de investigación": (
    "El informe de investigación documenta el proceso y resultados de una indagación o investigación: "
    "pregunta de investigación, estado de la cuestión, metodología, resultados, discusión y "
    "conclusiones. Es más extenso y estructurado que el informe de laboratorio.\n\n"
    "Cómo usarlo para evaluar: una rúbrica analítica que valore cada sección por separado permite "
    "retroalimentación precisa. Especial atención a la calidad de las fuentes usadas, la coherencia "
    "entre la pregunta y la metodología, y la capacidad de interpretar los resultados críticamente.\n\n"
    "Es el instrumento más adecuado para evaluar competencias de investigación en ESO, Bachillerato "
    "y FP. Puede complementarse con la defensa oral del informe."
),
"Monografía": (
    "La monografía es un trabajo escrito extenso y estructurado sobre un tema específico, que requiere "
    "búsqueda, selección y síntesis de fuentes, organización del contenido y redacción académica. "
    "Es más conceptual que el informe de investigación.\n\n"
    "Cómo usarla para evaluar: se valora la calidad de las fuentes, la organización lógica, la "
    "capacidad de síntesis y de elaborar ideas propias (no solo resumir), la corrección lingüística "
    "y el uso correcto de citas y referencias. Una rúbrica analítica o guía de corrección desglosada "
    "por secciones es la herramienta más adecuada.\n\n"
    "Es especialmente útil en Bachillerato y FP para desarrollar y evaluar la escritura académica "
    "y el pensamiento analítico."
),
"Ensayo": (
    "El ensayo es un texto argumentativo en el que el alumno defiende una tesis o posición sobre un "
    "tema, apoyándose en argumentos, ejemplos y fuentes. A diferencia de la monografía, tiene una "
    "voz personal más marcada.\n\n"
    "Cómo usarlo para evaluar: se valora la claridad de la tesis, la calidad de los argumentos, el "
    "uso de evidencias, la cohesión del texto y la corrección lingüística. Una rúbrica analítica "
    "permite retroalimentación específica sobre cada dimensión.\n\n"
    "Es un instrumento especialmente adecuado para evaluar pensamiento crítico, argumentación y "
    "escritura académica en lengua, filosofía, ciencias sociales y humanidades."
),
"Comentario de texto": (
    "El comentario de texto es un análisis crítico de un fragmento (literario, histórico, científico, "
    "filosófico) que el alumno lleva a cabo siguiendo una estructura: comprensión, contextualización, "
    "análisis formal y valoración personal.\n\n"
    "Cómo usarlo para evaluar: se valora la comprensión global del texto, la identificación de ideas "
    "principales, la contextualización adecuada, la calidad del análisis y la coherencia de la "
    "valoración. La guía de corrección o rúbrica debe adaptarse al tipo de texto y a la etapa.\n\n"
    "Es uno de los instrumentos más habituales en lengua y literatura, historia y filosofía. Permite "
    "evaluar comprensión lectora en profundidad, análisis y escritura."
),
"Comentario de gráfica o datos": (
    "El comentario de gráfica o datos consiste en interpretar y explicar la información contenida "
    "en gráficos, tablas, mapas o conjuntos de datos. El alumno debe describir, analizar y extraer "
    "conclusiones de los datos presentados.\n\n"
    "Cómo usarlo para evaluar: se valora si el alumno identifica correctamente las variables, "
    "describe tendencias y patrones, interpreta los datos en contexto y extrae conclusiones "
    "justificadas. Una guía de corrección por etapas (descripción → análisis → conclusión) "
    "orienta tanto la corrección como la realización de la tarea.\n\n"
    "Es un instrumento clave en matemáticas, ciencias, geografía, economía y cualquier área "
    "que trabaje con datos cuantitativos."
),
"Resumen": (
    "El resumen es la síntesis de un texto o contenido, recogiendo las ideas principales de forma "
    "breve y con las propias palabras del alumno. Implica comprensión, selección y reformulación.\n\n"
    "Cómo usarlo para evaluar: se valora si el alumno identifica las ideas principales (no las "
    "secundarias o los ejemplos), si prescinde de información irrelevante, si usa sus propias "
    "palabras y si el resumen es coherente y bien proporcionado. Una guía de corrección o lista "
    "de cotejo sencilla es suficiente.\n\n"
    "Es un instrumento muy accesible para evaluar la comprensión lectora y la capacidad de "
    "síntesis en cualquier etapa y materia."
),
"Esquema": (
    "El esquema es una representación visual y jerarquizada de la estructura de un contenido, "
    "que muestra las relaciones entre ideas principales, secundarias y detalles mediante "
    "sangrías, llaves, numeración u otros organizadores visuales.\n\n"
    "Cómo usarlo para evaluar: se valora si el alumno identifica correctamente la jerarquía de "
    "ideas, si la estructura es coherente, si usa la terminología adecuada y si la representación "
    "es clara y completa. Una lista de cotejo con los elementos esperados permite una corrección "
    "rápida.\n\n"
    "Es especialmente útil para evaluar la comprensión y la organización del conocimiento, así "
    "como como herramienta de estudio que el alumno puede usar y mejorar."
),
"Mapa conceptual": (
    "El mapa conceptual es una representación gráfica de las relaciones entre conceptos, con "
    "nodos (conceptos) y enlaces etiquetados que describen el tipo de relación entre ellos. "
    "Fue desarrollado por Novak como herramienta de aprendizaje significativo.\n\n"
    "Cómo usarlo para evaluar: se valora la corrección de los conceptos incluidos, la adecuación "
    "de los enlaces y sus etiquetas, la jerarquía (si los más generales están arriba) y la "
    "presencia de relaciones cruzadas entre ramas (señal de comprensión profunda). Una rúbrica "
    "o lista de cotejo específica para mapas conceptuales orienta la valoración.\n\n"
    "Permite evaluar la estructura del conocimiento de un alumno: no solo si sabe los conceptos, "
    "sino cómo los relaciona entre sí."
),
"Mapa mental": (
    "El mapa mental es una representación gráfica que parte de una idea central y se ramifica "
    "hacia ideas relacionadas, usando colores, imágenes y palabras clave. Es más libre y "
    "creativo que el mapa conceptual.\n\n"
    "Cómo usarlo para evaluar: se valora la riqueza de las asociaciones, la organización general, "
    "el uso de imágenes y palabras clave relevantes y la capacidad de relacionar ideas de distintas "
    "ramas. Una rúbrica sencilla con criterios de contenido y presentación es suficiente.\n\n"
    "Es especialmente útil para explorar ideas previas, hacer lluvias de ideas estructuradas, "
    "planificar proyectos y evaluar la riqueza de asociaciones en un tema."
),
"Línea del tiempo": (
    "La línea del tiempo es una representación gráfica cronológica de hechos, periodos o procesos, "
    "que permite visualizar la secuencia temporal y las relaciones entre eventos.\n\n"
    "Cómo usarla para evaluar: se valora la selección de hechos relevantes, la precisión de las "
    "fechas, la proporcionalidad de los intervalos temporales, la inclusión de información "
    "contextual y la claridad de la presentación. Una lista de cotejo o rúbrica sencilla es suficiente.\n\n"
    "Es un instrumento clave en historia, biología (evolución), literatura (movimientos literarios) "
    "y cualquier área con dimensión temporal."
),
"Glosario": (
    "El glosario es una lista de términos específicos de un tema o materia, con su definición "
    "elaborada por el propio alumno. Va más allá de copiar definiciones: implica comprensión "
    "y reformulación.\n\n"
    "Cómo usarlo para evaluar: se valora si las definiciones son precisas, si el alumno usa sus "
    "propias palabras, si incluye ejemplos cuando es pertinente y si la terminología es adecuada. "
    "Una lista de cotejo o guía de corrección por término permite una revisión eficiente.\n\n"
    "Es útil como tarea continua a lo largo de una unidad y como herramienta de estudio. "
    "Permite evaluar la comprensión del vocabulario específico de la materia."
),
"Ficha de lectura": (
    "La ficha de lectura recoge información estructurada sobre una lectura: identificación del "
    "texto (autor, título, género), resumen, ideas principales, opinión personal y valoración "
    "crítica. Es una herramienta de mediación entre la lectura y la escritura académica.\n\n"
    "Cómo usarla para evaluar: se valora la comprensión del texto, la capacidad de síntesis, "
    "la profundidad del comentario personal y la conexión entre el texto y el conocimiento previo "
    "o el contexto del alumno. Una plantilla estructurada con criterios claros facilita la "
    "corrección.\n\n"
    "Es especialmente útil en lengua y literatura, filosofía, ciencias sociales y cualquier "
    "materia que incorpore lectura de textos como fuente de aprendizaje."
),
"Reseña": (
    "La reseña es un texto que describe, analiza y valora críticamente una obra (libro, película, "
    "exposición, experimento, etc.). Combina descripción objetiva y valoración argumentada.\n\n"
    "Cómo usarla para evaluar: se valora la descripción precisa del objeto reseñado, la calidad "
    "del análisis, la solidez de los argumentos valorativos y la coherencia del texto. Una rúbrica "
    "que diferencie descripción, análisis y valoración permite retroalimentación específica.\n\n"
    "Es un instrumento excelente para evaluar pensamiento crítico, escritura argumentativa y "
    "capacidad de emitir juicios fundamentados. Adecuado en lengua, literatura, arte y ciencias."
),
"Artículo divulgativo": (
    "El artículo divulgativo es un texto que explica un tema científico, histórico o cultural "
    "de forma accesible para un público no especializado. Requiere seleccionar, simplificar "
    "y comunicar sin perder rigor.\n\n"
    "Cómo usarlo para evaluar: se valora la adecuación al público destinatario (lenguaje claro "
    "pero riguroso), la selección de información relevante, la estructura narrativa y la "
    "corrección de los contenidos. Una rúbrica específica para escritura divulgativa orienta "
    "tanto la producción como la corrección.\n\n"
    "Desarrolla la competencia comunicativa escrita, la comprensión profunda de la materia y "
    "la capacidad de traducir conocimiento especializado. Adecuado en ciencias, historia y lengua."
),
"Memoria de proyecto": (
    "La memoria de proyecto es el documento escrito que recoge todo el proceso y resultado de "
    "un proyecto: planificación inicial, desarrollo, dificultades encontradas, soluciones "
    "adoptadas, resultado final y reflexión sobre el aprendizaje.\n\n"
    "Cómo usarla para evaluar: se valora tanto la calidad del proceso documentado como la del "
    "resultado. Una rúbrica que diferencie secciones (planificación, desarrollo, producto, "
    "reflexión) permite retroalimentación específica. La reflexión final sobre lo aprendido "
    "tiene especial valor metacognitivo.\n\n"
    "Es el instrumento de evaluación principal en proyectos de aprendizaje-servicio, proyectos "
    "interdisciplinares y trabajos de investigación de Bachillerato."
),
"Plan de trabajo": (
    "El plan de trabajo es un documento previo al inicio de un proyecto en el que el alumno o "
    "equipo define objetivos, tareas, responsables, recursos y plazos. Permite evaluar la "
    "capacidad de planificación antes de ejecutar.\n\n"
    "Cómo usarlo para evaluar: se valora la claridad de los objetivos, el realismo de los plazos, "
    "la distribución equitativa de tareas y la previsión de dificultades. Al finalizar el "
    "proyecto, puede compararse el plan inicial con lo que realmente sucedió, lo que añade "
    "valor reflexivo.\n\n"
    "Es una herramienta formativa que ayuda al alumnado a desarrollar competencias de "
    "organización y gestión del tiempo, fundamentales para la autonomía."
),
"Acta de reunión": (
    "El acta de reunión es el registro escrito de lo que ocurrió en una reunión del grupo: "
    "quién asistió, qué se debatió, qué acuerdos se tomaron y qué tareas se asignaron. "
    "Es un instrumento habitual en trabajo cooperativo y proyectos grupales.\n\n"
    "Cómo usarla para evaluar: el docente puede revisar las actas para comprobar que el grupo "
    "funciona de forma organizada, que los roles rotan, que los acuerdos se cumplen y que la "
    "reflexión sobre el trabajo es genuina. También puede usarse como evidencia de proceso.\n\n"
    "Desarrolla habilidades de comunicación formal, organización y responsabilidad compartida. "
    "Es especialmente útil en proyectos de larga duración."
),
"Contrato de aprendizaje": (
    "El contrato de aprendizaje es un acuerdo negociado entre el docente y el alumno sobre "
    "qué va a aprender, cómo lo va a demostrar, en qué plazos y con qué criterios será evaluado. "
    "Personaliza el proceso de aprendizaje.\n\n"
    "Cómo usarlo para evaluar: el contrato define los criterios y evidencias de evaluación desde "
    "el inicio. El alumno sabe exactamente qué debe lograr y cómo lo va a demostrar. Al final del "
    "periodo, se revisa conjuntamente si se han cumplido los compromisos acordados.\n\n"
    "Favorece la autonomía, la motivación intrínseca y la responsabilidad. Es especialmente "
    "útil con alumnado con necesidades específicas, alumnado avanzado o en situaciones de "
    "recuperación."
),
"Ficha de reflexión": (
    "La ficha de reflexión es un documento breve donde el alumno responde a preguntas "
    "metacognitivas sobre su proceso de aprendizaje: qué aprendió, cómo lo aprendió, qué le "
    "costó, qué cambiaría y qué quiere saber más.\n\n"
    "Cómo usarla para evaluar: se valora la profundidad de la reflexión, la capacidad de "
    "identificar dificultades propias y la conexión entre el aprendizaje y la experiencia "
    "personal. No debe valorarse si las respuestas son 'correctas', sino si son honestas "
    "y reflexivas.\n\n"
    "Es un instrumento de cierre muy eficaz para sesiones, unidades o proyectos. Convierte "
    "la evaluación en un momento de aprendizaje sobre el propio aprendizaje."
),
"Autoinforme": (
    "El autoinforme es un documento más extenso que la ficha de reflexión, donde el alumno "
    "describe y valora su propio proceso de aprendizaje durante un periodo: qué hizo, cómo "
    "evolucionó, qué logró, qué le faltó y qué aprendió sobre sí mismo como aprendiz.\n\n"
    "Cómo usarlo para evaluar: se valora la honestidad, la profundidad, la capacidad de "
    "identificar patrones propios y la conexión entre la reflexión y las evidencias del "
    "portfolio. Puede complementar la calificación del docente en la evaluación sumativa.\n\n"
    "Es un instrumento de alto valor metacognitivo, especialmente en portfolios, proyectos "
    "de larga duración y evaluación por competencias."
),
"Resolución de problemas": (
    "La resolución de problemas como instrumento consiste en presentar al alumno una situación "
    "problemática real o contextualizada que debe analizar, planificar, resolver y justificar. "
    "Va más allá del ejercicio mecánico: requiere razonamiento y aplicación.\n\n"
    "Cómo usarla para evaluar: se valora el proceso completo (comprensión del problema, "
    "planificación, ejecución, verificación) además del resultado. Pedir al alumno que explique "
    "su razonamiento (por escrito o verbalmente) añade información sobre su pensamiento. Una "
    "guía de corrección por etapas es la herramienta más adecuada.\n\n"
    "Es el instrumento central de la evaluación competencial en matemáticas, física, química, "
    "tecnología y economía."
),
"Estudio de caso": (
    "El estudio de caso presenta una situación real o verosímil que el alumno debe analizar, "
    "diagnosticar e interpretar, proponiendo soluciones o conclusiones fundamentadas. Aplica "
    "conocimientos a un contexto concreto.\n\n"
    "Cómo usarlo para evaluar: se valora la comprensión de la situación, la identificación de "
    "variables relevantes, la calidad del análisis y la coherencia de las conclusiones o "
    "propuestas. Una guía de análisis estructurada (¿qué ocurre?, ¿por qué?, ¿qué harías?) "
    "orienta tanto al alumno como al evaluador.\n\n"
    "Es especialmente adecuado en ciencias de la salud, ciencias sociales, derecho, historia, "
    "economía y FP, donde aplicar conocimientos a situaciones reales es el objetivo central."
),
"Prueba escrita de desarrollo": (
    "La prueba escrita de desarrollo consiste en preguntas o tareas que el alumno responde "
    "con texto propio, elaborando argumentos, explicaciones, análisis o síntesis. Va más allá "
    "de la memorización: requiere organización, razonamiento y expresión escrita.\n\n"
    "Cómo usarla para evaluar: se valora con una guía de corrección o rúbrica que especifique "
    "qué contenidos debe incluir cada respuesta y con qué profundidad. Compartir los criterios "
    "antes de la prueba reduce la ansiedad y orienta el estudio del alumno.\n\n"
    "Permite evaluar comprensión profunda, capacidad de síntesis y escritura académica. "
    "Especialmente útil en humanidades, ciencias sociales y ciencias cuando se quiere ir más "
    "allá de la respuesta objetiva."
),
"Prueba objetiva": (
    "La prueba objetiva incluye ítems con una única respuesta correcta verificable: verdadero/falso, "
    "emparejamiento, completar espacios en blanco, ordenar elementos. La corrección es mecánica "
    "y no depende del juicio del evaluador.\n\n"
    "Cómo usarla para evaluar: se diseña con ítems claros y sin ambigüedad, alineados con los "
    "contenidos y criterios trabajados. Se establece el baremo (puntuación por acierto, penalización "
    "por error si la hay). La automatización de la corrección permite obtener resultados rápidamente.\n\n"
    "Es eficiente para comprobar conocimientos declarativos en grupos grandes. Su limitación "
    "es que no evalúa razonamiento profundo ni competencias complejas."
),
"Prueba tipo test": (
    "La prueba tipo test presenta ítems de opción múltiple con una respuesta correcta y varios "
    "distractores (opciones incorrectas plausibles). Es un subtipo de prueba objetiva muy extendido.\n\n"
    "Cómo usarla para evaluar: los distractores deben ser plausibles pero claramente incorrectos "
    "para quien ha aprendido el contenido. Evitar respuestas como 'todas las anteriores' o "
    "'ninguna de las anteriores', que facilitan el acierto por eliminación. El baremo debe "
    "especificar si hay penalización por error para desincentivar las respuestas al azar.\n\n"
    "Es muy eficiente para evaluar grandes cantidades de contenido en poco tiempo, pero no "
    "debe ser el único instrumento de evaluación."
),
"Prueba de respuesta corta": (
    "La prueba de respuesta corta pide al alumno que responda con una frase, término o cálculo "
    "breve. No es opción múltiple (hay que construir la respuesta) pero tampoco requiere "
    "desarrollo extenso.\n\n"
    "Cómo usarla para evaluar: se valora la precisión y corrección de la respuesta. La guía "
    "de corrección debe incluir las respuestas aceptables y posibles variantes equivalentes. "
    "Es más exigente que el test porque el alumno no puede guiarse por las opciones.\n\n"
    "Equilibra la eficiencia de la prueba objetiva con la necesidad de que el alumno construya "
    "su respuesta. Adecuada para vocabulario, definiciones, fórmulas, fechas y conceptos clave."
),
"Prueba oral": (
    "La prueba oral es una evaluación en la que el alumno responde verbalmente a preguntas "
    "del docente sobre un tema o conjunto de contenidos, demostrando su comprensión y "
    "capacidad de expresión.\n\n"
    "Cómo usarla para evaluar: el docente prepara un banco de preguntas de distinta dificultad "
    "y registra las respuestas con una rúbrica oral o guía de corrección. Puede incluir "
    "preguntas de seguimiento para explorar el razonamiento. Si el grupo es grande, puede "
    "hacerse en parejas con coevaluación.\n\n"
    "Permite valorar comprensión real (no memorización de texto) y expresión oral. Es "
    "especialmente útil con alumnado con dificultades de escritura y en idiomas."
),
"Prueba práctica": (
    "La prueba práctica es una evaluación en la que el alumno demuestra una habilidad, "
    "procedimiento o competencia ejecutándola en tiempo real: disección, análisis de muestra, "
    "construcción de un circuito, interpretación musical, reparación de un dispositivo.\n\n"
    "Cómo usarla para evaluar: el docente observa la ejecución con una lista de cotejo de "
    "proceso o rúbrica de desempeño. Si el producto es valorable (resultado del análisis, "
    "circuito funcionando), puede añadirse una valoración del resultado final.\n\n"
    "Es el instrumento más adecuado para evaluar saber hacer: procedimientos técnicos, "
    "habilidades artísticas, prácticas de laboratorio y competencias profesionales en FP."
),
"Prueba competencial contextualizada": (
    "La prueba competencial contextualizada es una prueba escrita u oral que presenta situaciones "
    "reales o verosímiles y pide al alumno que aplique sus conocimientos para analizarlas, "
    "interpretarlas o resolverlas. Es la forma de prueba más alineada con la evaluación competencial.\n\n"
    "Cómo usarla para evaluar: cada tarea de la prueba está asociada a un criterio de evaluación "
    "y a una competencia específica. Se valora con rúbricas o guías de corrección que contemplan "
    "el razonamiento y la aplicación, no solo el resultado correcto.\n\n"
    "Es la herramienta que mejor articula la calificación con la evaluación por criterios y "
    "competencias exigida por el marco curricular actual."
),
"Prueba con documentos": (
    "La prueba con documentos presenta textos, gráficos, mapas, imágenes u otros materiales "
    "que el alumno debe analizar, interpretar y usar para responder a las preguntas. "
    "Evalúa la capacidad de trabajar con fuentes, no solo de memorizar información.\n\n"
    "Cómo usarla para evaluar: se valora la comprensión de los documentos, la capacidad de "
    "extraer información relevante, la contextualización y la síntesis crítica. Una guía de "
    "corrección que especifique qué se espera en cada pregunta asegura coherencia.\n\n"
    "Es el formato de prueba más habitual en historia, geografía, ciencias sociales y lengua, "
    "y es la base de las pruebas de selectividad en muchas materias."
),
"Cuestionario digital": (
    "El cuestionario digital es un formulario en línea (Google Forms, Microsoft Forms, Socrative, "
    "Kahoot, etc.) con preguntas cerradas o abiertas que el alumno responde desde un dispositivo. "
    "Permite corrección automática y recogida instantánea de datos.\n\n"
    "Cómo usarlo para evaluar: se configura con las preguntas y, en el caso de respuestas cerradas, "
    "las respuestas correctas. El sistema corrige automáticamente y genera estadísticas de grupo. "
    "Las preguntas abiertas requieren revisión manual. Puede usarse como diagnóstico, ticket de "
    "salida o evaluación sumativa.\n\n"
    "Ahorra tiempo de corrección, permite retroalimentación inmediata y facilita el análisis "
    "de resultados del grupo para ajustar la enseñanza."
),
"Infografía": (
    "La infografía combina texto e imágenes para comunicar información de forma visual, clara "
    "y sintética sobre un tema. El alumno debe seleccionar la información relevante, jerarquizarla "
    "y diseñar una presentación visualmente efectiva.\n\n"
    "Cómo usarla para evaluar: se valora la selección y precisión de la información, la jerarquía "
    "visual, la legibilidad, la adecuación al destinatario y el uso de recursos gráficos. Una "
    "rúbrica que diferencie contenido y diseño permite retroalimentación específica.\n\n"
    "Desarrolla la competencia comunicativa visual, la capacidad de síntesis y la creatividad. "
    "Permite evaluar comprensión de contenidos de una forma diferente a la escritura lineal."
),
"Póster académico": (
    "El póster académico es una producción visual que presenta los resultados de un trabajo "
    "o investigación de forma sintética: pregunta, metodología, resultados y conclusiones. "
    "Se usa habitualmente en congresos científicos y puede trasladarse al aula.\n\n"
    "Cómo usarlo para evaluar: se valora la selección de información, la jerarquía visual, "
    "la precisión del contenido y la claridad del diseño. Si se acompaña de una defensa oral, "
    "puede valorarse también la capacidad de explicar y responder preguntas.\n\n"
    "Es especialmente adecuado en ciencias, tecnología y proyectos de investigación. Combina "
    "competencia comunicativa visual y dominio del contenido."
),
"Presentación digital": (
    "La presentación digital (PowerPoint, Google Slides, Canva, Prezi, etc.) es un soporte "
    "visual para una exposición oral. El alumno debe diseñarla de forma que apoye su discurso "
    "sin reemplazarlo.\n\n"
    "Cómo usarla para evaluar: conviene valorar por separado el diseño de la presentación "
    "(organización, legibilidad, uso de imágenes) y la calidad de la exposición oral que la "
    "acompaña. Una rúbrica que contempla ambas dimensiones evita confundir una presentación "
    "visualmente atractiva con un discurso de calidad.\n\n"
    "Es un instrumento muy habitual pero que requiere orientación explícita sobre qué hace "
    "una buena presentación (texto mínimo, imágenes relevantes, legibilidad)."
),
"Vídeo": (
    "El vídeo es una producción audiovisual creada por el alumno (documental, reportaje, "
    "tutorial, cortometraje, etc.) que integra imagen, sonido, guion y edición. Puede ser "
    "individual o grupal.\n\n"
    "Cómo usarlo para evaluar: se valoran por separado el contenido (precisión, profundidad, "
    "selección de información) y la producción (imagen, sonido, edición, guion). Una rúbrica "
    "analítica con criterios diferenciados permite retroalimentación específica en cada dimensión.\n\n"
    "Desarrolla la competencia digital, la comunicación audiovisual y la creatividad. Es "
    "especialmente motivador para el alumnado que tiene dificultades con la escritura."
),
"Videotutorial": (
    "El videotutorial es un vídeo en el que el alumno explica paso a paso cómo hacer algo: "
    "resolver un problema matemático, usar una herramienta, realizar un procedimiento de "
    "laboratorio, etc. Requiere dominar el contenido para poder explicarlo.\n\n"
    "Cómo usarlo para evaluar: se valora la claridad y precisión de la explicación, el orden "
    "lógico de los pasos, la corrección del contenido y la calidad de la producción. Si el "
    "alumno puede explicar algo de forma que otro lo entienda, demuestra comprensión profunda.\n\n"
    "Es un excelente instrumento para evaluar comprensión procedimental y la capacidad de "
    "comunicar conocimiento. La enseñanza entre iguales (peer teaching) tiene un alto valor "
    "de aprendizaje."
),
"Podcast": (
    "El podcast es una producción de audio (entrevista, reportaje, debate, programa informativo) "
    "creada por el alumno, que requiere guionización, locución, edición y publicación o entrega.\n\n"
    "Cómo usarlo para evaluar: se valora la calidad del guion (selección de información, "
    "estructura, rigor), la expresión oral (claridad, ritmo, vocabulario) y la producción "
    "técnica (sonido, edición). Una rúbrica analítica con estas tres dimensiones es adecuada.\n\n"
    "Favorece la expresión oral en un formato diferente al de la exposición presencial, lo que "
    "puede ser más cómodo para algunos alumnos. Desarrolla competencia comunicativa y digital."
),
"Cómic": (
    "El cómic es una narración secuencial que combina imágenes y texto para contar una historia "
    "o explicar un proceso. El alumno debe planificar la secuencia, diseñar los personajes y "
    "redactar los diálogos o textos.\n\n"
    "Cómo usarlo para evaluar: se valora la adecuación del contenido al tema, la coherencia "
    "narrativa, la calidad de los diálogos y la creatividad del diseño. Una rúbrica que "
    "diferencie contenido y formato permite retroalimentación específica.\n\n"
    "Es especialmente útil en lengua y literatura, historia, ciencias y educación artística. "
    "Permite evaluar comprensión de contenidos de una forma creativa y accesible."
),
"Maqueta": (
    "La maqueta es una representación tridimensional a escala de un objeto, espacio, estructura "
    "o sistema. Requiere planificación, diseño, construcción y justificación de las decisiones tomadas.\n\n"
    "Cómo usarla para evaluar: se valoran la fidelidad a lo representado, la calidad de la "
    "construcción, el uso adecuado de materiales y la precisión de las proporciones. Si se "
    "acompaña de una explicación oral o escrita, puede valorarse también la comprensión del "
    "modelo.\n\n"
    "Es especialmente útil en tecnología, arquitectura, geografía, historia y ciencias naturales "
    "para hacer visible lo que solo se describe en texto."
),
"Modelo digital": (
    "El modelo digital es una representación virtual (3D, simulación, diagrama interactivo) "
    "creada con herramientas digitales (Tinkercad, SketchUp, GeoGebra, etc.) que muestra "
    "la comprensión de un sistema, estructura o proceso.\n\n"
    "Cómo usarlo para evaluar: se valora la precisión del modelo respecto al referente real, "
    "la calidad técnica de la construcción digital y la capacidad de explicar qué representa "
    "y por qué se tomaron ciertas decisiones de diseño.\n\n"
    "Desarrolla la competencia digital y el pensamiento espacial. Es especialmente adecuado "
    "en tecnología, diseño, matemáticas y ciencias experimentales."
),
"Prototipo": (
    "El prototipo es una versión funcional (aunque incompleta o simplificada) de un producto, "
    "dispositivo o solución diseñada para probar su viabilidad y obtener retroalimentación "
    "antes del producto final.\n\n"
    "Cómo usarlo para evaluar: se valora la funcionalidad (¿cumple su función?), la adecuación "
    "a los requisitos, la calidad del diseño y la reflexión sobre lo que funciona y lo que "
    "habría que mejorar. El proceso de iteración (probar → mejorar → probar) es tan valioso "
    "como el prototipo final.\n\n"
    "Es el instrumento central en proyectos de design thinking, tecnología, FP y cualquier "
    "proceso de diseño centrado en el usuario."
),
"Página web": (
    "La página web es un producto digital que combina texto, imagen, vídeo y otros recursos "
    "en un entorno interactivo accesible en línea. Requiere planificación de contenidos, "
    "diseño de la estructura y habilidades técnicas de creación.\n\n"
    "Cómo usarla para evaluar: se valoran el contenido (precisión, profundidad, selección), "
    "la organización (navegación, estructura), el diseño (legibilidad, accesibilidad) y la "
    "corrección técnica. Una rúbrica analítica que diferencie estas dimensiones es la "
    "herramienta más adecuada.\n\n"
    "Desarrolla competencia digital, comunicación multimodal y comprensión de la materia. "
    "Es especialmente motivador para el alumnado con afinidad tecnológica."
),
"Entrada de blog": (
    "La entrada de blog es un texto de divulgación personal o académica publicado en un "
    "blog, que combina rigor en el contenido con un estilo más accesible y personal que el "
    "texto académico formal.\n\n"
    "Cómo usarla para evaluar: se valora la adecuación al destinatario, la precisión del "
    "contenido, la originalidad del enfoque, la calidad de la escritura y el uso de recursos "
    "digitales (imágenes, enlaces). Una rúbrica que diferencie contenido y formato es adecuada.\n\n"
    "Es un buen instrumento para trabajar la escritura con una audiencia real y desarrollar "
    "la voz propia del alumno. El hecho de que sea publicado añade motivación y responsabilidad."
),
"Foro de discusión": (
    "El foro de discusión es un espacio de intercambio escrito asíncrono (en plataforma digital) "
    "donde el alumnado debate, argumenta y comenta sobre un tema, leyendo y respondiendo a las "
    "aportaciones de sus compañeros.\n\n"
    "Cómo usarlo para evaluar: se valoran la calidad de la aportación inicial (argumentación, "
    "uso de fuentes) y la calidad de las respuestas a otros (escucha activa, respeto, "
    "profundización). Una rúbrica de participación en foro con criterios de calidad, no solo "
    "de cantidad, es la herramienta más adecuada.\n\n"
    "Permite la participación de alumnos que no intervienen fácilmente en debates presenciales. "
    "Deja trazas escritas que facilitan la evaluación."
),
"Documento colaborativo": (
    "El documento colaborativo es un documento digital (Google Docs, Word Online, etc.) que "
    "varios alumnos editan simultánea o asíncronamente para construir un texto, análisis o "
    "producto compartido.\n\n"
    "Cómo usarlo para evaluar: el historial de revisiones permite ver la contribución individual "
    "de cada miembro, lo que hace la evaluación del trabajo grupal más justa. Se valora tanto "
    "el producto final como el proceso de construcción colaborativa.\n\n"
    "Es especialmente útil para proyectos grupales donde la contribución individual es difícil "
    "de distinguir en el resultado final. El historial de revisiones es la clave para la "
    "evaluación individualizada."
),
"Portfolio digital": (
    "El portfolio digital es una colección organizada de evidencias de aprendizaje almacenadas "
    "en formato digital (Google Sites, Seesaw, Mahara, carpeta de Drive, etc.), con reflexiones "
    "del alumno sobre cada evidencia.\n\n"
    "Cómo usarlo para evaluar: se valoran la selección de evidencias (¿muestra lo más significativo?), "
    "la calidad de las reflexiones (¿qué aprendí con esto?, ¿cómo lo haría diferente?) y la "
    "organización general. El portfolio digital permite compartirlo con familias y otros docentes.\n\n"
    "Es la herramienta más completa para la evaluación por competencias y el seguimiento "
    "longitudinal del aprendizaje. Desarrolla la autonomía y la metacognición del alumno."
),
"KPSI": (
    "El KPSI (Knowledge and Prior Study Inventory) es un cuestionario de evaluación diagnóstica "
    "en el que el alumno indica, para cada concepto o habilidad del tema, si lo sabe (y puede "
    "explicarlo), cree que lo sabe, no lo sabe o no lo entiende.\n\n"
    "Cómo usarlo para evaluar: se aplica al inicio de una unidad o proyecto para detectar "
    "conocimientos previos y concepciones erróneas. No tiene función calificadora. Al finalizar "
    "la unidad, puede repetirse para que el alumno vea su propio progreso.\n\n"
    "Es una herramienta de diagnóstico rápida y valiosa que permite al docente ajustar la "
    "planificación y al alumno tomar conciencia de lo que ya sabe y lo que necesita aprender."
),
"Mapa conceptual inicial": (
    "El mapa conceptual inicial es un mapa conceptual elaborado por el alumno al comienzo "
    "de una unidad, sin haber estudiado el tema aún, para mostrar qué sabe y cómo relaciona "
    "los conceptos en ese momento.\n\n"
    "Cómo usarlo para evaluar: se usa exclusivamente como diagnóstico, nunca para calificar. "
    "Al finalizar la unidad, el alumno elabora un nuevo mapa y compara ambos para visualizar "
    "su aprendizaje. La diferencia entre el mapa inicial y el final es una evidencia poderosa "
    "del progreso.\n\n"
    "Permite al docente detectar concepciones previas, tanto correctas como erróneas, y "
    "ajustar la secuencia didáctica en consecuencia."
),
"Lluvia de ideas": (
    "La lluvia de ideas (brainstorming) es una actividad en la que el alumnado genera de forma "
    "libre y sin censura todas las ideas que se les ocurren sobre un tema o problema. "
    "Se usa para activar conocimientos previos, generar hipótesis o explorar soluciones posibles.\n\n"
    "Cómo usarla para evaluar: no tiene función calificadora en sí misma, pero permite al "
    "docente detectar qué saben y cómo piensan los alumnos sobre el tema antes de empezar. "
    "Las ideas generadas pueden clasificarse, debatirse y revisarse al final de la unidad.\n\n"
    "Es una herramienta diagnóstica y motivadora. En grupos, puede revelar la riqueza "
    "colectiva de conocimientos previos y las ideas más y menos extendidas."
),
"Borrador": (
    "El borrador es una versión preliminar de un trabajo, no terminada ni pulida, que el alumno "
    "entrega para recibir retroalimentación antes de la entrega final. Es el instrumento central "
    "de la evaluación formativa en tareas escritas.\n\n"
    "Cómo usarlo para evaluar: el docente (o los compañeros en coevaluación) lee el borrador "
    "y ofrece retroalimentación específica sobre qué está bien y qué debe mejorar. No se "
    "califica el borrador; se califica la versión final después de la revisión.\n\n"
    "El ciclo borrador → retroalimentación → revisión → entrega final es uno de los procesos "
    "más efectivos para mejorar la escritura y el aprendizaje en general."
),
"Entrega parcial": (
    "La entrega parcial es una versión incompleta pero avanzada de un proyecto o trabajo, que "
    "se presenta en un momento intermedio para que el docente pueda dar retroalimentación "
    "y el alumno pueda ajustar el rumbo antes de terminar.\n\n"
    "Cómo usarla para evaluar: se valora con una retroalimentación oral o escrita centrada "
    "en lo que está bien encaminado y lo que debe revisarse. Puede tener una puntuación "
    "parcial que contribuya a la nota final, incentivando el trabajo sostenido.\n\n"
    "Evita la acumulación de trabajo al final y permite detectar problemas de comprensión "
    "o de planificación cuando todavía hay tiempo para corregirlos."
),
"Bitácora de proyecto": (
    "La bitácora de proyecto es un diario de seguimiento del proceso de un proyecto: qué se "
    "hizo en cada sesión, qué decisiones se tomaron, qué dificultades surgieron y cómo se "
    "resolvieron. Es el registro del proceso, no del resultado.\n\n"
    "Cómo usarla para evaluar: el docente la revisa periódicamente para comprobar el avance, "
    "detectar dificultades a tiempo y valorar la calidad del proceso. Una lista de cotejo "
    "o rúbrica de proceso específica para bitácoras orienta la valoración.\n\n"
    "Hace visible el proceso de aprendizaje, que de otro modo solo se conoce por el producto "
    "final. Es especialmente valiosa en proyectos de larga duración y trabajos grupales."
),
"Revisión por pares": (
    "La revisión por pares es el proceso en que un alumno lee y comenta el trabajo de un "
    "compañero, aplicando criterios compartidos, con el objetivo de ayudarle a mejorarlo "
    "antes de la entrega final.\n\n"
    "Cómo usarla para evaluar: se proporciona una ficha de revisión o rúbrica de coevaluación "
    "con criterios concretos. El revisor debe dar retroalimentación específica y accionable, "
    "no solo decir 'está bien' o 'mejora la redacción'. El proceso mismo de revisar el trabajo "
    "ajeno es una poderosa experiencia de aprendizaje.\n\n"
    "Es uno de los instrumentos de evaluación formativa con mayor impacto en la calidad del "
    "trabajo final. Desarrolla pensamiento crítico, comprensión de los criterios y empatía."
),
"Dos estrellas y un deseo": (
    "Las 'dos estrellas y un deseo' es una técnica de retroalimentación formativa en la que "
    "el evaluador (docente o compañero) señala dos aspectos positivos del trabajo (las estrellas) "
    "y una sugerencia de mejora concreta (el deseo).\n\n"
    "Cómo usarla para evaluar: se entrega una tarjeta o formulario con tres apartados ("
    "'Lo que está muy bien:', 'Otra cosa que funciona:', 'Una cosa que podrías mejorar:'). "
    "Es estructuralmente sencilla pero requiere que los comentarios sean específicos y concretos, "
    "no genéricos ('está bien escrito').\n\n"
    "Es una herramienta especialmente adecuada para introducir la coevaluación con grupos "
    "que no tienen práctica en ella, por su formato accesible y su balance entre lo positivo "
    "y lo mejorable."
),
"Semáforo de aprendizaje": (
    "El semáforo de aprendizaje es una técnica de autoevaluación rápida en la que el alumno "
    "indica su nivel de comprensión de un contenido usando tres colores: verde (lo entiendo "
    "bien), amarillo (tengo algunas dudas), rojo (no lo entiendo o estoy perdido).\n\n"
    "Cómo usarlo para evaluar: puede hacerse con tarjetas de colores físicas, con post-its, "
    "con un formulario digital o con una paleta en la pizarra. Al final de una explicación "
    "o sesión, el docente ve de un vistazo cuántos alumnos están en verde, amarillo o rojo "
    "y ajusta la siguiente sesión.\n\n"
    "Es una herramienta de evaluación formativa instantánea que permite al docente regular "
    "el ritmo de la enseñanza en tiempo real. Requiere un clima de confianza para que los "
    "alumnos sean honestos."
),
"Billete de salida": (
    "El billete de salida (exit ticket) es una respuesta breve que el alumno entrega al "
    "final de la clase para mostrar qué aprendió, qué duda le quedó o cómo aplicaría lo "
    "aprendido. Es una forma rápida de evaluación formativa al cierre de la sesión.\n\n"
    "Cómo usarlo para evaluar: puede ser una pregunta escrita en papel o un formulario "
    "digital. El docente revisa las respuestas antes de la siguiente clase para identificar "
    "qué alumnos necesitan más apoyo y qué conceptos hay que reforzar.\n\n"
    "Es una de las estrategias de evaluación formativa más sencillas y efectivas. Con "
    "cinco minutos al final de cada clase, el docente obtiene información valiosa sobre "
    "el estado real del aprendizaje del grupo."
),
}

with open('/home/jjdeharo/Documentos/github/evaluacion/data/instrumentos.json', encoding='utf-8') as f:
    instrumentos = json.load(f)

for item in instrumentos:
    nombre = item['Instrumento']
    if nombre in instrumentos_desc:
        item['Descripción detallada'] = instrumentos_desc[nombre]

with open('/home/jjdeharo/Documentos/github/evaluacion/data/instrumentos.json', 'w', encoding='utf-8') as f:
    json.dump(instrumentos, f, ensure_ascii=False, indent=2)

total = sum(1 for i in instrumentos if 'Descripción detallada' in i)
print(f"Instrumentos actualizados: {total}/{len(instrumentos)}")
