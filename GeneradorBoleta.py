import json
from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(200, 10, 'Boleta Restaurante', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-30)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Gracias por su compra. Para cualquier consulta, llámenos al +56 9 1234 5678.', 0, 1, 'C')

    def add_info_empresa(self, nombre_restaurante, rut, direccion, telefono):
        self.set_font('Arial', '', 10)
        self.cell(100, 10, f'Razón Social del Negocio: {nombre_restaurante}', ln=True)
        self.cell(100, 10, f'RUT: {rut}', ln=True)
        self.cell(100, 10, f'Dirección: {direccion}', ln=True)
        self.cell(100, 10, f'Teléfono: {telefono}', ln=True)

    def add_fecha(self):
        self.cell(0, 10, f'Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', ln=True, align='R')
        self.ln(10)

    def add_table_header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(60, 10, 'Nombre', 1)
        self.cell(40, 10, 'Cantidad', 1)
        self.cell(40, 10, 'Precio Unitario', 1)
        self.cell(40, 10, 'Subtotal', 1)
        self.ln()

    def add_item(self, nombre, cantidad, precio_unitario, subtotal):
        self.set_font('Arial', '', 10)
        self.cell(60, 10, nombre, 1)
        self.cell(40, 10, f'{cantidad}', 1, align='C')
        self.cell(40, 10, f'${precio_unitario:.2f}', 1, align='R')
        self.cell(40, 10, f'${subtotal:.2f}', 1, align='R')
        self.ln()

    def add_totales(self, subtotal, iva, total):
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        self.cell(140, 10, 'Subtotal:', 0, 0, 'R')
        self.cell(40, 10, f'${subtotal:.2f}', 1, 1, 'R')
        self.cell(140, 10, f'IVA (19%):', 0, 0, 'R')
        self.cell(40, 10, f'${iva:.2f}', 1, 1, 'R')
        self.cell(140, 10, 'Total:', 0, 0, 'R')
        self.cell(40, 10, f'${total:.2f}', 1, 1, 'R')

# Leer datos del archivo JSON
with open('data_boleta.json', 'r') as f:
    data = json.load(f)

items = data['items']
subtotal = data['subtotal']
iva = data['iva']
total = data['total']

# Datos de ejemplo (puedes modificar estos datos según tu empresa)
nombre_restaurante = "Mi Restaurante"
rut = "12345678-9"
direccion = "Calle Falsa 123"
telefono = "+56 9 1234 5678"

# Crear el PDF
pdf = PDF()
pdf.add_page()

# Agregar información del restaurante
pdf.add_info_empresa(nombre_restaurante, rut, direccion, telefono)

# Agregar fecha
pdf.add_fecha()

# Agregar tabla de productos
pdf.add_table_header()
for item in items:
    pdf.add_item(item['nombre'], item['cantidad'], item['precio_unitario'], item['subtotal'])

# Agregar totales
pdf.add_totales(subtotal, iva, total)

# Guardar el PDF
pdf.output('recibo_restaurante.pdf')

print("Recibo generado correctamente.")
