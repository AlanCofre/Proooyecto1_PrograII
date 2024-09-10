from fpdf import FPDF


class Ingrediente: 
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

    def actualizar_cantidad(self, cantidad):
        self.cantidad += cantidad
    
    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"


class Menu:
    def __init__(self, nombre, ingredientes_necesarios, precio):
        self.nombre = nombre
        self.ingredientes_necesarios = ingredientes_necesarios
        self.precio = precio
    
    def ingredientes_suficientes(self, stock):
        for ingrediente, cantidad_necesaria in self.ingredientes_necesarios.items():
            if ingrediente not in stock.ingredientes or stock.ingredientes[ingrediente].cantidad < cantidad_necesaria:
                return False
        return True
    
    def descontar_ingredientes(self, stock):
        if self.ingredientes_suficientes(stock):
            for ingrediente, cantidad in self.ingredientes_necesarios.items():
                stock.ingredientes[ingrediente].actualizar_cantidad(-cantidad)          

    def reponer_ingredientes(self, stock):
        for ingrediente, cantidad in self.ingredientes_necesarios.items():
            stock.ingredientes[ingrediente].actualizar_cantidad(cantidad)

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

    def obtener_ingredientes(self):
        return self.ingredientes
    
    
     

