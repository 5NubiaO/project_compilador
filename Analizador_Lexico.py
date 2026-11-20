import re

#Caso de estudio: MiuNu --> GramaticasPruebas.txt

#Tabla de Errores Lexicos

errores_lexicos ={
    "L01": "Token invalido",
    "L02": "Simbolo no valido",
    "S00": "No se cerro cadena"
}


# Palabras reservadas
palabras_reservadas = {
    "LEE", "IMPRIMIR", "SI", "SINO",
    "PARA", "MIENTRAS", "ENRANGO",
    "TRUE", "FALSE", "DO", "WHILE"
}

# Operadores
operadores = {
    "==", "!=", ">=", "<=", "//",
    "+", "-", "*", "/", ">", "<", "=", "&", "|", "^"
}

# Símbolos
agrupacion = {"(", ")", "{", "}", ":", "."}
puntuacion = {","}

# Expresiones regulares
ID = re.compile(r"^[A-Za-zÑñ][A-Za-zÑñ0-9]*$")#necesario anadir n
CONSE = re.compile(r"^[0-9]+$")
CONSF = re.compile(r"^[0-9]+\.[0-9]+$")
CONSC = re.compile(r'^"[^"]*"$')#todo lo que este dentro de ""

# Como pinas verificar el alfabetoP1
alfabeto_valido = re.compile(r'[A-Za-zÑñ0-9+\-*/<>=!&|^(){}:.,\"\s]')#nada mas lo que esta adentro


#ConsC
def verificar_alfabeto(texto,errores):
    lineas = texto.split("\n")

    for num_linea, linea in enumerate(lineas, start=1):

        #eliminar strings antes de validar, remplaxo de bandera
        linea_sin_cadenas = re.sub(r'"[^"]*"', '', linea)

        for c in linea_sin_cadenas:
            if c.isspace():
                continue

            if not alfabeto_valido.match(c):
                errores.append(("L02", num_linea,c))

        # verificar si hay cadena mal cerrada
        if linea.count('"') % 2 != 0:
            errores.append(("S00", num_linea))



# separa en tokens 
def tokenizar(texto,errores):
    tokens = []
    lineas = texto.split("\n")

    patron = r'"[^"]*"|==|!=|>=|<=|//|[A-Za-zÑñ][A-Za-zÑñ0-9]*|\d+\.\d+|\d+|[+\-*/<>=&|^(){}:.,]'
    for num_linea, linea in enumerate(lineas, start=1):
        if not linea.strip(): #para lineas vacias just in casse
            continue

        mal_formado = re.search(r"\d+[A-Za-zÑñ]+", linea)
        if mal_formado:
            token_error = mal_formado.group() #cosas como 12A
            if ("L01", num_linea, token_error) not in errores:
                errores.append(("L01", num_linea, token_error))

        encontrados = re.findall(patron, linea)
       
        for token in encontrados:
            tokens.append((token, num_linea))

    return tokens



# ANALIZADOR LEXICO

def analizar(tokens,errores):
    for token, linea in tokens:
        if token in palabras_reservadas:
            #print(token, "Palabra Reservada")
            continue

        elif token in operadores:
           #print(token, "Operador")
           continue

        elif token in agrupacion:
            #print(token, "Signo de Agrupacion")
            continue

        elif token in puntuacion:
            #print(token, "Signo de Puntuacion")
            continue
        
        elif CONSF.match(token):
            #print(token, "Constante Flotante")
            continue 
        
        elif CONSE.match(token):
            #print(token, "Constante Entera")
            continue

        elif CONSC.match(token):
            #print(token, "Cadena de Texto")
            continue   
        
        elif ID.match(token):
            #print(token, "ID")
            continue

         
        else:
            if ("L01", linea, token) not in errores:
                errores.append(("L01", linea,token))
    
          

def ejecutar_lexico(archivo):

    errores = []

    with open(archivo, "r", encoding="utf-8") as file:
        contenido = file.read()

    verificar_alfabeto(contenido,errores)
    tokens = tokenizar(contenido,errores)
    analizar(tokens,errores)

    return tokens,errores


