from Ingredientes import Ingrediente

class Stock:
    def __init__(self):
        self.ingredientes = {}

    def agregar_ingrediente(self, nombre, cantidad):
        if nombre in self.ingredientes:
            self.ingredientes[nombre].cantidad += cantidad
        else:
            self.ingredientes[nombre] = Ingrediente(nombre, cantidad)

    def eliminar_ingrediente(self, nombre, cantidad):
        if nombre in self.ingredientes and self.ingredientes[nombre].cantidad >= cantidad:
            self.ingredientes[nombre].cantidad -= cantidad
            if self.ingredientes[nombre].cantidad == 0:
                del self.ingredientes[nombre]

    def obtener_ingredientes(self):
        return [(ingrediente.nombre, ingrediente.cantidad) for ingrediente in self.ingredientes.values()]

    def verificar_ingredientes(self, ingredientes_necesarios):
        # Verifica si hay suficientes ingredientes en el stock para un menú
        for nombre, cantidad in ingredientes_necesarios.items():
            if nombre not in self.ingredientes or self.ingredientes[nombre].cantidad < cantidad:
                return False
        return True
