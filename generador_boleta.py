from fpdf import FPDF

# Datos del pedido (puedes importar estos datos o definirlos aquí)
productos = {
    "Papas Fritas": {"precio": 1500, "cantidad": 0},
    "Bebida": {"precio": 1000, "cantidad": 0},
    "Hamburguesa": {"precio": 3000, "cantidad": 0},
    "Completo": {"precio": 2500, "cantidad": 0}
}

def generar_boleta():
    # Recolectar datos del pedido
    items = [
        {"nombre": producto, "cantidad": datos["cantidad"], "precio_unitario": datos["precio"], "subtotal": datos["cantidad"] * datos["precio"]}
        for producto, datos in productos.items() if datos["cantidad"] > 0
    ]
    
    subtotal = sum(item['subtotal'] for item in items)
    iva = subtotal * 0.19
    total = subtotal + iva
    
    # Crear el PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.cell(200, 10, txt="Boleta de Pedido", ln=True, align="C")
    
    # Detalles del pedido
    pdf.ln(10)  # Espacio
    pdf.cell(100, 10, txt="Producto", border=1)
    pdf.cell(30, 10, txt="Cantidad", border=1)
    pdf.cell(30, 10, txt="Subtotal", border=1)
    pdf.ln()
    
    for item in items:
        pdf.cell(100, 10, txt=item["nombre"], border=1)
        pdf.cell(30, 10, txt=str(item["cantidad"]), border=1)
        pdf.cell(30, 10, txt=f"${item['subtotal']}", border=1)
        pdf.ln()
    
    pdf.ln(10)  # Espacio
    pdf.cell(100, 10, txt="Subtotal", border=1)
    pdf.cell(30, 10, txt=f"${subtotal}", border=1)
    pdf.ln()
    
    pdf.cell(100, 10, txt="IVA (19%)", border=1)
    pdf.cell(30, 10, txt=f"${iva:.2f}", border=1)
    pdf.ln()
    
    pdf.cell(100, 10, txt="Total", border=1)
    pdf.cell(30, 10, txt=f"${total:.2f}", border=1)
    
    # Guardar el PDF
    pdf.output("Boleta_pedido.pdf")
    print("Boleta generada exitosamente.")

if __name__ == "__main__":
    generar_boleta()
