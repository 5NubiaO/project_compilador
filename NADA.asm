.MODEL SMALL
.CODE
Inicio:
    mov Ax, @Data
    mov Ds, Ax
    mov ax, 4C00h
    int 21h
.DATA
Salto db 10,13,24h
.STACK
END Inicio
