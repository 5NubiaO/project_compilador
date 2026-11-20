import re
from Analizador_Sintactico import IMPRIMIR, VAR, EXPARI, LEE, SI, SINO, COND, ID, CONSC, PARA, MIENTRAS, DO, WHILE, OPDO

def es_constante(valor):
    return valor.replace('.', '', 1).isdigit()

def generar_asm(archivo_entrada, nombre_salida):
    codigo_asm = []
    data_asm = [".DATA", "Salto db 10,13,24h"]
    variables_detectadas = set()
    procedimientos_usados = set() # Registro dinamico de que funciones incluir
    macros_usadas = set()
    contador_mge = 1
    
    # Manejo de Etiquetas para SI / SINO
    #pila_etiquetas = []
    contador_si = 0
    #Manejo Etiquetas PARA
    #pila_para = []
    contador_para = 0
    #Manejo de MIENTRAS
    contador_mientras = 0
    #Manejo de DO-WHILE
    contador_do =0

    pila_bloques = []
    #cont_imp =0

    #Estructura inicial y macros (procedimientos on the way)
    #codigo_asm.append(".MODEL SMALL") - cambiar para orden y las dinamicas

    biblioteca_macros = obtener_macros()

    '''Cambio a macros dinamicas mejor
    codigo_asm.append("IMPRIME Macro Mensaje")
    codigo_asm.append("    mov Ah, 09")
    codigo_asm.append("    mov dx, offset Mensaje")
    codigo_asm.append("    int 21h")
    codigo_asm.append("EndM")
    
    
    pruebas +2digitos
    
    codigo_asm.append("LEER Macro Entrada")
    codigo_asm.append("    mov Ah, 0Ah")
    codigo_asm.append("    mov dx, offset Entrada")
    codigo_asm.append("    int 21h")
    codigo_asm.append("EndM")

    codigo_asm.append("POTENCIA Macro Base, Exp")
    codigo_asm.append("    local Calcular1, Calcular2, Calcula, FinM")
    codigo_asm.append("    Cmp Exp, 0\n    jne Calcular1\n    Mov Resultado, al\n    jmp FinM")
    codigo_asm.append("Calcular1:\n    Cmp Exp, 1\n    jne Calcular2\n    Mov Resultado, al\n    jmp FinM")
    codigo_asm.append("Calcular2:\n    Xor Cx, Cx\n    Mov Cl, Exp\n    Dec Cx\n    Xor Ax, Ax\n    Mov Al, Base")
    codigo_asm.append("Calcula:\n    Mul Base\n    loop Calcula\n    Mov Resultado, Al\n    FinM:")
    codigo_asm.append("EndM")
    #fin de la prueba
    '''

    #codigo_asm.append(".CODE")-resto y esto abajo por dinamismo
    
    #lectura y a ensamblador
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea in ["Inicio:", "Fin"]: continue

            #IMPRIMIR
            if re.fullmatch(IMPRIMIR, linea):
                macros_usadas.add("IMPRIME")
                contenido = re.search(r"\((.*)\)", linea).group(1)
                if contenido.startswith('"'): #texto constante
                    nom_mge = f"Mge{contador_mge}"
                    texto_limpio = contenido.replace('"', '')
                    data_asm.append(f'{nom_mge} db "{texto_limpio}$"')
                    codigo_asm.append(f"    IMPRIME {nom_mge}")
                    contador_mge += 1
                else:
                    #Es un numero o variable
                    if '.' in contenido: # Es una constante decimal (ej: 3.1416)
                        #Quitar el punto para enviarlo como entero
                        valor_escalado = contenido.replace('.', '')
                        #contar los decimales que tenia para colocar el punto donde debe ir
                        posicion_punto = len(contenido.split('.')[1])
                        
                        codigo_asm.append(f"    mov ax, {valor_escalado}")
                        #Usar BL para pasar la cantidad de decimales al procedimiento
                        codigo_asm.append(f"    mov bl, {posicion_punto}")
                        procedimientos_usados.add("ImprimirDecimal")
                        codigo_asm.append("    call ImprimirDecimal")
                    else:
                        #es entero o variable
                        if contenido.replace ('.','',1).isdigit():
                            codigo_asm.append(f"    mov al, {int(float(contenido))}")
                        else:
                            codigo_asm.append(f"    mov al, {contenido}_val")
                        procedimientos_usados.add("ImprimirNumero")    
                        codigo_asm.append("     call ImprimirNumero")
                codigo_asm.append("    IMPRIME Salto")

            #LEE (implementar +2digitos)
            elif re.fullmatch(LEE, linea):
                macros_usadas.add("LEER")
                macros_usadas.add("IMPRIME")
                var_nombre = re.search(r"\((.*)\)", linea).group(1)
                variables_detectadas.add(var_nombre)
                procedimientos_usados.add("LeerNumero")
                #codigo_asm.append("    call LeerNumero")
                #codigo_asm.append(f"    mov {var_nombre}, al")
                codigo_asm.append(f"    LEER {var_nombre}")
                #codigo_asm.append(f"    lea dx, {var_nombre}")
                codigo_asm.append(f"    call LeerNumero")
                codigo_asm.append(f"    mov al, Resultado")
                codigo_asm.append(f"    mov {var_nombre}_val, al")
                codigo_asm.append("    IMPRIME Salto")
            
            #Asignacion SIMPLE
            elif re.fullmatch(VAR, linea):

                partes = linea.split("=")
                var_nombre = partes[0].strip()
                valor = partes[1].strip()
                variables_detectadas.add(var_nombre)

                #Si es constante
                if es_constante(valor):
                    codigo_asm.append(f"    mov {var_nombre}_val, {valor}")

                #Si es variable
                else:
                    variables_detectadas.add(valor)
                    codigo_asm.append(f"    mov al, {valor}_val")
                    codigo_asm.append(f"    mov {var_nombre}_val, al")

            #SI (Condicionales)
            elif re.fullmatch(SI, linea):
                contador_si += 1
                match_cond = re.search(r"SI\s+(.*?)\s*:", linea)
                condicion = match_cond.group(1)
                partes = re.split(r"(>=|<=|==|!=|>|<)", condicion)
                op1, rel, op2 = partes[0].strip(), partes[1].strip(), partes[2].strip()

                codigo_asm.append(f";Inicio SI {contador_si} ----------------------------------------")
                codigo_asm.append("    xor ax, ax")
                codigo_asm.append(f"    mov al, {op1}_val" 
                                  if not es_constante(op1) else f"    mov al, {op1}")
                codigo_asm.append(f"    cmp al, {op2}_val" if not es_constante(op2) else f"    cmp al, {op2}")

                label_sino = f"Sino_{contador_si}"
                label_fin = f"FinSi_{contador_si}"
                pila_bloques.append({
                    "tipo": "SI",
                    "label_sino": label_sino,
                    "label_fin": label_fin,
                    "estado": "ABIERTO"
                })
                #Saltos EMU
                if rel == ">": codigo_asm.append(f"    JBE {label_sino}")
                elif rel == "<": codigo_asm.append(f"    JAE {label_sino}")
                elif rel == ">=": codigo_asm.append(f"    JB {label_sino}")
                elif rel == "<=": codigo_asm.append(f"    JA {label_sino}")
                elif rel == "==": codigo_asm.append(f"    JNE {label_sino}")
                elif rel == "!=": codigo_asm.append(f"    JE {label_sino}")

            #.SINO:
            elif linea == ".SINO:":

                if pila_bloques and pila_bloques[-1]["tipo"] == "SI":

                    bloque = pila_bloques[-1]

                    codigo_asm.append(f"    jmp {bloque['label_fin']}")
                    codigo_asm.append(f"{bloque['label_sino']}:")

                    bloque["estado"] = "EN_SINO"

            #CIERRE DE BLOQUES (.)
            elif linea == ".":

                if not pila_bloques:
                    continue

                bloque = pila_bloques[-1]
                #cierrre SI
                if bloque["tipo"] == "SI":
                    pila_bloques.pop()
                    label_sino = bloque["label_sino"]
                    label_fin = bloque["label_fin"]

                    #Si nunca hubo SINO
                    if bloque["estado"] == "ABIERTO":
                        codigo_asm.append(f"{label_sino}:")

                    codigo_asm.append(f"{label_fin}:")
                    codigo_asm.append(";Fin bloque SI --------------------------------")
                #cierre PARA
                elif bloque["tipo"] == "PARA":
                    pila_bloques.pop()

                    variable = bloque["variable"]
                    label_para = bloque["label_para"]
                    label_fin = bloque["label_fin"]

                    codigo_asm.append(f"    inc {variable}_val")
                    codigo_asm.append(f"    loop {label_para}")

                    #Recuperar CX si hay otro PARA afuera
                    for elem in reversed(pila_bloques):
                        if elem["tipo"] == "PARA":
                            codigo_asm.append("    pop cx")
                            break

                    codigo_asm.append(f"{label_fin}:")
                    codigo_asm.append(";Fin bloque PARA ------------------------------")
                #cierre MIENTRAS
                elif bloque["tipo"] == "MIENTRAS":
                    pila_bloques.pop()
                    codigo_asm.append(
                        f"    jmp {bloque['label_inicio']}"
                    )
                    codigo_asm.append(
                        f"{bloque['label_fin']}:"
                    )
                    codigo_asm.append(
                        ";Fin bloque MIENTRAS --------------------------"
                    )
                #cierre DO
                elif bloque["tipo"]== "DO":
                    pass

            #EXPARIS
            elif re.fullmatch(EXPARI, linea):
                match = re.match(rf"(?P<destino>{ID})\s*=\s*(?P<op1>{OPDO})\s*(?P<operador>\+|\-|\*|/|//|\^)\s*(?P<op2>{OPDO})",linea)
                if match:
                    destino = match.group("destino")
                    op1 = match.group("op1")
                    operador = match.group("operador")
                    op2 = match.group("op2")
                    variables_detectadas.add(destino)
                    
                    mapa_ops = {'+': 'Sumar', '-': 'Restar', '*': 'Multiplicar', 
                                '/': 'Dividir', '//': 'Residuo', '^': 'Potencia'}
                    proc = mapa_ops[operador]
                    procedimientos_usados.add(proc)
                    
                    #puede ser cons o variable, modificar
                    codigo_asm.append("    xor ax, ax")
                    codigo_asm.append(f"    mov al, {op1}_val" 
                                      if not es_constante(op1) 
                                      else f"    mov al, {op1}")
                    codigo_asm.append(f"    mov bl, {op2}_val" 
                                      if not es_constante(op2) 
                                      else f"    mov bl, {op2}")
                    codigo_asm.append(f"    call {proc}")
                    codigo_asm.append(f"    mov {destino}_val, al")

            #PARA
            elif re.fullmatch(PARA, linea):

                contador_para += 1

                match_para = re.search(
                    rf"PARA\s+(?P<var>{ID})\s+ENRANGO\s*\(\s*(?P<inicio>{OPDO})\s*,\s*(?P<fin>{OPDO})\s*\)\s*:",
                    linea
                )

                variable = match_para.group("var")
                inicio = match_para.group("inicio")
                fin = match_para.group("fin")

                variables_detectadas.add(variable)

                label_para = f"Para_{contador_para}"
                label_fin = f"FinPara_{contador_para}"

                #iniciar var
                if es_constante(inicio):
                    codigo_asm.append(
                        f"    mov {variable}_val, {inicio}"
                    )
                else:
                    codigo_asm.append(
                        f"    mov al, {inicio}_val"
                    )
                    codigo_asm.append(
                        f"    mov {variable}_val, al"
                    )

               # Calcular cantidad de iteraciones
                #CX = fin - inicio
                if es_constante(fin):
                    codigo_asm.append(f"    mov al, {fin}")
                else:
                    codigo_asm.append(f"    mov al, {fin}_val")

                if es_constante(inicio):
                    codigo_asm.append(f"    sub al, {inicio}")
                else:
                    codigo_asm.append(f"    sub al, {inicio}_val")

                codigo_asm.append("    inc al")
                #guardar cx si hay para anterior
                if pila_bloques:
                    for bloque in reversed(pila_bloques):
                        if bloque["tipo"] == "PARA":
                            codigo_asm.append("    push cx")
                            break

                pila_bloques.append({
                    "tipo": "PARA",
                    "label_para": label_para,
                    "label_fin": label_fin,
                    "variable": variable
                })        
                codigo_asm.append("    mov cl, al")
                codigo_asm.append("    xor ch, ch")

                codigo_asm.append(f"{label_para}:")

            #MIENTRAS
            elif re.fullmatch(MIENTRAS, linea):
                contador_mientras += 1

                match_cond = re.search(r"MIENTRAS\s+(.*?)\s*:", linea)
                condicion = match_cond.group(1)
                partes = re.split(r"(>=|<=|==|!=|>|<)", condicion)
                op1 = partes[0].strip()
                rel = partes[1].strip()
                op2 = partes[2].strip()

                label_inicio = f"Mientras_{contador_mientras}"
                label_fin = f"FinMientras_{contador_mientras}"

                codigo_asm.append(f"{label_inicio}:")
                codigo_asm.append("    xor ax, ax")
                codigo_asm.append(f"    mov al, {op1}_val" 
                                  if not es_constante(op1) 
                                  else f"    mov al, {op1}")
                codigo_asm.append(f"    cmp al, {op2}_val"
                                    if not es_constante(op2)
                                    else f"    cmp al, {op2}")
                #Saltos
                if rel == ">":
                    codigo_asm.append(f"    JBE {label_fin}")

                elif rel == "<":
                    codigo_asm.append(f"    JAE {label_fin}")

                elif rel == ">=":
                    codigo_asm.append(f"    JB {label_fin}")

                elif rel == "<=":
                    codigo_asm.append(f"    JA {label_fin}")

                elif rel == "==":
                    codigo_asm.append(f"    JNE {label_fin}")

                elif rel == "!=":
                    codigo_asm.append(f"    JE {label_fin}")

                #Guardar bloque
                pila_bloques.append({
                    "tipo": "MIENTRAS",
                    "label_inicio": label_inicio,
                    "label_fin": label_fin
                })

            #DO -WHILE    
            elif re.fullmatch(DO, linea):

                contador_do += 1

                label_inicio = f"DoInicio_{contador_do}"

                codigo_asm.append(f"{label_inicio}:")

                pila_bloques.append({
                    "tipo": "DO",
                    "label_inicio": label_inicio
                })
            #WHILE
            elif linea.startswith(".WHILE"):

                match_cond = re.search(r"\.WHILE\s+(.*)", linea)
                condicion = match_cond.group(1).rstrip(".").strip()

                partes = re.split(r"(>=|<=|==|!=|>|<)", condicion)

                op1 = partes[0].strip()
                rel = partes[1].strip()
                op2 = partes[2].strip()

                #Buscar el DO mas cercano
                bloque_do = None

                for i in range(len(pila_bloques)-1, -1, -1):

                    if pila_bloques[i]["tipo"] == "DO":

                        bloque_do = pila_bloques.pop(i)
                        break

                if bloque_do:

                    label_inicio = bloque_do["label_inicio"]
                    codigo_asm.append("    xor ax, ax")
                    codigo_asm.append("    xor bx, bx")

                    codigo_asm.append(
                        f"    mov al, {op1}_val"
                        if not es_constante(op1)
                        else f"    mov al, {op1}"
                    )

                    codigo_asm.append(
                        f"    mov bl, {op2}_val"
                        if not es_constante(op2)
                        else f"    mov bl, {op2}"
                    )
                    codigo_asm.append("    cmp al, bl")

                    #SALTOS SI LA CONDICION ES VERDADERA
                    if rel == ">":
                        codigo_asm.append(f"    JA {label_inicio}")

                    elif rel == "<":
                        codigo_asm.append(f"    JB {label_inicio}")

                    elif rel == ">=":
                        codigo_asm.append(f"    JAE {label_inicio}")

                    elif rel == "<=":
                        codigo_asm.append(f"    JBE {label_inicio}")

                    elif rel == "==":
                        codigo_asm.append(f"    JE {label_inicio}")

                    elif rel == "!=":
                        codigo_asm.append(f"    JNE {label_inicio}")

                    codigo_asm.append(";Fin bloque DO-WHILE --------------------------")

    codigo_final = []

    codigo_final.append(".MODEL SMALL")

    #MACROS
    biblioteca_macros = obtener_macros()

    for macro in macros_usadas:
        if macro in biblioteca_macros:
            codigo_final.append(biblioteca_macros[macro])

    codigo_final.append(".CODE")
    codigo_final.append("Inicio:")
    codigo_final.append("    mov Ax, @Data")
    codigo_final.append("    mov Ds, Ax")

    codigo_final.extend(codigo_asm)

    codigo_asm = codigo_final

    #--Final de los prog
    codigo_asm.append("    mov ax, 4C00h")
    codigo_asm.append("    int 21h")

    #seleccionar cuales procedimientos deben aparecer
    biblioteca = obtener_biblioteca_completa()
    if procedimientos_usados:
        codigo_asm.append(";PROCEDIMIENTOS------------------------------------------------------------")
    for proc in procedimientos_usados:
        if proc in biblioteca:
            codigo_asm.append(biblioteca[proc])

    #poner variables auxiliares de sistema si se usaron procedimientos
    if "LeerNumero" in procedimientos_usados or any(op in procedimientos_usados for op in ['Sumar', 'Restar', 'Multiplicar', 'Dividir', 'Residuo', 'Potencia']):
        data_asm.append("Resultado db 0")
    
    if "ImprimirNumero" in procedimientos_usados or "ImprimirDecimal" in procedimientos_usados:
        data_asm.append("BufferPrint db 10, ?, 10 dup ('$')")

    #datos dinamicos
    for var in variables_detectadas:
        data_asm.append(f"{var} db 8, ?, 8 dup (24h)")
        #despues de conver
        data_asm.append(f"{var}_val db 0")
    
    codigo_asm.extend(data_asm)
    codigo_asm.append(".STACK")
    codigo_asm.append("END Inicio")

    #ESCRITURA DEL ARCHIVO
    if not nombre_salida.endswith(".asm"):
        nombre_salida += ".asm"
    with open(nombre_salida, "w", encoding="utf-8") as f_out:
        for l in codigo_asm:
            f_out.write(l + "\n")
    
    print(f"Hooray: Archivo '{nombre_salida}' generado correctamente.")

def obtener_biblioteca_completa():
    """Diccionario que contiene el codigo fuente de todos los procedimientos posibles vistos con villa hasta ahoritas"""
    biblioteca = {
        #"LeerNumero": "LeerNumero proc\n    mov ah, 01h\n    int 21h\n    sub al, 30h\n    ret\nLeerNumero endp",
        "LeerNumero": (
            "LeerNumero proc\n"
            "    mov si, dx\n    xor ax, ax\n    mov al, [si+1]\n    mov cx, ax\n"
            "    add si, 2\n    add si, ax\n    dec si\n"
            "    mov byte ptr [Resultado], 0\n  " 
            "    mov bl, 1\n    mov bh, 10\n"
            "L_Loop:\n    mov al, [si]\n    sub al, 30h\n    xor ah, ah\n    mul bl\n    add byte ptr [Resultado], al\n    mov al, bl\n    mul bh\n    mov bl, al\n    dec si\n    loop L_Loop\n    ret\n"
            "LeerNumero endp"
        ),
        "Sumar": "Sumar proc\n    add al, bl\n    xor ah, ah\n    ret\nSumar endp",
        "Restar": "Restar proc\n    sub al, bl\n    xor ah, ah\n    ret\nRestar endp",
        "Multiplicar": "Multiplicar proc\n    xor ah, ah\n    mul bl\n    ret\nMultiplicar endp",
        "Dividir": "Dividir proc\n    xor ah, ah\n    div bl\n    ret\nDividir endp",
        "Residuo": "Residuo proc\n    xor ah, ah\n    div bl\n    mov al, ah\n    xor ah, ah\n    ret\nResiduo endp",
        "Potencia": (
            "Potencia proc\n"
            "    push cx\n"
            "    xor cx, cx\n"
            "    mov cl, bl\n"
            "    mov bl, al\n"
            "    mov al, 1\n"
            "PotLoop:\n"
            "    mul bl\n"
            "    loop PotLoop\n"
            "    pop cx\n"
            "    ret\n"
            "Potencia endp"
        ),
        #"ImprimirNumero": "ImprimirNumero proc\n    push ax\n    mov bl, 10\n    xor ah, ah\n    div bl\n    mov bh, ah\n    add al, 30h\n    mov dl, al\n    mov ah, 02h\n    int 21h\n    mov al, bh\n    add al, 30h\n    mov dl, al\n    mov ah, 02h\n    int 21h\n    pop ax\n    ret\nImprimirNumero endp"
        "ImprimirNumero": (
            "ImprimirNumero proc\n"
            "    push cx\n"
            "    xor ah, ah\n    mov bx, 10\n    xor cx, cx\n"
            "Conv_L:\n    xor dx, dx\n    div bx\n    push dx\n    inc cx\n"
            "    cmp ax, 0\n    jne Conv_L\n"
            "    mov di, offset BufferPrint+2\n"
            "Const_S:\n    pop dx\n    add dl, 30h\n    mov [di], dl\n    inc di\n    loop Const_S\n"
            "    mov byte ptr [di], '$'\n    IMPRIME BufferPrint+2\n "  
            "    pop cx\n"
            " ret\n"
            "ImprimirNumero endp"
        ),
        "ImprimirDecimal": (
            "ImprimirDecimal proc\n"
            "    push cx\n"
            "    push bx\n"              #guardar cantidad de decimales
            "    xor cx, cx\n"
            "    mov si, bx\n"          #SI = cantidad de decimales
            "    mov bx, 10\n"
            
            "Conv_D:\n"
            "    xor dx, dx\n"
            "    div bx\n"
            "    push dx\n"
            "    inc cx\n"
            "    cmp ax, 0\n"
            "    jne Conv_D\n"

            "    mov di, offset BufferPrint+2\n"

            "Print_Loop:\n"
            "    pop dx\n"
            "    add dl, 30h\n"
            "    mov [di], dl\n"
            "    inc di\n"

            "    dec cx\n"

            "    cmp cx, si\n"          #comparar con decimales originales
            "    jne NoPunto\n"

            "    mov byte ptr [di], '.'\n"
            "    inc di\n"

            "NoPunto:\n"
            "    cmp cx, 0\n"
            "    jne Print_Loop\n"

            "    mov byte ptr [di], '$'\n"
            "    IMPRIME BufferPrint+2\n"

            "    pop bx\n"
            "    pop cx\n"
            "    ret\n"
            "ImprimirDecimal endp"
        ),
        "MIENTRAS": (
            "Mientras proc \n"
            "   "
        )
    }
    return biblioteca

def obtener_macros():
    return {

        "IMPRIME": (
            "IMPRIME Macro Mensaje\n"
            "    mov Ah, 09\n"
            "    mov dx, offset Mensaje\n"
            "    int 21h\n"
            "EndM"
        ),

        "LEER": (
            "LEER Macro Entrada\n"
            "    mov Ah, 0Ah\n"
            "    mov dx, offset Entrada\n"
            "    int 21h\n"
            "EndM"
        )

    }