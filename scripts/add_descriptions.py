#!/usr/bin/env python3
"""Añade el campo 'Descripción detallada' a los tres JSON de evaluación."""
import json

# ─── TÉCNICAS ────────────────────────────────────────────────────────────────
tecnicas_desc = {
"Observación sistemática": (
    "La observación sistemática es una técnica en la que el docente planifica de antemano qué va a observar, "
    "en qué momentos y con qué instrumento de registro. No es mirar de forma genérica, sino atender a criterios "
    "concretos y observables mientras el alumnado actúa.\n\n"
    "Cómo aplicarla: antes de la sesión se define qué indicadores se van a observar (p. ej., 'utiliza el material "
    "de laboratorio correctamente', 'argumenta con evidencias', 'escucha activamente'). Durante la actividad, el "
    "docente usa una lista de cotejo, escala de observación o rúbrica para registrar lo que ve. Al finalizar, esa "
    "información sirve para dar retroalimentación, ajustar la enseñanza o contribuir a la calificación.\n\n"
    "Es especialmente útil en actividades prácticas, debates, exposiciones, talleres y trabajo cooperativo, "
    "donde la evidencia del aprendizaje sucede en directo y no queda en un producto físico."
),
"Observación incidental": (
    "La observación incidental registra hechos relevantes que emergen de forma espontánea durante la actividad "
    "cotidiana del aula, sin que el docente los haya previsto. Un comentario perspicaz, una dificultad recurrente, "
    "un conflicto en el grupo o una iniciativa inesperada son ejemplos de evidencias incidentales.\n\n"
    "Cómo aplicarla: el docente debe tener siempre a mano un registro anecdótico, una libreta o una aplicación "
    "donde anotar brevemente la fecha, el nombre del alumno y el hecho observado. Estas notas, acumuladas a lo "
    "largo del tiempo, permiten ver patrones de conducta, progreso o dificultades que una observación planificada "
    "podría no captar.\n\n"
    "No sustituye a la observación sistemática, sino que la complementa aportando evidencias inesperadas y matices "
    "cualitativos sobre el proceso de aprendizaje."
),
"Análisis de producciones": (
    "El análisis de producciones consiste en valorar los artefactos o productos elaborados por el alumnado: "
    "textos escritos, informes, proyectos, presentaciones, vídeos, mapas conceptuales, maquetas, portfolios o "
    "cualquier otro producto tangible o digital.\n\n"
    "Cómo aplicarla: se define con antelación qué criterios se van a valorar y con qué herramienta (rúbrica, "
    "guía de corrección, escala descriptiva). La revisión puede hacerse fuera del horario de clase, lo que "
    "permite al docente dedicar más tiempo y atención que durante una observación en directo. Es fundamental "
    "devolver retroalimentación escrita que explique no solo el nivel alcanzado, sino qué puede mejorar y cómo.\n\n"
    "Cuando el producto final no refleja todo el aprendizaje (porque el proceso fue complejo o el trabajo fue "
    "grupal), conviene complementarlo con seguimiento del proceso, borradores o entrevistas breves."
),
"Pruebas específicas": (
    "Las pruebas específicas son situaciones diseñadas expresamente para comprobar aprendizajes en condiciones "
    "controladas. Incluyen pruebas escritas de desarrollo, pruebas tipo test, pruebas de respuesta corta, pruebas "
    "orales y pruebas prácticas.\n\n"
    "Cómo aplicarlas: el diseño debe estar alineado con los criterios de evaluación y los saberes trabajados. "
    "Cada pregunta o tarea debe poder asociarse a un criterio concreto. Es recomendable compartir con antelación "
    "los criterios de corrección (o al menos el tipo de tarea) para que el alumnado pueda prepararse de forma "
    "orientada.\n\n"
    "Son útiles para acreditar logros y para comparar resultados, pero no deben ser el único instrumento de "
    "evaluación. Combinadas con otras evidencias (producciones, observación, autoevaluación), ofrecen una imagen "
    "más completa y justa del aprendizaje."
),
"Intercambios orales": (
    "Los intercambios orales son situaciones en las que el docente obtiene evidencias de aprendizaje mediante la "
    "comunicación oral: preguntas al grupo, debates dirigidos, coloquios, entrevistas individuales o defensas de "
    "proyectos.\n\n"
    "Cómo aplicarlos: conviene planificar las preguntas o el guion antes de la sesión y tener preparado un "
    "instrumento de registro (rúbrica oral, escala de observación, lista de cotejo). Si el intercambio es grupal, "
    "es difícil observar a todos a la vez; puede alternarse el foco de atención o grabarse para revisión posterior "
    "(con los permisos correspondientes).\n\n"
    "Permiten valorar comprensión profunda, argumentación, capacidad de síntesis, fluidez y expresión oral, "
    "aspectos que una prueba escrita no captura. También permiten al docente hacer preguntas de seguimiento para "
    "explorar el razonamiento subyacente."
),
"Autoevaluación": (
    "La autoevaluación es el proceso por el que el propio alumnado valora su aprendizaje, su proceso de trabajo "
    "o el resultado que ha producido, usando criterios previamente establecidos y comprendidos.\n\n"
    "Cómo aplicarla: no es pedir una opinión libre ('¿te ha gustado?'), sino proporcionar una escala, rúbrica "
    "o lista de indicadores concretos y pedir al alumnado que los aplique honestamente a su propio desempeño. "
    "Conviene que previamente hayan visto ejemplos de aplicación de esos criterios y hayan discutido qué significa "
    "cada nivel.\n\n"
    "Su valor principal es metacognitivo: obliga al alumnado a reflexionar sobre lo que saben, lo que les cuesta "
    "y cómo pueden mejorar. Cuando se combina con la valoración del docente, permite identificar discrepancias y "
    "trabajar la autorregulación."
),
"Coevaluación": (
    "La coevaluación es la valoración que hace el alumnado del trabajo o desempeño de sus compañeros, usando "
    "criterios compartidos. Es una forma de evaluación entre iguales que, bien diseñada, mejora la comprensión "
    "de los criterios y desarrolla el pensamiento crítico.\n\n"
    "Cómo aplicarla: los criterios deben ser claros, concretos y haber sido trabajados antes. Es recomendable "
    "empezar con tareas donde valorar el trabajo ajeno sea relativamente sencillo (p. ej., comprobar si un "
    "esquema incluye los elementos requeridos) antes de pasar a valoraciones más complejas. Para reducir el sesgo "
    "de amistad, puede hacerse de forma anónima o cruzada.\n\n"
    "Su función principal es formativa: los comentarios de los compañeros, combinados con criterios claros, "
    "ayudan a mejorar el trabajo antes de la entrega final. Solo debe contribuir a la calificación cuando el "
    "alumnado tenga suficiente práctica y confianza en el proceso."
),
"Heteroevaluación": (
    "La heteroevaluación es la valoración realizada por el docente u otro agente externo al alumno (un experto, "
    "un familiar, otro docente). Es la forma más habitual de evaluación en el sistema escolar.\n\n"
    "Cómo aplicarla: para que sea justa y transparente, debe basarse en criterios explícitos, conocidos por el "
    "alumnado de antemano. El uso de rúbricas, guías de corrección o escalas descriptivas reduce la subjetividad "
    "y facilita la coherencia entre distintas correcciones. La retroalimentación que acompaña a la valoración es "
    "tan importante como la nota.\n\n"
    "No debe ser la única forma de evaluación: combinarla con autoevaluación y coevaluación ofrece una imagen "
    "más completa del aprendizaje y favorece la autonomía y la responsabilidad del alumnado."
),
"Evaluación diagnóstica": (
    "La evaluación diagnóstica recoge información sobre el punto de partida del alumnado antes de iniciar una "
    "unidad, proyecto o situación de aprendizaje. Su objetivo es detectar conocimientos previos, concepciones "
    "erróneas, intereses y necesidades, para ajustar la planificación.\n\n"
    "Cómo aplicarla: puede realizarse mediante preguntas abiertas, KPSI (lo sé / creo que lo sé / no lo sé), "
    "lluvia de ideas, mapa conceptual inicial, cuestionario breve o una tarea exploratoria. Lo importante es que "
    "sea rápida, no penalizadora y que los resultados influyan realmente en cómo se enseña a continuación.\n\n"
    "Una buena evaluación diagnóstica permite al docente partir de donde está el alumnado, no de donde debería "
    "estar según el currículo, y diseñar las actividades con mayor precisión."
),
"Evaluación formativa": (
    "La evaluación formativa es aquella cuya función principal es mejorar el aprendizaje mientras está en curso, "
    "no calificar al final. No es un tipo de instrumento, sino una función que puede cumplir cualquier actividad "
    "de evaluación si la información que genera se usa para ajustar la enseñanza o el aprendizaje.\n\n"
    "Cómo aplicarla: implica tres pasos: recoger evidencias (observación, preguntas, revisión de borradores, "
    "tickets de salida), analizarlas para identificar dónde está cada alumno respecto a los criterios, y devolver "
    "retroalimentación útil y a tiempo para que el alumnado pueda actuar sobre ella. La clave es que la "
    "retroalimentación llegue cuando todavía hay margen para mejorar.\n\n"
    "La evaluación formativa requiere tiempo y planificación, pero es la que más impacto tiene sobre el "
    "aprendizaje según la investigación educativa."
),
"Evaluación sumativa": (
    "La evaluación sumativa valora el grado de logro alcanzado al final de un periodo de aprendizaje (unidad, "
    "trimestre, proyecto, curso). Su función es acreditar, certificar o sintetizar lo aprendido y suele traducirse "
    "en una calificación.\n\n"
    "Cómo aplicarla: debe basarse en evidencias variadas recogidas durante el proceso, no solo en una prueba "
    "final. Idealmente, la calificación final integra información de distintos momentos y formatos (producciones, "
    "actuaciones, pruebas, autoevaluación). El uso de criterios explícitos y conocidos de antemano hace la "
    "calificación más justa y comprensible para el alumnado.\n\n"
    "Cuando se combina con evaluación formativa a lo largo del proceso, la nota final refleja mejor el aprendizaje "
    "real y reduce el peso desproporcionado de una sola prueba."
),
"Evaluación competencial": (
    "La evaluación competencial valora la capacidad del alumnado de movilizar de forma integrada conocimientos, "
    "habilidades y actitudes ante situaciones significativas y contextualizadas. No se limita a comprobar si se "
    "sabe un contenido aislado, sino si se sabe aplicar en un contexto real o verosímil.\n\n"
    "Cómo aplicarla: requiere diseñar tareas auténticas que se parezcan a situaciones del mundo real o de la "
    "disciplina. Los criterios de evaluación deben estar vinculados a las competencias clave y a los descriptores "
    "operativos del nivel educativo. Las rúbricas competenciales y los perfiles de logro son herramientas "
    "especialmente adecuadas.\n\n"
    "La evaluación competencial implica evaluar de forma integrada varios saberes y competencias a la vez, lo que "
    "supone un reto de diseño pero ofrece una imagen más fiel de lo que el alumnado es capaz de hacer."
),
"Evaluación mediante desempeño": (
    "La evaluación mediante desempeño valora cómo actúa el alumnado ante una tarea compleja o práctica: qué "
    "decisiones toma, cómo organiza el proceso, qué procedimientos aplica y cómo gestiona las dificultades. "
    "La evidencia es la actuación observable, no solo el resultado.\n\n"
    "Cómo aplicarla: el docente observa mientras el alumnado realiza la tarea (laboratorio, taller, simulación, "
    "debate, exposición) y registra lo que ve con una rúbrica de desempeño, escala de observación o lista de "
    "cotejo. Es fundamental que los criterios sean conocidos con antelación para que el alumnado sepa qué se "
    "espera de su actuación.\n\n"
    "Es especialmente útil en ciencias experimentales, educación física, artes, FP y cualquier área donde el "
    "procedimiento y la actitud son tan importantes como el resultado final."
),
"Evaluación mediante proyectos": (
    "La evaluación mediante proyectos valora de forma integral el proceso y el producto de un proyecto: "
    "planificación, investigación, creación, comunicación de resultados y reflexión sobre lo aprendido.\n\n"
    "Cómo aplicarla: conviene definir desde el inicio qué se va a evaluar en el proceso (planificación, "
    "organización, revisiones) y qué en el producto final (calidad, coherencia, presentación). Herramientas "
    "diferenciadas para proceso y producto permiten una valoración más justa. Las entregas parciales y las "
    "bitácoras de proyecto ayudan a que el seguimiento sea continuo y no dependa solo de la entrega final.\n\n"
    "Permite evaluar de forma integrada múltiples competencias y criterios a la vez, incluyendo trabajo en equipo, "
    "creatividad, investigación y comunicación."
),
"Evaluación mediante indagación": (
    "La evaluación mediante indagación valora los procesos de pensamiento científico: formulación de preguntas, "
    "planteamiento de hipótesis, diseño de procedimientos, recogida y análisis de datos, y elaboración de "
    "conclusiones basadas en evidencias.\n\n"
    "Cómo aplicarla: se evalúa no solo el resultado (si la hipótesis era correcta o incorrecta), sino la calidad "
    "del razonamiento en cada fase del proceso. Herramientas como la rúbrica de indagación o las listas de cotejo "
    "de proceso permiten valorar cada paso de forma independiente. Los informes de investigación y las bitácoras "
    "son los instrumentos más habituales.\n\n"
    "Es especialmente adecuada en ciencias naturales, ciencias sociales y proyectos de investigación, donde el "
    "proceso de construcción del conocimiento es tan importante como el resultado."
),
"Evaluación mediante resolución de problemas": (
    "La evaluación mediante resolución de problemas valora el proceso completo: comprensión del enunciado, "
    "identificación de datos relevantes, planificación de la estrategia, ejecución y verificación del resultado. "
    "No basta con que el resultado sea correcto; importa el razonamiento y la justificación.\n\n"
    "Cómo aplicarla: los problemas deben ser contextualizados y requerir aplicación real de conocimientos, no "
    "solo reproducción de fórmulas o algoritmos. La guía de corrección o la rúbrica deben valorar cada fase del "
    "proceso, no solo la respuesta final. Pedir al alumnado que explique cómo lo ha resuelto (por escrito u "
    "oralmente) añade información valiosa sobre su razonamiento.\n\n"
    "Adecuada en matemáticas, física, química, tecnología, economía y cualquier área con problemas aplicados."
),
"Evaluación mediante estudio de casos": (
    "El estudio de casos presenta al alumnado una situación real o verosímil que debe analizar, diagnosticar o "
    "sobre la que debe tomar decisiones y justificarlas. Permite evaluar comprensión aplicada, juicio crítico y "
    "capacidad de argumentación.\n\n"
    "Cómo aplicarlo: el caso debe ser auténtico, suficientemente complejo y contextualizado en el ámbito de la "
    "materia. El alumnado recibe la situación y debe responder preguntas o elaborar un análisis estructurado. "
    "La rúbrica o guía de análisis debe valorar la calidad del razonamiento, la selección de información "
    "relevante y la coherencia de las conclusiones.\n\n"
    "Especialmente útil en ciencias sociales, salud, derecho, economía, historia y cualquier área donde la "
    "aplicación al mundo real es central."
),
"Evaluación mediante simulación": (
    "La evaluación mediante simulación recrea situaciones verosímiles (juego de rol, simulacro, dramatización, "
    "casos prácticos interactivos) para observar cómo actúa el alumnado en ese contexto. Permite valorar "
    "habilidades difíciles de observar en situaciones ordinarias.\n\n"
    "Cómo aplicarla: se diseña un escenario con roles, información y objetivos definidos. El docente observa "
    "con una rúbrica de desempeño o registro anecdótico mientras la simulación se desarrolla. Es importante "
    "hacer un cierre reflexivo donde el alumnado analice sus propias decisiones y las comparta con el grupo.\n\n"
    "Adecuada para evaluar comunicación, toma de decisiones, resolución de conflictos, protocolos de actuación "
    "y habilidades sociales en contextos profesionales o cívicos."
),
"Evaluación mediante evidencias digitales": (
    "La evaluación mediante evidencias digitales recoge y valora producciones, participaciones y registros "
    "generados en entornos digitales: documentos colaborativos, foros, portfolios digitales, vídeos, "
    "historiales de revisión, analíticas de plataforma o contribuciones en wikis.\n\n"
    "Cómo aplicarla: conviene definir qué tipo de evidencias digitales se van a valorar y con qué criterios. "
    "El historial de revisión de un documento compartido, por ejemplo, permite ver la contribución individual "
    "en un trabajo grupal. Las analíticas de una plataforma LMS pueden mostrar tiempos de acceso, intentos y "
    "patrones de estudio, pero no deben usarse como única fuente de valoración.\n\n"
    "Las evidencias digitales permiten evaluar la competencia digital de forma auténtica y dan acceso a procesos "
    "que en papel serían invisibles. Las analíticas complementan el juicio pedagógico, pero no lo sustituyen."
),
}

# ─── HERRAMIENTAS ─────────────────────────────────────────────────────────────
herramientas_desc = {
"Rúbrica analítica": (
    "La rúbrica analítica es una matriz que desglosa la tarea en criterios separados y describe los niveles de "
    "desempeño para cada uno. Cada criterio se valora de forma independiente, lo que permite dar una "
    "retroalimentación precisa sobre qué aspectos están bien y cuáles necesitan mejora.\n\n"
    "Cómo usarla: se diseña una tabla donde las filas son los criterios (p. ej., 'estructura', 'argumentación', "
    "'corrección lingüística') y las columnas son los niveles (p. ej., 'excelente', 'satisfactorio', 'en proceso', "
    "'inicial'). Cada celda contiene un descriptor que explica cómo es el desempeño en ese nivel para ese criterio. "
    "Al evaluar, el docente lee cada fila y marca el nivel que mejor describe lo observado.\n\n"
    "Es la herramienta más adecuada para tareas complejas donde importa dar retroalimentación detallada. "
    "Requiere tiempo de diseño, pero una vez creada puede reutilizarse y compartirse con el alumnado como guía."
),
"Rúbrica global u holística": (
    "La rúbrica holística valora el desempeño de forma global, ofreciendo una descripción de cada nivel que "
    "abarca el conjunto de la tarea sin separar criterios individuales. El evaluador elige el nivel que mejor "
    "describe el trabajo en su totalidad.\n\n"
    "Cómo usarla: se redactan 3-5 descripciones globales ordenadas de mayor a menor calidad. Al evaluar, se "
    "lee el trabajo completo y se selecciona la descripción que mejor encaja. Es más rápida que la rúbrica "
    "analítica, pero ofrece menos información diagnóstica.\n\n"
    "Adecuada cuando el tiempo es limitado, cuando la tarea es corta o cuando se quiere dar una valoración "
    "general rápida. Para trabajos donde la retroalimentación detallada es prioritaria, la rúbrica analítica "
    "es más apropiada."
),
"Rúbrica de proceso": (
    "La rúbrica de proceso centra la evaluación en cómo se desarrolla la tarea: planificación, organización, "
    "revisiones, gestión del tiempo, toma de decisiones y uso de recursos. No valora el producto final, sino "
    "el camino recorrido para llegar a él.\n\n"
    "Cómo usarla: los criterios incluyen aspectos como 'define objetivos claros al inicio', 'registra los "
    "avances y dificultades', 'revisa y ajusta el plan cuando es necesario' o 'gestiona bien el tiempo del "
    "grupo'. Se aplica durante el desarrollo del proyecto, no al final.\n\n"
    "Es fundamental en proyectos de larga duración, investigaciones y portfolios, donde el proceso de "
    "aprendizaje es tan valioso como el resultado. Permite identificar dificultades a tiempo y ofrecer "
    "retroalimentación mientras todavía hay margen para actuar."
),
"Rúbrica de producto": (
    "La rúbrica de producto evalúa las características del artefacto final entregado: calidad, estructura, "
    "contenido, presentación, coherencia y adecuación a los requisitos. A diferencia de la rúbrica de proceso, "
    "no tiene en cuenta cómo se llegó al resultado.\n\n"
    "Cómo usarla: los criterios se centran en el producto en sí: 'la información es precisa y relevante', "
    "'la estructura es clara y coherente', 'el formato es adecuado al destinatario'. Cada criterio tiene "
    "niveles descritos que permiten ubicar el trabajo.\n\n"
    "Se complementa con la rúbrica de proceso en proyectos extensos. Usada sola, puede llevar a valorar "
    "solo el resultado y no el aprendizaje."
),
"Rúbrica oral": (
    "La rúbrica oral es una rúbrica analítica diseñada específicamente para valorar actuaciones orales: "
    "exposiciones, debates, defensas de proyecto, presentaciones, entrevistas o coloquios.\n\n"
    "Cómo usarla: los criterios habituales incluyen 'claridad y organización del discurso', 'uso de vocabulario "
    "específico', 'contacto visual y postura', 'respuesta a preguntas' y 'adecuación al tiempo'. Durante la "
    "actuación, el evaluador marca el nivel de cada criterio mientras observa. Si hay muchos alumnos, puede "
    "grabarse la actuación para revisar después (con los permisos necesarios).\n\n"
    "Compartirla antes de la actuación permite al alumnado prepararse con mayor orientación y reduce la "
    "ansiedad al saber exactamente qué se va a valorar."
),
"Rúbrica de trabajo cooperativo": (
    "La rúbrica de trabajo cooperativo evalúa la calidad de la colaboración dentro del grupo: participación "
    "equitativa, comunicación, responsabilidad individual, resolución de conflictos y contribución al objetivo "
    "común.\n\n"
    "Cómo usarla: puede aplicarla el docente mediante observación, el propio alumno mediante autoevaluación, "
    "o los compañeros mediante coevaluación (o las tres a la vez). Los criterios deben distinguir entre "
    "comportamientos observables ('participa activamente en las discusiones', 'cumple con las tareas "
    "asignadas') y resultados del grupo.\n\n"
    "Es especialmente útil para evitar que el trabajo grupal diluya la responsabilidad individual y para dar "
    "retroalimentación sobre las habilidades sociales y de colaboración."
),
"Rúbrica competencial": (
    "La rúbrica competencial está diseñada para valorar el grado de desarrollo de una competencia específica "
    "(comunicativa, matemática, digital, científica, etc.) a través de una tarea contextualizada. Sus criterios "
    "están alineados con los descriptores operativos del nivel educativo.\n\n"
    "Cómo usarla: los criterios reflejan los elementos clave de la competencia (p. ej., para la competencia "
    "comunicativa: 'comprende textos complejos', 'produce textos adecuados al contexto', 'argumenta con "
    "evidencias'). Cada criterio tiene 3-4 niveles descritos. Puede usarse para valorar una sola tarea o "
    "como perfil acumulado a lo largo del curso.\n\n"
    "Es la herramienta más adecuada para la evaluación por competencias que exige el marco curricular actual."
),
"Lista de cotejo o control": (
    "La lista de cotejo es una herramienta de verificación que enumera los elementos, pasos o comportamientos "
    "que deben estar presentes en una tarea o actuación. Para cada ítem, el evaluador marca simplemente si "
    "está presente (sí/no) o si se ha cumplido.\n\n"
    "Cómo usarla: se elabora una lista de indicadores concretos y observables (p. ej., 'incluye introducción', "
    "'cita las fuentes', 'usa el material de seguridad'). Durante o después de la actividad, se marca cada "
    "ítem. No hay niveles intermedios; es una verificación binaria.\n\n"
    "Es rápida de aplicar y muy útil para actividades con requisitos claros y cerrados: protocolos de "
    "laboratorio, presentaciones con requisitos definidos, procedimientos técnicos. Para tareas con matices "
    "cualitativos, es preferible una rúbrica o escala."
),
"Escala de observación": (
    "La escala de observación permite registrar el grado en que se manifiesta un comportamiento, actitud o "
    "habilidad durante una actividad. A diferencia de la lista de cotejo (sí/no), ofrece varios puntos en "
    "la escala (p. ej., siempre / casi siempre / a veces / raramente / nunca).\n\n"
    "Cómo usarla: se definen los indicadores que se van a observar y se elige una escala de frecuencia o "
    "calidad. Durante la actividad, el docente marca el nivel observado para cada alumno. Puede diseñarse para "
    "observar a varios alumnos a la vez si los indicadores son pocos y concretos.\n\n"
    "Útil para evaluar participación, actitudes, procedimientos y habilidades sociales en actividades grupales, "
    "debates, prácticas y talleres."
),
"Escala de valoración": (
    "La escala de valoración asigna un valor numérico o cualitativo a cada criterio evaluado, sin llegar a "
    "describir qué significa cada nivel con la precisión de una rúbrica. Es un punto intermedio entre la lista "
    "de cotejo y la rúbrica analítica.\n\n"
    "Cómo usarla: se listan los criterios y junto a cada uno se coloca una escala (p. ej., 1-4 o "
    "insuficiente/suficiente/bien/excelente). El evaluador asigna un valor a cada criterio según su juicio. "
    "Es más rápida que una rúbrica porque no requiere descriptores detallados para cada celda.\n\n"
    "Adecuada cuando el docente tiene suficiente experiencia para aplicar criterios implícitamente, pero puede "
    "ser menos fiable y menos informativa para el alumnado que una rúbrica con descriptores."
),
"Escala descriptiva": (
    "La escala descriptiva es una variante de la escala de valoración en la que cada punto de la escala va "
    "acompañado de una descripción verbal que explica qué caracteriza ese nivel. Es más precisa que la escala "
    "numérica pero menos detallada que la rúbrica analítica.\n\n"
    "Cómo usarla: para cada criterio se redactan 3-4 descripciones ordenadas de mayor a menor calidad. Al "
    "evaluar, se lee la descripción que mejor corresponde al trabajo observado. Puede combinarse con una "
    "puntuación numérica asociada a cada nivel.\n\n"
    "Es un buen punto de partida para docentes que quieren introducir criterios más explícitos sin invertir "
    "el tiempo que requiere diseñar una rúbrica analítica completa."
),
"Guía de corrección": (
    "La guía de corrección especifica qué se debe encontrar en una respuesta correcta o de calidad: qué "
    "conceptos, qué argumentos, qué pasos, qué elementos. Orientala corrección de pruebas escritas, orales "
    "o prácticas.\n\n"
    "Cómo usarla: antes de corregir, el docente elabora una guía que lista los puntos esperados en cada "
    "pregunta o tarea, con indicación de cuántos puntos vale cada uno. Al corregir, compara la respuesta del "
    "alumno con la guía y asigna la puntuación correspondiente. Puede incluir ejemplos de respuestas "
    "aceptables o de errores frecuentes.\n\n"
    "Aumenta la consistencia de la corrección entre distintas correcciones del mismo docente o entre "
    "diferentes docentes que corrigen el mismo examen."
),
"Plantilla de corrección": (
    "La plantilla de corrección es un documento estructurado que organiza la tarea de corrección: lista "
    "las preguntas o tareas, indica la puntuación máxima de cada una y proporciona espacio para anotar la "
    "puntuación obtenida y observaciones.\n\n"
    "Cómo usarla: se prepara antes de la corrección y se usa como hoja de registro durante el proceso. "
    "Puede incluir respuestas modelo, criterios generales y notas sobre errores típicos detectados durante "
    "la corrección.\n\n"
    "Es especialmente útil cuando hay muchas pruebas que corregir o cuando varios docentes corrigen el mismo "
    "instrumento, ya que garantiza uniformidad y agiliza el proceso."
),
"Baremo": (
    "El baremo es un sistema de puntuación que establece cuánto vale cada parte de una prueba, tarea o "
    "conjunto de criterios, y cómo se traducen las puntuaciones parciales en una nota global.\n\n"
    "Cómo usarlo: se define la puntuación máxima de cada pregunta, ejercicio o criterio, y se indica la "
    "fórmula de cálculo de la nota final (suma directa, ponderación, redondeo). Si hay penalización por "
    "error, debe especificarse claramente. El baremo debe hacerse público antes de la prueba para que el "
    "alumnado sepa qué peso tiene cada parte.\n\n"
    "Un baremo bien diseñado refleja la importancia relativa de cada contenido o competencia evaluada y "
    "facilita la calificación objetiva."
),
"Registro anecdótico": (
    "El registro anecdótico es un documento donde el docente anota, de forma breve y fechada, hechos "
    "significativos observados en el alumnado: un progreso notable, una dificultad persistente, una "
    "conducta destacable, una intervención relevante.\n\n"
    "Cómo usarlo: puede ser una libreta, una ficha por alumno, una aplicación o una hoja dividida por "
    "alumnos. Lo importante es registrar el hecho tal como se observó (sin interpretarlo todavía) y "
    "añadir la fecha. Con el tiempo, la acumulación de anécdotas permite ver patrones de aprendizaje o "
    "comportamiento que de otro modo pasarían desapercibidos.\n\n"
    "Es especialmente útil en etapas sin calificación numérica, para completar boletines descriptivos, "
    "orientar tutorías y fundamentar la evaluación formativa continua."
),
"Registro descriptivo": (
    "El registro descriptivo es una herramienta narrativa en la que el docente describe con cierto detalle "
    "el desempeño de un alumno o grupo durante una actividad o periodo, sin reducirlo a una puntuación.\n\n"
    "Cómo usarlo: se redacta una descripción cualitativa que explica qué hizo el alumno, cómo lo hizo y "
    "qué evidencias se observaron. Puede estructurarse por criterios o por momentos de la actividad. "
    "Es más elaborado que el registro anecdótico y más apropiado para informes periódicos.\n\n"
    "Permite comunicar a las familias y al propio alumno una imagen rica y matizada del aprendizaje, más "
    "allá de lo que puede transmitir una nota numérica."
),
"Diario del profesor": (
    "El diario del profesor es un cuaderno o documento digital donde el docente registra sus reflexiones "
    "sobre el desarrollo de las clases: qué funcionó, qué no, qué aprendió el alumnado, qué dificultades "
    "surgieron y qué cambiaría la próxima vez.\n\n"
    "Cómo usarlo: conviene escribir en él con regularidad (al final de cada sesión o semana) y de forma "
    "reflexiva, no solo descriptiva. Preguntas como '¿qué evidencias de aprendizaje observé hoy?', "
    "'¿qué alumnos me preocupan y por qué?' o '¿qué ajustaría?' orientan la reflexión.\n\n"
    "No es solo un registro de lo que ocurrió, sino una herramienta de mejora de la práctica docente. "
    "Con el tiempo, se convierte en una fuente valiosa de información para ajustar la planificación."
),
"Hoja de seguimiento individual": (
    "La hoja de seguimiento individual recoge, para cada alumno, información acumulada sobre su evolución "
    "a lo largo de un periodo: tareas entregadas, resultados, observaciones, asistencia a tutorías, "
    "compromisos de mejora.\n\n"
    "Cómo usarla: se diseña una ficha por alumno con los criterios o indicadores que se quieren monitorizar. "
    "El docente la actualiza periódicamente con información de distintas fuentes. Al final del periodo, "
    "ofrece una visión longitudinal del progreso.\n\n"
    "Es especialmente útil para el seguimiento personalizado en grupos con necesidades diversas, para "
    "preparar tutorías individuales y para fundamentar las decisiones de promoción."
),
"Hoja de seguimiento grupal": (
    "La hoja de seguimiento grupal es una versión colectiva de la hoja de seguimiento individual: recoge "
    "en una misma tabla información de todos los alumnos del grupo, lo que permite comparar y detectar "
    "tendencias generales.\n\n"
    "Cómo usarla: cada fila es un alumno y cada columna es un criterio, tarea o momento de observación. "
    "El docente la actualiza periódicamente. Una ojeada al conjunto permite identificar qué alumnos "
    "necesitan más atención, qué criterios el grupo en general no ha alcanzado y qué aspectos han mejorado.\n\n"
    "Es una herramienta de gestión de aula muy útil para docentes con varios grupos, ya que permite "
    "mantener una visión global del estado del aprendizaje."
),
"Registro de participación": (
    "El registro de participación documenta las intervenciones del alumnado durante las sesiones: quién "
    "participa, con qué frecuencia, qué calidad tienen las aportaciones y si cumple con los turnos y "
    "normas de participación.\n\n"
    "Cómo usarlo: puede ser tan sencillo como un listado de alumnos donde se marca cada intervención, "
    "o tan elaborado como una escala de observación que valora la calidad de las aportaciones. Lo "
    "importante es que sea manejable durante la clase y no distraiga al docente de su función principal.\n\n"
    "Permite dar retroalimentación objetiva sobre la participación, detectar quién nunca interviene y "
    "fundamentar este apartado si forma parte de la calificación."
),
"Registro de trabajo cooperativo": (
    "El registro de trabajo cooperativo documenta el funcionamiento del grupo durante actividades "
    "colaborativas: distribución de roles, cumplimiento de tareas individuales, calidad de la comunicación "
    "y resolución de conflictos.\n\n"
    "Cómo usarlo: puede combinarse con observación directa del docente, autoevaluación del grupo y "
    "coevaluación entre los miembros. Registrar qué ocurre en cada grupo durante la sesión permite "
    "intervenir a tiempo si algún grupo tiene dificultades de funcionamiento.\n\n"
    "Es especialmente útil en proyectos y actividades grupales extensas, donde el funcionamiento del "
    "equipo tiene tanto peso como el resultado final."
),
"Notas de campo": (
    "Las notas de campo son anotaciones breves, rápidas e informales que el docente toma durante la "
    "clase para no perder evidencias de aprendizaje que de otro modo se olvidarían. Son el material "
    "en bruto que luego puede elaborarse en registros más formales.\n\n"
    "Cómo usarlas: pueden tomarse en papel, en el móvil o en una tableta. Lo importante es que sean "
    "inmediatas, concretas y fechadas. No es necesario que sean completas o formales; se trata de "
    "capturar lo esencial para poder recuperarlo después.\n\n"
    "Son la base de la observación incidental y del registro anecdótico. Con el tiempo, las notas de "
    "campo acumuladas permiten ver el progreso de cada alumno con más precisión que la memoria del docente."
),
"Ficha de valoración": (
    "La ficha de valoración es un documento estructurado que recoge la valoración de un alumno o trabajo "
    "según criterios predefinidos, con espacio para puntuaciones, niveles y comentarios cualitativos.\n\n"
    "Cómo usarla: se diseña con los criterios relevantes para la tarea, la escala de valoración y "
    "espacio para observaciones. Puede entregarse al alumno tras la corrección como documento de "
    "retroalimentación. Si se usa en todas las entregas, el alumno puede ver su evolución a lo largo "
    "del curso.\n\n"
    "Es más flexible que una rúbrica fija y más informativa que una nota sola. Adecuada para valoraciones "
    "periódicas de trabajos individuales."
),
"Ficha de retroalimentación": (
    "La ficha de retroalimentación es un documento diseñado específicamente para comunicar al alumno qué "
    "ha hecho bien, qué puede mejorar y cómo hacerlo. Va más allá de la puntuación y se centra en "
    "información accionable.\n\n"
    "Cómo usarla: una estructura habitual incluye: '¿Qué has hecho bien?', '¿Qué puedes mejorar?' y "
    "'¿Cómo puedes mejorarlo?'. También puede usarse el formato 'dos estrellas y un deseo' o una "
    "tabla con fortalezas y áreas de mejora. Se entrega junto con o en lugar de la nota, especialmente "
    "en evaluación formativa.\n\n"
    "La retroalimentación es más efectiva cuando es específica, oportuna y orientada a la mejora. "
    "Una ficha bien diseñada ayuda al docente a ser sistemático en este proceso."
),
"Matriz de valoración": (
    "La matriz de valoración es una tabla que cruza criterios de evaluación con niveles de logro, similar "
    "a una rúbrica, pero a menudo más sintética. Puede incluir descriptores cualitativos, puntuaciones "
    "o ambos.\n\n"
    "Cómo usarla: se diseña con los criterios en filas y los niveles en columnas. Cada celda puede "
    "contener una descripción, una puntuación o ambas. Al evaluar, se marca la celda que corresponde "
    "al nivel observado en cada criterio.\n\n"
    "Es un término genérico que engloba las rúbricas analíticas. La diferencia principal respecto a "
    "la rúbrica es que la matriz puede ser más esquemática y no siempre incluye descriptores completos "
    "en cada celda."
),
"Banco de descriptores": (
    "El banco de descriptores es una colección de frases descriptivas listas para usar en la construcción "
    "de rúbricas, informes y fichas de retroalimentación. Evita tener que redactar descriptores desde "
    "cero cada vez.\n\n"
    "Cómo usarlo: se organiza por criterios, competencias o áreas, con descriptores para distintos niveles "
    "de desempeño. Al diseñar una rúbrica, el docente selecciona y adapta los descriptores del banco "
    "en lugar de redactarlos desde cero.\n\n"
    "Es una herramienta de eficiencia que reduce el tiempo de diseño de instrumentos de evaluación y "
    "favorece la coherencia terminológica entre distintas asignaturas o docentes del mismo departamento."
),
"Perfil de logro": (
    "El perfil de logro describe, para cada competencia o criterio de evaluación, qué sabe hacer el "
    "alumno en un momento dado y en qué nivel se encuentra. Es una fotografía del estado actual del "
    "aprendizaje.\n\n"
    "Cómo usarlo: se elabora a partir de la información recogida con distintos instrumentos a lo largo "
    "del proceso. Puede presentarse como una tabla, un radar o un texto descriptivo. Sirve para informar "
    "a familias y alumnos, orientar tutorías y planificar apoyos.\n\n"
    "En el marco de la evaluación por competencias (LOMLOE), el perfil de logro es la referencia para "
    "la calificación de cada competencia específica."
),
"Diana de evaluación": (
    "La diana de evaluación es una representación gráfica circular dividida en sectores, cada uno "
    "correspondiente a un criterio. El alumnado (o el docente) pinta cada sector desde el centro hasta "
    "el nivel que considera alcanzado, creando una imagen visual del perfil de desempeño.\n\n"
    "Cómo usarla: se imprime o dibuja una diana con tantos sectores como criterios se quieran valorar. "
    "Cada sector está dividido en 3-5 anillos concéntricos que representan los niveles. Se colorea cada "
    "sector hasta el nivel alcanzado. El resultado es un gráfico fácilmente interpretable de un vistazo.\n\n"
    "Es especialmente útil para la autoevaluación, la coevaluación y la comunicación visual del progreso. "
    "Su formato gráfico la hace muy accesible para el alumnado de cualquier edad."
),
"Semáforo de evaluación": (
    "El semáforo de evaluación usa los colores rojo, amarillo y verde para indicar el nivel de logro de "
    "cada criterio o tarea: verde (logrado), amarillo (en proceso) y rojo (no logrado o inicial).\n\n"
    "Cómo usarlo: se aplica a una lista de criterios, tareas o indicadores. El docente o el propio "
    "alumno asigna un color a cada ítem según el nivel alcanzado. Es inmediatamente legible y muy "
    "visual, lo que facilita identificar de un vistazo dónde está cada alumno.\n\n"
    "Adecuado para el seguimiento formativo rápido, la comunicación a familias y la autoevaluación. "
    "Se complementa con retroalimentación escrita que explique qué hacer para pasar de rojo a verde."
),
"Escala de autoevaluación": (
    "La escala de autoevaluación es una herramienta que el propio alumno usa para valorar su desempeño, "
    "proceso o producto según criterios predefinidos. Puede ser numérica, de frecuencia o cualitativa.\n\n"
    "Cómo usarla: se proporciona al alumno una lista de indicadores y una escala para cada uno. El alumno "
    "la completa de forma individual y honesta. Para que sea efectiva, los criterios deben haber sido "
    "trabajados previamente y el alumno debe comprender qué significa cada nivel.\n\n"
    "Su valor es principalmente metacognitivo: obliga al alumno a reflexionar sobre su propio aprendizaje. "
    "Puede combinarse con la valoración del docente para identificar discrepancias y trabajarlas en tutoría."
),
"Rúbrica de autoevaluación": (
    "La rúbrica de autoevaluación es una rúbrica analítica que el propio alumno aplica a su trabajo o "
    "actuación. Tiene la misma estructura que cualquier rúbrica (criterios + niveles descritos), pero "
    "está redactada en primera persona o en un lenguaje accesible para el alumno.\n\n"
    "Cómo usarla: el alumno lee los descriptores de cada criterio y selecciona el nivel que mejor "
    "describe su propio desempeño. Conviene que también añada una evidencia o justificación de su "
    "elección. Comparar la autoevaluación con la del docente es una actividad de gran valor formativo.\n\n"
    "Es especialmente útil en portfolios, proyectos y tareas complejas donde el alumno puede revisar "
    "su propio trabajo con calma."
),
"Rúbrica de coevaluación": (
    "La rúbrica de coevaluación es una rúbrica analítica que los alumnos aplican al trabajo o actuación "
    "de sus compañeros. Permite estructurar la revisión entre pares con criterios claros y niveles "
    "descritos.\n\n"
    "Cómo usarla: cada alumno recibe la rúbrica y la aplica al trabajo de un compañero (asignado de "
    "forma aleatoria o rotatoria). Puede hacerse de forma anónima para reducir el sesgo. Los comentarios "
    "cualitativos son tan importantes como la puntuación asignada.\n\n"
    "Para que sea efectiva, los alumnos deben haber practicado aplicar los criterios antes de usarla "
    "en la coevaluación. El docente debe revisar los resultados y usarlos como punto de partida para "
    "la discusión."
),
"Ficha de coevaluación": (
    "La ficha de coevaluación es una versión simplificada de la rúbrica de coevaluación: suele incluir "
    "menos criterios, preguntas más directas y espacio para comentarios libres. Está pensada para que "
    "el proceso de revisión entre pares sea más accesible y rápido.\n\n"
    "Cómo usarla: incluye preguntas como '¿Qué ha hecho bien tu compañero?', '¿Qué podría mejorar?' y "
    "'¿Qué puntuación le darías en este criterio y por qué?'. Se entrega al alumno evaluado junto con "
    "el trabajo devuelto.\n\n"
    "Es una buena introducción a la coevaluación para grupos que no tienen práctica en ella, ya que "
    "su formato es menos exigente que una rúbrica completa."
),
"Lista de cotejo de autoevaluación": (
    "La lista de cotejo de autoevaluación es una lista de verificación que el propio alumno completa "
    "para comprobar si su trabajo o actuación cumple con los requisitos definidos. Cada ítem se responde "
    "con sí/no o con una marca de verificación.\n\n"
    "Cómo usarla: antes de entregar un trabajo, el alumno revisa su lista para asegurarse de que ha "
    "incluido todos los elementos requeridos. Esto reduce los errores por olvido y desarrolla la "
    "responsabilidad sobre el propio trabajo.\n\n"
    "Es especialmente útil para tareas con requisitos claros y cerrados (formato de un informe, "
    "elementos de una presentación, pasos de un protocolo) y para etapas de revisión antes de la "
    "entrega final."
),
"Registro de compromisos de mejora": (
    "El registro de compromisos de mejora es un documento donde el alumno anota qué aspectos va a "
    "mejorar y cómo, tras recibir retroalimentación. Es el paso que convierte la evaluación formativa "
    "en acción.\n\n"
    "Cómo usarlo: tras la devolución de una tarea o una sesión de retroalimentación, el alumno escribe "
    "uno o varios compromisos concretos ('voy a revisar la conclusión porque no responde a la pregunta "
    "inicial', 'voy a citar las fuentes en el siguiente trabajo'). El docente revisa estos compromisos "
    "en la siguiente entrega.\n\n"
    "Cierra el ciclo de la evaluación formativa: recogida de evidencias → retroalimentación → acción "
    "de mejora. Sin este último paso, la retroalimentación tiene poco impacto real."
),
"Cuaderno de calificaciones": (
    "El cuaderno de calificaciones es el registro central donde el docente anota las calificaciones "
    "de cada alumno en cada tarea, prueba o criterio evaluado a lo largo del periodo.\n\n"
    "Cómo usarlo: puede ser físico (libreta) o digital (hoja de cálculo, plataforma educativa). "
    "Incluye el nombre de los alumnos, las tareas o criterios en columnas y las calificaciones en las "
    "celdas correspondientes. Una buena organización permite calcular la nota final de forma "
    "transparente y reproducible.\n\n"
    "Más allá de ser un registro administrativo, puede usarse para detectar tendencias (alumnos que "
    "mejoran o empeoran sistemáticamente) y para planificar apoyos personalizados."
),
"Tabla de calificación por criterios": (
    "La tabla de calificación por criterios organiza la calificación final desagregada por criterios "
    "de evaluación, en lugar de dar una única nota global. Cada criterio tiene su propio peso y "
    "calificación.\n\n"
    "Cómo usarla: se lista cada criterio de evaluación con su ponderación y la calificación obtenida. "
    "La nota final resulta de la suma ponderada. Este formato es el que exige la normativa vigente "
    "(LOMLOE) para la evaluación por criterios de evaluación y competencias específicas.\n\n"
    "Permite al alumnado y a las familias conocer exactamente en qué criterios está el alumno bien y "
    "en cuáles necesita mejorar, lo que hace la calificación mucho más informativa."
),
"Matriz de ponderación": (
    "La matriz de ponderación especifica qué peso relativo tiene cada criterio, competencia o tarea "
    "en la calificación final. Define las reglas del juego antes de que comience el proceso de evaluación.\n\n"
    "Cómo usarla: se elabora una tabla con todos los elementos evaluables y su porcentaje o peso "
    "correspondiente, verificando que la suma sea el 100%. Debe comunicarse al alumnado al inicio del "
    "periodo para que puedan organizar su esfuerzo de forma informada.\n\n"
    "Una buena matriz de ponderación refleja las prioridades pedagógicas: si el proceso es tan "
    "importante como el producto, ambos deben tener un peso significativo."
),
"Escala numérica": (
    "La escala numérica asigna una puntuación en una escala de números (p. ej., 1-10, 0-100, 1-4) a "
    "cada criterio o al trabajo en su conjunto. Es el sistema de calificación más extendido en el "
    "sistema educativo español.\n\n"
    "Cómo usarla: cada puntuación de la escala debe tener un significado claro (qué implica un 5 "
    "frente a un 7). Sin criterios explícitos, la escala numérica puede resultar subjetiva e "
    "inconsistente entre correcciones. Combinada con descriptores cualitativos, gana en fiabilidad.\n\n"
    "Su ventaja es la facilidad de comunicación y cálculo. Su limitación es que no informa sobre "
    "qué debe mejorar el alumno, por lo que debe acompañarse siempre de retroalimentación cualitativa."
),
"Escala verbal": (
    "La escala verbal sustituye los números por descriptores cualitativos: insuficiente, suficiente, "
    "bien, notable, excelente; o iniciado, en proceso, logrado, sobresaliente. Cada nivel describe "
    "un grado de logro.\n\n"
    "Cómo usarla: se asocia cada nivel verbal a una descripción de lo que implica y, si es necesario, "
    "a una puntuación numérica equivalente. Es la escala que emplea el currículo de muchas etapas "
    "educativas (p. ej., Primaria: 'insuficiente, suficiente, bien, notable, sobresaliente').\n\n"
    "Tiene la ventaja de ser más descriptiva que una nota numérica y comunicar mejor el nivel de "
    "logro. Es la base de los perfiles de logro competencial."
),
"Conversor de niveles a calificación": (
    "El conversor de niveles a calificación es una tabla o fórmula que traduce los niveles cualitativos "
    "de una rúbrica o escala descriptiva en una calificación numérica, facilitando el proceso de "
    "calificación cuando el currículo exige nota numérica.\n\n"
    "Cómo usarlo: se establece la equivalencia entre niveles y puntuaciones (p. ej., 'excelente = 9-10', "
    "'notable = 7-8', 'bien = 6', 'suficiente = 5', 'insuficiente = 1-4'). Si hay varios criterios "
    "ponderados, el conversor calcula la nota final a partir de los niveles asignados.\n\n"
    "Permite combinar una evaluación cualitativa y orientada al aprendizaje con la obligación normativa "
    "de emitir calificaciones numéricas."
),
"Hoja de cálculo de evaluación": (
    "La hoja de cálculo de evaluación (Excel, Google Sheets, etc.) es un registro digital que centraliza "
    "todas las calificaciones y permite calcular automáticamente medias, ponderaciones y notas finales.\n\n"
    "Cómo usarla: se organiza con alumnos en filas y tareas o criterios en columnas. Las fórmulas "
    "calculan automáticamente las medias ponderadas. Puede incluir gráficos de progreso, filtros por "
    "alumno o criterio y exportación a informes.\n\n"
    "Es la herramienta más eficiente para gestionar la calificación de grupos grandes. Con macros o "
    "complementos específicos, puede generar informes personalizados para cada alumno automáticamente."
),
"Informe individual de evaluación": (
    "El informe individual de evaluación es un documento que recoge, para un alumno concreto, "
    "información sobre su nivel de logro en los criterios o competencias evaluados, junto con "
    "observaciones sobre el proceso y recomendaciones de mejora.\n\n"
    "Cómo elaborarlo: integra información de distintas fuentes (calificaciones, observaciones, "
    "autoevaluación, entrevistas). Va más allá del boletín de notas: incluye contexto cualitativo "
    "que explica los resultados y orienta los siguientes pasos.\n\n"
    "Es el documento de comunicación más completo entre el centro y la familia. Su elaboración requiere "
    "tiempo, pero tiene un alto valor orientador para el alumno y sus familias."
),
"Acta de evaluación": (
    "El acta de evaluación es el documento oficial que recoge las calificaciones finales de todos los "
    "alumnos de un grupo al término de un periodo evaluativo (trimestre, curso). Tiene valor administrativo "
    "y legal.\n\n"
    "Cómo usarla: se cumplimenta en las sesiones de evaluación, recoge las calificaciones por "
    "materia o criterio y la decisión de promoción o titulación. Debe firmarse por todos los docentes "
    "del grupo y archivarse según la normativa del centro.\n\n"
    "Es el registro final del proceso evaluativo. Su cumplimentación correcta es una obligación "
    "administrativa, pero el proceso pedagógico que la sustenta es lo que le da sentido."
),
"Formulario digital": (
    "El formulario digital (Google Forms, Microsoft Forms, Typeform, etc.) permite recoger respuestas "
    "de forma estructurada y automática: cuestionarios de autoevaluación, encuestas de satisfacción, "
    "pruebas de respuesta cerrada, tickets de salida o registros de actividad.\n\n"
    "Cómo usarlo: se diseña el formulario con preguntas cerradas (selección múltiple, escala Likert, "
    "casillas) o abiertas. Las respuestas se centralizan automáticamente en una hoja de cálculo o "
    "panel de resultados. Puede configurarse para dar retroalimentación inmediata al alumno.\n\n"
    "Ahorra tiempo de corrección en evaluaciones cerradas, facilita el análisis de resultados del "
    "grupo y permite realizar diagnósticos rápidos al inicio de la clase."
),
"Rúbrica digital": (
    "La rúbrica digital es una rúbrica implementada en una plataforma o aplicación educativa (Google "
    "Classroom, Canvas, Moodle, Rubric Maker, etc.) que permite aplicarla directamente en el entorno "
    "digital, automatizar el cálculo de la puntuación y enviar la retroalimentación al alumno.\n\n"
    "Cómo usarla: se crea la rúbrica en la plataforma, asociándola a una tarea. Al corregir, el docente "
    "marca los niveles directamente en la plataforma y añade comentarios. La puntuación se calcula "
    "automáticamente y el alumno recibe la retroalimentación en su espacio personal.\n\n"
    "Reduce el tiempo de corrección, facilita la coherencia entre correcciones y permite al alumno "
    "acceder a su retroalimentación de forma inmediata y organizada."
),
"Historial de revisión": (
    "El historial de revisión es el registro automático de cambios que generan las aplicaciones de "
    "edición colaborativa (Google Docs, Word Online, etc.). Permite ver quién hizo qué cambios, cuándo "
    "y en qué orden a lo largo de todo el proceso de elaboración de un documento.\n\n"
    "Cómo usarlo: al abrir el historial de versiones de un documento compartido, el docente puede "
    "ver la contribución individual de cada miembro del grupo, detectar si el trabajo se hizo de "
    "forma sostenida o a última hora, e identificar quién aportó las ideas clave.\n\n"
    "Es una evidencia de proceso muy valiosa en trabajos grupales digitales, ya que hace visible "
    "lo que de otro modo sería invisible: quién trabajó, cuándo y cuánto."
),
"Panel de progreso": (
    "El panel de progreso es una representación visual del estado de avance de cada alumno en los "
    "objetivos, tareas o criterios del curso. Puede ser un tablero físico en el aula o un dashboard "
    "digital en la plataforma educativa.\n\n"
    "Cómo usarlo: se diseña con filas de alumnos y columnas de objetivos o tareas. El estado de cada "
    "celda (logrado, en proceso, pendiente) se actualiza periódicamente. Un panel bien diseñado permite "
    "al docente ver de un vistazo el estado del grupo y a cada alumno conocer su propio progreso.\n\n"
    "Favorece la transparencia, la autorregulación y la motivación. En versiones digitales, puede "
    "actualizarse automáticamente con los datos de la plataforma."
),
"Analíticas de aprendizaje": (
    "Las analíticas de aprendizaje son datos recogidos automáticamente por plataformas educativas "
    "(LMS, aplicaciones, juegos educativos) sobre el comportamiento y rendimiento del alumnado: "
    "tiempo de acceso, intentos, errores, patrones de navegación, puntuaciones.\n\n"
    "Cómo usarlas: la plataforma genera informes automáticos que el docente puede revisar para "
    "detectar quién no accede a los materiales, qué contenidos generan más errores o qué alumnos "
    "necesitan apoyo. No deben usarse como única fuente de valoración.\n\n"
    "Son especialmente útiles para identificar tendencias grupales e individuales de forma eficiente. "
    "El juicio pedagógico del docente es imprescindible para interpretar los datos y no reducir el "
    "aprendizaje a métricas."
),
"Banco digital de evidencias": (
    "El banco digital de evidencias es un repositorio organizado (carpeta en Drive, portfolio digital, "
    "plataforma específica) donde se almacenan las producciones y documentos de evaluación de cada "
    "alumno a lo largo del tiempo.\n\n"
    "Cómo usarlo: cada alumno tiene su propio espacio donde guarda sus trabajos, borradores, "
    "autoevaluaciones y retroalimentaciones recibidas. El docente puede acceder para revisar el "
    "progreso longitudinal. Al final del curso, el banco ofrece una imagen completa del recorrido "
    "de aprendizaje.\n\n"
    "Es la base del portfolio digital. Permite la evaluación continua, la reflexión sobre el "
    "progreso y la comunicación de evidencias a familias y otros docentes."
),
}

# ─── APLICAR A TÉCNICAS ───────────────────────────────────────────────────────
with open('/home/jjdeharo/Documentos/github/evaluacion/data/tecnicas.json', encoding='utf-8') as f:
    tecnicas = json.load(f)

for item in tecnicas:
    nombre = item['Técnica']
    if nombre in tecnicas_desc:
        item['Descripción detallada'] = tecnicas_desc[nombre]

with open('/home/jjdeharo/Documentos/github/evaluacion/data/tecnicas.json', 'w', encoding='utf-8') as f:
    json.dump(tecnicas, f, ensure_ascii=False, indent=2)
print(f"Técnicas actualizadas: {sum(1 for t in tecnicas if 'Descripción detallada' in t)}/{len(tecnicas)}")

# ─── APLICAR A HERRAMIENTAS ───────────────────────────────────────────────────
with open('/home/jjdeharo/Documentos/github/evaluacion/data/herramientas.json', encoding='utf-8') as f:
    herramientas = json.load(f)

for item in herramientas:
    nombre = item['Herramienta']
    if nombre in herramientas_desc:
        item['Descripción detallada'] = herramientas_desc[nombre]

with open('/home/jjdeharo/Documentos/github/evaluacion/data/herramientas.json', 'w', encoding='utf-8') as f:
    json.dump(herramientas, f, ensure_ascii=False, indent=2)
print(f"Herramientas actualizadas: {sum(1 for h in herramientas if 'Descripción detallada' in h)}/{len(herramientas)}")

print("Listo.")
