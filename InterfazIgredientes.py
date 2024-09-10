import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# Clases de Ingredientes y Stock
class Ingrediente: 
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

class Stock:
    def __init__(self):
        self.ingredientes = {}
    
    def agregar_ingrediente(self, nombre, cantidad):
        if nombre in self.ingredientes:
            self.ingredientes[nombre].cantidad += cantidad
        else:
            self.ingredientes[nombre] = Ingrediente(nombre, cantidad)

    def obtener_ingredientes(self):
        return self.ingredientes

# Crear instancia de Stock
almacen_ingredientes = Stock()

# Función para actualizar el Treeview
def actualizar_treeview():
    for item in tree.get_children():
        tree.delete(item)
    for ingrediente in almacen_ingredientes.obtener_ingredientes().values():
        tree.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

# Función para agregar ingrediente
def agregar_ingrediente():
    nombre = entry_nombre.get()
    cantidad = int(entry_cantidad.get())
    almacen_ingredientes.agregar_ingrediente(nombre, cantidad)
    actualizar_treeview()

# Configuración de la interfaz
root = ctk.CTk()
root.title("Gestión de Ingredientes")

# Labels y entradas
label_nombre = ctk.CTkLabel(root, text="Nombre del Ingrediente")
label_nombre.grid(row=0, column=0, padx=10, pady=10)
entry_nombre = ctk.CTkEntry(root)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

label_cantidad = ctk.CTkLabel(root, text="Cantidad")
label_cantidad.grid(row=1, column=0, padx=10, pady=10)
entry_cantidad = ctk.CTkEntry(root)
entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

# Botón para agregar ingrediente
boton_agregar = ctk.CTkButton(root, text="Agregar Ingrediente", command=agregar_ingrediente)
boton_agregar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Treeview para mostrar ingredientes
tree = ttk.Treeview(root, columns=("Nombre", "Cantidad"), show="headings")
tree.heading("Nombre", text="Nombre")
tree.heading("Cantidad", text="Cantidad")
tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Configurar tamaños de columnas
tree.column("Nombre", width=150)
tree.column("Cantidad", width=100)

# Iniciar la aplicación
root.mainloop()
