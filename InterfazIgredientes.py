import customtkinter as ctk
from tkinter import ttk
from Ingredientes import Ingrediente
from Menus import Menu

# Crear la ventana principal
ventana = ctk.CTk()
ventana.title("Gestión de Ingredientes")
ventana.geometry("600x500")

# Establecer tema y tamaño de fuente
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Variables para los ingredientes
ingredientes = []

# Crear una tabla (Treeview) para mostrar los ingredientes
tabla = ttk.Treeview(ventana, columns=("Nombre", "Cantidad"), show="headings", height=15)
tabla.heading("Nombre", text="Nombre")
tabla.heading("Cantidad", text="Cantidad")
tabla.pack(pady=10)

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
    selected_item = tabla.selection()
    if selected_item:
        item_values = tabla.item(selected_item)['values']
        nombre = item_values[0]
        global ingredientes
        ingredientes = [i for i in ingredientes if i.nombre != nombre]
        mostrar_ingredientes()

# Función para mostrar los ingredientes en la tabla
def mostrar_ingredientes():
    # Limpiar la tabla
    for row in tabla.get_children():
        tabla.delete(row)
    
    # Insertar los ingredientes en la tabla
    for ingrediente in ingredientes:
        tabla.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

# Crear un frame para los controles de agregar ingredientes
frame_agregar = ctk.CTkFrame(ventana)
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
eliminar_button = ctk.CTkButton(ventana, text="Eliminar Ingrediente", command=eliminar_ingrediente, fg_color="red")
eliminar_button.pack(pady=10)

# Ejecutar la interfaz
ventana.mainloop()
