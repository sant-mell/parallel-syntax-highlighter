import sys
import os

# Santiago Aguilar Mello 
# Vladimir Pinera Reyes
# Daniela Janet Gil Gonzalez

digitos = "0123456789"
letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# columnas de la tabla:
# 0 letra, 1 digito, 2 punto, 3 e/E, 4 menos, 5 comilla,
# 6 mas, 7 asterisco, 8 diagonal, 9 igual, 10 gato,
# 11 salto, 12 espacio/tab, 13 guion_bajo, 14 otro

# estados:
# 0 inicio
# 1 entero, 2 decimal, 3 exp_inicio, 4 exp_signo, 5 exp_digitos
# 6 punto_inicial, 7 decimal_punto_inicial
# 8 string_inicio, 9 string_cuerpo
# 10 identificador, 11 comentario
# 12 posible_multiplicacion_o_power, 13 posible_asignacion_o_igual
# 22 error
tabla = [
    [10, 1, 6, 10, 600, 8, 500, 12, 800, 13, 11, 0, 0, 10, 22],
    [100, 1, 2, 3, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    [200, 2, 200, 3, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200],
    [22, 5, 22, 22, 4, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [22, 5, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [200, 5, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200],
    [22, 7, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
    [200, 7, 200, 3, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200],
    [9, 9, 9, 9, 9, 300, 9, 9, 9, 9, 9, 22, 9, 9, 9],
    [9, 9, 9, 9, 9, 300, 9, 9, 9, 9, 9, 22, 9, 9, 9],
    [10, 10, 400, 10, 400, 400, 400, 400, 400, 400, 400, 400, 400, 10, 400],
    [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 1200, 11, 11, 11],
    [700, 700, 700, 700, 700, 700, 700, 1000, 700, 700, 700, 700, 700, 700, 700],
    [1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 900, 1100, 1100, 1100, 1100, 1100],
]

# tokens del DFA
tokens = {
    100: "int",
    200: "float",
    300: "string",
    400: "identifier",
    500: "suma",
    600: "resta",
    700: "multi",
    800: "division",
    900: "igual",
    1000: "power",
    1100: "asignacion",
    1200: "comentario",
    22: "error",
}


def imprimir_token(lexema, tipo):
    print(lexema, "\t", tipo)


def escapar_html(texto):
    texto = texto.replace("&", "&amp;")
    texto = texto.replace("<", "&lt;")
    texto = texto.replace(">", "&gt;")
    texto = texto.replace('"', "&quot;")
    return texto


def clase_css(tipo):
    if tipo in ("int", "float"):
        return "numero"
    if tipo == "string":
        return "cadena"
    if tipo == "identifier":
        return "identificador"
    if tipo in ("suma", "resta", "multi", "division", "igual", "power", "asignacion"):
        return "operador"
    if tipo == "comentario":
        return "comentario"
    if tipo == "error":
        return "error"
    return "normal"


def obtener_columna(caracter):
    if caracter in letras and caracter not in "Ee":
        return 0
    if caracter in digitos:
        return 1
    if caracter == ".":
        return 2
    if caracter in "Ee":
        return 3
    if caracter == "-":
        return 4
    if caracter in "\"'":
        return 5
    if caracter == "+":
        return 6
    if caracter == "*":
        return 7
    if caracter == "/":
        return 8
    if caracter == "=":
        return 9
    if caracter == "#":
        return 10
    if caracter == "\n":
        return 11
    if caracter in " \t":
        return 12
    if caracter == "_":
        return 13
    return 14


def agregar_segmento(salida, lexema, tipo=None):
        salida.append((lexema, tipo))


def generar_html(segmentos, archivo_entrada, archivo_salida):
        partes = []
        for lexema, tipo in segmentos:
                lexema_html = escapar_html(lexema)
                if tipo is None:
                        partes.append(lexema_html)
                else:
                        partes.append(f'<span class="{clase_css(tipo)}">{lexema_html}</span>')

        contenido = "".join(partes)
        html = f"""<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Resaltador DFA - {escapar_html(archivo_entrada)}</title>
    <style>
        :root {{
            --fondo: #f6f2e8;
            --panel: #fffdf7;
            --texto: #1f1b16;
            --numero: #005f73;
            --cadena: #8b2e16;
            --identificador: #2a4d14;
            --operador: #a03a00;
            --comentario: #6b7280;
            --error: #b00020;
            --borde: #d8cbb5;
        }}

        body {{
            margin: 0;
            background: linear-gradient(145deg, #efe8d8 0%, #f8f5ec 55%, #efe2cb 100%);
            color: var(--texto);
            font-family: 'Courier New', Courier, monospace;
        }}

        .contenedor {{
            max-width: 1000px;
            margin: 28px auto;
            padding: 0 16px;
        }}

        h1 {{
            margin: 0 0 12px;
            font-size: 1.15rem;
            letter-spacing: 0.4px;
        }}

        .codigo {{
            background: var(--panel);
            border: 1px solid var(--borde);
            border-radius: 10px;
            padding: 16px;
            overflow-x: auto;
            box-shadow: 0 8px 24px rgba(63, 44, 18, 0.08);
            white-space: pre;
            line-height: 1.45;
            font-size: 14px;
        }}

        .numero {{ color: var(--numero); }}
        .cadena {{ color: var(--cadena); }}
        .identificador {{ color: var(--identificador); }}
        .operador {{ color: var(--operador); font-weight: 700; }}
        .comentario {{ color: var(--comentario); font-style: italic; }}
        .error {{ color: var(--error); background: rgba(176, 0, 32, 0.12); }}
    </style>
</head>
<body>
    <main class=\"contenedor\">
        <h1>Resaltado léxico por DFA: {escapar_html(archivo_entrada)}</h1>
        <div class=\"codigo\">{contenido}</div>
    </main>
</body>
</html>
"""

        with open(archivo_salida, "w", encoding="utf-8") as archivo_html:
                archivo_html.write(html)


def lexer_python(archivo):
    with open(archivo, encoding="utf-8") as archivo_entrada:
        texto = archivo_entrada.read()

    if not texto.endswith("\n"):
        texto += "\n"

    estado = 0
    lexema = ""
    comilla_activa = ""
    posicion = 0
    segmentos = []

    while posicion < len(texto):
        caracter = texto[posicion]
        columna = obtener_columna(caracter)
        siguiente_estado = tabla[estado][columna]

        if estado in (8, 9):
            if caracter == comilla_activa:
                lexema += caracter
                imprimir_token(lexema, tokens[300])
                agregar_segmento(segmentos, lexema, tokens[300])
                estado = 0
                lexema = ""
                comilla_activa = ""
                posicion += 1
                continue

            if caracter == "\n":
                imprimir_token(lexema, tokens[22])
                agregar_segmento(segmentos, lexema, tokens[22])
                agregar_segmento(segmentos, "\n")
                estado = 0
                lexema = ""
                comilla_activa = ""
                posicion += 1
                continue

            lexema += caracter
            estado = 9
            posicion += 1
            continue

        if siguiente_estado == 0:
            agregar_segmento(segmentos, caracter)
            estado = 0
            lexema = ""
            posicion += 1
            continue

        if siguiente_estado in (100, 200, 400, 700, 1100):
            token_estado = siguiente_estado
            if token_estado in (700, 1100):
                simbolos = {700: "*", 1100: "="}
                imprimir_token(simbolos[token_estado], tokens[token_estado])
                agregar_segmento(segmentos, simbolos[token_estado], tokens[token_estado])
            else:
                imprimir_token(lexema, tokens[token_estado])
                agregar_segmento(segmentos, lexema, tokens[token_estado])

            estado = 0
            lexema = ""
            continue

        if siguiente_estado in (500, 600, 800, 900, 1000, 1200):
            simbolos = {
                500: "+",
                600: "-",
                800: "/",
                900: "==",
                1000: "**",
            }

            if siguiente_estado == 1200:
                imprimir_token(lexema, tokens[1200])
                agregar_segmento(segmentos, lexema, tokens[1200])
                agregar_segmento(segmentos, "\n")
                estado = 0
                lexema = ""
                posicion += 1
                continue

            imprimir_token(simbolos[siguiente_estado], tokens[siguiente_estado])
            agregar_segmento(segmentos, simbolos[siguiente_estado], tokens[siguiente_estado])
            estado = 0
            lexema = ""
            posicion += 1
            continue

        if siguiente_estado == 22:
            imprimir_token(caracter, tokens[22])
            agregar_segmento(segmentos, caracter, tokens[22])
            estado = 0
            lexema = ""
            posicion += 1
            continue

        if estado == 0 and siguiente_estado in (500, 600, 800):
            simbolos = {500: "+", 600: "-", 800: "/"}
            imprimir_token(simbolos[siguiente_estado], tokens[siguiente_estado])
            agregar_segmento(segmentos, simbolos[siguiente_estado], tokens[siguiente_estado])
            estado = 0
            lexema = ""
            posicion += 1
            continue

        if estado == 0 and siguiente_estado == 8:
            comilla_activa = caracter

        if estado == 0 and siguiente_estado in (12, 13):
            lexema = caracter
            estado = siguiente_estado
            posicion += 1
            continue

        if estado == 11 and caracter == "\n":
            estado = 0
            lexema = ""
            posicion += 1
            continue

        lexema += caracter
        estado = siguiente_estado
        posicion += 1

    return segmentos


if len(sys.argv) not in (2, 3):
    print("Uso: python lexer_dfa_python.py <archivo_python.py> [archivo_salida.html]")
    sys.exit(1)

archivo_entrada = sys.argv[1]
if not archivo_entrada.lower().endswith(".py"):
    print("Error: el archivo de entrada debe tener extension .py")
    sys.exit(1)

if not os.path.isfile(archivo_entrada):
    print("Error: no se encontro el archivo de entrada")
    sys.exit(1)

if len(sys.argv) == 3:
    archivo_salida = sys.argv[2]
else:
    base, _ = os.path.splitext(archivo_entrada)
    archivo_salida = f"{base}.html"

segmentos_lexer = lexer_python(archivo_entrada)
generar_html(segmentos_lexer, archivo_entrada, archivo_salida)
print("HTML generado en:", archivo_salida)