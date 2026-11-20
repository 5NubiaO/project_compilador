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
    mov J_val, 0
    mov J_val, 1
    mov al, 10
    sub al, 1
    inc al
    mov cl, al
    xor ch, ch
Para_1:
    mov al, J_val
     call ImprimirNumero
    IMPRIME Salto
    inc J_val
    loop Para_1
FinPara_1:
;Fin bloque PARA ------------------------------------
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
BufferPrint db 10, ?, 10 dup ('$')
J db 8, ?, 8 dup (24h)
J_val db 0
.STACK
END Inicio
