CROSS_COMPILE=aarch64-linux-gnu-
CC=$(CROSS_COMPILE)gcc
LD=$(CROSS_COMPILE)ld
OBJCOPY=$(CROSS_COMPILE)objcopy
CFLAGS=-nostdlib -nostartfiles -ffreestanding -fno-builtin -Wall -O2

all: kernel8.img

boot.o: src/boot.S
	$(CC) $(CFLAGS) -c -o boot.o src/boot.S

kernel.o: src/kernel.c
	$(CC) $(CFLAGS) -c -o kernel.o src/kernel.c

kernel8.elf: boot.o kernel.o linker.ld
	$(LD) -T linker.ld -o kernel8.elf boot.o kernel.o

kernel8.img: kernel8.elf
	$(OBJCOPY) -O binary kernel8.elf kernel8.img

clean:
	rm -f *.o kernel8.elf kernel8.img

.PHONY: all clean
