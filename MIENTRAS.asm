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
    mov I_val, 0
Mientras_1:
    mov al, I_val
    cmp al, 5
    JAE FinMientras_1
    IMPRIME Mge1
    IMPRIME Salto
    mov al, I_val
     call ImprimirNumero
    IMPRIME Salto
    mov al, I_val
    mov bl, 1
    call Sumar
    mov I_val, al
    jmp Mientras_1
FinMientras_1:
;Fin bloque MIENTRAS --------------------------
    mov ax, 4C00h
    int 21h
;PROCEDIMIENTOS------------------------------------------------------------
Sumar proc
    add al, bl
    xor ah, ah
    ret
Sumar endp
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
Mge1 db "Valor:$"
Resultado db 0
BufferPrint db 10, ?, 10 dup ('$')
I db 8, ?, 8 dup (24h)
I_val db 0
.STACK
END Inicio
