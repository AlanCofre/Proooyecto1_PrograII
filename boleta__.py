from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Boleta Restaurante', 0, 1, 'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Pagina %s' % self.page_no(), 0, 0, 'C')

pdf = PDF()

# Agregar página
pdf.add_page()

# Título
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Boleta Restaurante', 0, 1, 'C')

# Datos de la empresa
pdf.set_font('Arial', '', 10)
pdf.cell(0, 10, 'Razon Social del Negocio: 12345678-9', 0, 1, 'L')
pdf.cell(0, 10, 'Direccion: Calle Falsa 123', 0, 1, 'L')
pdf.cell(0, 10, 'Telefono: +56 9 1234 5678', 0, 1, 'L')

# Fecha
pdf.cell(0, 10, 'Fecha: 22/08/2024 16:47:17', 0, 1, 'L')

# Espacio
pdf.ln(10)

# Tabla de productos
pdf.set_font('Arial', 'B', 10)
pdf.cell(40, 10, 'Nombre', 1)
pdf.cell(30, 10, 'Cantidad', 1)
pdf.cell(50, 10, 'Precio Unitario', 1)
pdf.cell(50, 10, 'Subtotal', 1)
pdf.ln()

# Esta sección queda vacía para rellenar con los productos más adelante
productos = []  # Lista vacía para ser rellenada luego
for producto in productos:
    pdf.cell(40, 10, producto[0], 1)
    pdf.cell(30, 10, str(producto[1]), 1)
    pdf.cell(50, 10, f'${producto[2]:,.2f}', 1)
    pdf.cell(50, 10, f'${producto[3]:,.2f}', 1)
    pdf.ln()

# Subtotal, IVA y Total
subtotal = 0  # Subtotal vacio, para modificar luego
iva = 0       # IVA vacío, para modificar luego
total = 0     # Total vacío, para modificar luego

pdf.ln(10)
pdf.cell(0, 10, f'Subtotal: ${subtotal:,.2f}', 0, 1, 'R')
pdf.cell(0, 10, f'IVA (19%): ${iva:,.2f}', 0, 1, 'R')
pdf.cell(0, 10, f'Total: ${total:,.2f}', 0, 1, 'R')

# Mensaje final
pdf.ln(10)
pdf.cell(0, 10, 'Gracias por su compra. Para cualquier consulta, llamenos al +56 9 1234 5678', 0, 1, 'C')
pdf.cell(0, 10, 'Los productos adquiridos no tienen garantia.', 0, 1, 'C')

# Guardar PDF
pdf.output('/mnt/data/boleta_restaurante_vacio.pdf')