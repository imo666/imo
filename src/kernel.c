#include <stdint.h>

void kernel_main(void) {
    // Loop forever
    while (1) {
        __asm__ volatile("wfe");
    }
}
