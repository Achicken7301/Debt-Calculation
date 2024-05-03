import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Sample DataFrames
dataframes = [
    pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}),
    pd.DataFrame({"X": [7, 8, 9], "Y": [10, 11, 12]}),
]

# Create PDF
pdf_filename = "output.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
styles = getSampleStyleSheet()

# Generate PDF content
content = []

for i, df in enumerate(dataframes):
    # Add title header
    title = Paragraph(f"<br/><b>Header {i+1}</b><br/>", styles["Heading1"])
    content.append(title)

    # Convert DataFrame to table
    table_data = [df.columns[:,].values.astype(str).tolist()] + df.values.tolist()
    table = Table(table_data)

    # Apply table style
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                ("TEXTCOLOR", (0, 0), (-1, 0), (0, 0, 0)),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), (0.85, 0.85, 0.85)),
                ("GRID", (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
            ]
        )
    )

    content.append(table)

    # Add space between tables
    content.append(Paragraph("<br/><br/>", styles["BodyText"]))

# Build PDF
doc.build(content)

print("PDF generated successfully.")
