from fpdf import FPDF

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