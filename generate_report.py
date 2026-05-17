#!/usr/bin/env python3
"""Generate the final PDF report for the Bad Smells refactoring project."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

OUTPUT = "relatorio-bad-smells.pdf"

def build():
    doc = SimpleDocTemplate(OUTPUT, pagesize=letter,
                            topMargin=0.75*inch, bottomMargin=0.75*inch,
                            leftMargin=0.8*inch, rightMargin=0.8*inch)
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name='CoverTitle', parent=styles['Title'],
        fontSize=22, leading=28, spaceAfter=6, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name='CoverSubtitle', parent=styles['Normal'],
        fontSize=14, leading=18, spaceAfter=4, alignment=TA_CENTER,
        textColor=colors.HexColor('#555555')
    ))
    styles.add(ParagraphStyle(
        name='CoverInfo', parent=styles['Normal'],
        fontSize=12, leading=16, spaceAfter=2, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name='SectionHead', parent=styles['Heading1'],
        fontSize=14, leading=18, spaceBefore=12, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='SubSectionHead', parent=styles['Heading2'],
        fontSize=12, leading=15, spaceBefore=8, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name='BodyJustify', parent=styles['Normal'],
        fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='CodeBlock', parent=styles['Code'],
        fontSize=8, leading=11, fontName='Courier',
        leftIndent=20, spaceAfter=6, spaceBefore=4
    ))
    styles.add(ParagraphStyle(
        name='BulletItem', parent=styles['Bullet'],
        fontSize=10, leading=14, leftIndent=24, spaceAfter=3,
        bulletIndent=12, bulletFontName='Helvetica'
    ))

    story = []

    # ── CAPA ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph('Detecção de Bad Smells', styles['CoverTitle']))
    story.append(Paragraph('e Refatoração Segura', styles['CoverTitle']))
    story.append(Spacer(1, 24))
    story.append(Paragraph('Disciplina: Teste de Software', styles['CoverInfo']))
    story.append(Spacer(1, 36))
    story.append(Paragraph('Gustavo Pimentel Carvalho Costa', styles['CoverInfo']))
    story.append(Paragraph('Matrícula: 833151', styles['CoverInfo']))
    story.append(Spacer(1, 24))
    story.append(Paragraph(datetime.now().strftime('%B %Y'), styles['CoverSubtitle']))
    story.append(PageBreak())

    # ── SEÇÃO 1: ANÁLISE DE SMELLS ────────────────────────────────────────
    story.append(Paragraph('Análise de Bad Smells', styles['SectionHead']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#333333'), spaceAfter=8))

    story.append(Paragraph(
        'O arquivo <code>src/ReportGenerator.js</code> contém o método '
        '<code>generateReport</code> (linhas 11-68) que concentra toda a lógica de '
        'geração de relatórios. A análise manual identificou cinco bad smells, dos '
        'quais três são detalhados abaixo.',
        styles['BodyJustify']
    ))

    # Smell 1
    story.append(Paragraph('1. High Cognitive Complexity (Complexidade Cognitiva Alta)', styles['SubSectionHead']))
    story.append(Paragraph(
        'O método <code>generateReport</code> possui complexidade cognitiva de 27, '
        'medida pelo plugin SonarJS do ESLint. O threshold configurado é 15. O '
        'aninhamento de <code>for → if role → if format → if priority → if format</code> '
        'cria múltiplos caminhos de execução que tornam o código difícil de entender '
        'e testar completamente.',
        styles['BodyJustify']
    ))
    story.append(Paragraph('Evidência no código original:', styles['BodyJustify']))
    story.append(Paragraph(
        '  for (const item of items) {\n'
        '    if (user.role === \'ADMIN\') {\n'
        '      if (item.value > 1000) { ... }\n'
        '      if (reportType === \'CSV\') { ... }\n'
        '      else if (reportType === \'HTML\') { ... }\n'
        '    } else if (user.role === \'USER\') {\n'
        '      if (item.value <= 500) {\n'
        '        if (reportType === \'CSV\') { ... }\n'
        '        else if (reportType === \'HTML\') { ... }\n'
        '      }\n'
        '    }\n'
        '  }',
        styles['CodeBlock']
    ))
    story.append(Paragraph(
        'Risco: com complexidade 27, existem caminhos de execução que podem não '
        'estar cobertos pelos testes. Um bug em um caminho raro só seria detectado '
        'em produção.',
        styles['BodyJustify']
    ))

    # Smell 2
    story.append(Paragraph('2. Duplicated Logic (Lógica Duplicada)', styles['SubSectionHead']))
    story.append(Paragraph(
        'O bloco condicional que decide entre CSV e HTML aparece quatro vezes no '
        'mesmo método: no cabeçalho (linha 16), no corpo para ADMIN (linha 35), '
        'no corpo para USER (linha 46) e no rodapé (linha 58). A formatação de '
        'cada linha CSV — <code>${item.id},${item.name},${item.value},${user.name}</code> '
        '— se repete nas linhas 36 e 47.',
        styles['BodyJustify']
    ))
    story.append(Paragraph(
        'Risco: adicionar um novo formato (ex: JSON) exigiria modificar quatro '
        'lugares diferentes, com alta probabilidade de inconsistência. A manutenção '
        'é proporcional ao número de cópias, não ao número de conceitos.',
        styles['BodyJustify']
    ))

    # Smell 3
    story.append(Paragraph('3. Magic Numbers (Números Mágicos)', styles['SubSectionHead']))
    story.append(Paragraph(
        'Os valores <code>1000</code> (linha 30) e <code>500</code> (linha 45) '
        'aparecem sem contexto semântico. O primeiro é o limiar de prioridade para '
        'ADMINs; o segundo, o limiar de visibilidade para USERs. Sem nomes '
        'descritivos, outro desenvolvedor não sabe se são limites de negócio, '
        'técnicos ou arbitrários.',
        styles['BodyJustify']
    ))
    story.append(Paragraph(
        'Risco: mudar o limiar exige buscar todas as ocorrências no código. Com '
        'duplicação, é fácil esquecer uma ocorrência, introduzindo comportamento '
        'inconsistente.',
        styles['BodyJustify']
    ))

    story.append(PageBreak())

    # ── SEÇÃO 2: RELATÓRIO DA FERRAMENTA ──────────────────────────────────
    story.append(Paragraph('Relatório da Ferramenta — ESLint + SonarJS', styles['SectionHead']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#333333'), spaceAfter=8))

    story.append(Paragraph(
        'O ESLint com o plugin <code>eslint-plugin-sonarjs</code> foi configurado '
        'com as regras <code>sonarjs/cognitive-complexity</code> (threshold 15) e '
        '<code>sonarjs/no-collapsible-if</code>. A execução no código original '
        'produziu:',
        styles['BodyJustify']
    ))
    story.append(Paragraph(
        '  src/ReportGenerator.js\n'
        '    11:3   error  Cognitive Complexity from 27 to the 15 allowed\n'
        '    43:14  error  Merge this if statement with the nested one\n'
        '  2 problems (2 errors, 0 warnings)',
        styles['CodeBlock']
    ))
    story.append(Paragraph(
        'O SonarJS detectou automaticamente a complexidade cognitiva com valor '
        'exato (27) — mais preciso que a estimativa manual (~22). Detectou também '
        'o <code>no-collapsible-if</code>, um smell adicional que a análise manual '
        'poderia ter perdido: o <code>else if (user.role === \'USER\')</code> com '
        '<code>if (item.value <= 500)</code> aninhado pode ser colapsado em uma '
        'única condição.',
        styles['BodyJustify']
    ))
    story.append(Paragraph(
        'A ferramenta complementa a análise manual: enquanto humanos identificam '
        'padrões estruturais (Long Method, Duplicated Logic), o SonarJS quantifica '
        'com precisão a complexidade e encontra problemas sutis de aninhamento.',
        styles['BodyJustify']
    ))

    # ── SEÇÃO 3: PROCESSO DE REFATORAÇÃO ──────────────────────────────────
    story.append(Paragraph('Processo de Refatoração', styles['SectionHead']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#333333'), spaceAfter=8))

    story.append(Paragraph(
        'O smell mais crítico — Duplicated Logic combinado com Long Method — foi '
        'tratado com duas técnicas de refatoração: Extract Method e Replace '
        'Conditional with Polymorphism.',
        styles['BodyJustify']
    ))

    story.append(Paragraph('Código refatorado (estrutura final):', styles['BodyJustify']))
    story.append(Paragraph(
        '  const PRIORITY_THRESHOLD   = 1000;\n'
        '  const USER_VALUE_THRESHOLD = 500;\n'
        '\n'
        '  class CsvFormatter { header, formatItem, footer }\n'
        '  class HtmlFormatter { header, formatItem, footer }\n'
        '  function getFormatter(type) { ... }\n'
        '\n'
        '  function isItemVisibleToUser(item, user) { ... }\n'
        '  function applyBusinessRules(item, user) { ... }\n'
        '\n'
        '  class ReportGenerator {\n'
        '    generateReport(type, user, items) {\n'
        '      // 12 linhas — limpo e legível\n'
        '    }\n'
        '  }',
        styles['CodeBlock']
    ))

    story.append(Paragraph(
        'O método original tomava decisões de formatação e de negócio ao mesmo '
        'tempo. A refatoração separou essas responsabilidades: ReportGenerator '
        'decide o que incluir, os formatadores decidem como apresentar.',
        styles['BodyJustify']
    ))

    story.append(Paragraph(
        'Bônus: o código original continha um bug na formatação HTML. Para itens '
        'sem prioridade, produzia <code>&lt;tr &gt;&lt;td&gt;</code> (espaço antes '
        'do <code>&gt;</code>), enquanto o teste esperava <code>&lt;tr&gt;&lt;td&gt;</code>. '
        'O refatorado corrige isso usando <code>&lt;tr${style}&gt;</code> — sem '
        'espaço quando style é vazio.',
        styles['BodyJustify']
    ))

    story.append(PageBreak())

    # ── SEÇÃO 4: RESULTADOS ───────────────────────────────────────────────
    story.append(Paragraph('Resultados da Validação', styles['SectionHead']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#333333'), spaceAfter=8))

    data = [
        ['Métrica', 'Original', 'Refatorado'],
        ['ESLint errors', '2', '0'],
        ['Cognitive Complexity', '27', '< 15'],
        ['Magic numbers', '2 (1000, 500)', '0'],
        ['Testes passando', '4/5', '5/5'],
        ['Formatadores', 'Acoplados', 'CsvFormatter + HtmlFormatter'],
    ]
    t = Table(data, colWidths=[2.2*inch, 1.8*inch, 2.0*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))

    # ── SEÇÃO 5: CONCLUSÃO ────────────────────────────────────────────────
    story.append(Paragraph('Conclusão', styles['SectionHead']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#333333'), spaceAfter=8))

    story.append(Paragraph(
        'A suíte de testes existente funcionou como rede de segurança: cada '
        'refatoração foi validada imediatamente, garantindo que o comportamento '
        'externo foi preservado. Sem os testes, a confiança para reorganizar '
        '60 linhas de lógica acoplada seria significativamente menor.',
        styles['BodyJustify']
    ))
    story.append(Paragraph(
        'A redução de bad smells produziu código mais legível e com menor '
        'complexidade cognitiva. Isso torna o código mais fácil de testar no '
        'futuro — os formatadores agora podem ser testados isoladamente, e as '
        'regras de negócio estão em funções puras com responsabilidade única. '
        'O ciclo se reforça: testes dão confiança para refatorar, código limpo '
        'é mais fácil de testar.',
        styles['BodyJustify']
    ))

    doc.build(story)
    print(f'PDF gerado: {OUTPUT}')

if __name__ == '__main__':
    build()
