ENTRY(_start)
SECTIONS
{
    . = 0x40080000; /* Load address for QEMU virt */

    .text : {
        *(.text*)
    }

    .rodata : {
        *(.rodata*)
    }

    .data : {
        *(.data*)
    }

    .bss : {
        _bss_start = .;
        *(.bss*)
        *(COMMON)
        _bss_end = .;
    }

    . = ALIGN(16);
    _stack_top = . + 0x10000; /* 64 KiB stack */
}
