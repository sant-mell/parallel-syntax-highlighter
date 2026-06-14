# Sample input: numeric literals of every supported kind
entero = 42
decimal = 3.14159
cientifico = 6.022e23
negativo_exp = 1.6e-19
solo_punto = .5
combinado = 2.0e10

def suma(a, b):
    # returns the sum of two numbers
    resultado = a + b
    return resultado

total = suma(entero, decimal) * 2 - 7 / 3
