// Motor de recomendación pedagógica
// Aplica reglas simples y combinadas para recomendar técnicas, instrumentos y herramientas

class RecommendationEngine {
  constructor(data) {
    this.tecnicas = data.tecnicas || [];
    this.instrumentos = data.instrumentos || [];
    this.herramientas = data.herramientas || [];
    this.reglasDecision = data.reglas_decision || [];
    this.reglasCombinadas = data.reglas_combinadas || [];
    this.instrumentosMaterias = data.instrumentos_materias || [];
    this.criteriosAdecuacion = data.criterios_adecuacion || [];
  }

  recommend(caseData) {
    const scores = {
      tecnicas: {},
      instrumentos: {},
      herramientas: {}
    };
    const reglasActivadas = [];
    const advertencias = [];

    // Inicializar puntuaciones en 0
    this.tecnicas.forEach(t => { scores.tecnicas[t['Técnica']] = 0; });
    this.instrumentos.forEach(i => { scores.instrumentos[i['Instrumento']] = 0; });
    this.herramientas.forEach(h => { scores.herramientas[h['Herramienta']] = 0; });

    // Aplicar reglas simples
    this.reglasDecision.forEach(regla => {
      const campo = regla['campo'];
      const valor = String(regla['valor'] || '').toLowerCase().trim();
      const tipo = regla['recomienda_tipo'];
      const nombre = regla['recomienda_nombre'];
      const puntos = parseFloat(regla['puntos'] || 0);
      const explicacion = regla['explicación'] || regla['explicacion'] || '';

      if (!campo || !valor || !nombre) return;

      const valorCaso = this._getCampoValor(caseData, campo);
      if (!valorCaso) return;

      let coincide = false;
      const valoresCaso = Array.isArray(valorCaso)
        ? valorCaso.map(v => String(v).toLowerCase().trim())
        : [String(valorCaso).toLowerCase().trim()];

      coincide = valoresCaso.some(vc => vc.includes(valor) || valor.includes(vc));

      if (coincide) {
        if (tipo === 'tecnica' && scores.tecnicas[nombre] !== undefined) {
          scores.tecnicas[nombre] += puntos;
          reglasActivadas.push({ tipo: 'simple', campo, valor, nombre, puntos, explicacion });
        } else if (tipo === 'instrumento' && scores.instrumentos[nombre] !== undefined) {
          scores.instrumentos[nombre] += puntos;
          reglasActivadas.push({ tipo: 'simple', campo, valor, nombre, puntos, explicacion });
        } else if (tipo === 'herramienta' && scores.herramientas[nombre] !== undefined) {
          scores.herramientas[nombre] += puntos;
          reglasActivadas.push({ tipo: 'simple', campo, valor, nombre, puntos, explicacion });
        }
      }
    });

    // Aplicar boost por materia específica
    if (caseData.materia) {
      const materia = caseData.materia.toLowerCase();
      this.instrumentosMaterias.forEach(im => {
        const materiaRef = String(im['Materia/ámbito'] || '').toLowerCase();
        if (materiaRef && materia.includes(materiaRef.split('/')[0].trim())) {
          const nombreInstr = im['Instrumento específico'];
          if (nombreInstr && scores.instrumentos[nombreInstr] !== undefined) {
            scores.instrumentos[nombreInstr] += 2;
          }
        }
      });
    }

    // Aplicar reglas combinadas (prioridad alta)
    const reglasCombinadasActivadas = [];
    this.reglasCombinadas.forEach(rc => {
      if (this._evaluarReglasCombinadas(caseData, rc)) {
        reglasCombinadasActivadas.push(rc);
        const justificacion = rc['Justificacion'] || rc['Justificación'] || '';
        reglasActivadas.push({
          tipo: 'combinada',
          condicion: rc['Condicion combinada'] || rc['Condición combinada'],
          justificacion,
          prioridad: 'Alta'
        });

        // Boost fuerte a las recomendaciones de reglas combinadas
        const tecnica = rc['Tecnica recomendada'] || rc['Técnica recomendada'] || '';
        const instrumento = rc['Instrumento principal'] || '';
        const herramienta = rc['Herramienta principal'] || '';
        const herramientaComp = rc['Herramienta complementaria'] || '';

        tecnica.split('+').forEach(t => {
          const nombre = t.trim();
          const key = this._findClosestKey(scores.tecnicas, nombre);
          if (key) scores.tecnicas[key] += 8;
        });

        instrumento.split('+').forEach(i => {
          const nombre = i.trim();
          const key = this._findClosestKey(scores.instrumentos, nombre);
          if (key) scores.instrumentos[key] += 8;
        });

        [herramienta, herramientaComp].forEach(h => {
          if (!h) return;
          const key = this._findClosestKey(scores.herramientas, h.trim());
          if (key) scores.herramientas[key] += 6;
        });
      }
    });

    // Aplicar conflictos y resoluciones
    this._resolverConflictos(caseData, scores, advertencias);

    // Ordenar y construir propuesta
    const tecnicasOrdenadas = this._ordenarPorPuntuacion(scores.tecnicas);
    const instrumentosOrdenados = this._ordenarPorPuntuacion(scores.instrumentos);
    const herramientasOrdenadas = this._ordenarPorPuntuacion(scores.herramientas);

    const propuestaPrincipal = {
      tecnicas: tecnicasOrdenadas.slice(0, 2).filter(([, p]) => p > 0).map(([n]) => n),
      instrumentos: instrumentosOrdenados.slice(0, 2).filter(([, p]) => p > 0).map(([n]) => n),
      herramientas: herramientasOrdenadas.slice(0, 2).filter(([, p]) => p > 0).map(([n]) => n),
      justificacion: this._generarJustificacion(caseData, reglasActivadas, reglasCombinadasActivadas)
    };

    const alternativas = this._generarAlternativas(caseData, tecnicasOrdenadas, instrumentosOrdenados, herramientasOrdenadas);
    const complementos = this._generarComplementos(caseData, herramientasOrdenadas);

    return {
      resumen_caso: this._generarResumen(caseData),
      propuesta_principal: propuestaPrincipal,
      alternativas,
      complementos,
      reglas_activadas: reglasActivadas,
      advertencias,
      puntuaciones: {
        tecnicas: Object.fromEntries(tecnicasOrdenadas.filter(([, p]) => p > 0)),
        instrumentos: Object.fromEntries(instrumentosOrdenados.filter(([, p]) => p > 0)),
        herramientas: Object.fromEntries(herramientasOrdenadas.filter(([, p]) => p > 0))
      }
    };
  }

  _getCampoValor(caseData, campo) {
    const val = caseData[campo];
    if (val === undefined || val === null || val === '') return null;
    return val;
  }

  _evaluarReglasCombinadas(caseData, rc) {
    const condicion = String(rc['Condicion combinada'] || rc['Condición combinada'] || '').toLowerCase();
    const campos = String(rc['Campos implicados'] || '').toLowerCase();

    // Mapeo de condiciones a campos del caso
    const contexto = String(caseData.contexto || '').toLowerCase();
    const tipoEvidencia = Array.isArray(caseData.tipo_evidencia)
      ? caseData.tipo_evidencia.join(' ').toLowerCase()
      : String(caseData.tipo_evidencia || '').toLowerCase();
    const productoFinal = String(caseData.producto_final || '').toLowerCase();
    const participacion = Array.isArray(caseData.participacion_alumnado)
      ? caseData.participacion_alumnado.join(' ').toLowerCase()
      : String(caseData.participacion_alumnado || '').toLowerCase();
    const finalidad = Array.isArray(caseData.finalidad)
      ? caseData.finalidad.join(' ').toLowerCase()
      : String(caseData.finalidad || '').toLowerCase();
    const desempeno = String(caseData.desempeno_observable || '').toLowerCase();

    if (condicion.includes('laboratorio') && condicion.includes('informe final')) {
      return (contexto.includes('laboratorio') || tipoEvidencia.includes('practica')) &&
             (productoFinal === 'si' || productoFinal === 'sí' || tipoEvidencia.includes('escrita'));
    }
    if (condicion.includes('laboratorio') && condicion.includes('sin informe')) {
      return (contexto.includes('laboratorio') || tipoEvidencia.includes('practica')) &&
             productoFinal !== 'si' && productoFinal !== 'sí';
    }
    if (condicion.includes('debate') && condicion.includes('coevaluacion')) {
      return (contexto.includes('debate') || tipoEvidencia.includes('oral')) &&
             (participacion.includes('autoevaluacion') || participacion.includes('coevaluacion'));
    }
    if (condicion.includes('debate') && condicion.includes('calificacion')) {
      return (contexto.includes('debate') || tipoEvidencia.includes('oral')) &&
             (finalidad.includes('calificar') || finalidad.includes('sumativa'));
    }
    if (condicion.includes('exposicion') || condicion.includes('exposición')) {
      return contexto.includes('exposicion') || contexto.includes('exposición') ||
             tipoEvidencia.includes('oral') && (productoFinal === 'si' || productoFinal === 'sí');
    }
    if (condicion.includes('proyecto') && condicion.includes('defensa')) {
      return (contexto.includes('proyecto') || tipoEvidencia.includes('proyecto')) &&
             (tipoEvidencia.includes('oral') || desempeno === 'si' || desempeno === 'sí');
    }
    if (condicion.includes('proyecto') && !condicion.includes('defensa')) {
      return contexto.includes('proyecto') || tipoEvidencia.includes('proyecto');
    }
    if (condicion.includes('kpsi') || condicion.includes('diagnostico') || condicion.includes('diagnóstico')) {
      return finalidad.includes('diagnost') || contexto.includes('kpsi');
    }
    if (condicion.includes('autoevaluacion') || condicion.includes('autoevaluación')) {
      return participacion.includes('autoevaluacion') || finalidad.includes('autoevaluacion');
    }
    if (condicion.includes('portafolio') || condicion.includes('portfolio')) {
      return tipoEvidencia.includes('portafolio') || tipoEvidencia.includes('portfolio');
    }
    if (condicion.includes('prueba') || condicion.includes('test')) {
      return tipoEvidencia.includes('cerrada') || tipoEvidencia.includes('test') ||
             contexto.includes('prueba') || contexto.includes('test');
    }

    return false;
  }

  _findClosestKey(obj, nombre) {
    const nombreLower = nombre.toLowerCase();
    // Búsqueda exacta
    const exacta = Object.keys(obj).find(k => k.toLowerCase() === nombreLower);
    if (exacta) return exacta;
    // Búsqueda parcial
    const parcial = Object.keys(obj).find(k =>
      k.toLowerCase().includes(nombreLower) || nombreLower.includes(k.toLowerCase())
    );
    return parcial || null;
  }

  _resolverConflictos(caseData, scores, advertencias) {
    const tipoEvidencia = Array.isArray(caseData.tipo_evidencia)
      ? caseData.tipo_evidencia.join(' ').toLowerCase()
      : String(caseData.tipo_evidencia || '').toLowerCase();
    const complejidad = String(caseData.complejidad || '').toLowerCase();
    const desempeno = String(caseData.desempeno_observable || '').toLowerCase();
    const participacion = Array.isArray(caseData.participacion_alumnado)
      ? caseData.participacion_alumnado.join(' ').toLowerCase()
      : String(caseData.participacion_alumnado || '').toLowerCase();
    const requisitos = String(caseData.requisitos_cerrados || '').toLowerCase();
    const finalidad = Array.isArray(caseData.finalidad)
      ? caseData.finalidad.join(' ').toLowerCase()
      : String(caseData.finalidad || '').toLowerCase();
    const momento = Array.isArray(caseData.momento)
      ? caseData.momento.join(' ').toLowerCase()
      : String(caseData.momento || '').toLowerCase();

    // Si hay respuestas cerradas, boost a herramientas objetivas
    if (tipoEvidencia.includes('cerrada') || requisitos === 'si' || requisitos === 'sí') {
      if (scores.herramientas['Rúbrica analítica'] !== undefined)
        scores.herramientas['Rúbrica analítica'] -= 3;
      if (scores.herramientas['Lista de cotejo'] !== undefined)
        scores.herramientas['Lista de cotejo'] += 3;
      if (scores.herramientas['Guía de corrección'] !== undefined)
        scores.herramientas['Guía de corrección'] += 2;
    }

    // Sin desempeño observable → bajar observación sistemática
    if (desempeno === 'no' || desempeno === '') {
      if (scores.tecnicas['Observación sistemática'] !== undefined)
        scores.tecnicas['Observación sistemática'] -= 2;
    }

    // Sin participación del alumnado → no coevaluación como principal
    if (!participacion.includes('autoevaluacion') && !participacion.includes('coevaluacion')) {
      if (scores.herramientas['Ficha de coevaluación'] !== undefined)
        scores.herramientas['Ficha de coevaluación'] -= 4;
      if (scores.tecnicas['Coevaluación'] !== undefined)
        scores.tecnicas['Coevaluación'] -= 4;
    }

    // Complejidad alta → boost rúbrica analítica
    if (complejidad === 'alta' || complejidad === 'muy alta') {
      if (scores.herramientas['Rúbrica analítica'] !== undefined)
        scores.herramientas['Rúbrica analítica'] += 3;
    }

    // Complejidad baja + requisitos cerrados → boost lista de cotejo
    if ((complejidad === 'baja' || complejidad === 'media') && (requisitos === 'si' || requisitos === 'sí')) {
      if (scores.herramientas['Lista de cotejo'] !== undefined)
        scores.herramientas['Lista de cotejo'] += 3;
      if (scores.herramientas['Rúbrica analítica'] !== undefined)
        scores.herramientas['Rúbrica analítica'] -= 2;
    }

    // Diagnóstica → no calificación
    if (finalidad.includes('diagnost')) {
      advertencias.push('La finalidad diagnóstica no debe usarse para penalizar ni para calificar. Se recomienda usar los resultados para ajustar la enseñanza.');
      if (scores.tecnicas['Evaluación sumativa'] !== undefined)
        scores.tecnicas['Evaluación sumativa'] -= 5;
    }

    // Momento inicial → boost diagnóstica
    if (momento.includes('inicial') || momento.includes('diagnóst')) {
      if (scores.tecnicas['Evaluación diagnóstica'] !== undefined)
        scores.tecnicas['Evaluación diagnóstica'] += 3;
    }

    // Advertencias pedagógicas generales
    if (tipoEvidencia.includes('oral') || tipoEvidencia.includes('practica')) {
      advertencias.push('No conviene valorar solo el producto final si el proceso (actuación oral o práctica) es relevante.');
    }
    if (participacion.includes('coevaluacion')) {
      advertencias.push('La coevaluación requiere criterios claros y entrenamiento previo del alumnado.');
    }
    if (scores.herramientas['Lista de cotejo'] > 5) {
      advertencias.push('Una lista de cotejo es rápida y clara, pero no describe bien niveles de calidad. Considera combinarla con una rúbrica si se necesita retroalimentación detallada.');
    }
    if (scores.herramientas['Rúbrica analítica'] > 5) {
      advertencias.push('Una rúbrica analítica requiere tiempo de elaboración, pero facilita la retroalimentación y la autoevaluación del alumnado.');
    }
  }

  _ordenarPorPuntuacion(scores) {
    return Object.entries(scores).sort(([, a], [, b]) => b - a);
  }

  _generarResumen(caseData) {
    const partes = [];
    if (caseData.actividad) partes.push(caseData.actividad);
    if (caseData.materia) partes.push(`en ${caseData.materia}`);
    if (caseData.curso) partes.push(`(${caseData.curso})`);
    if (partes.length === 0 && caseData.descripcion_libre) return caseData.descripcion_libre;
    return partes.join(' ') || 'Caso sin descripción';
  }

  _generarJustificacion(caseData, reglasActivadas, reglasCombinadasActivadas) {
    const partes = [];

    // Mencionar reglas combinadas activadas
    reglasCombinadasActivadas.forEach(rc => {
      const just = rc['Justificacion'] || rc['Justificación'] || '';
      if (just) partes.push(just);
    });

    // Construir justificación basada en entradas clave
    const tipoEvidencia = Array.isArray(caseData.tipo_evidencia)
      ? caseData.tipo_evidencia : [String(caseData.tipo_evidencia || '')];
    const finalidad = Array.isArray(caseData.finalidad)
      ? caseData.finalidad : [String(caseData.finalidad || '')];
    const complejidad = caseData.complejidad || '';

    if (tipoEvidencia.some(t => t.includes('oral'))) {
      partes.push('La actividad genera evidencia oral observable, lo que justifica el uso de técnicas de intercambio oral y observación sistemática.');
    }
    if (tipoEvidencia.some(t => t.includes('practica') || t.includes('práctica'))) {
      partes.push('Hay una actuación práctica que debe registrarse mientras se produce, lo que requiere observación sistemática con lista de cotejo o escala.');
    }
    if (tipoEvidencia.some(t => t.includes('escrita') || t.includes('informe') || t.includes('produccion'))) {
      partes.push('Existe una producción escrita que permite valorar calidad, estructura y contenido mediante análisis de producciones.');
    }
    if (complejidad === 'alta' || complejidad === 'muy alta') {
      partes.push('La complejidad alta de la tarea justifica el uso de una rúbrica analítica que permita valorar múltiples dimensiones con descriptores claros.');
    }
    if (finalidad.some(f => f.includes('retroalimentar') || f.includes('feedback'))) {
      partes.push('La finalidad formativa y de retroalimentación favorece el uso de herramientas que describan niveles y proporcionen información específica al alumnado.');
    }
    if (finalidad.some(f => f.includes('calificar'))) {
      partes.push('La necesidad de calificación requiere herramientas que permitan valorar de forma objetiva y justificada.');
    }

    if (partes.length === 0) {
      partes.push('La recomendación se basa en el análisis de las características del caso: tipo de evidencia, finalidad, momento y complejidad de la tarea.');
    }

    return partes.join(' ');
  }

  _generarAlternativas(caseData, tecnicas, instrumentos, herramientas) {
    const alternativas = [];
    const complejidad = String(caseData.complejidad || '').toLowerCase();
    const top3Her = herramientas.slice(0, 5).filter(([, p]) => p > 0).map(([n]) => n);

    if (top3Her.includes('Rúbrica analítica') && top3Her.includes('Lista de cotejo')) {
      alternativas.push('Escala de valoración en lugar de lista de cotejo, si se quiere graduar el nivel de desempeño sin la complejidad de una rúbrica completa.');
    }
    if (top3Her.includes('Rúbrica analítica') && complejidad !== 'alta') {
      alternativas.push('Guía de corrección en lugar de rúbrica analítica, si los criterios de la tarea son más cerrados y se necesita rapidez en la corrección.');
    }
    if (herramientas.slice(0, 3).some(([n]) => n.includes('Rúbrica'))) {
      alternativas.push('Rúbrica holística en lugar de analítica si se prefiere una valoración global más rápida y la tarea no requiere retroalimentación detallada por criterios.');
    }

    return alternativas.slice(0, 2);
  }

  _generarComplementos(caseData, herramientas) {
    const complementos = [];
    const participacion = Array.isArray(caseData.participacion_alumnado)
      ? caseData.participacion_alumnado.join(' ').toLowerCase()
      : String(caseData.participacion_alumnado || '').toLowerCase();
    const necesitaFeedback = String(caseData.necesita_feedback || '').toLowerCase();
    const tipoEvidencia = Array.isArray(caseData.tipo_evidencia)
      ? caseData.tipo_evidencia.join(' ').toLowerCase()
      : String(caseData.tipo_evidencia || '').toLowerCase();

    if (necesitaFeedback === 'si' || necesitaFeedback === 'sí') {
      complementos.push('Ficha de retroalimentación: permite devolver información específica y orientada a la mejora.');
    }
    if (participacion.includes('autoevaluacion')) {
      complementos.push('Ficha de autoevaluación: facilita la metacognición y la responsabilidad del alumnado sobre su aprendizaje.');
    }
    if (participacion.includes('coevaluacion')) {
      complementos.push('Ficha de coevaluación entre iguales: útil para actividades grupales y para que el alumnado comprenda los criterios de evaluación.');
    }

    return complementos.slice(0, 2);
  }

  // Obtener detalle de una técnica
  getTecnicaDetalle(nombre) {
    return this.tecnicas.find(t => t['Técnica'] === nombre || t['Técnica']?.includes(nombre));
  }

  // Obtener detalle de una herramienta
  getHerramientaDetalle(nombre) {
    return this.herramientas.find(h => h['Herramienta'] === nombre || h['Herramienta']?.includes(nombre));
  }

  // Obtener criterios de adecuación de una herramienta
  getCriteriosAdecuacion(nombre) {
    return this.criteriosAdecuacion.find(c =>
      c['Elemento'] === nombre || String(c['Elemento'] || '').toLowerCase().includes(nombre.toLowerCase())
    );
  }
}

window.RecommendationEngine = RecommendationEngine;
