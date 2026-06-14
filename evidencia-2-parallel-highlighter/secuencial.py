import sys
import os
import datetime

from lexer_dfa import lexer_python, generar_html

# Santiago Aguilar Mello
# Vladimir Pinera Reyes
# Daniela Janet Gil Gonzalez

def buscar_archivos_python(directorio_raiz):
    # Recorre el directorio y todos sus subdirectorios (os.walk hace el recorrido en profundidad) y regresa la lista de rutas .py
    rutas = []
    for carpeta, _, archivos in os.walk(directorio_raiz):
        for nombre in archivos:
            if nombre.lower().endswith(".py"):
                rutas.append(os.path.join(carpeta, nombre))
    rutas.sort()
    return rutas


def resaltar_archivo(ruta_entrada):
    # Aplica el lexer DFA a un archivo y genera su HTML junto al archivo original
    base, _ = os.path.splitext(ruta_entrada)
    ruta_salida = f"{base}.html"
    segmentos = lexer_python(ruta_entrada)
    generar_html(segmentos, ruta_entrada, ruta_salida)
    return ruta_salida


def procesar_directorios(directorios):
    # Junta los archivos de todos los directorios recibidos y los procesa de manera secuencial, midiendo el tiempo del proceso
    rutas = []
    for directorio in directorios:
        rutas.extend(buscar_archivos_python(directorio))

    inicio = datetime.datetime.now()
    for ruta in rutas:
        resaltar_archivo(ruta)
    fin = datetime.datetime.now()
    duracion = (fin - inicio).total_seconds()

    return len(rutas), duracion


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python Secuencial.py <directorio> [directorio2 ...]")
        sys.exit(1)

    total, segundos = procesar_directorios(sys.argv[1:])
    print(f"Version secuencial: {total} archivos resaltados en {segundos:.4f} s")