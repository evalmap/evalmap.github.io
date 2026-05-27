// Módulo de exportación de resultados
class Exporter {
  copiarPortapapeles(texto) {
    navigator.clipboard.writeText(texto).then(() => {
      this._notificar('Copiado al portapapeles');
    }).catch(() => {
      // Fallback para navegadores sin API clipboard
      const el = document.createElement('textarea');
      el.value = texto;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      this._notificar('Copiado al portapapeles');
    });
  }

  exportarMarkdown(resultado, herramientaGenerada) {
    let md = `# Evaluación: ${resultado.resumen_caso}\n\n`;

    if (resultado.propuesta_principal) {
      const pp = resultado.propuesta_principal;
      md += `## Propuesta principal\n\n`;
      if (pp.tecnicas?.length) md += `**Técnica(s):** ${pp.tecnicas.join(' + ')}\n\n`;
      if (pp.instrumentos?.length) md += `**Instrumento(s):** ${pp.instrumentos.join(' + ')}\n\n`;
      if (pp.herramientas?.length) md += `**Herramienta(s):** ${pp.herramientas.join(' + ')}\n\n`;
      if (pp.justificacion) md += `**Justificación:** ${pp.justificacion}\n\n`;
    }

    if (resultado.alternativas?.length) {
      md += `## Alternativas\n\n`;
      resultado.alternativas.forEach((alt, i) => {
        md += `${i + 1}. ${alt}\n`;
      });
      md += '\n';
    }

    if (resultado.advertencias?.length) {
      md += `## Consideraciones pedagógicas\n\n`;
      resultado.advertencias.forEach(adv => {
        md += `- ${adv}\n`;
      });
      md += '\n';
    }

    if (resultado.reglas_activadas?.length) {
      md += `## Criterios aplicados\n\n`;
      resultado.reglas_activadas.forEach(r => {
        if (r.tipo === 'combinada') {
          md += `- Se ha activado la regla combinada "${r.condicion}": ${r.justificacion}\n`;
        } else if (r.explicacion) {
          md += `- ${r.explicacion}\n`;
        }
      });
      md += '\n';
    }

    if (herramientaGenerada) {
      md += this._herramientaAMarkdown(herramientaGenerada);
    }

    return md;
  }

  exportarTextoProgramacion(resultado) {
    const pp = resultado.propuesta_principal;
    if (!pp) return '';

    const tecnicas = pp.tecnicas?.join(' y ') || '';
    const instrumentos = pp.instrumentos?.join(', complementado con ') || '';
    const herramientas = pp.herramientas?.join(' y ') || '';

    let texto = `Para la evaluación de esta actividad se utilizará ${tecnicas}. `;
    if (instrumentos) texto += `El instrumento principal será ${instrumentos}. `;
    if (herramientas) texto += `Para registrar y valorar las evidencias se empleará ${herramientas}. `;
    texto += `${pp.justificacion || ''}`;

    return texto.trim();
  }

  exportarTextoAlumnado(resultado) {
    const pp = resultado.propuesta_principal;
    if (!pp) return '';

    let texto = `¿Cómo se evaluará esta actividad?\n\n`;
    if (pp.tecnicas?.length) texto += `Se observará tu desempeño mediante: ${pp.tecnicas.join(' y ')}.\n\n`;
    if (pp.instrumentos?.length) texto += `La actividad evaluada será: ${pp.instrumentos.join(' y ')}.\n\n`;
    if (pp.herramientas?.length) texto += `Para valorar tu trabajo se usará: ${pp.herramientas.join(' y ')}.\n\n`;
    texto += `Antes de entregar o realizar la actividad, asegúrate de revisar los criterios de evaluación.`;

    return texto;
  }

  exportarCSV(resultado) {
    const filas = [
      ['Elemento', 'Puntuación'],
    ];

    const p = resultado.puntuaciones;
    if (p) {
      Object.entries(p.tecnicas || {}).forEach(([n, s]) => filas.push([`Técnica: ${n}`, s]));
      Object.entries(p.instrumentos || {}).forEach(([n, s]) => filas.push([`Instrumento: ${n}`, s]));
      Object.entries(p.herramientas || {}).forEach(([n, s]) => filas.push([`Herramienta: ${n}`, s]));
    }

    return filas.map(f => f.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n');
  }

  descargarArchivo(contenido, nombre, tipo) {
    const blob = new Blob([contenido], { type: tipo });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = nombre;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  _herramientaAMarkdown(herramienta) {
    let md = `## Herramienta generada: ${herramienta.titulo}\n\n`;

    if (herramienta.tipo === 'rubrica_analitica' || herramienta.tipo === 'rubrica_oral') {
      const niveles = herramienta.niveles || [];
      md += `| Criterio | ${niveles.join(' | ')} |\n`;
      md += `|${'-|'.repeat(niveles.length + 1)}\n`;
      (herramienta.criterios || []).forEach(c => {
        const descs = (c.descriptores || []).map(d => d.replace(/\|/g, '\\|'));
        md += `| ${c.criterio} | ${descs.join(' | ')} |\n`;
      });
    } else if (herramienta.tipo === 'lista_cotejo') {
      md += `| Indicador | Sí | No | Observaciones |\n`;
      md += `|---|---|---|---|\n`;
      (herramienta.indicadores || []).forEach(i => {
        md += `| ${i.indicador} | | | |\n`;
      });
    } else if (herramienta.tipo === 'guia_correccion') {
      md += `| Apartado | Criterios de corrección | Puntuación | Observaciones |\n`;
      md += `|---|---|---|---|\n`;
      (herramienta.apartados || []).forEach(a => {
        md += `| ${a.apartado} | ${a.criterios} | ${a.puntuacion} | |\n`;
      });
    } else if (herramienta.tipo === 'ficha_autoevaluacion') {
      (herramienta.preguntas || []).forEach(p => {
        md += `**${p.pregunta}**\n\n_Respuesta:_ \n\n`;
      });
    } else if (herramienta.tipo === 'ficha_coevaluacion') {
      md += `**Alumno/a evaluado/a:**  \n**Evaluador/a:**  \n\n`;
      md += `| Aspecto | Comentario positivo | Sugerencia de mejora | Evidencia | Valoración |\n`;
      md += `|---|---|---|---|---|\n`;
      (herramienta.aspectos || []).forEach(a => {
        md += `| ${a.aspecto} | | | | |\n`;
      });
    }

    return md + '\n';
  }

  generarHTMLImprimible(resultado, herramientaGenerada) {
    const pp = resultado.propuesta_principal || {};
    let html = `<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Evaluación: ${resultado.resumen_caso}</title>
<style>
  body { font-family: Georgia, serif; max-width: 800px; margin: 2em auto; color: #222; }
  h1 { color: #1a4f72; } h2 { color: #2471a3; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th, td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 0.9em; }
  th { background: #eaf4fb; }
  .badge { display: inline-block; background: #2471a3; color: white; border-radius: 4px; padding: 2px 8px; margin: 2px; font-size: 0.85em; }
  .advertencia { background: #fef9e7; border-left: 4px solid #f1c40f; padding: 8px 12px; margin: 8px 0; }
  @media print { body { margin: 1em; } }
</style></head><body>
<h1>Diseño de evaluación</h1>
<p><strong>Caso:</strong> ${resultado.resumen_caso}</p>
<h2>Propuesta principal</h2>
<p><strong>Técnica(s):</strong> ${(pp.tecnicas || []).map(t => `<span class="badge">${t}</span>`).join(' ')}</p>
<p><strong>Instrumento(s):</strong> ${(pp.instrumentos || []).map(i => `<span class="badge">${i}</span>`).join(' ')}</p>
<p><strong>Herramienta(s):</strong> ${(pp.herramientas || []).map(h => `<span class="badge">${h}</span>`).join(' ')}</p>
<p><strong>Justificación:</strong> ${pp.justificacion || ''}</p>`;

    if (resultado.advertencias?.length) {
      html += `<h2>Consideraciones pedagógicas</h2>`;
      resultado.advertencias.forEach(a => {
        html += `<div class="advertencia">${a}</div>`;
      });
    }

    if (herramientaGenerada) {
      html += this._herramientaAHTML(herramientaGenerada);
    }

    html += `<p style="font-size:0.8em;color:#888;margin-top:2em">Generado con el Asistente de Diseño de Evaluación</p>
</body></html>`;
    return html;
  }

  _herramientaAHTML(herramienta) {
    let html = `<h2>${herramienta.titulo}</h2>`;
    if (herramienta.tipo === 'rubrica_analitica' || herramienta.tipo === 'rubrica_oral') {
      const niveles = herramienta.niveles || [];
      html += `<table><thead><tr><th>Criterio</th>${niveles.map(n => `<th>${n}</th>`).join('')}</tr></thead><tbody>`;
      (herramienta.criterios || []).forEach(c => {
        html += `<tr><td><strong>${c.criterio}</strong></td>${(c.descriptores || []).map(d => `<td>${d}</td>`).join('')}</tr>`;
      });
      html += '</tbody></table>';
    } else if (herramienta.tipo === 'lista_cotejo') {
      html += `<table><thead><tr><th>Indicador</th><th>Sí</th><th>No</th><th>Observaciones</th></tr></thead><tbody>`;
      (herramienta.indicadores || []).forEach(i => {
        html += `<tr><td>${i.indicador}</td><td>□</td><td>□</td><td></td></tr>`;
      });
      html += '</tbody></table>';
    } else if (herramienta.tipo === 'guia_correccion') {
      html += `<table><thead><tr><th>Apartado</th><th>Criterios</th><th>Puntuación</th><th>Obs.</th></tr></thead><tbody>`;
      (herramienta.apartados || []).forEach(a => {
        html += `<tr><td>${a.apartado}</td><td>${a.criterios}</td><td>${a.puntuacion}</td><td></td></tr>`;
      });
      html += '</tbody></table>';
    } else if (herramienta.tipo === 'ficha_autoevaluacion') {
      (herramienta.preguntas || []).forEach(p => {
        html += `<p><strong>${p.pregunta}</strong></p><p style="border-bottom:1px solid #ccc;min-height:3em"></p>`;
      });
    } else if (herramienta.tipo === 'ficha_coevaluacion') {
      html += `<p><strong>Alumno/a evaluado/a:</strong> ___________________ &nbsp;&nbsp; <strong>Evaluador/a:</strong> ___________________</p>`;
      html += `<table><thead><tr><th>Aspecto</th><th>Comentario positivo</th><th>Sugerencia</th><th>Evidencia</th><th>Valoración</th></tr></thead><tbody>`;
      (herramienta.aspectos || []).forEach(a => {
        html += `<tr><td>${a.aspecto}</td><td></td><td></td><td></td><td></td></tr>`;
      });
      html += '</tbody></table>';
    }
    return html;
  }

  _notificar(msg) {
    const el = document.createElement('div');
    el.textContent = msg;
    el.style.cssText = 'position:fixed;bottom:20px;right:20px;background:#2471a3;color:white;padding:8px 16px;border-radius:6px;z-index:9999;font-size:0.9em;box-shadow:0 2px 8px rgba(0,0,0,0.3)';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2500);
  }
}

window.Exporter = Exporter;
