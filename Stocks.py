from Ingredientes import Ingrediente

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
    
    
     