# Análise de Bad Smells — ReportGenerator.js

Arquivo analisado: `src/ReportGenerator.js` | Método: `generateReport` (linha 11-68)

---

## Smell 1 — Long Method (Método Longo)

**Localização:** `generateReport`, linhas 11-68 (~60 linhas).

**Evidência:** O método faz tudo: gera cabeçalho (linhas 16-24), processa corpo com loop (linhas 27-55), gera rodapé (linhas 58-65). Mistura lógica de negócio (filtragem por role) com lógica de formatação (CSV/HTML).

**Risco:** Impossível reutilizar a geração de cabeçalho sem arrastar o método inteiro. Um bug em qualquer parte compromete o todo.

**Técnica:** Extract Method → `generateHeader()`, `generateBody()`, `generateFooter()`.

---

## Smell 2 — High Cognitive Complexity (Complexidade Cognitiva Alta)

**Localização:** Aninhamento `for → if role → if format → if priority → if format`.

**Evidência:** SonarJS reporta complexidade **27** (threshold: 15). O cálculo manual aproxima 22, mas o algoritmo oficial conta incrementos de nesting adicionais.

```
for (items)                          → +1
  if (user.role === 'ADMIN')         → +2
    if (item.value > 1000)           → +3
    if (reportType === 'CSV')        → +3
    else if (reportType === 'HTML')  → +3
  else if (user.role === 'USER')     → +2
    if (item.value <= 500)           → +3
      if (reportType === 'CSV')      → +4
      else if (reportType === 'HTML')→ +4
```

**Erro adicional:** `sonarjs/no-collapsible-if` na linha 43 — `else if (user.role === 'USER') { if (item.value <= 500) }` pode ser colapsado.

**Risco:** 27 = muitos caminhos não testados. Alta probabilidade de bugs em caminhos raros.

**Técnica:** Decompose Conditional + Extract Method.

---

## Smell 3 — Duplicated Logic (Lógica Duplicada)

**Localização:** O bloco `if (reportType === 'CSV') ... else if (reportType === 'HTML')` aparece **4 vezes**: cabeçalho (linha 16), corpo ADMIN (linha 35), corpo USER (linha 46), rodapé (linha 58).

**Evidência:** A formatação de cada linha CSV (`${item.id},${item.name},${item.value},${user.name}\n`) se repete nas linhas 36 e 47.

**Risco:** Adicionar um novo formato (JSON) exige modificar 4 lugares. Alta probabilidade de inconsistência.

**Técnica:** Replace Conditional with Polymorphism → classes `CsvFormatter` e `HtmlFormatter`.

---

## Smell 4 — Magic Numbers (Números Mágicos)

**Localização:**
- Linha 30: `item.value > 1000` — limiar de prioridade ADMIN
- Linha 45: `item.value <= 500` — limiar de visibilidade USER

**Evidência:** Os valores `1000` e `500` aparecem sem contexto semântico.

**Risco:** Mudar o limiar exige buscar todas as ocorrências. Com duplicação, fácil esquecer uma.

**Técnica:** Introduce Explaining Constant → `PRIORITY_THRESHOLD`, `USER_VALUE_THRESHOLD`.

---

## Smell 5 — Divergent Change (Mudança Divergente)

**Localização:** `generateReport` muda por duas razões independentes:
1. Regra de negócio (filtragem por role, prioridade)
2. Formato de saída (CSV, HTML, futuro JSON)

**Evidência:** Lógica de negócio e formatação estão acopladas no mesmo método.

**Risco:** Viola SRP. Mudar um formato pode quebrar lógica de negócio e vice-versa.

**Técnica:** Extract Class → separar `ReportGenerator` (negócio) de formatadores (apresentação).

---

## Output do ESLint (npx eslint src/)

```
src/ReportGenerator.js
  11:3   error  Refactor this function to reduce its Cognitive Complexity from 27 to the 15 allowed  sonarjs/cognitive-complexity
  43:14  error  Merge this if statement with the nested one                                          sonarjs/no-collapsible-if

2 problems (2 errors, 0 warnings)
```
