# Sample input: operators, identifiers and control flow
contador = 0
limite = 100
acumulado = 0

while contador < limite:
    if contador % 2 == 0:
        acumulado = acumulado + contador
    else:
        acumulado = acumulado - 1
    contador = contador + 1

potencia = 2 ** 10
producto = acumulado * potencia
asignacion = producto == 0

resultado_final = (producto + 5) / (limite - 1)
