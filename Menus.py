from Stocks import Stock

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




