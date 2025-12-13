# Este es el inicio de nuestra herramienta Ping Sweeper
# Es un script de prueba de conectividad básico y reutilizable.

import os
import sys

# Pedir la IP de destino al usuario para reutilización
target_ip = input("Por favor, introduce la IP de destino para el Ping (Ej: 10.0.0.1): ")

print(f"Iniciando prueba de ping en {target_ip}...")

# Comando de ping: -c 1 (solo un paquete), -W 1 (timeout de 1 segundo)
# Usamos 'os.system' para ejecutar el comando de terminal
response = os.system(f"ping -c 1 -W 1 {target_ip}")

if response == 0:
    print(f"\n[ÉXITO] Host {target_ip} está en línea (Responde a Ping).")
else:
    print(f"\n[FALLO] Host {target_ip} NO responde al Ping o está filtrado.")

print("Prueba de conectividad completada.")
