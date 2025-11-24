CROSS_COMPILE ?= aarch64-linux-gnu-
CC := $(CROSS_COMPILE)gcc
LD := $(CROSS_COMPILE)ld
OBJCOPY := $(CROSS_COMPILE)objcopy
CFLAGS := -nostdlib -nostartfiles -ffreestanding -fno-builtin -Wall -O2

QEMU ?= qemu-system-aarch64
QEMU_FLAGS := -M virt -cpu cortex-a53 -nographic

all: kernel8.img

boot.o: src/boot.S
	$(CC) $(CFLAGS) -c -o $@ $<

kernel.o: src/kernel.c
	$(CC) $(CFLAGS) -c -o $@ $<

kernel8.elf: boot.o kernel.o linker.ld
	$(LD) -T linker.ld -o $@ boot.o kernel.o

kernel8.img: kernel8.elf
	$(OBJCOPY) -O binary $< $@

run: kernel8.img
	$(QEMU) $(QEMU_FLAGS) -kernel $<

clean:
	rm -f *.o kernel8.elf kernel8.img

.PHONY: all clean run
