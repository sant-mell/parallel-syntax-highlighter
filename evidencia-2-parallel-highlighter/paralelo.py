import sys
import os
import datetime
from multiprocessing import Pool

from secuencial import buscar_archivos_python, resaltar_archivo

# Santiago Aguilar Mello
# Vladimir Pinera Reyes
# Daniela Janet Gil Gonzalez

def procesar_directorios(directorios):
    rutas = []
    for directorio in directorios:
        rutas.extend(buscar_archivos_python(directorio))

    procesos = os.cpu_count()
    inicio = datetime.datetime.now()
    with Pool(processes=procesos) as pool:
        pool.map(resaltar_archivo, rutas)
    fin = datetime.datetime.now()
    duracion = (fin - inicio).total_seconds()

    return len(rutas), duracion, procesos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python Paralelo.py <directorio> [directorio2 ...]")
        sys.exit(1)

    total, segundos, procesos = procesar_directorios(sys.argv[1:])
    print(f"Version paralela ({procesos} procesos): "
          f"{total} archivos resaltados en {segundos:.4f} s")