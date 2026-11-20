
from Analizador_Lexico import ejecutar_lexico, errores_lexicos
from Analizador_Sintactico import analizar_sintactico, errores_sintacticos
from Analizador_Semantico import analizar_semantico, errores_semanticos

from Generador_Codigo import generar_asm

archivo = "GramaticasPruebas.txt"

'''

#LEXICO
tokens,errores_lex = ejecutar_lexico(archivo)
for clave, linea in errores_lex:
    print(f"Error {clave}: {errores_lexicos[clave]} en linea {linea}")
if not errores_lex:
    print("Analizador lexico correcto")#

#SINTACTICO
errores_sint = analizar_sintactico(archivo)
for clave, linea in errores_sint:
    print(f"Error {clave}: {errores_sintacticos[clave]} en linea {linea}")
if not errores_sint:
    print("Analizador sintactico correcto")

#SEMANTICO
errores_sem = analizar_semantico(archivo)
for clave, linea in errores_sem:
    print(f"Error {clave}: {errores_semanticos[clave]} en linea {linea}")
if not errores_sem:
    print("Analizador semantico correcto")    

'''
errores = []
# LEXICO
tokens, errores_lex = ejecutar_lexico(archivo)
errores += errores_lex

# SINTACTICO
errores_sint = analizar_sintactico(archivo)
errores += errores_sint

# SEMANTICO
errores_sem = analizar_semantico(archivo)
errores += errores_sem

errores.sort(key=lambda e: e[1])    
for error in errores:
    if len(error) == 2:
        clave, linea = error
        detalle = None
    else:
        clave, linea, detalle = error

    if clave in errores_lexicos:
        msg = f"Error {clave}: {errores_lexicos[clave]} en linea {linea}"
        if detalle: msg += f"'{detalle}'"
        print(msg)

    elif clave in errores_sintacticos:
        msg = f"Error {clave}: {errores_sintacticos[clave]} en linea {linea}"
        if detalle: msg += f"'{detalle}'" 
        print(msg)

    elif clave in errores_semanticos:
        if clave == "M03" and detalle:
            print(f"Error {clave}: Variable '{detalle}' no definida en linea {linea}")
        else:
            msg = f"Error {clave}: {errores_semanticos[clave]} en linea {linea}"
            if detalle: msg += f" '{detalle}'"
            print(msg)
if not errores:
    print("Todo bien...Ensamblador on the way")
    nombre_user = input("Nombre del archivo .asm: ").strip()
    if not nombre_user:
        nombre_user = "Archivo"

    generar_asm(archivo, nombre_user)
else:
    print(f"{len(errores)} errores encontrados")