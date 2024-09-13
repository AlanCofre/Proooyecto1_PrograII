class Menu:
    def __init__(self, nombre, precio, ingredientes):
        self.nombre = nombre
        self.precio = precio
        self.ingredientes = ingredientes

# Definir los menús disponibles
MENUS_DISPONIBLES = [
    Menu("Papas fritas", 500, {"papas": 5}),
    Menu("Pepsi", 1100, {"bebida": 1}),
    Menu("Completo", 1800, {"vienesa": 1, "pan de completo": 1, "tomate": 1, "palta": 1}),
    Menu("Hamburguesa", 3500, {"pan de hamburguesa": 1, "lamina de queso": 1, "churrasco de carne": 1}),
]
