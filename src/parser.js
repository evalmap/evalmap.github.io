// Parser de texto libre a estructura de datos del formulario
class FreeTextParser {
  parse(texto) {
    const t = texto.toLowerCase();
    const resultado = {
      etapa: '', curso: '', materia: '', actividad: texto,
      contexto: '', tipo_evidencia: [], finalidad: [], momento: [],
      complejidad: '', agrupamiento: '', participacion_alumnado: '',
      producto_final: '', desempeno_observable: '', respuestas_esperadas: '',
      requisitos_cerrados: '', necesita_calificacion: '', necesita_feedback: '',
      criterios_evaluacion: '', aspectos_valorar: [], tiempo_disponible: '',
      numero_alumnos: '', salida_deseada: ''
    };

    // Etapa
    if (t.includes('bachillerato')) resultado.etapa = 'Bachillerato';
    else if (t.includes('eso') || t.match(/\d\.º de (la )?eso/)) resultado.etapa = 'ESO';
    else if (t.includes('primaria')) resultado.etapa = 'Primaria';
    else if (t.includes(' fp') || t.includes('formación profesional')) resultado.etapa = 'FP';
    else if (t.includes('universidad') || t.includes('universitario')) resultado.etapa = 'Universidad';

    // Curso
    const cursoMatch = texto.match(/(\d\.º[^,\.]*(?:bachillerato|eso|primaria|fp|curso)?)/i);
    if (cursoMatch) resultado.curso = cursoMatch[1].trim();

    // Materia
    const materias = {
      'biología': 'Biología', 'física': 'Física', 'química': 'Química',
      'matemáticas': 'Matemáticas', 'matemática': 'Matemáticas',
      'lengua': 'Lengua', 'historia': 'Historia', 'geografía': 'Geografía',
      'inglés': 'Inglés', 'ciencias': 'Ciencias', 'filosofía': 'Filosofía',
      'economía': 'Economía', 'tecnología': 'Tecnología', 'informática': 'Informática',
      'arte': 'Arte', 'música': 'Música', 'educación física': 'Educación Física'
    };
    for (const [key, val] of Object.entries(materias)) {
      if (t.includes(key)) { resultado.materia = val; break; }
    }

    // Contexto / tipo de actividad
    if (t.includes('laboratorio') || t.includes('práctica') || t.includes('práctica de laboratorio')) {
      resultado.contexto = 'laboratorio';
      resultado.tipo_evidencia.push('actuacion_practica');
      resultado.desempeno_observable = 'si';
    }
    if (t.includes('debate')) {
      resultado.contexto = 'debate';
      resultado.tipo_evidencia.push('actuacion_oral');
      resultado.desempeno_observable = 'si';
    }
    if (t.includes('exposición') || t.includes('exposicion') || t.includes('presentación oral')) {
      resultado.contexto = 'exposicion';
      resultado.tipo_evidencia.push('actuacion_oral');
      resultado.desempeno_observable = 'si';
    }
    if (t.includes('proyecto')) {
      resultado.contexto = 'proyecto';
      resultado.tipo_evidencia.push('produccion_escrita');
      if (t.includes('defensa') || t.includes('oral')) resultado.tipo_evidencia.push('actuacion_oral');
    }
    if (t.includes('test') || t.includes('prueba') || t.includes('examen')) {
      resultado.contexto = 'prueba';
      resultado.tipo_evidencia.push('respuesta_cerrada');
    }
    if (t.includes('ensayo') || t.includes('redacción') || t.includes('composición')) {
      resultado.contexto = 'produccion_escrita';
      resultado.tipo_evidencia.push('produccion_escrita');
    }
    if (t.includes('portafolio') || t.includes('portfolio')) {
      resultado.contexto = 'portafolio';
      resultado.tipo_evidencia.push('produccion_escrita');
      resultado.tipo_evidencia.push('proceso');
    }
    if (t.includes('kpsi')) {
      resultado.contexto = 'kpsi';
      resultado.tipo_evidencia.push('respuesta_escrita');
      resultado.finalidad.push('diagnosticar');
      resultado.momento.push('inicial');
    }
    if (t.includes('trabajo en grupo') || t.includes('trabajo cooperativo') || t.includes('grupal')) {
      resultado.agrupamiento = 'grupo';
      resultado.tipo_evidencia.push('produccion_grupal');
    }

    // Producto final
    if (t.includes('informe') || t.includes('memoria') || t.includes('producto final')) {
      resultado.producto_final = 'si';
      if (!resultado.tipo_evidencia.includes('produccion_escrita'))
        resultado.tipo_evidencia.push('produccion_escrita');
    }

    // Finalidad
    if (t.includes('calificar') || t.includes('nota') || t.includes('calificación')) {
      resultado.finalidad.push('calificar');
      resultado.necesita_calificacion = 'si';
    }
    if (t.includes('retroalimentación') || t.includes('feedback') || t.includes('mejorar')) {
      resultado.finalidad.push('retroalimentar');
      resultado.necesita_feedback = 'si';
    }
    if (t.includes('diagnóstico') || t.includes('conocimientos previos') || t.includes('inicial')) {
      resultado.finalidad.push('diagnosticar');
      resultado.momento.push('inicial');
    }

    // Momento
    if (t.includes('al inicio') || t.includes('antes de') || t.includes('conocimientos previos')) {
      resultado.momento.push('inicial');
    }
    if (t.includes('durante') || t.includes('en proceso') || t.includes('seguimiento')) {
      resultado.momento.push('proceso');
    }
    if (t.includes('al final') || t.includes('final de') || t.includes('al término')) {
      resultado.momento.push('final');
    }

    // Complejidad
    if (t.includes('complej') || t.includes('avanzad') || t.includes('superior')) {
      resultado.complejidad = 'alta';
    } else if (t.includes('sencill') || t.includes('básic') || t.includes('simple') || t.includes('test')) {
      resultado.complejidad = 'baja';
    } else {
      resultado.complejidad = 'media';
    }

    // Participación del alumnado
    if (t.includes('autoevaluación') || t.includes('autoevaluacion')) {
      resultado.participacion_alumnado = 'alumno';
    } else if (t.includes('coevaluación') || t.includes('coevaluacion') || t.includes('entre iguales')) {
      resultado.participacion_alumnado = 'iguales';
    }

    // Eliminar duplicados en arrays
    resultado.tipo_evidencia = [...new Set(resultado.tipo_evidencia)];
    resultado.finalidad = [...new Set(resultado.finalidad)];
    resultado.momento = [...new Set(resultado.momento)];

    return resultado;
  }
}

window.FreeTextParser = FreeTextParser;
