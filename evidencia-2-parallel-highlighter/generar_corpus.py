import os
import sys

# Santiago Aguilar Mello
# Vladimir Pinera Reyes
# Daniela Janet Gil Gonzalez

# Generates a directory of sizable .py files so the parallel benchmark has
# enough work per file to overcome the process-spawn overhead of a Pool.
# Usage: python generar_corpus.py <directorio_salida> [numero_archivos] [bloques_por_archivo]

BLOQUE = '''# bloque de prueba para el lexer DFA
entero_{i} = {i}
decimal_{i} = {i}.{i}5
cientifico_{i} = {i}.0e{i}
cadena_{i} = "valor numero {i} con un # adentro"
no_comentario_{i} = {i} // 2   # esto si es comentario
def funcion_{i}(a, b):
    resultado = a * b + {i} - a / 2
    return resultado
acumulado_{i} = funcion_{i}(entero_{i}, decimal_{i}) ** 2
'''


def generar(directorio, archivos, bloques):
    os.makedirs(directorio, exist_ok=True)
    for n in range(archivos):
        ruta = os.path.join(directorio, f"modulo_{n:04d}.py")
        with open(ruta, "w", encoding="utf-8") as f:
            for i in range(bloques):
                f.write(BLOQUE.format(i=i))
    print(f"Generados {archivos} archivos en {directorio} ({bloques} bloques cada uno)")


if __name__ == "__main__":
    directorio = sys.argv[1] if len(sys.argv) > 1 else "corpus"
    archivos = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    bloques = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    generar(directorio, archivos, bloques)
