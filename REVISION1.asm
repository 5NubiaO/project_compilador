.MODEL SMALL
IMPRIME Macro Mensaje
    mov Ah, 09
    mov dx, offset Mensaje
    int 21h
EndM
LEER Macro Entrada
    mov Ah, 0Ah
    mov dx, offset Entrada
    int 21h
EndM
.CODE
Inicio:
    mov Ax, @Data
    mov Ds, Ax
    mov A_val, 0
    mov B_val, 0
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
    mov al, A_val
    cmp al, 0
    JNE Sino_1
    IMPRIME Mge3
    IMPRIME Salto
    jmp FinSi_1
Sino_1:
;Inicio SI 2 ----------------------------------------
    mov al, B_val
    cmp al, 0
    JNE Sino_2
    IMPRIME Mge4
    IMPRIME Salto
    jmp FinSi_2
Sino_2:
;Inicio SI 3 ----------------------------------------
    mov al, A_val
    cmp al, B_val
    JBE Sino_3
    mov C1_val, 0
    mov C2_val, 1
    mov I_val, 0
    mov I_val, 0
    mov al, B_val
    sub al, 0
    inc al
    mov cl, al
    xor ch, ch
Para_1:
    mov al, C1_val
     call ImprimirNumero
    IMPRIME Salto
    mov al, C1_val
    mov bl, C2_val
    call Sumar
    mov AUX_val, al
    mov al, C2_val
    mov C1_val, al
    mov al, AUX_val
    mov C2_val, al
    inc I_val
    loop Para_1
FinPara_1:
;Fin bloque PARA ------------------------------
    jmp FinSi_3
Sino_3:
;Inicio SI 4 ----------------------------------------
    mov al, A_val
    cmp al, B_val
    JAE Sino_4
    mov NUM_val, 2
    mov J_val, 0
    mov J_val, 0
    mov al, A_val
    sub al, 0
    inc al
    mov cl, al
    xor ch, ch
Para_2:
    mov al, NUM_val
    mov bl, NUM_val
    call Multiplicar
    mov CUAD_val, al
    mov al, CUAD_val
     call ImprimirNumero
    IMPRIME Salto
    mov al, NUM_val
    mov bl, 1
    call Sumar
    mov NUM_val, al
    inc J_val
    loop Para_2
FinPara_2:
;Fin bloque PARA ------------------------------
    jmp FinSi_4
Sino_4:
    mov NUMI_val, 1
    mov K_val, 0
    mov K_val, 0
    mov al, 10
    sub al, 0
    inc al
    mov cl, al
    xor ch, ch
Para_3:
    mov al, NUMI_val
    mov bl, 2
    call Residuo
    mov RES_val, al
;Inicio SI 5 ----------------------------------------
    mov al, RES_val
    cmp al, 0
    JE Sino_5
    mov al, NUMI_val
     call ImprimirNumero
    IMPRIME Salto
Sino_5:
FinSi_5:
;Fin bloque SI --------------------------------
    mov al, NUMI_val
    mov bl, 1
    call Sumar
    mov NUMI_val, al
    inc K_val
    loop Para_3
FinPara_3:
;Fin bloque PARA ------------------------------
FinSi_4:
;Fin bloque SI --------------------------------
FinSi_3:
;Fin bloque SI --------------------------------
FinSi_2:
;Fin bloque SI --------------------------------
FinSi_1:
;Fin bloque SI --------------------------------
    mov ax, 4C00h
    int 21h
;PROCEDIMIENTOS------------------------------------------------------------
Multiplicar proc
    xor ah, ah
    mul bl
    ret
Multiplicar endp
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
.DATA
Salto db 10,13,24h
Mge1 db "Ingrese el valor de A: $"
Mge2 db "Ingrese el valor de B: $"
Mge3 db "PROGRAMA TERMINADO$"
Mge4 db "PROGRAMA TERMINADO$"
Resultado db 0
BufferPrint db 10, ?, 10 dup ('$')
A db 8, ?, 8 dup (24h)
A_val db 0
RES db 8, ?, 8 dup (24h)
RES_val db 0
CUAD db 8, ?, 8 dup (24h)
CUAD_val db 0
K db 8, ?, 8 dup (24h)
K_val db 0
C2 db 8, ?, 8 dup (24h)
C2_val db 0
NUM db 8, ?, 8 dup (24h)
NUM_val db 0
B db 8, ?, 8 dup (24h)
B_val db 0
J db 8, ?, 8 dup (24h)
J_val db 0
I db 8, ?, 8 dup (24h)
I_val db 0
AUX db 8, ?, 8 dup (24h)
AUX_val db 0
NUMI db 8, ?, 8 dup (24h)
NUMI_val db 0
C1 db 8, ?, 8 dup (24h)
C1_val db 0
.STACK
END Inicio
