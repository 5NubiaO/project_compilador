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
    mov J_val, 10
    mov K_val, 1
Mientras_1:
    mov al, K_val
    cmp al, 5
    JA FinMientras_1
    mov al, K_val
    mov J_val, al
Mientras_2:
    mov al, J_val
    cmp al, 5
    JA FinMientras_2
    mov al, J_val
     call ImprimirNumero
    IMPRIME Salto
    mov al, J_val
    mov bl, 1
    call Sumar
    mov J_val, al
    jmp Mientras_2
FinMientras_2:
;Fin bloque MIENTRAS --------------------------
    mov al, K_val
    mov bl, 1
    call Sumar
    mov K_val, al
    IMPRIME Mge1
    IMPRIME Salto
    jmp Mientras_1
FinMientras_1:
;Fin bloque MIENTRAS --------------------------
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
Sumar proc
    add al, bl
    xor ah, ah
    ret
Sumar endp
.DATA
Salto db 10,13,24h
Mge1 db " $"
Resultado db 0
BufferPrint db 10, ?, 10 dup ('$')
K db 8, ?, 8 dup (24h)
K_val db 0
J db 8, ?, 8 dup (24h)
J_val db 0
.STACK
END Inicio
