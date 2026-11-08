#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║  GhostTrack v1.0                                             ║
║  Created by: sys-alderson-root                               ║
║  "Control is an illusion."                                   ║
║  fsociety // hello, friend.                                  ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import socket
import requests
import hashlib
import time

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    PHONE_ENABLED = True
except ImportError:
    PHONE_ENABLED = False

BANNER = r"""
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗████████╗██████╗  █████╗  ██████╗██╗  ██╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
██║  ███╗███████║██║   ██║███████╗   ██║      ██║   ██████╔╝███████║██║     █████╔╝ 
██║   ██║██╔══██║██║   ██║╚════██║   ██║      ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ 
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║      ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                                                                                     
     [ GhostTrack v1.0 ]   [ Created by: sys-alderson-root ]   [ fsociety ]
=====================================================================================
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    clear()
    print(BANNER)
    print(" [ 1 ] Tracker une adresse IP")
    if PHONE_ENABLED:
        print(" [ 2 ] Tracker un numéro de téléphone")
    else:
        print(" [ 2 ] Tracker un numéro (Module 'phonenumbers' manquant)")
    print(" [ 3 ] Tracker un nom d'utilisateur")
    print(" [ 4 ] Tracker une adresse email")
    print(" [ 5 ] Brute Force (Simulation locale)")
    print(" [ 6 ] Quitter")
    return input("\n[root@ghosttrack:~]# ")

def tracker_ip():
    ip = input("\n[?] Adresse IP à tracker : ").strip()
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        if data.get("status") == "success":
            print(f"\n[+] IP : {data.get('query')}")
            print(f"[+] Pays : {data.get('country')}")
            print(f"[+] Ville : {data.get('city')}")
            print(f"[+] FAI : {data.get('isp')}")
            print(f"[+] Localisation : {data.get('loc')}")
        else:
            print("[-] IP invalide ou introuvable.")
    except Exception as e:
        print(f"[-] Erreur : {e}")
    input("\n[>] Appuie sur Entrée...")

def tracker_tel():
    if not PHONE_ENABLED:
        print("\n[-] Module 'phonenumbers' non installé. Fais : pip install phonenumbers")
        input("\n[>] Appuie sur Entrée...")
        return
    num = input("\n[?] Numéro (format +336XXXXXXXX) : ").strip()
    try:
        parsed = phonenumbers.parse(num)
        print(f"\n[+] Pays : {geocoder.description_for_number(parsed, 'fr')}")
        print(f"[+] Opérateur : {carrier.name_for_number(parsed, 'fr')}")
        print(f"[+] Fuseau : {timezone.time_zones_for_number(parsed)}")
    except:
        print("[-] Numéro invalide.")
    input("\n[>] Appuie sur Entrée...")

def tracker_username():
    username = input("\n[?] Nom d'utilisateur : ").strip()
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "TikTok": f"https://tiktok.com/@{username}"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"\n[*] Recherche de {username}...\n")
    for site, url in sites.items():
        try:
            r = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
            
            if r.status_code == 200:
                print(f"[+] TROUVÉ sur {site} : {url}")
            elif r.status_code == 404:
                print(f"[-] NON TROUVÉ sur {site}")
            else:
                print(f"[?] INCERTAIN sur {site} (Code {r.status_code})")
        except:
            print(f"[!] ERREUR sur {site}")
    input("\n[>] Appuie sur Entrée...")

def tracker_email():
    email = input("\n[?] Adresse email : ").strip()
    hash_md5 = hashlib.md5(email.strip().lower().encode()).hexdigest()
    print(f"\n[+] Hash MD5 (pour Gravatar) : {hash_md5}")
    print(f"[+] Gravatar : https://www.gravatar.com/avatar/{hash_md5}")
    print(f"[+] Have I Been Pwned : https://haveibeenpwned.com/account/{email}")
    print(f"[+] Google Search : https://www.google.com/search?q={email}")
    input("\n[>] Appuie sur Entrée...")

def brute_force():
    print("\n[?] Mode Brute Force (Simulation locale)")
    target = input("[?] Hash cible (MD5/SHA1/SHA256) : ").strip().lower()
    wordlist_path = input("[?] Wordlist (ex: rockyou.txt) : ").strip()
    
    try:
        with open(wordlist_path, "r", encoding="latin-1", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[-] Fichier introuvable.")
        input("\n[>] Appuie sur Entrée...")
        return

    print(f"\n[*] Test de {len(passwords)} mots...")
    for i, mdp in enumerate(passwords, 1):
        if hashlib.md5(mdp.encode()).hexdigest() == target:
            print(f"\n[+] BOOM ! (MD5) Mot de passe : {mdp}")
            input("\n[>] Appuie sur Entrée...")
            return
        elif hashlib.sha1(mdp.encode()).hexdigest() == target:
            print(f"\n[+] BOOM ! (SHA1) Mot de passe : {mdp}")
            input("\n[>] Appuie sur Entrée...")
            return
        elif hashlib.sha256(mdp.encode()).hexdigest() == target:
            print(f"\n[+] BOOM ! (SHA256) Mot de passe : {mdp}")
            input("\n[>] Appuie sur Entrée...")
            return
        if i % 10000 == 0:
            print(f"[*] {i} mots testés...", end="\r")
            
    print("\n[-] ÉCHEC : Introuvable.")
    input("\n[>] Appuie sur Entrée...")

def main():
    while True:
        choix = menu()
        if choix == "1":
            tracker_ip()
        elif choix == "2":
            tracker_tel()
        elif choix == "3":
            tracker_username()
        elif choix == "4":
            tracker_email()
        elif choix == "5":
            brute_force()
        elif choix == "6":
            print("\n[i] Fermeture de GhostTrack. Au revoir, friend.")
            break
        else:
            print("\n[-] Choix invalide.")
            input("[>] Appuie sur Entrée...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] Interrompu.")
        sys.exit()
