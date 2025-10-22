# Rainfall
This project is the exploitation of (elf-like) binary


qemu-system-x86_64 -boot d -cdrom ./rainfall.iso -m 2048 -enable-kvm \
-net nic -net user,hostfwd=tcp::8888-:4242
``
ssh utilisateur@localhost -p 8888

x/10i $eip   # 32 bits
x/10i $rip   # 64 bits

) set disassembly-flavor intel
(gdb) x/20i $eip
