from fpdf import FPDF
import os

def generar_boleta(items, subtotal, iva, total):
    pdf = FPDF()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Boleta de Venta", ln=True, align="C")

    # Encabezados de la tabla
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 10, txt="Producto", border=1)
    pdf.cell(40, 10, txt="Cantidad", border=1)
    pdf.cell(50, 10, txt="Precio Unitario", border=1)
    pdf.cell(40, 10, txt="Subtotal", border=1)
    pdf.ln()

    # Añadir los items a la boleta
    pdf.set_font("Arial", "", 12)
    for item in items:
        pdf.cell(60, 10, txt=item["nombre"], border=1)
        pdf.cell(40, 10, txt=str(item["cantidad"]), border=1)
        pdf.cell(50, 10, txt=f"${item['precio_unitario']}", border=1)
        pdf.cell(40, 10, txt=f"${item['subtotal']}", border=1)
        pdf.ln()

    # Añadir Subtotal, IVA, y Total
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Subtotal: ${subtotal}", ln=True, align="R")
    pdf.cell(200, 10, txt=f"IVA (19%): ${iva}", ln=True, align="R")
    pdf.cell(200, 10, txt=f"Total: ${total}", ln=True, align="R")

    # Guardar el PDF
    pdf_output_path = "boleta.pdf"
    pdf.output(pdf_output_path)

    # Abrir el archivo PDF con el visor predeterminado del sistema operativo
    os.startfile(pdf_output_path)
