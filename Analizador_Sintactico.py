from Analizador_Lexico import palabras_reservadas
#Reglas de Produccion
import re

'''
<PROGRAMA>:: <BLOQUE> 
<BLOQUE>:: <SENTENCIA> <BLOQUE> | <SENTENCIA> 

'''
#<NUMEROS>:: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9  
NUMEROS = r"[0-9]"
#<LETRAS>:: A | B | C | D | E | F | G | H | I | J | K | L | M | N | Ñ | O | P | Q | R | S | T | U | V | W | X | Y | Z |a | b | c | d | e | f | g | h | i | j | k | l | m | n | ñ | o | p | q | r | s | t | u | v | w | x | y | z 
LETRAS = r"[A-Za-zÑñ]" 
#<RESTOID>:: <RESTOID><LETRAS>| <RESTOID><NUMEROS> | Ɛ 
RESTOID = rf"(?:{LETRAS}|{NUMEROS})*"

#<ID>:: <LETRAS><RESTOID>
ID = rf"{LETRAS}{RESTOID}"

  
#<CONSE>:: <NUMEROS><CONSE>|<NUMEROS>  
CONSE = rf"({NUMEROS})+"
#<CONSF>:: <CONSE>.<CONSE>  
CONSF = rf"{CONSE}\.{CONSE}"
#<CONSC>:: “*\.”  
CONSC = r'"[^"]*"'
#<CONS>:: <CONSE>|<CONSF>|<CONSC>
CONS = rf"(?:{CONSF}|{CONSE}|{CONSC})"


#<OPDO>::<ID>|<CONS> | TRUE | FALSE  
OPDO = rf"(?:{ID}|{CONS}|TRUE|FALSE)"  #probablemente quitar TRUE | FALSE


#<OPARIT>:: + | - | * | / | // | ^  
OPARIT = r"(?:\+|\-|\*|/|//|\^)"
#<EXPARI>:: <ID> = <OPDO><OPARIT><OPDO>  
EXPARI = rf"{ID}\s*=\s*{OPDO}\s*{OPARIT}\s*{OPDO}"


#<VAR>:: <ID> = <OPDO> 
VAR = rf"{ID}\s*=\s*{OPDO}"
#<LEE>:: LEE(<ID>)
LEE = rf"LEE\s*\(\s*{ID}\s*\)"
#<IMPRIMIR>:: IMPRIMIR(<OPDO>)  
IMPRIMIR = rf"IMPRIMIR\s*\(\s*{OPDO}\s*\)"


#<REL>::  > | < | <= | >= | == |!=   
REL = r"(?:>=|<=|==|!=|>|<)"
#<LOGIC>:: & | |  
LOGIC = r"(?:&|\|)"


#<COND_SIMPLEX>:: <OPDO><REL><OPDO>  
COND_SIMPLEX = rf"{OPDO}\s*{REL}\s*{OPDO}"
#<COND_COMP>:: <COND_SIMPLEX><LOGIC><COND_SIMPLEX>  
COND_COMP = rf"{COND_SIMPLEX}\s*{LOGIC}\s*{COND_SIMPLEX}"
#<COND>:: <COND_SIMPLEX>|<COND_COMP>  
COND = rf"(?:{COND_COMP}|{COND_SIMPLEX})"


#<SI>:: SI<COND>: <BLOQUE>.   
SI = rf"SI\s*{COND}\s*:"   #Validacion del bloque aparte, no en regex, Semantico?
#<SINO_OP>:: SINO: <BLOQUE>| ε .  
SINO = r"SINO\s*:"

#<PARA>:PARA <ID> ENRANGO ( <OPDO> , <OPDO> ) : <BLOQUE> . 
PARA = rf"PARA\s+{ID}\s+ENRANGO\s*\(\s*{OPDO}\s*,\s*{OPDO}\s*\)\s*:"

#<MIENTRAS>:: MIENTRAS <COND> : <BLOQUE> . 
MIENTRAS = rf"MIENTRAS\s+{COND}\s*:"

#<DO>:: DO : <BLOQUE>. WHILE<COND>. 
DO = r"DO\s*:"
WHILE = rf"WHILE\s*{COND}"


#<SENTENCIA>:: <EXPARI> | <LEE> | <IMPRIMIR> | <SI> | <PARA> | <MIENTRAS>| <VAR>| <DO> 
SENTENCIA = rf"(?:{EXPARI}|{LEE}|{IMPRIMIR}|{VAR}|{SI}|{PARA}|{MIENTRAS}|{DO})"


#TABLA de Errores
errores_sintacticos = {
    "S01": "Estructura Invalida",
    "S02": "Falta simbolo esperado",
    "S03": "Uso incorrecto de Palabra Reservada",
    "S04": "Bloque mal formado",
    "S05": "Expresion Invalida"
}

'''
Verificaciones
'''

def verificar_sentencia(linea, num, errores):

    #palabras reservadas como ID
    if "=" in linea:
        lado_izq = linea.split("=")[0].strip()
        if lado_izq in palabras_reservadas:
            errores.append(("S03", num))
            return False
        
    if re.fullmatch(LEE, linea):
        return True

    elif re.fullmatch(IMPRIMIR, linea):
        return True

    elif re.fullmatch(EXPARI, linea):
        return True

    elif re.fullmatch(VAR, linea):
        return True

    elif re.fullmatch(SI, linea):
        return "SI"

    elif re.fullmatch(SINO, linea):
        return "SINO"

    elif re.fullmatch(PARA, linea):
        return "PARA"

    elif re.fullmatch(MIENTRAS, linea):
        return "MIENTRAS"

    elif re.fullmatch(DO, linea):
        return "DO"

    elif re.fullmatch(WHILE + r"\.", linea):
        return "WHILE"

    elif linea == ".":
        return "FIN"

    #MErrores
    

    #Simbolos faltantes
    if "(" in linea and ")" not in linea:
        errores.append(("S02", num))
        return False

    if linea.startswith("SI") and ":" not in linea:
        errores.append(("S02", num))
        return False

    if linea.startswith("PARA") and ":" not in linea:
        errores.append(("S02", num))
        return False

    if linea.startswith("MIENTRAS") and ":" not in linea:
        errores.append(("S02", num))
        return False

    if linea.startswith("DO") and ":" not in linea:
        errores.append(("S02", num))
        return False

    if linea.startswith("WHILE") and not linea.endswith("."):
        errores.append(("S02", num))
        return False

    #EXPARI Invalida
    if "=" in linea and not re.fullmatch(EXPARI, linea) and not re.fullmatch(VAR, linea):
        errores.append(("S05", num))
        return False

    #Estructura Invalida
    errores.append(("S01", num))
    return False


def analizar_sintactico(archivo):

    errores = []

    with open(archivo, "r", encoding="utf-8") as f:

        for num, linea in enumerate(f, start=1):

            linea = linea.strip()

            if not linea:
                continue

            #.SINO
            lineas_a_procesar = []

            if linea.startswith(".") and len(linea) > 1:
                lineas_a_procesar.append(".")
                resto = linea[1:].strip()
                if resto:
                    lineas_a_procesar.append(resto)
            else:
                lineas_a_procesar.append(linea)

            for sub_linea in lineas_a_procesar:

                verificar_sentencia(sub_linea, num, errores)

    return errores

