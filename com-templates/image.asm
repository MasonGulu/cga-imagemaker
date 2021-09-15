org 0x100
cpu 8086


DELAYTIMEH      equ 1
                ; 1 = 0xffff iterations
                ; 10 = ~8 seconds
                ; 1 = 0.8 seconds
IMAGETYPE       equ 4
                ; Image type
                ; 0 unchanged
                ; 1 320x200 palette 0
                ; 2 320x200 palette 1 
                ; 3 640x200
                ; 4 80 x100 composite
IMAGESIZE       equ 16000
IMAGESTART      equ (16000 - IMAGESIZE)
IMAGEMODE       equ 2
                ; Mode
                ; 0 delay and then exit, resetting video
                ; 1 delay and then exit, don't reset video
                ; 2 wait for keyboard, reset video
                ; 3 wait for keyboard, don't reset video

; CONSTANTS
CGA_REG_SELECT  equ 0x3D4
CGA_REG_CONTENT equ 0x3D5
CGA_MODE        equ 0x3D8
CGA_COLOR       equ 0x3D9
IMAGE_DATA_LEN  equ 7
ONE_SECOND      equ 18136

entry:
    mov ax, 0xb800
    push es 
    mov es, ax 
                ; AX contains the address of DATA_imagetype
handle_image:
    mov al, IMAGETYPE
    cmp al, 0
    je load_image; Video mode is unchanged, just load the next image

    cmp al, 1 
    je CGA_320_0; 320x200 palette 0

    cmp al, 2 
    je CGA_320_1; 320x200 palette 1

    cmp al, 3 
    je CGA_640  ; 640x200

    cmp al, 4 
    je COMP_160 ; 160x80 

    jmp exit

CGA_320_0:
    mov ax, 0x0004
    int 0x10    ; Make the bios set the video mode to 320x200 color

    mov dx, CGA_COLOR
    mov al, 0b000000
    out dx, al  ; Set color palette to 0

    jmp load_image
CGA_320_1:
    mov ax, 0x0004
    int 0x10    ; Make the bios set the video mode to 320x200 color
    
    mov dx, CGA_COLOR
    mov al, 0b100000
    out dx, al  ; Set color palette to 1

    jmp load_image
CGA_640:
    mov ax, 0x0006
    int 0x10    ; Make the bios set the video mode to 640x200

    jmp load_image
COMP_160:
    mov dx, CGA_MODE 
    mov al, 0b000001
    out dx, al  ; Set mode to 80x25 and disable video signal

    mov dx, CGA_REG_SELECT 
    mov al, 0x04
    out dx, al 
    mov dx, CGA_REG_CONTENT 
    mov al, 0x7f
    out dx, al  ; Set vertical line total to 127

    mov dx, CGA_REG_SELECT
    mov al, 0x06
    out dx, al 
    mov dx, CGA_REG_CONTENT
    mov al, 0x64
    out dx, al  ; Set vertical displayed character rows to 100

    mov dx, CGA_REG_SELECT
    mov al, 0x07
    out dx, al 
    mov dx, CGA_REG_CONTENT
    mov al, 0x70
    out dx, al  ; Set vertical scan position to 112

    mov dx, CGA_REG_SELECT
    mov al, 0x09
    out dx, al 
    mov dx, CGA_REG_CONTENT
    mov al, 0x01
    out dx, al  ; Set character scan line count to 1
    ; Code adapted from https://github.com/drwonky/cgax16demo/blob/master/CGA16DMO.CPP

    mov dx, CGA_MODE 
    mov al, 0b001001
    out dx, al  ; Enable video again
load_image:
    ; Copy image into memory
    mov cx, IMAGESIZE
                ; CX tells rep how many times to repeat.
    mov si, DATA_image
                ; Source offset DS:SI
    mov di, IMAGESTART
                ; Starting offset in CGA ram ES:DI
    pushf 
    cld         ; Make sure movsb increments SI and DI
    rep movsb   ; Copy!
    popf
    mov al, IMAGEMODE 
    cmp al, 2
    je keyboard_wait
                ; Keyboard mode
                ; if not then fall through to do_delay
    mov al, IMAGEMODE 
    cmp al, 3
    je keyboard_wait

do_delay:
    mov ax, DELAYTIMEH 
    delay:
        cmp ax, 0
        je exit_delay
        call SUB_delay
        sub ax, 1
        jmp delay
    exit_delay:
    mov al, IMAGEMODE 
    cmp al, 1
    je exit 
    jmp reset_video

keyboard_wait:
    mov ax, 0
    int 0x16    ; Wait for keyboard
    mov al, IMAGEMODE
    cmp al, 3
    je exit     ; Don't reset video
reset_video:
    mov ax, 0x0003
    int 0x10    ; Change video mode
exit:
    pop es 
    mov ah, 0x4C
    mov al, 0
    int 0x21    ; Terminate program DOS
    retf        ; Terminate program BASIC

SUB_delay:
    push ax 
    mov ax, 0xffff
    delay_loop:
        cmp ax, 0
        je delay_finish
        sub ax, 1
        jmp delay_loop
    delay_finish:
        pop ax 
        ret 

DATA_image: