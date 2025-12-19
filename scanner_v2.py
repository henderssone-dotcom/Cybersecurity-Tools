import socket  # Librería base para comunicaciones de red
import sys     # Librería para interactuar con el sistema (necesaria para salir limpiamente)

# ==========================================
# CONFIGURACIÓN INICIAL
# ==========================================

# Pedimos la IP. input() siempre devuelve un texto (string).
target_ip = input("Por favor, introduce la IP a escanear (Ej: 10.0.0.1 o 127.0.0.1): ")

# Lista de puertos comunes a verificar:
# 21: FTP (Transferencia de archivos)
# 22: SSH (Conexión remota segura - Linux/Raspberry)
# 80: HTTP (Web no segura)
# 443: HTTPS (Web segura)
port_range = [21, 22, 80, 443]

# Establecemos un tiempo de espera de 1 segundo.
# Si el puerto no responde en 1 seg, asumimos que está cerrado/filtrado.
# Sin esto, el programa podría quedarse "colgado" infinitamente esperando respuesta.
socket.setdefaulttimeout(1)

print(f"[*] Iniciando escaneo educativo en {target_ip}...\n")

# ==========================================
# BUCLE DE ESCANEO
# ==========================================

try:
    # Iteramos sobre cada puerto de nuestra lista
    for port in port_range:
        
        # 1. CREACIÓN DEL SOCKET (La "Puerta")
        # socket.AF_INET  -> Indica que usaremos IPv4 (ej. 192.168.1.1)
        # socket.SOCK_STREAM -> Indica que usaremos TCP (Protocolo orientado a conexión, fiable)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 2. INTENTO DE CONEXIÓN
        # Usamos connect_ex() en lugar de connect().
        # - connect(): Si falla, lanza una excepción (error) y detiene el programa.
        # - connect_ex(): Si falla, solo devuelve un número de error, permitiendo que el programa siga.
        # Devuelve 0 si la conexión fue exitosa (Puerto Abierto).
        result = s.connect_ex((target_ip, port))
        
        # 3. VERIFICACIÓN DEL RESULTADO
        if result == 0:
            print(f"[+] Puerto {port}: ABIERTO")
        else:
            # Si result es diferente de 0, hubo un error (puerto cerrado o filtrado).
            # Ejemplos de códigos de error: 111 (Connection refused), 11 (Resource temporarily unavailable)
            print(f"[-] Puerto {port}: CERRADO/FILTRADO (Código: {result})")
            
        # 4. CIERRE DEL SOCKET
        # Es vital cerrar el socket después de usarlo para liberar los recursos del sistema.
        s.close()

except KeyboardInterrupt:
    # Este bloque se ejecuta SI Y SOLO SI el usuario presiona Ctrl + C
    print("\n\n[!] Interrupción detectada (Ctrl+C).")
    print("[!] Saliendo del programa de forma segura...")
    sys.exit() # Cierra el script inmediatamente sin mostrar errores feos

print("\n[*] Escaneo completado con éxito.")