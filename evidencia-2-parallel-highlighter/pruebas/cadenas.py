# Sample input: strings and comment edge cases
saludo = "hola mundo"
con_gato = "esto tiene un # que no es comentario"
no_comentario = 2 // 1   # this // is not a python comment, the # is
vacia = ""

class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def describir(self):
        return self.nombre + " tiene " + str(self.edad)

p = Persona("Santiago", 20)
print(p.describir())
