from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_JUSTIFY

def generate_pdf(data_dict):
    # Create the PDF document
    c = SimpleDocTemplate('doc1.pdf', pagesize=landscape(A4), topMargin=0.4 * inch, bottomMargin=0.5 * inch)
    styles = getSampleStyleSheet()
    story = []

    # Header Section
    right_style = ParagraphStyle(name='Right', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=10)
    header_style = ParagraphStyle(name='HeaderStyle', parent=styles['Normal'], fontSize=10)

    header_data = [
        [Paragraph('The Regional Head', header_style),'',''],
        [Paragraph('Bank of Baroda', header_style), Paragraph('Branch Name: ', right_style), Paragraph(f'{data_dict["branch"]}', header_style)],
        [Paragraph(f"{data_dict['region']}", header_style), Paragraph('Date: ', right_style), Paragraph(f"{data_dict['date']}", header_style)],
    ]
    header_table = Table(header_data, colWidths=[5 * inch, 1.1 * inch, 4.9 * inch], rowHeights=[0.13 * inch, 0.13 * inch, 0.13 * inch])
    story.append(header_table)

    # Subject Line
    subject_style = ParagraphStyle(name='SubjectStyle', parent=styles['Normal'], leftIndent=4)
    lakh_style = ParagraphStyle(name='LakhStyle', parent=styles["Normal"], fontSize=7, alignment=TA_RIGHT, rightIndent=60)
    subject_data = [
        [Paragraph('<br />')],
        [Paragraph("Dear Madam/Sir,", header_style)],
        [Paragraph(f'Statement of Controllable Expenses under Profit and Loss Accounts for the Month of {data_dict["month_text"]} - {data_dict['year']}', subject_style)],
        [Paragraph('<br />')],
        [Paragraph('Rupees in Lakhs', lakh_style)]
    ]
    subject_table = Table(subject_data, colWidths=[11 * inch], rowHeights=[0.5 * inch, 0.14 * inch, 0.14 * inch, 0.14 * inch, 0.05 * inch])

    story.append(subject_table)

    # Table Data with fixed first 3 columns and dynamic other columns
    table_head_style = ParagraphStyle(name='TableHeadStyle', parent=styles["Normal"], fontSize=8, alignment=TA_CENTER)

    table_head_data = [
        [Paragraph('A', table_head_style), Paragraph('B', table_head_style), Paragraph('C', table_head_style), Paragraph('D', table_head_style),
         Paragraph('E', table_head_style), Paragraph('F', table_head_style), Paragraph('G', table_head_style), Paragraph('H', table_head_style),
         Paragraph('I', table_head_style), Paragraph('J', table_head_style)],
        [Paragraph("S.No.", table_head_style),
         Paragraph("Particulars", table_head_style),
         Paragraph("PL CODE", table_head_style),
         Paragraph(f"{data_dict['prev_to_prev_year']} Outstanding (Full Year)", table_head_style),
         Paragraph(f"{data_dict['prev_year']} Outstanding (Full Year)", table_head_style),
         Paragraph(f"Monthly Average up to {data_dict['current_year_month']} (E/12)", table_head_style),
         Paragraph(f"Expenditure of Current Month {data_dict['current_month']}", table_head_style),
         Paragraph("Increase/Decrease in Column 'G' over Column 'F'", table_head_style),
         Paragraph(f"Cumulative from {data_dict['start_date']} till Previous Month", table_head_style),
         Paragraph(f"Cumulative from {data_dict['start_date']} to current Month", table_head_style),
         Paragraph("Monthly Average of Cumulative (No of Month)", table_head_style)]
    ]

    table1 = Table(table_head_data, colWidths=[0.5 * inch, 2.5 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch,
                                               0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    story.append(table1)

    # Process the data for the table
    for row in data_dict["table_data"]:
        # The first three columns are fixed, so keep them as is
        row_data = row[:3]
        
        # The remaining columns are dynamic, so they can be added based on the form data
        for i in range(3, len(row)):
            row_data.append(Paragraph(f'{row[i]}', styles['Normal']))  # Add dynamic data as Paragraph

        row[:] = row_data  # Replace the original row data with the processed one

    # Adjust table style for dynamic data
    table_style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (1, 1), (1, -1), 'Mangal'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8)
    ])

    table = Table(data_dict["table_data"], colWidths=[0.5 * inch, 2.5 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch,
                                                     0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch])
    table.setStyle(table_style)
    story.append(table)

    story.append(Spacer(1, 10))

    # Justification
    just_body_style = ParagraphStyle(name='JustBodyStyle', parent=styles["Normal"], alignment=TA_JUSTIFY)

    justification_data = [
        ["Note: If % increase in Column 'G' is more than 10% please give reasons to avoid further correspondence.", ""],
        ["Justification", Paragraph(f"{data_dict['justification']}", just_body_style)]
    ]

    justification_table = Table(justification_data, colWidths=[2 * inch, 8 * inch], rowHeights=[0.2 * inch, 0.7 * inch])

    justification_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
        ('SPAN', (0, 0), (1, 0)),
        ('FONTSIZE', (0, 0), (0, -1), 8)
    ])

    justification_table.setStyle(justification_style)

    story.append(justification_table)

    story.append(Spacer(1, 70))

    # Footer
    footer_data = [[Paragraph(f"Place: {data_dict['place']}", styles['Normal']), Paragraph("(Branch Head)", styles['Normal'])]]
    footer_table = Table(footer_data, colWidths=[5 * inch, 5 * inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 6)
    ]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(footer_table)

    # Build the document
    c.build(story)
