from fpdf import FPDF


def generate_report():

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )

    pdf.cell(
        200,
        10,
        txt="AI Job Report",
        ln=True
    )

    pdf.output("report.pdf")