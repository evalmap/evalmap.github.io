// Generador de herramientas de evaluación
class ToolGenerator {
  constructor(data) {
    this.plantillas = data.plantillas || [];
  }

  generarRubricaAnalitica({ instrumento, criterios, niveles, materia, actividad }) {
    const nivelesBase = niveles && niveles.length > 0 ? niveles : ['Inicial', 'En proceso', 'Adecuado', 'Avanzado'];
    const criteriosBase = criterios && criterios.length > 0 ? criterios : this._inferirCriterios(instrumento, actividad);

    return {
      tipo: 'rubrica_analitica',
      titulo: `Rúbrica analítica: ${instrumento || actividad || 'Tarea'}`,
      instrumento,
      niveles: nivelesBase,
      criterios: criteriosBase.map(criterio => ({
        criterio,
        descriptores: this._generarDescriptores(criterio, nivelesBase, instrumento)
      }))
    };
  }

  generarRubricaOral({ actividad, aspectos, niveles }) {
    const nivelesBase = niveles || ['Inicial', 'En proceso', 'Adecuado', 'Avanzado'];
    const aspectosBase = aspectos && aspectos.length > 0 ? aspectos :
      ['Contenido y adecuación al tema', 'Estructura y organización del discurso', 'Expresión oral y vocabulario', 'Interacción y respuesta a preguntas', 'Uso de evidencias o ejemplos'];

    return {
      tipo: 'rubrica_oral',
      titulo: `Rúbrica de evaluación oral: ${actividad || 'Actividad oral'}`,
      niveles: nivelesBase,
      criterios: aspectosBase.map(aspecto => ({
        criterio: aspecto,
        descriptores: this._generarDescriptoresOral(aspecto, nivelesBase)
      }))
    };
  }

  generarListaCotejo({ instrumento, indicadores, actividad }) {
    const indicadoresBase = indicadores && indicadores.length > 0 ? indicadores :
      this._inferirIndicadores(instrumento, actividad);

    return {
      tipo: 'lista_cotejo',
      titulo: `Lista de cotejo: ${instrumento || actividad || 'Tarea'}`,
      indicadores: indicadoresBase.map(ind => ({
        indicador: ind,
        si: false,
        no: false,
        observaciones: ''
      }))
    };
  }

  generarEscalaValoracion({ instrumento, criterios, niveles, actividad }) {
    const nivelesBase = niveles || ['1 - Insuficiente', '2 - Suficiente', '3 - Bien', '4 - Muy bien', '5 - Excelente'];
    const criteriosBase = criterios && criterios.length > 0 ? criterios : this._inferirCriterios(instrumento, actividad);

    return {
      tipo: 'escala_valoracion',
      titulo: `Escala de valoración: ${instrumento || actividad || 'Tarea'}`,
      niveles: nivelesBase,
      criterios: criteriosBase.map(c => ({ criterio: c, valoracion: null }))
    };
  }

  generarGuiaCorreccion({ instrumento, apartados, actividad }) {
    const apartadosBase = apartados && apartados.length > 0 ? apartados :
      this._inferirApartados(instrumento, actividad);

    return {
      tipo: 'guia_correccion',
      titulo: `Guía de corrección: ${instrumento || actividad || 'Tarea'}`,
      apartados: apartadosBase.map(ap => ({
        apartado: ap.nombre || ap,
        criterios: ap.criterios || 'Criterios de corrección a definir.',
        puntuacion: ap.puntuacion || '',
        observaciones: ''
      }))
    };
  }

  generarFichaAutoevaluacion({ actividad, preguntas }) {
    const preguntasBase = preguntas && preguntas.length > 0 ? preguntas : [
      '¿Qué he aprendido con esta actividad?',
      '¿Qué evidencia demuestra que lo he aprendido?',
      '¿Qué parte me ha resultado más difícil? ¿Por qué?',
      '¿Qué podría mejorar en mi trabajo?',
      '¿Qué haré de forma diferente la próxima vez?',
      '¿En qué aspectos me siento más seguro/a?',
      '¿Qué necesito seguir practicando o estudiando?'
    ];

    return {
      tipo: 'ficha_autoevaluacion',
      titulo: `Ficha de autoevaluación: ${actividad || 'Actividad'}`,
      preguntas: preguntasBase.map(p => ({ pregunta: p, respuesta: '' }))
    };
  }

  generarFichaCoevaluacion({ actividad, aspectos }) {
    const aspectosBase = aspectos && aspectos.length > 0 ? aspectos : [
      'Participación activa en el trabajo o actividad',
      'Claridad y precisión en la exposición de ideas',
      'Aportación de argumentos o evidencias',
      'Escucha y respeto hacia las aportaciones de los demás',
      'Cumplimiento de la tarea o rol asignado'
    ];

    return {
      tipo: 'ficha_coevaluacion',
      titulo: `Ficha de coevaluación: ${actividad || 'Actividad'}`,
      nombre_evaluado: '',
      nombre_evaluador: '',
      aspectos: aspectosBase.map(asp => ({
        aspecto: asp,
        comentario_positivo: '',
        sugerencia_mejora: '',
        evidencia_concreta: '',
        valoracion: null
      }))
    };
  }

  generarHojaSeguimiento({ actividad, alumnos, sesiones, criterios }) {
    return {
      tipo: 'hoja_seguimiento',
      titulo: `Hoja de seguimiento: ${actividad || 'Proyecto'}`,
      sesiones: sesiones || ['Sesión 1', 'Sesión 2', 'Sesión 3'],
      criterios: criterios || ['Participación', 'Avance en la tarea', 'Colaboración', 'Uso del tiempo'],
      registros: []
    };
  }

  generarRegistroDiagnostico({ materia, unidad, preguntas }) {
    const preguntasBase = preguntas || [
      { pregunta: `¿Qué sé sobre ${unidad || 'el tema'}?`, respuesta: '' },
      { pregunta: '¿Qué me interesa aprender?', respuesta: '' },
      { pregunta: '¿Qué preguntas tengo sobre el tema?', respuesta: '' }
    ];

    return {
      tipo: 'registro_diagnostico',
      titulo: `Registro diagnóstico: ${unidad || materia || 'Unidad'}`,
      preguntas: preguntasBase
    };
  }

  _inferirCriterios(instrumento, actividad) {
    const instr = String(instrumento || '').toLowerCase();
    const act = String(actividad || '').toLowerCase();

    if (instr.includes('informe') || act.includes('informe')) {
      return ['Planteamiento e hipótesis', 'Procedimiento experimental', 'Registro de datos', 'Análisis de resultados', 'Conclusiones', 'Lenguaje científico y presentación'];
    }
    if (instr.includes('proyecto')) {
      return ['Planificación y organización', 'Investigación y fuentes', 'Desarrollo y contenido', 'Creatividad y originalidad', 'Presentación final', 'Trabajo en equipo'];
    }
    if (instr.includes('ensayo') || instr.includes('texto')) {
      return ['Adecuación al tema', 'Estructura y coherencia', 'Argumentación', 'Uso de fuentes', 'Expresión y vocabulario', 'Presentación'];
    }
    if (instr.includes('exposicion') || instr.includes('exposición') || act.includes('exposicion')) {
      return ['Contenido y dominio del tema', 'Estructura y organización', 'Expresión oral', 'Uso de recursos visuales', 'Respuesta a preguntas'];
    }
    return ['Contenido', 'Organización', 'Calidad de la presentación', 'Uso de fuentes o evidencias', 'Conclusiones o reflexión final'];
  }

  _inferirIndicadores(instrumento, actividad) {
    const instr = String(instrumento || '').toLowerCase();
    const act = String(actividad || '').toLowerCase();

    if (instr.includes('laboratorio') || act.includes('laboratorio')) {
      return [
        'Utiliza el material de laboratorio de forma segura y correcta.',
        'Sigue el procedimiento establecido sin saltarse pasos.',
        'Registra los datos de forma ordenada con unidades correctas.',
        'Mantiene limpio y ordenado el área de trabajo.',
        'Colabora con el grupo de forma responsable.',
        'El informe incluye hipótesis, procedimiento, datos y conclusión.',
        'La conclusión está vinculada a los datos obtenidos.'
      ];
    }
    if (instr.includes('debate') || act.includes('debate')) {
      return [
        'Interviene de forma ordenada respetando los turnos de palabra.',
        'Aporta argumentos relacionados con el tema.',
        'Escucha activamente las intervenciones de los compañeros/as.',
        'Responde a los argumentos contrarios con respeto.',
        'Utiliza evidencias o ejemplos concretos para apoyar sus ideas.',
        'Muestra un tono adecuado y vocabulario apropiado.'
      ];
    }
    if (instr.includes('proyecto')) {
      return [
        'Entrega las partes del proyecto en los plazos establecidos.',
        'La información está bien organizada y es pertinente.',
        'Incluye fuentes variadas y cita correctamente.',
        'El producto final es original y elaborado.',
        'Todos los miembros del grupo participan activamente.'
      ];
    }
    return [
      'Cumple con los requisitos mínimos de la tarea.',
      'La presentación es clara y ordenada.',
      'El contenido es correcto y pertinente.',
      'Utiliza el vocabulario adecuado al contexto.',
      'Entrega en el plazo establecido.'
    ];
  }

  _inferirApartados(instrumento, actividad) {
    const instr = String(instrumento || '').toLowerCase();
    if (instr.includes('informe')) {
      return [
        { nombre: 'Hipótesis o pregunta de investigación', criterios: 'La hipótesis es clara, observable y relacionada con el experimento.', puntuacion: '1 punto' },
        { nombre: 'Procedimiento', criterios: 'Describe los pasos seguidos de forma ordenada y comprensible.', puntuacion: '2 puntos' },
        { nombre: 'Registro de datos', criterios: 'Los datos están organizados en tabla con unidades correctas.', puntuacion: '2 puntos' },
        { nombre: 'Análisis', criterios: 'Interpreta los datos y los relaciona con la hipótesis.', puntuacion: '3 puntos' },
        { nombre: 'Conclusiones', criterios: 'Formula conclusiones coherentes con los datos obtenidos.', puntuacion: '2 puntos' }
      ];
    }
    return [
      { nombre: 'Apartado 1', criterios: '', puntuacion: '' },
      { nombre: 'Apartado 2', criterios: '', puntuacion: '' },
      { nombre: 'Apartado 3', criterios: '', puntuacion: '' }
    ];
  }

  _generarDescriptores(criterio, niveles, instrumento) {
    const crit = criterio.toLowerCase();
    const descriptoresBase = {
      'planteamiento e hipótesis': [
        'No formula hipótesis o esta no guarda relación con el experimento.',
        'Formula una hipótesis vaga o incompleta.',
        'Formula una hipótesis observable y relacionada con las variables.',
        'Formula una hipótesis precisa, verificable y bien relacionada con las variables dependiente e independiente.'
      ],
      'procedimiento experimental': [
        'El procedimiento es incompleto o incorrecto.',
        'Describe algunos pasos, pero falta precisión o hay errores.',
        'Describe el procedimiento de forma ordenada y comprensible.',
        'Describe el procedimiento con detalle, precisión y orden, incluyendo materiales y condiciones.'
      ],
      'registro de datos': [
        'No registra datos o lo hace de forma caótica.',
        'Registra datos, pero faltan unidades o hay errores de organización.',
        'Registra los datos de forma ordenada y con unidades correctas.',
        'Registra datos de forma sistemática, en tabla bien diseñada, con unidades y repeticiones si procede.'
      ],
      'análisis de resultados': [
        'No analiza los resultados o hace afirmaciones sin fundamento.',
        'Describe los resultados sin interpretarlos ni relacionarlos con la hipótesis.',
        'Interpreta los resultados y los relaciona con la hipótesis.',
        'Analiza los resultados con rigor, identifica tendencias y relaciona los datos con la hipótesis y el marco teórico.'
      ],
      'conclusiones': [
        'No incluye conclusión o esta no tiene relación con los datos.',
        'La conclusión es superficial o no está bien apoyada en los datos.',
        'Formula una conclusión coherente vinculada a los resultados.',
        'Formula conclusiones precisas, evalúa la hipótesis y propone posibles mejoras o nuevas preguntas.'
      ],
      'lenguaje científico y presentación': [
        'El vocabulario es inapropiado y la presentación muy deficiente.',
        'Usa algún término científico, pero la presentación es poco cuidada.',
        'Usa vocabulario científico adecuado y la presentación es ordenada.',
        'Usa vocabulario científico preciso y la presentación es clara, ordenada y bien estructurada.'
      ]
    };

    // Buscar descriptor específico
    for (const [key, desc] of Object.entries(descriptoresBase)) {
      if (crit.includes(key.split(' ')[0]) || key.includes(crit.split(' ')[0])) {
        return niveles.map((n, i) => desc[Math.min(i, desc.length - 1)]);
      }
    }

    // Descriptores genéricos
    return niveles.map((nivel, i) => {
      if (i === 0) return `No alcanza los criterios mínimos en ${criterio.toLowerCase()}.`;
      if (i === 1) return `Alcanza parcialmente los criterios de ${criterio.toLowerCase()}, con errores o imprecisiones notables.`;
      if (i === 2) return `Cumple satisfactoriamente los criterios de ${criterio.toLowerCase()}.`;
      return `Supera los criterios de ${criterio.toLowerCase()} con calidad, precisión y autonomía.`;
    });
  }

  _generarDescriptoresOral(aspecto, niveles) {
    const asp = aspecto.toLowerCase();
    const descriptores = {
      'contenido': [
        'El contenido es escaso, incorrecto o no se ajusta al tema.',
        'El contenido es parcialmente correcto y con lagunas importantes.',
        'El contenido es correcto y pertinente al tema.',
        'El contenido es preciso, completo y muestra dominio del tema.'
      ],
      'estructura': [
        'La intervención carece de estructura reconocible.',
        'La estructura es confusa o los apartados no se diferencian con claridad.',
        'La intervención tiene una estructura clara con introducción, desarrollo y cierre.',
        'La estructura es coherente, bien organizada y facilita la comprensión del discurso.'
      ],
      'expresión oral': [
        'La expresión es confusa, con errores graves o dificultad para entender el mensaje.',
        'La expresión es comprensible, pero con errores o falta de fluidez.',
        'La expresión es clara y fluida, con vocabulario adecuado.',
        'La expresión es precisa, fluida y adaptada al contexto comunicativo con vocabulario rico.'
      ],
      'interacción': [
        'No interactúa con el interlocutor o muestra dificultades graves para responder.',
        'Responde a las preguntas con dificultad o de forma superficial.',
        'Responde a las preguntas de forma adecuada y mantiene la interacción.',
        'Responde con precisión, amplía la respuesta con ejemplos y gestiona bien la interacción.'
      ],
      'evidencias': [
        'No utiliza evidencias ni ejemplos concretos.',
        'Menciona algún ejemplo, pero sin relacionarlo claramente con el argumento.',
        'Utiliza evidencias o ejemplos pertinentes para apoyar sus ideas.',
        'Utiliza evidencias variadas, bien seleccionadas y las integra con eficacia en el discurso.'
      ]
    };

    for (const [key, desc] of Object.entries(descriptores)) {
      if (asp.includes(key)) {
        return niveles.map((n, i) => desc[Math.min(i, desc.length - 1)]);
      }
    }

    return niveles.map((nivel, i) => {
      if (i === 0) return `No alcanza los criterios mínimos en ${aspecto.toLowerCase()}.`;
      if (i === 1) return `Alcanza parcialmente los criterios de ${aspecto.toLowerCase()}.`;
      if (i === 2) return `Cumple adecuadamente los criterios de ${aspecto.toLowerCase()}.`;
      return `Destaca en ${aspecto.toLowerCase()} con calidad y precisión.`;
    });
  }
}

window.ToolGenerator = ToolGenerator;
