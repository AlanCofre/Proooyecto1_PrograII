import customtkinter as ctk
from tkinter import ttk
from PIL import Image

# Crear la ventana principal
ventana = ctk.CTk()
ventana.title("Sistema de Pedidos")
ventana.geometry("700x600")

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

# Etiqueta para mostrar el total
total_label = ctk.CTkLabel(ventana, text="Total: 0 CLP", font=("Arial", 16))
total_label.pack(pady=10)

# Ejecutar la interfaz
ventana.mainloop()