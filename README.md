# Minimal ARM64 Kernel Example

This repository contains a very small example of a bare-metal AArch64 (ARM64) kernel. The code boots on the QEMU `virt` machine and immediately enters an infinite low-power wait loop.

## Building

A cross compiler for AArch64 is required. On Ubuntu it can be installed with:

```sh
sudo apt-get install gcc-aarch64-linux-gnu
```

Build the kernel image:

```sh
make
```

This produces `kernel8.img`.

## Running with QEMU

The kernel can be run with QEMU using:

```sh
qemu-system-aarch64 -M virt -cpu cortex-a53 -nographic -kernel kernel8.img
```

The kernel writes a short boot message to the PL011 UART, which appears on the `qemu-system-aarch64` console. After printing, it idles in a low-power wait loop.
