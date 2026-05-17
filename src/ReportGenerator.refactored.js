// ── Constantes de negócio ──────────────────────────────────────────────────
const PRIORITY_THRESHOLD   = 1000;
const USER_VALUE_THRESHOLD = 500;

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

// ── Lógica de negócio ──────────────────────────────────────────────────────

function isItemVisibleToUser(item, user) {
  if (user.role === 'ADMIN') return true;
  if (user.role === 'USER')  return item.value <= USER_VALUE_THRESHOLD;
  return false;
}

function applyBusinessRules(item, user) {
  const clone = { ...item };
  if (user.role === 'ADMIN' && clone.value > PRIORITY_THRESHOLD) {
    clone.priority = true;
  }
  return clone;
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

    for (const rawItem of items) {
      if (!isItemVisibleToUser(rawItem, user)) continue;

      const item = applyBusinessRules(rawItem, user);
      report += formatter.formatItem(item, user);
      total += item.value;
    }

    report += formatter.footer(total);
    return report.trim();
  }
}
