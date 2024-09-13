import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from Ingredientes import Ingrediente
from Menus import Menu, MENUS_DISPONIBLES
from Stocks import Stock
from Pedidos import Pedido
from generador_boleta import generar_boleta


# Crear la ventana principal
ventana = ctk.CTk()
ventana.title("Sistema de Gestión de Pedidos")
ventana.geometry("800x600")

# Establecer tema y tamaño de fuente
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Crear instancias de Stock y Pedido
stock = Stock()
pedido = Pedido()

# Crear el Tabview para las pestañas
tabview = ctk.CTkTabview(ventana)
tabview.pack(expand=True, fill='both')

# Pestaña de Gestión de Ingredientes
pestaña_ingredientes = tabview.add("Gestión de Ingredientes")

# Pestaña de Venta de Menús
pestaña_menus = tabview.add("Venta de Menús")

# --- Pestaña de Gestión de Ingredientes ---
# Crear una tabla (Treeview) para mostrar los ingredientes
tabla_ingredientes = ttk.Treeview(pestaña_ingredientes, columns=("Nombre", "Cantidad"), show="headings", height=15)
tabla_ingredientes.heading("Nombre", text="Nombre")
tabla_ingredientes.heading("Cantidad", text="Cantidad")
tabla_ingredientes.pack(pady=10)

# Función para agregar un ingrediente
def agregar_ingrediente():
    nombre = nombre_entry.get()
    cantidad = cantidad_entry.get()
    if nombre and cantidad.isdigit():
        cantidad = int(cantidad)
        # Añadir ingrediente al stock
        stock.agregar_ingrediente(nombre, cantidad)
        mostrar_ingredientes()
        nombre_entry.delete(0, 'end')
        cantidad_entry.delete(0, 'end')

# Función para eliminar un ingrediente
def eliminar_ingrediente():
    selected_item = tabla_ingredientes.selection()
    if selected_item:
        item_values = tabla_ingredientes.item(selected_item)['values']
        nombre = item_values[0]
        # Eliminar ingrediente del stock
        stock.eliminar_ingrediente(nombre, item_values[1])
        mostrar_ingredientes()

# Función para mostrar los ingredientes en la tabla
def mostrar_ingredientes():
    # Limpiar la tabla
    for row in tabla_ingredientes.get_children():
        tabla_ingredientes.delete(row)
    
    # Insertar los ingredientes en la tabla
    for nombre, cantidad in stock.obtener_ingredientes():
        tabla_ingredientes.insert("", "end", values=(nombre, cantidad))


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

# Función para actualizar el pedido
def actualizar_pedido(producto):
    # Buscar el menú correspondiente en la lista de menús disponibles
    menu_seleccionado = None
    for menu in MENUS_DISPONIBLES:
        if menu.nombre == producto:
            menu_seleccionado = menu
            break

    if menu_seleccionado:
        # Verificar si hay suficientes ingredientes en el stock
        if stock.verificar_ingredientes(menu_seleccionado.ingredientes):
            # Descontar los ingredientes del stock
            for ingrediente, cantidad in menu_seleccionado.ingredientes.items():
                stock.eliminar_ingrediente(ingrediente, cantidad)

            # Actualizar el pedido
            pedido.agregar_menu(menu_seleccionado)  # Esto agrega el menú al pedido
            mostrar_pedido()

            # Actualizar la interfaz de gestión de ingredientes
            mostrar_ingredientes()
        else:
            messagebox.showwarning("No hay suficiente stock", f"No hay suficiente stock para {producto}.")

# Función para mostrar el pedido en la tabla y calcular el total
def mostrar_pedido():
    # Limpiar la tabla
    for row in tabla_menus.get_children():
        tabla_menus.delete(row)
    
    total_general = 0  # Inicializar el total general
    
    for menu in pedido.menus:
        cantidad = 1  # Cada menú representa una unidad de producto
        valor = menu.precio
        total_general += valor  # Sumar el valor de cada producto al total general
        tabla_menus.insert("", "end", values=(menu.nombre, cantidad, valor))
    
    # Actualizar la etiqueta del total acumulado
    total_label.configure(text=f"Total: {total_general} CLP")

# Función para eliminar el menú seleccionado y devolver los ingredientes al stock
def eliminar_menu_seleccionado():
    # Obtener el elemento seleccionado en el Treeview
    selected_item = tabla_menus.selection()
    
    if selected_item:
        # Obtener los valores del producto seleccionado
        item_values = tabla_menus.item(selected_item, 'values')
        producto_seleccionado = item_values[0]  # El primer valor es el nombre del producto

        # Buscar el menú en el pedido actual
        for menu in pedido.menus:
            if menu.nombre == producto_seleccionado:
                # Devolver los ingredientes al stock
                for ingrediente, cantidad in menu.ingredientes.items():
                    stock.agregar_ingrediente(ingrediente, cantidad)
                
                # Eliminar el menú del pedido
                pedido.eliminar_menu(menu)
                break

        # Eliminar el menú seleccionado de la tabla de pedidos
        tabla_menus.delete(selected_item)
        
        # Actualizar la interfaz de gestión de ingredientes
        mostrar_ingredientes()
    else:
        print("No se ha seleccionado ningún producto.")

# Función para generar la boleta y pasar los datos correctamente
def generar_boleta_interfaz():
    # Recolectar datos del pedido
    items = [
        {"nombre": menu.nombre, "cantidad": sum(1 for m in pedido.menus if m.nombre == menu.nombre), "precio_unitario": menu.precio, "subtotal": sum(1 for m in pedido.menus if m.nombre == menu.nombre) * menu.precio}
        for menu in set(pedido.menus)
    ]
    
    # Calcular subtotal, IVA, y total
    subtotal = sum(item['subtotal'] for item in items)
    iva = subtotal * 0.19
    total = subtotal + iva
    
    # Llamar a la función generar_boleta del módulo generador_boleta.py
    generar_boleta(items, subtotal, iva, total)

# Crear botones con íconos para cada producto
frame_botones = ctk.CTkFrame(pestaña_menus)
frame_botones.pack(pady=10)

# Cargar las imágenes
icon_papas = ctk.CTkImage(Image.open("IMG/icono_papas_fritas_64x64.png"), size=(40, 40))
icon_bebida = ctk.CTkImage(Image.open("IMG/icono_cola_64x64.png"), size=(40, 40))
icon_hamburguesa = ctk.CTkImage(Image.open("IMG/icono_hamburguesa_negra_64x64.png"), size=(40, 40))
icon_completo = ctk.CTkImage(Image.open("IMG/icono_hotdog_sin_texto_64x64.png"), size=(40, 40))

ctk.CTkButton(frame_botones, image=icon_papas, text="Papas Fritas", command=lambda: actualizar_pedido("Papas fritas"), width=200, height=40).grid(row=0, column=0, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_bebida, text="Pepsi", command=lambda: actualizar_pedido("Pepsi"), width=200, height=40).grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_hamburguesa, text="Hamburguesa", command=lambda: actualizar_pedido("Hamburguesa"), width=200, height=40).grid(row=1, column=0, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_completo, text="Completo", command=lambda: actualizar_pedido("Completo"), width=200, height=40).grid(row=1, column=1, padx=10, pady=10)

# Botón para eliminar el menú
eliminar_button = ctk.CTkButton(pestaña_menus, text="Eliminar Pedido", command=eliminar_menu_seleccionado, fg_color="red")
eliminar_button.pack(pady=10)

# Botón para generar la boleta
generar_boleta_button = ctk.CTkButton(pestaña_menus, text="Generar Boleta", command=generar_boleta_interfaz)
generar_boleta_button.pack(pady=10)

# Etiqueta para mostrar el total
total_label = ctk.CTkLabel(pestaña_menus, text="Total: 0 CLP", font=("Arial", 16))
total_label.pack(pady=10)

# Mostrar los ingredientes al inicio
mostrar_ingredientes()

# Ejecutar el bucle principal de la interfaz
ventana.mainloop()
