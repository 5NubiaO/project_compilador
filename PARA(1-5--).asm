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
    mov K_val, 0
    mov J_val, 1
    mov al, 5
    sub al, 1
    inc al
    push cx
    mov cl, al
    xor ch, ch
Para_1:
    mov al, J_val
    mov K_val, al
    mov al, 5
    sub al, J_val
    inc al
    push cx
    mov cl, al
    xor ch, ch
Para_2:
    mov al, K_val
     call ImprimirNumero
    IMPRIME Salto
    inc K_val
    loop Para_2
    pop cx
FinPara_2:
;Fin bloque PARA ------------------------------
    IMPRIME Mge1
    IMPRIME Salto
    inc J_val
    loop Para_1
FinPara_1:
;Fin bloque PARA ------------------------------
    IMPRIME Mge2
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
Mge1 db ",$"
Mge2 db " $"
BufferPrint db 10, ?, 10 dup ('$')
J db 8, ?, 8 dup (24h)
J_val db 0
K db 8, ?, 8 dup (24h)
K_val db 0
.STACK
END Inicio
