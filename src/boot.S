.section .text
.global _start

_start:
    ldr x0, =_stack_top
    mov sp, x0

    /* Zero-initialize the .bss section */
    ldr x1, =_bss_start
    ldr x2, =_bss_end
    mov x3, #0
1:
    cmp x1, x2
    b.ge 2f
    str x3, [x1], #8
    b 1b
2:

    bl kernel_main
1:
    wfe
    b 1b

.size _start, . - _start
