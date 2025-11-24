#include <stdint.h>

// PL011 UART base address on QEMU's virt machine
#define UART0_BASE 0x09000000UL
#define UART0_DR   (*(volatile uint32_t *)(UART0_BASE + 0x00))
#define UART0_FR   (*(volatile uint32_t *)(UART0_BASE + 0x18))
#define UART_FR_TXFF 0x20

static void uart_putc(char c) {
    // Wait until the transmit FIFO is not full
    while (UART0_FR & UART_FR_TXFF) {
        __asm__ volatile("wfe");
    }
    UART0_DR = (uint32_t)c;
}

static void uart_puts(const char *s) {
    while (*s) {
        if (*s == '\n') {
            uart_putc('\r');
        }
        uart_putc(*s++);
    }
}

void kernel_main(void) {
    uart_puts("Hello from the StoryViz kernel!\n");

    // Loop forever
    while (1) {
        __asm__ volatile("wfe");
    }
}
