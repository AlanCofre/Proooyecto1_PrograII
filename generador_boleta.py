from fpdf import FPDF
import os

def generar_boleta(items, subtotal, iva, total):
    pdf = FPDF()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Boleta de Venta", ln=True, align="C")
    pdf.ln(10)

    # Datos de la empresa
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Restaurante XYZ", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 10, txt="Dirección: Calle Falsa 123", ln=True, align="C")
    pdf.cell(200, 10, txt="Teléfono: 123-456-789", ln=True, align="C")
    pdf.ln(10)

    # Encabezados de la tabla
    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 10, txt="Producto", border=1, align="C")
    pdf.cell(30, 10, txt="Cantidad", border=1, align="C")
    pdf.cell(40, 10, txt="Precio Unitario", border=1, align="C")
    pdf.cell(40, 10, txt="Subtotal", border=1, align="C")
    pdf.ln()

    # Añadir los items a la boleta
    pdf.set_font("Arial", "", 10)
    for item in items:
        pdf.cell(80, 10, txt=item["nombre"], border=1)
        pdf.cell(30, 10, txt=str(item["cantidad"]), border=1, align="R")
        pdf.cell(40, 10, txt=f"${item['precio_unitario']}", border=1, align="R")
        pdf.cell(40, 10, txt=f"${item['subtotal']}", border=1, align="R")
        pdf.ln()

    # Añadir Subtotal, IVA, y Total
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, txt=f"Subtotal:", ln=True, align="R")
    pdf.cell(150, 10, txt=f"IVA (19%):", ln=True, align="R")
    pdf.cell(150, 10, txt=f"Total:", ln=True, align="R")

    pdf.set_font("Arial", "", 12)
    pdf.cell(150, 10, txt=f"${subtotal}", ln=True, align="R")
    pdf.cell(150, 10, txt=f"${iva}", ln=True, align="R")
    pdf.cell(150, 10, txt=f"${total}", ln=True, align="R")

    # Nota final
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, txt="¡Gracias por su compra!", ln=True, align="C")

    # Guardar el PDF
    pdf_output_path = "boleta.pdf"
    pdf.output(pdf_output_path)

    # Abrir el archivo PDF con el visor predeterminado del sistema operativo
    os.startfile(pdf_output_path)
