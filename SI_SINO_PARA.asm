.MODEL SMALL
IMPRIME Macro Mensaje
    mov Ah, 09
    mov dx, offset Mensaje
    int 21h
EndM
.CODE
Inicio:
    mov Ax, @Data
    mov Ds, Ax
    mov A_val, 1
    mov B_val, 3
    mov I_val, 0
    mov J_val, 0
    IMPRIME Mge1
    IMPRIME Salto
    mov al, A_val
    mov I_val, al
    mov al, 5
    sub al, A_val
    inc al
    push cx
    mov cl, al
    xor ch, ch
Para_1:
    IMPRIME Mge2
    IMPRIME Salto
    mov al, I_val
     call ImprimirNumero
    IMPRIME Salto
;Inicio SI 1 ----------------------------------------
    mov al, I_val
    cmp al, 2
    JBE Sino_1
    IMPRIME Mge3
    IMPRIME Salto
    mov al, I_val
    mov J_val, al
    mov al, 5
    sub al, I_val
    inc al
    push cx
    mov cl, al
    xor ch, ch
Para_2:
    IMPRIME Mge4
    IMPRIME Salto
    mov al, J_val
     call ImprimirNumero
    IMPRIME Salto
;Inicio SI 2 ----------------------------------------
    mov al, J_val
    cmp al, 4
    JNE Sino_2
    IMPRIME Mge5
    IMPRIME Salto
Sino_2:
FinSi_2:
;Fin bloque SI --------------------------------
;Inicio SI 3 ----------------------------------------
    mov al, J_val
    cmp al, 4
    JAE Sino_3
    IMPRIME Mge6
    IMPRIME Salto
Sino_3:
FinSi_3:
;Fin bloque SI --------------------------------
;Inicio SI 4 ----------------------------------------
    mov al, J_val
    cmp al, 4
    JBE Sino_4
    IMPRIME Mge7
    IMPRIME Salto
Sino_4:
FinSi_4:
;Fin bloque SI --------------------------------
    inc J_val
    loop Para_2
    pop cx
FinPara_2:
;Fin bloque PARA ------------------------------
Sino_1:
FinSi_1:
;Fin bloque SI --------------------------------
;Inicio SI 5 ----------------------------------------
    mov al, I_val
    cmp al, 2
    JA Sino_5
    IMPRIME Mge8
    IMPRIME Salto
;Inicio SI 6 ----------------------------------------
    mov al, I_val
    cmp al, 1
    JNE Sino_6
    IMPRIME Mge9
    IMPRIME Salto
Sino_6:
FinSi_6:
;Fin bloque SI --------------------------------
;Inicio SI 7 ----------------------------------------
    mov al, I_val
    cmp al, 2
    JNE Sino_7
    IMPRIME Mge10
    IMPRIME Salto
Sino_7:
FinSi_7:
;Fin bloque SI --------------------------------
    jmp FinSi_5
Sino_5:
    IMPRIME Mge11
    IMPRIME Salto
FinSi_5:
;Fin bloque SI --------------------------------
    IMPRIME Mge12
    IMPRIME Salto
    IMPRIME Mge13
    IMPRIME Salto
    inc I_val
    loop Para_1
FinPara_1:
;Fin bloque PARA ------------------------------
    IMPRIME Mge14
    IMPRIME Salto
    mov ax, 4C00h
    int 21h
;PROCEDIMIENTOS------------------------------------------------------------
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
Mge1 db "Inicio del programa$"
Mge2 db "Valor de I:$"
Mge3 db "I es mayor que 2$"
Mge4 db "J vale:$"
Mge5 db "J llego a 4$"
Mge6 db "J es menor que 4$"
Mge7 db "J es mayor que 4$"
Mge8 db "I es pequeno$"
Mge9 db "I vale uno$"
Mge10 db "I vale dos$"
Mge11 db "Entrando al SINO de I pequeno$"
Mge12 db "Fin de vuelta de I$"
Mge13 db "$"
Mge14 db "Programa terminado$"
BufferPrint db 10, ?, 10 dup ('$')
B db 8, ?, 8 dup (24h)
B_val db 0
A db 8, ?, 8 dup (24h)
A_val db 0
I db 8, ?, 8 dup (24h)
I_val db 0
J db 8, ?, 8 dup (24h)
J_val db 0
.STACK
END Inicio
