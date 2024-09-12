import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from Ingredientes import Ingrediente
from Menus import Menu

# Crear la ventana principal
ventana = ctk.CTk()
ventana.title("Sistema de Gestión de Pedidos")
ventana.geometry("800x600")

# Establecer tema y tamaño de fuente
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Crear el Notebook para las pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill='both')

# Pestaña de Gestión de Ingredientes
pestaña_ingredientes = ttk.Frame(notebook)
notebook.add(pestaña_ingredientes, text="Gestión de Ingredientes")

# Pestaña de Venta de Menús
pestaña_menus = ttk.Frame(notebook)
notebook.add(pestaña_menus, text="Venta de Menús")

# --- Pestaña de Gestión de Ingredientes ---
# Crear una tabla (Treeview) para mostrar los ingredientes
tabla_ingredientes = ttk.Treeview(pestaña_ingredientes, columns=("Nombre", "Cantidad"), show="headings", height=15)
tabla_ingredientes.heading("Nombre", text="Nombre")
tabla_ingredientes.heading("Cantidad", text="Cantidad")
tabla_ingredientes.pack(pady=10)

# Variables para los ingredientes
ingredientes = []

# Función para agregar un ingrediente
def agregar_ingrediente():
    nombre = nombre_entry.get()
    cantidad = cantidad_entry.get()
    if nombre and cantidad.isdigit():
        cantidad = int(cantidad)
        ingrediente = Ingrediente(nombre, cantidad)
        ingredientes.append(ingrediente)
        mostrar_ingredientes()
        nombre_entry.delete(0, 'end')
        cantidad_entry.delete(0, 'end')

# Función para eliminar un ingrediente
def eliminar_ingrediente():
    selected_item = tabla_ingredientes.selection()
    if selected_item:
        item_values = tabla_ingredientes.item(selected_item)['values']
        nombre = item_values[0]
        global ingredientes
        ingredientes = [i for i in ingredientes if i.nombre != nombre]
        mostrar_ingredientes()

# Función para mostrar los ingredientes en la tabla
def mostrar_ingredientes():
    # Limpiar la tabla
    for row in tabla_ingredientes.get_children():
        tabla_ingredientes.delete(row)
    
    # Insertar los ingredientes en la tabla
    for ingrediente in ingredientes:
        tabla_ingredientes.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

# Crear un frame para los controles de agregar ingredientes
frame_agregar = ctk.CTkFrame(pestaña_ingredientes)
frame_agregar.pack(pady=10)

# Entrada para nombre del ingrediente
nombre_label = ctk.CTkLabel(frame_agregar, text="Nombre del Ingrediente:")
nombre_label.grid(row=0, column=0, padx=10, pady=5)
nombre_entry = ctk.CTkEntry(frame_agregar)
nombre_entry.grid(row=0, column=1, padx=10, pady=5)

# Entrada para cantidad del ingrediente
cantidad_label = ctk.CTkLabel(frame_agregar, text="Cantidad:")
cantidad_label.grid(row=1, column=0, padx=10, pady=5)
cantidad_entry = ctk.CTkEntry(frame_agregar)
cantidad_entry.grid(row=1, column=1, padx=10, pady=5)

# Botón para agregar ingrediente
agregar_button = ctk.CTkButton(frame_agregar, text="Agregar Ingrediente", command=agregar_ingrediente)
agregar_button.grid(row=2, columnspan=2, pady=10)

# Botón para eliminar ingrediente
eliminar_button = ctk.CTkButton(pestaña_ingredientes, text="Eliminar Ingrediente", command=eliminar_ingrediente, fg_color="red")
eliminar_button.pack(pady=10)

# --- Pestaña de Venta de Menús ---
# Crear la tabla (Treeview) para mostrar el pedido
tabla_menus = ttk.Treeview(pestaña_menus, columns=("Producto", "Cantidad", "Valor"), show="headings", height=8)
tabla_menus.heading("Producto", text="Producto")
tabla_menus.heading("Cantidad", text="Cantidad")
tabla_menus.heading("Valor", text="Valor Total (CLP)")
tabla_menus.pack(pady=10)

# Variables para los productos
productos = {
    "Papas Fritas": {"precio": 500, "cantidad": 0},
    "Bebida": {"precio": 1100, "cantidad": 0},
    "Hamburguesa": {"precio": 3500, "cantidad": 0},
    "Completo": {"precio": 1800, "cantidad": 0}
}

# Función para actualizar el pedido
def actualizar_pedido(producto):
    productos[producto]["cantidad"] += 1
    mostrar_pedido()

# Función para mostrar el pedido en la tabla y calcular el total
def mostrar_pedido():
    # Limpiar la tabla
    for row in tabla_menus.get_children():
        tabla_menus.delete(row)
    
    total_general = 0  # Inicializar el total general
    
    for producto, datos in productos.items():
        cantidad = datos["cantidad"]
        if cantidad > 0:
            valor = cantidad * datos["precio"]
            total_general += valor  # Sumar el valor de cada producto al total general
            tabla_menus.insert("", "end", values=(producto, cantidad, valor))
    
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
frame_botones = ctk.CTkFrame(pestaña_menus)
frame_botones.pack(pady=10)

# Cargar las imágenes
icon_papas = ctk.CTkImage(Image.open("IMG/icono_papas_fritas_64x64.png"), size=(40, 40))
icon_bebida = ctk.CTkImage(Image.open("IMG/icono_cola_64x64.png"), size=(40, 40))
icon_hamburguesa = ctk.CTkImage(Image.open("IMG/icono_hamburguesa_negra_64x64.png"), size=(40, 40))
icon_completo = ctk.CTkImage(Image.open("IMG/icono_hotdog_sin_texto_64x64.png"), size=(40, 40))

ctk.CTkButton(frame_botones, image=icon_papas, text="Papas Fritas", command=lambda: actualizar_pedido("Papas Fritas"), width=200, height=40).grid(row=0, column=0, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_bebida, text="Bebida", command=lambda: actualizar_pedido("Bebida"), width=200, height=40).grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_hamburguesa, text="Hamburguesa", command=lambda: actualizar_pedido("Hamburguesa"), width=200, height=40).grid(row=1, column=0, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_completo, text="Completo", command=lambda: actualizar_pedido("Completo"), width=200, height=40).grid(row=1, column=1, padx=10, pady=10)

# Botón para eliminar el menú
eliminar_button = ctk.CTkButton(pestaña_menus, text="Eliminar Pedido", command=eliminar_pedido, fg_color="red")
eliminar_button.pack(pady=10)

# Botón para generar la boleta
generar_boleta_button = ctk.CTkButton(pestaña_menus, text="Generar Boleta", command=generar_boleta, fg_color="blue")
generar_boleta_button.pack(pady=10)

# Etiqueta para mostrar el total
total_label = ctk.CTkLabel(pestaña_menus, text="Total: 0 CLP", font=("Arial", 16))
total_label.pack(pady=10)

# Ejecutar la interfaz
ventana.mainloop()
