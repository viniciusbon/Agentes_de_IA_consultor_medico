from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def gerar_laudo_pdf(caminho_arquivo: str):
    """
    Gera um PDF de laudo de exame com estilo mais profissional.
    """
    doc = SimpleDocTemplate(caminho_arquivo, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # Estilos customizados
    titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], alignment=1, fontSize=16, spaceAfter=20)
    subtitulo = ParagraphStyle('Subtitulo', parent=styles['Heading2'], alignment=0, textColor=colors.HexColor("#004080"))
    normal_central = ParagraphStyle('Central', parent=styles['Normal'], alignment=1, fontSize=10, textColor=colors.grey)

    # --- Cabeçalho ---
    try:
        logo = Image("logo.png", width=3*cm, height=3*cm)  # se tiver um logo
        story.append(logo)
    except:
        pass
    story.append(Paragraph("Laboratório Vida & Saúde", titulo))
    story.append(Paragraph("<b>Paciente:</b> Fulano da Silva (Exemplo)", styles['Normal']))
    story.append(Paragraph("<b>Médico(a):</b> Dr(a). Ciclana Costa", styles['Normal']))
    story.append(Paragraph("<b>Data da Coleta:</b> 25/09/2025", styles['Normal']))
    story.append(Spacer(1, 1*cm))
    
    # --- Título da Seção ---
    story.append(Paragraph("Resultados de Exames Bioquímicos", subtitulo))
    story.append(Spacer(1, 0.5*cm))

    # --- Dados da Tabela ---
    dados = [
        ['Exame', 'Resultado', 'Unidade', 'Valores de Referência'],
        ['Hemoglobina', '15.1', 'g/dL', '13.5 - 17.5'],
        ['Hematócrito', '45', '%', '41 - 53'],
        ['Leucócitos', '3.800', '/mm³', '4.500 - 11.000'],  # Baixo
        ['Plaquetas', '250.000', '/mm³', '150.000 - 450.000'],
        ['Glicose', '115', 'mg/dL', '70 - 99'],             # Alto
        ['Colesterol Total', '220', 'mg/dL', '< 200'],      # Alto
        ['Triglicerídeos', '140', 'mg/dL', '< 150'],
        ['Creatinina', '1.1', 'mg/dL', '0.6 - 1.2']
    ]
    
    tabela = Table(dados, colWidths=[5*cm, 3*cm, 3*cm, 5*cm])

    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004080")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F5F5F5")),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.grey)
    ])

    tabela.setStyle(estilo_tabela)

    # --- Destacar resultados fora do intervalo ---
    destaques = {
        "Leucócitos": colors.red,
        "Glicose": colors.red,
        "Colesterol Total": colors.red
    }
    for i, linha in enumerate(dados[1:], start=1):
        if linha[0] in destaques:
            tabela.setStyle([('TEXTCOLOR', (1, i), (1, i), destaques[linha[0]])])

    story.append(tabela)
    story.append(Spacer(1, 2*cm))

    # --- Rodapé ---
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("________________________", styles['Normal']))
    story.append(Paragraph("Assinatura do Responsável Técnico", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Este laudo é confidencial e de uso exclusivo do paciente.", normal_central))

    # --- Gera o PDF ---
    doc.build(story)
    print(f"PDF '{caminho_arquivo}' gerado com sucesso!")


if __name__ == "__main__":
    gerar_laudo_pdf("Exame.pdf")
