import customtkinter as ctk
from tkinter import ttk
from PIL import Image

class Ingrediente: 
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad
    
    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"

class Menu:
    def __init__(self, nombre, ingredientes_necesarios, precio):
        self.nombre = nombre
        self.ingredientes_necesarios = ingredientes_necesarios
        self.precio = precio

class Pedido:
    def __init__(self):
        self.menus = []
        self.total = 0 
    
    def agregar_menu(self, menu, stock):
        if menu.ingredientes_suficientes(stock):
            menu.descontar_ingredientes(stock)
            self.menus.append(menu)
            self.total += menu.precio

    def eliminar_menu(self, menu, stock):
        if menu in self.menus:
            menu.reponer_ingredientes(stock)
            self.menus.remove(menu)
            self.total -= menu.precio

    def generar_boleta(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Boleta de Pedido", ln=True, align="C")

        for menu in self.menus:
            pdf.cell(200, 10, txt=f"Total: ${self.total}", ln=True)
            pdf.output("Boleta_pedido.pdf")

# Crear la ventana principal
ventana = ctk.CTk()
ventana.title("Sistema de Pedidos")
ventana.geometry("500x400")

# Establecer tema y tamaño de fuente
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Cargar las imágenes
icon_papas = ctk.CTkImage(Image.open("IMG/icono_papas_fritas_64x64.png"), size=(40, 40))
icon_bebida = ctk.CTkImage(Image.open("IMG/icono_cola_64x64.png"), size=(40, 40))
icon_hamburguesa = ctk.CTkImage(Image.open("IMG/icono_hamburguesa_negra_64x64.png"), size=(40, 40))
icon_completo = ctk.CTkImage(Image.open("IMG/icono_hotdog_sin_texto_64x64.png"), size=(40, 40))

# Variables para los productos
productos = {
    "Papas Fritas": {"precio": 1500, "cantidad": 0},
    "Bebida": {"precio": 1000, "cantidad": 0},
    "Hamburguesa": {"precio": 3000, "cantidad": 0},
    "Completo": {"precio": 2500, "cantidad": 0}
}

# Crear una tabla (Treeview) para mostrar el pedido
tabla = ttk.Treeview(ventana, columns=("Producto", "Cantidad", "Valor"), show="headings", height=8)
tabla.heading("Producto", text="Producto")
tabla.heading("Cantidad", text="Cantidad")
tabla.heading("Valor", text="Valor Total (CLP)")
tabla.pack(pady=10)

# Función para actualizar el pedido
def actualizar_pedido(producto):
    productos[producto]["cantidad"] += 1
    mostrar_pedido()

# Función para mostrar el pedido en la tabla y calcular el total
def mostrar_pedido():
    # Limpiar la tabla
    for row in tabla.get_children():
        tabla.delete(row)
    
    total_general = 0  # Inicializar el total general
    
    for producto, datos in productos.items():
        cantidad = datos["cantidad"]
        if cantidad > 0:
            valor = cantidad * datos["precio"]
            total_general += valor  # Sumar el valor de cada producto al total general
            tabla.insert("", "end", values=(producto, cantidad, valor))
    
    # Actualizar la etiqueta del total acumulado
    total_label.configure(text=f"Total: {total_general} CLP")

# Función para eliminar todos los productos
def eliminar_pedido():
    for producto in productos:
        productos[producto]["cantidad"] = 0
    mostrar_pedido()

# Función para generar la boleta
def generar_boleta():
    # Recolectar datos del pedido
    items = [
        {"nombre": producto, "cantidad": datos["cantidad"], "precio_unitario": datos["precio"], "subtotal": datos["cantidad"] * datos["precio"]}
        for producto, datos in productos.items() if datos["cantidad"] > 0
    ]
    
    subtotal = sum(item['subtotal'] for item in items)
    iva = subtotal * 0.19
    total = subtotal + iva
    
    # Pasar datos al script de generación de boletas
    subprocess.run(['python', 'generador_boleta.py', str(subtotal), str(iva), str(total)], check=True)

# Crear botones con íconos para cada producto
frame_botones = ctk.CTkFrame(ventana)
frame_botones.pack(pady=10)

ctk.CTkButton(frame_botones, image=icon_papas, text="Papas Fritas", command=lambda: actualizar_pedido("Papas Fritas"), width=200, height=40).grid(row=0, column=0, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_bebida, text="Bebida", command=lambda: actualizar_pedido("Bebida"), width=200, height=40).grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_hamburguesa, text="Hamburguesa", command=lambda: actualizar_pedido("Hamburguesa"), width=200, height=40).grid(row=1, column=0, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_completo, text="Completo", command=lambda: actualizar_pedido("Completo"), width=200, height=40).grid(row=1, column=1, padx=10, pady=10)

# Botón para eliminar el menú
eliminar_button = ctk.CTkButton(ventana, text="Eliminar Pedido", command=eliminar_pedido, fg_color="red")
eliminar_button.pack(pady=10)

# Botón para generar la boleta
generar_boleta_button = ctk.CTkButton(ventana, text="Generar Boleta", command=generar_boleta, fg_color="blue")
generar_boleta_button.pack(pady=10)

# Etiqueta para mostrar el total
total_label = ctk.CTkLabel(ventana, text="Total: 0 CLP", font=("Arial", 16))
total_label.pack(pady=10)

# Ejecutar la interfaz
ventana.mainloop()
