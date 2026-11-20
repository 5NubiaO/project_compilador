.MODEL SMALL
LEER Macro Entrada
    mov Ah, 0Ah
    mov dx, offset Entrada
    int 21h
EndM
IMPRIME Macro Mensaje
    mov Ah, 09
    mov dx, offset Mensaje
    int 21h
EndM
.CODE
Inicio:
    mov Ax, @Data
    mov Ds, Ax
    mov A_val, 0
    mov B_val, 0
    mov salir_val, 0
DoInicio_1:
    IMPRIME Mge1
    IMPRIME Salto
    LEER A
    call LeerNumero
    mov al, Resultado
    mov A_val, al
    IMPRIME Salto
    IMPRIME Mge2
    IMPRIME Salto
    LEER B
    call LeerNumero
    mov al, Resultado
    mov B_val, al
    IMPRIME Salto
;Inicio SI 1 ----------------------------------------
    xor ax, ax
    mov al, A_val
    cmp al, 0
    JNE Sino_1
    mov salir_val, 1
    jmp FinSi_1
Sino_1:
;Inicio SI 2 ----------------------------------------
    xor ax, ax
    mov al, B_val
    cmp al, 0
    JNE Sino_2
    mov salir_val, 1
    jmp FinSi_2
Sino_2:
;Inicio SI 3 ----------------------------------------
    xor ax, ax
    mov al, A_val
    cmp al, 5
    JBE Sino_3
    IMPRIME Mge3
    IMPRIME Salto
    jmp FinSi_3
Sino_3:
;Inicio SI 4 ----------------------------------------
    xor ax, ax
    mov al, B_val
    cmp al, 5
    JBE Sino_4
    IMPRIME Mge4
    IMPRIME Salto
    mov salir_val, 0
    jmp FinSi_4
Sino_4:
;Inicio SI 5 ----------------------------------------
    xor ax, ax
    mov al, A_val
    cmp al, B_val
    JBE Sino_5
    mov f1_val, 0
    mov f2_val, 1
    mov temp_val, 0
    mov i_val, 0
    mov i_val, 0
    mov al, B_val
    sub al, 0
    inc al
    mov cl, al
    xor ch, ch
Para_1:
    mov al, f1_val
     call ImprimirNumero
    IMPRIME Salto
    xor ax, ax
    mov al, f1_val
    mov bl, f2_val
    call Sumar
    mov temp_val, al
    mov al, f2_val
    mov f1_val, al
    mov al, temp_val
    mov f2_val, al
    inc i_val
    loop Para_1
FinPara_1:
;Fin bloque PARA ------------------------------
Sino_5:
FinSi_5:
;Fin bloque SI --------------------------------
;Inicio SI 6 ----------------------------------------
    xor ax, ax
    mov al, A_val
    cmp al, B_val
    JAE Sino_6
    mov num_val, 2
    mov cuadrado_val, 0
    mov i_val, 0
    mov i_val, 0
    mov al, A_val
    sub al, 0
    inc al
    mov cl, al
    xor ch, ch
Para_2:
    xor ax, ax
    mov al, num_val
    mov bl, num_val
    call Multiplicar
    mov cuadrado_val, al
    mov al, cuadrado_val
     call ImprimirNumero
    IMPRIME Salto
    xor ax, ax
    mov al, num_val
    mov bl, 1
    call Sumar
    mov num_val, al
    inc i_val
    loop Para_2
FinPara_2:
;Fin bloque PARA ------------------------------
Sino_6:
FinSi_6:
;Fin bloque SI --------------------------------
;Inicio SI 7 ----------------------------------------
    xor ax, ax
    mov al, A_val
    cmp al, B_val
    JNE Sino_7
    mov numero_val, 1
    mov contador_val, 0
    mov res_val, 0
Mientras_1:
    xor ax, ax
    mov al, contador_val
    cmp al, 10
    JAE FinMientras_1
    xor ax, ax
    mov al, numero_val
    mov bl, 2
    call Residuo
    mov res_val, al
;Inicio SI 8 ----------------------------------------
    xor ax, ax
    mov al, res_val
    cmp al, 0
    JE Sino_8
    mov al, numero_val
     call ImprimirNumero
    IMPRIME Salto
    xor ax, ax
    mov al, contador_val
    mov bl, 1
    call Sumar
    mov contador_val, al
Sino_8:
FinSi_8:
;Fin bloque SI --------------------------------
    xor ax, ax
    mov al, numero_val
    mov bl, 1
    call Sumar
    mov numero_val, al
    jmp Mientras_1
FinMientras_1:
;Fin bloque MIENTRAS --------------------------
Sino_7:
FinSi_7:
;Fin bloque SI --------------------------------
FinSi_4:
;Fin bloque SI --------------------------------
FinSi_3:
;Fin bloque SI --------------------------------
FinSi_2:
;Fin bloque SI --------------------------------
FinSi_1:
;Fin bloque SI --------------------------------
    xor ax, ax
    xor bx, bx
    mov al, salir_val
    mov bl, 0
    cmp al, bl
    JE DoInicio_1
;Fin bloque DO-WHILE --------------------------
    mov ax, 4C00h
    int 21h
;PROCEDIMIENTOS------------------------------------------------------------
Multiplicar proc
    xor ah, ah
    mul bl
    ret
Multiplicar endp
Residuo proc
    xor ah, ah
    div bl
    mov al, ah
    xor ah, ah
    ret
Residuo endp
Sumar proc
    add al, bl
    xor ah, ah
    ret
Sumar endp
LeerNumero proc
    mov si, dx
    xor ax, ax
    mov al, [si+1]
    mov cx, ax
    add si, 2
    add si, ax
    dec si
    mov byte ptr [Resultado], 0
      mov bl, 1
    mov bh, 10
L_Loop:
    mov al, [si]
    sub al, 30h
    xor ah, ah
    mul bl
    add byte ptr [Resultado], al
    mov al, bl
    mul bh
    mov bl, al
    dec si
    loop L_Loop
    ret
LeerNumero endp
ImprimirNumero proc
    push cx
    xor ah, ah
    mov bx, 10
    xor cx, cx
Conv_L:
    xor dx, dx
    div bx
    push dx
    inc cx
    cmp ax, 0
    jne Conv_L
    mov di, offset BufferPrint+2
Const_S:
    pop dx
    add dl, 30h
    mov [di], dl
    inc di
    loop Const_S
    mov byte ptr [di], '$'
    IMPRIME BufferPrint+2
     pop cx
 ret
ImprimirNumero endp
.DATA
Salto db 10,13,24h
Mge1 db "VALOR DE A:$"
Mge2 db "VALOR DE B:$"
Mge3 db "A > 5$"
Mge4 db "B > 5$"
Resultado db 0
BufferPrint db 10, ?, 10 dup ('$')
temp db 8, ?, 8 dup (24h)
temp_val db 0
f1 db 8, ?, 8 dup (24h)
f1_val db 0
f2 db 8, ?, 8 dup (24h)
f2_val db 0
contador db 8, ?, 8 dup (24h)
contador_val db 0
salir db 8, ?, 8 dup (24h)
salir_val db 0
B db 8, ?, 8 dup (24h)
B_val db 0
res db 8, ?, 8 dup (24h)
res_val db 0
num db 8, ?, 8 dup (24h)
num_val db 0
numero db 8, ?, 8 dup (24h)
numero_val db 0
i db 8, ?, 8 dup (24h)
i_val db 0
A db 8, ?, 8 dup (24h)
A_val db 0
cuadrado db 8, ?, 8 dup (24h)
cuadrado_val db 0
.STACK
END Inicio
