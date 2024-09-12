from fpdf import FPDF

def generar_boleta(items, subtotal, iva, total):
    pdf = FPDF()
    pdf.add_page()

    # Título de la boleta
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Boleta de Venta', ln=True, align='C')

    # Espacio
    pdf.ln(10)

    # Encabezados de tabla
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(80, 10, 'Producto', border=1)
    pdf.cell(40, 10, 'Cantidad', border=1)
    pdf.cell(40, 10, 'Precio Unitario', border=1)
    pdf.cell(40, 10, 'Subtotal', border=1)
    pdf.ln()

    # Agregar productos
    pdf.set_font('Arial', '', 12)
    for item in items:
        pdf.cell(80, 10, item['nombre'], border=1)
        pdf.cell(40, 10, str(item['cantidad']), border=1)
        pdf.cell(40, 10, f"{item['precio_unitario']} CLP", border=1)
        pdf.cell(40, 10, f"{item['subtotal']} CLP", border=1)
        pdf.ln()

    # Espacio
    pdf.ln(10)

    # Subtotal, IVA y Total
    pdf.cell(160, 10, 'Subtotal:', border=0)
    pdf.cell(40, 10, f"{subtotal} CLP", border=1, ln=True)
    
    pdf.cell(160, 10, 'IVA (19%):', border=0)
    pdf.cell(40, 10, f"{iva} CLP", border=1, ln=True)

    pdf.cell(160, 10, 'Total:', border=0)
    pdf.cell(40, 10, f"{total} CLP", border=1, ln=True)

    # Guardar el PDF
    pdf.output('boleta.pdf')
    