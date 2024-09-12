import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

class Ingrediente:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

    def actualizar_cantidad(self, cantidad):
        self.cantidad += cantidad
        if self.cantidad < 0:
            self.cantidad = 0

class Stock:
    def __init__(self):
        self.ingredientes = {}

    def agregar_ingrediente(self, nombre, cantidad):
        if nombre in self.ingredientes:
            self.ingredientes[nombre].actualizar_cantidad(cantidad)
        else:
            self.ingredientes[nombre] = Ingrediente(nombre, cantidad)

    def eliminar_ingrediente(self, nombre):
        if nombre in self.ingredientes:
            del self.ingredientes[nombre]

    def mostrar_ingredientes(self):
        return {nombre: ingrediente.cantidad for nombre, ingrediente in self.ingredientes.items()}

class Aplicacion:
    def __init__(self, root):
        self.stock = Stock()

        self.root = root
        self.root.title("Gestión de Ingredientes y Pedidos")
        self.root.geometry("600x450")
        self.root.configure(background="black")  # Fondo negro

        # Estilo para que coincida con la vista negra
        style = ttk.Style()
        style.configure("TLabel", background="black", foreground="white", font=("Helvetica", 12))
        style.configure("TButton", background="black", foreground="white", font=("Helvetica", 10))
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black", font=("Helvetica", 10))
        style.map("TButton", background=[('active', '#5E5E5E')])

        # Pestañas superiores
        self.notebook = ttk.Notebook(self.root)
        self.frame_ingredientes = ttk.Frame(self.notebook, padding="10", style="TFrame")
        self.frame_pedidos = ttk.Frame(self.notebook, padding="10", style="TFrame")

        self.notebook.add(self.frame_ingredientes, text="Ingreso de Ingredientes")
        self.notebook.add(self.frame_pedidos, text="Pedido")
        self.notebook.pack(expand=True, fill="both")

        # Etiquetas y entradas para los ingredientes
        self.nombre_label = ttk.Label(self.frame_ingredientes, text="Nombre del Ingrediente:")
        self.nombre_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.nombre_entry = ttk.Entry(self.frame_ingredientes, width=25)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.cantidad_label = ttk.Label(self.frame_ingredientes, text="Cantidad:")
        self.cantidad_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.cantidad_entry = ttk.Entry(self.frame_ingredientes, width=25)
        self.cantidad_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        # Botón para agregar ingrediente
        self.agregar_btn = ttk.Button(self.frame_ingredientes, text="Ingresar Ingrediente", command=self.agregar_ingrediente)
        self.agregar_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Lista de ingredientes
        self.frame_lista = ttk.Frame(self.frame_ingredientes)
        self.frame_lista.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.lista_ingredientes = ttk.Treeview(self.frame_lista, columns=("Nombre", "Cantidad"), show="headings", height=10)
        self.lista_ingredientes.heading("Nombre", text="Nombre")
        self.lista_ingredientes.heading("Cantidad", text="Cantidad")
        self.lista_ingredientes.column("Nombre", width=150)
        self.lista_ingredientes.column("Cantidad", width=80)
        self.lista_ingredientes.pack(side="left", fill="y")

        # Scrollbar para la lista
        self.scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.lista_ingredientes.yview)
        self.lista_ingredientes.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Botón para eliminar ingrediente
        self.eliminar_btn = ttk.Button(self.frame_ingredientes, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        self.eliminar_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Botón para generar menú (placeholder)
        self.generar_menu_btn = ttk.Button(self.frame_ingredientes, text="Generar Menú", command=self.generar_menu)
        self.generar_menu_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def agregar_ingrediente(self):
        nombre = self.nombre_entry.get()
        cantidad = self.cantidad_entry.get()

        if nombre and cantidad.isdigit():
            cantidad = int(cantidad)
            self.stock.agregar_ingrediente(nombre, cantidad)
            self.actualizar_lista()
            self.nombre_entry.delete(0, tk.END)
            self.cantidad_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un nombre y una cantidad válida.")

    def eliminar_ingrediente(self):
        selected_item = self.lista_ingredientes.selection()
        if selected_item:
            nombre = self.lista_ingredientes.item(selected_item, 'values')[0]
            self.stock.eliminar_ingrediente(nombre)
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", "Seleccione un ingrediente para eliminar.")

    def actualizar_lista(self):
        for item in self.lista_ingredientes.get_children():
            self.lista_ingredientes.delete(item)

        for nombre, cantidad in self.stock.mostrar_ingredientes().items():
            self.lista_ingredientes.insert("", tk.END, values=(nombre, cantidad))

    def generar_menu(self):
        messagebox.showinfo("Menú", "Función para generar menú aún no implementada.")

# Configurar la ventana principal con un tema
root = ThemedTk(theme="breeze")  # Puedes probar con otros temas como 'radiance', 'arc', 'clearlooks'
app = Aplicacion(root)
root.mainloop()

