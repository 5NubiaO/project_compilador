from Analizador_Lexico import palabras_reservadas

import re
from Analizador_Sintactico import (
    verificar_sentencia,
    ID, VAR, EXPARI, LEE, IMPRIMIR
)

errores_semanticos = {
    "M01": "Palabra reservada no puede ser identificador",
    "M02": "Hay bloques sin cerrar",
    "M03": "Variable no defina",
    "M04": "Tipo de Dato incompatible",
    "M05": "Cadena en una Expresion Regular",
    "M06": "SINO sin Si",
    "M07": "Bloque WHILE/DO incompleto",
    "M08": "Reasignacion con tipo incopatible",
    "M09": "'.' sin bloque",
    "M10": "Estructura SI invalida"
}

def obtener_tipo(valor, tabla, errores, linea):

    #print(f"DEBUG valor='{valor}'")
    
    if re.fullmatch(r"\d+", valor):
        return "CONSTE"
    
    elif re.fullmatch(r"\d+\.\d+", valor):
        return "CONSF"
    
    elif re.fullmatch(r'"[^"]*"', valor):
        return "CONSC"
    
    elif re.fullmatch(ID, valor):
        if valor not in tabla:
            errores.append(("M03", linea, valor))
            return None
        return tabla[valor]
    
    return None

def verificar_tipos_condicion(condicion, tabla, errores, linea):
    
    #separar por operadores logicos (&, |)
    comparaciones = re.split(r"\s*(?:&|\|)\s*", condicion)

    for comp in comparaciones:
        partes = re.split(r"(>=|<=|==|!=|>|<)", comp)

        if len(partes) != 3:
            continue  # ya es error sintactico probablemente

        izq = partes[0].strip()
        der = partes[2].strip()

        tipo_izq = obtener_tipo(izq, tabla, errores, linea)
        tipo_der = obtener_tipo(der, tabla, errores, linea)

        if tipo_izq is None or tipo_der is None:
            continue

        if tipo_izq != tipo_der:
            errores.append(("M04", linea))

def analizar_semantico(archivo):
    errores = []

    pila = []
    tabla_simbolos = {} #almacenar el id y tipo
    

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
                #hay que limpiar el SI que ya termino
                if pila and pila[-1]["tipo"] == "SI" and pila[-1].get("estado") == "CERRADO_POR_PUNTO":
                    # Si la linea actual NO empieza con .SINO, el SI anterior ya murio
                    if "SINO" not in sub_linea:
                        pila.pop()
                
                errores_sint_local = []

                #Vars
                #asigancion simple
                if re.fullmatch(VAR, sub_linea):

                    id_izq = sub_linea.split("=")[0].strip()

                    #PR no ID
                    if id_izq in palabras_reservadas:
                        errores.append(("M01", num))
                        continue

                    valor = sub_linea.split("=")[1].strip()
                    tipo = obtener_tipo(valor, tabla_simbolos, errores, num)

                    if tipo is None:
                        continue

                    #reasigancionn incompatible
                    if id_izq in tabla_simbolos and tabla_simbolos[id_izq] != tipo:
                        errores.append(("M08", num))

                    tabla_simbolos[id_izq] = tipo

                #EXPARIS
                elif re.fullmatch(EXPARI, sub_linea):

                    id_izq = sub_linea.split("=")[0].strip()

                    if id_izq in palabras_reservadas:
                        errores.append(("M01", num))
                        continue

                    rhs = sub_linea.split("=")[1]

                    #M05 cadenas 
                    if re.search(r'"[^"]*"', rhs):
                        errores.append(("M05", num))
                        continue

                    operandos = re.findall(ID + r"|\d+\.\d+|\d+", rhs)

                    tipos = []
                    for op in operandos:
                        tipo = obtener_tipo(op, tabla_simbolos, errores, num)
                        if tipo is None:
                            break
                        tipos.append(tipo)

                    if len(tipos) < 2:
                        continue

                    #determinar tipo resultado
                    if "CONSF" in tipos:
                        tipo_resultado = "CONSF"
                    else:
                        tipo_resultado = "CONSTE"

                    #incompatibe
                    if id_izq in tabla_simbolos and tabla_simbolos[id_izq] != tipo_resultado:
                        errores.append(("M08", num))

                    tabla_simbolos[id_izq] = tipo_resultado

                #LEE
                elif re.fullmatch(LEE, sub_linea):
                    var = re.findall(ID, sub_linea)[0]
                    tabla_simbolos[var] = "CONSTE" #asumire que es un entero

                #IMPRIMIR()
                elif re.fullmatch(IMPRIMIR, sub_linea):
                    contenido = sub_linea[sub_linea.find("(")+1 : sub_linea.rfind(")")].strip()
                    
                    #cadena
                    if re.fullmatch(r'"[^"]*"', contenido):
                        pass

                    #num
                    elif re.fullmatch(r"\d+(\.\d+)?", contenido):
                        pass

                    #ID
                    else:
                        if contenido not in tabla_simbolos:
                            errores.append(("M03", num, contenido))

                #Estructuras de bloques

                resultado = verificar_sentencia(sub_linea, num, errores_sint_local)

                if resultado == "SI":
                    condicion = sub_linea[sub_linea.find("SI") + 2 : sub_linea.rfind(":")].strip()
                    verificar_tipos_condicion(condicion, tabla_simbolos, errores, num)
                    pila.append({"tipo": "SI", "estado": "ABIERTO", "linea": num})

                elif resultado == "SINO": #Buscra si hay un SI en la cima que este esperando
                    if not pila or pila[-1]["tipo"] != "SI":
                        errores.append(("M06", num))
                        continue
                    #SI entra en la seccion del SINO
                    pila[-1]["estado"] = "EN_SINO"

                elif resultado == "PARA":
                    pila.append({"tipo": "PARA", "linea": num})

                elif resultado == "MIENTRAS":
                    pila.append({"tipo": "MIENTRAS","linea": num})

                elif resultado == "DO":
                    pila.append({
                        "tipo": "DO",
                        "linea": num,
                        "cuerpo_cerrado": False
                    })

                elif resultado == "WHILE":
                    encontrado = False
                    #Buscar el do mas cercano
                    for i in range(len(pila)-1, -1, -1):
                        if pila[i]["tipo"] == "DO":
                            if not pila[i].get("cuerpo_cerrado",False):
                                errores.append(("M07", num))#BLOQUE INCOMPLETO
                            #cerrar DO correctamente
                            pila.pop(i)
                            encontrado = True
                            break

                    if not encontrado:
                        errores.append(("M07", num)) #WHILE SIN DO

                elif resultado == "FIN":
                    if not pila:
                        errores.append(("M09", num))
                        continue
                    
                    top = pila[-1]
                    if top["tipo"] == "SI":
                        # Marcamos que el cuerpo del SI cerró, pero lo dejamos en la pila
                        # para ver si viene un SINO en la siguiente sub-línea o línea.
                        top["estado"] = "CERRADO_POR_PUNTO"
                    
                    elif top["tipo"] == "DO":
                        # El punto en un DO-WHILE solo cierra el cuerpo, no el bloque.
                        top["cuerpo_cerrado"] = True
                    
                    else:
                        # PARA y MIENTRAS se eliminan de la pila inmediatamente.
                        pila.pop()

                #estructuras invalidas 
                elif resultado is False:

                    if sub_linea.startswith("SI"):
                        pila.append({"tipo": "SI", "estado": "ABIERTO", "linea": num})

                    elif sub_linea.startswith("PARA"):
                        pila.append({"tipo": "PARA", "linea": num})

                    elif sub_linea.startswith("MIENTRAS"):
                        pila.append({"tipo": "MIENTRAS", "linea": num})

                    elif sub_linea.startswith("DO"):
                        pila.append({"tipo": "DO", "linea": num})

                    pass

                '''
                print(f"[DEBUG] Linea {num} -> '{sub_linea}'")
                print(f"[DEBUG] Pila: {pila}\n")
                '''

    #validacion final            
    for elem in pila:
        if elem["tipo"] == "DO":
            errores.append(("M07", elem["linea"]))
        elif elem["tipo"] == "SI" and elem["estado"] == "CERRADO_POR_PUNTO": #un SI valido din SINO que se cerro por punto, eso o ya paso un Sino
            continue
        else:
            errores.append(("M02", elem["linea"]))

    return errores