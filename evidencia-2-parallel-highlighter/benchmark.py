import sys

import secuencial
import paralelo

# Santiago Aguilar Mello
# Vladimir Pinera Reyes
# Daniela Janet Gil Gonzalez

DIRECTORIO_PRUEBAS = "pruebas"
REPETICIONES = 5

if __name__ == "__main__":
    directorios = sys.argv[1:] if len(sys.argv) > 1 else [DIRECTORIO_PRUEBAS]

    print(f"{'Corrida':<10}{'Secuencial (s)':>16}{'Paralela (s)':>14}{'Speedup':>10}")

    suma_sec = 0
    suma_par = 0
    procesos = 0

    for i in range(1, REPETICIONES + 1):
        total, t_sec = secuencial.procesar_directorios(directorios)
        _, t_par, procesos = paralelo.procesar_directorios(directorios)
        suma_sec += t_sec
        suma_par += t_par
        print(f"{i:<10}{t_sec:>16.4f}{t_par:>14.4f}{t_sec / t_par:>10.3f}x")

    prom_sec = suma_sec / REPETICIONES
    prom_par = suma_par / REPETICIONES
    print(f"\n{total} archivos, {procesos} nucleos")
    print(f"Promedio secuencial: {prom_sec:.4f} s")
    print(f"Promedio paralela:   {prom_par:.4f} s")
    print(f"Speedup promedio:    {prom_sec / prom_par:.3f}x")
