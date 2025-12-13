import socket

# Pedir la IP de destino al usuario
target_ip = input("Por favor, introduce la IP a escanear (Ej: 10.0.0.1 o 127.0.0.1): ")
port_range = [21, 22, 80, 443] 

# Establecer un timeout de 1 segundo (necesario para no colgarse)
socket.setdefaulttimeout(1) 

print(f"Iniciando escaneo simple en {target_ip}...")

for port in port_range:
    # Creamos el objeto socket (IPv4 y TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Intentamos la conexión. connect_ex devuelve 0 si es exitoso.
    result = s.connect_ex((target_ip, port))

    if result == 0:
        print(f"Puerto {port}: ABIERTO")
    else:
        # Aquí puedes ver el código de error si quieres (ej. 111)
        print(f"Puerto {port}: CERRADO/FILTRADO")

    s.close() 

print("Escaneo completado.")