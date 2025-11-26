#include <stdint.h>

#define UART0_BASE 0x09000000UL
#define UART_DR (*(volatile uint32_t *)(UART0_BASE + 0x00))
#define UART_FR (*(volatile uint32_t *)(UART0_BASE + 0x18))
#define UART_FR_TXFF (1u << 5)

static void uart_putc(char c) {
    while (UART_FR & UART_FR_TXFF) {
        // Wait for space in the FIFO
    }
    UART_DR = (uint32_t)c;
}

static void uart_puts(const char *s) {
    while (*s) {
        uart_putc(*s++);
    }
}

void kernel_main(void) {
    uart_puts("Booting minimal ARM64 kernel on QEMU virt...\n");

    // Loop forever
    while (1) {
        __asm__ volatile("wfe");
    }
}
