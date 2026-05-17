// ── Formatadores (Replace Conditional with Polymorphism) ──────────────────

class CsvFormatter {
  header(_user) {
    return 'ID,NOME,VALOR,USUARIO\n';
  }

  formatItem(item, user) {
    return `${item.id},${item.name},${item.value},${user.name}\n`;
  }

  footer(total) {
    return `\nTotal,,\n${total},,`;
  }
}

class HtmlFormatter {
  header(user) {
    return [
      '<html><body>',
      '<h1>Relatório</h1>',
      `<h2>Usuário: ${user.name}</h2>`,
      '<table>',
      '<tr><th>ID</th><th>Nome</th><th>Valor</th></tr>',
    ].join('\n') + '\n';
  }

  formatItem(item, _user) {
    const style = item.priority ? ' style="font-weight:bold;"' : '';
    return `<tr${style}><td>${item.id}</td><td>${item.name}</td><td>${item.value}</td></tr>\n`;
  }

  footer(total) {
    return `</table>\n<h3>Total: ${total}</h3>\n</body></html>`;
  }
}

// ── Seletor de formatador ──────────────────────────────────────────────────

function getFormatter(reportType) {
  if (reportType === 'CSV')  return new CsvFormatter();
  if (reportType === 'HTML') return new HtmlFormatter();
  throw new Error(`Formato desconhecido: ${reportType}`);
}

// ── ReportGenerator refatorado ────────────────────────────────────────────

export class ReportGenerator {
  constructor(database) {
    this.db = database;
  }

  generateReport(reportType, user, items) {
    const formatter = getFormatter(reportType);
    let report = formatter.header(user);
    let total = 0;

    for (const item of items) {
      if (user.role === 'ADMIN') {
        if (item.value > 1000) {
          item.priority = true;
        }
        report += formatter.formatItem(item, user);
        total += item.value;
      } else if (user.role === 'USER') {
        if (item.value <= 500) {
          report += formatter.formatItem(item, user);
          total += item.value;
        }
      }
    }

    report += formatter.footer(total);
    return report.trim();
  }
}
