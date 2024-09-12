import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from Menus import Menu
from Ingredientes import Ingrediente
from Pedidos import Pedido

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

# Crear menús
papas_fritas = Menu("Papas Fritas", [Ingrediente("Papas", 5)], 500)
bebida = Menu("Bebida", [Ingrediente("Bebida", 1)], 1100)
hamburguesa = Menu("Hamburguesa", [Ingrediente("Pan Hamburguesa", 1), Ingrediente("Churrasco de Carne", 1), Ingrediente("Lámina de Queso", 1)], 3500)
completo = Menu("Completo", [Ingrediente("Pan", 1), Ingrediente("Vienesa", 1), Ingrediente("Tomate", 1), Ingrediente("Palta", 1)], 1800)

# Crear un objeto de la clase Pedido
pedido = Pedido()

# Crear una tabla (Treeview) para mostrar el pedido
tabla = ttk.Treeview(ventana, columns=("Producto", "Cantidad", "Valor"), show="headings", height=8)
tabla.heading("Producto", text="Producto")
tabla.heading("Cantidad", text="Cantidad")
tabla.heading("Valor", text="Valor Total (CLP)")
tabla.pack(pady=10)

# Función para actualizar el pedido
def actualizar_pedido(menu):
    pedido.agregar_menu(menu, stock)  # Usar el objeto Pedido para manejar la lógica
    mostrar_pedido()

# Función para mostrar el pedido en la tabla y calcular el total
def mostrar_pedido():
    # Limpiar la tabla
    for row in tabla.get_children():
        tabla.delete(row)
    
    total_general = pedido.total  # Usar el total del objeto Pedido
    
    # Mostrar cada menú en la tabla
    for menu in pedido.menus:
        cantidad = sum(1 for m in pedido.menus if m.nombre == menu.nombre)  # Contar cuántas veces se ha agregado el menú
        valor = cantidad * menu.precio
        tabla.insert("", "end", values=(menu.nombre, cantidad, valor))
    
    # Actualizar la etiqueta del total acumulado
    total_label.configure(text=f"Total: {total_general} CLP")

# Función para eliminar todos los productos
def eliminar_pedido():
    for menu in pedido.menus[:]:  # Iterar sobre una copia de la lista para evitar errores
        pedido.eliminar_menu(menu, stock)
    mostrar_pedido()

# Función para generar la boleta
def generar_boleta():
    pedido.generar_boleta()  # Usar el método del objeto Pedido

# Crear botones con íconos para cada producto
frame_botones = ctk.CTkFrame(ventana)
frame_botones.pack(pady=10)

ctk.CTkButton(frame_botones, image=icon_papas, text="Papas Fritas", command=lambda: actualizar_pedido(papas_fritas), width=200, height=40).grid(row=0, column=0, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_bebida, text="Bebida", command=lambda: actualizar_pedido(bebida), width=200, height=40).grid(row=0, column=1, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_hamburguesa, text="Hamburguesa", command=lambda: actualizar_pedido(hamburguesa), width=200, height=40).grid(row=1, column=0, padx=10, pady=10)
ctk.CTkButton(frame_botones, image=icon_completo, text="Completo", command=lambda: actualizar_pedido(completo), width=200, height=40).grid(row=1, column=1, padx=10, pady=10)

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
