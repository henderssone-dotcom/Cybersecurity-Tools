import os       # Librería para ejecutar comandos del sistema (como escribir en la terminal)
import platform # Librería para detectar si estamos en Mac, Windows o Linux
import socket   # Librería para redes (la usaremos para averiguar nombres de equipos)
import sys      # Librería para interactuar con el sistema (necesaria para salir con Ctrl+C)
from datetime import datetime # Para mostrar la hora exacta de inicio

# ==========================================
# 1. BLOQUE PRINCIPAL PROTEGIDO (TRY)
# ==========================================
# Iniciamos el bloque 'try' AQUÍ arriba para proteger TODO el programa.
# Si el usuario presiona Ctrl+C en cualquier momento (incluso al introducir la IP),
# el programa saltará al bloque 'except' del final, evitando errores rojos feos.
try:
    print("--- BARRIDO DE PING (PING SWEEP) ---")
    print("[*] Modo Educativo: Activado (Versión Blindada y Comentada)\n")

    # Solicitamos la red al usuario.
    # Al estar dentro del try, si cancelas aquí, se cierra limpio.
    net = input("Introduce la red base (Ej: 10.0.0): ")

    # ==========================================
    # 2. DETECCIÓN INTELIGENTE DEL SISTEMA
    # ==========================================
    # El comando 'ping' usa banderas (flags) distintas según el sistema operativo.
    # Aquí automatizamos esa detección para que el script sea "Cross-Platform".
    
    sistema_actual = platform.system()

    if sistema_actual == "Windows":
        # CONFIGURACIÓN PARA WINDOWS
        # -n 1 : Envía solo 1 paquete (ping) por IP.
        # -w 200 : Espera máximo 200 milisegundos.
        parametro_ping = "-n 1 -w 200"
    else:
        # CONFIGURACIÓN PARA MAC / LINUX
        # -c 1 : Envía solo 1 paquete (count).
        # -W 500 : Espera máximo 500 milisegundos (0.5 seg).
        # NOTA: El timeout (-W) es CRÍTICO para la velocidad. Sin él, 
        # esperaríamos 10 seg por cada IP vacía.
        parametro_ping = "-c 1 -W 500"

    print(f"\n[*] Sistema detectado: {sistema_actual}")
    print(f"[*] Iniciando barrido rápido en {net}.1 hasta {net}.254...")
    print(f"[*] Hora de inicio: {datetime.now()}")
    print("-" * 60)

    # ==========================================
    # 3. EL BUCLE DE BÚSQUEDA (EL MOTOR)
    # ==========================================
    # Recorremos el rango estándar de una subred doméstica (1-254).
    for ip_host in range(1, 255):
        
        # Construimos la IP completa concatenando strings.
        # Ej: "10.0.0" + "." + "50" -> "10.0.0.50"
        ip = net + "." + str(ip_host)
        
        # Armamos el comando final.
        # Ej: "ping -c 1 -W 500 10.0.0.50"
        comando = f"ping {parametro_ping} {ip}"
        
        # EJECUCIÓN DEL COMANDO:
        # os.popen() abre una tubería al sistema y ejecuta el comando.
        # .read() captura la respuesta de texto de la terminal.
        respuesta = os.popen(comando).read()
        
        # ANÁLISIS DE LA RESPUESTA:
        # Buscamos "ttl" (Time To Live). Si aparece, el host respondió.
        # Usamos .lower() para evitar problemas con mayúsculas/minúsculas.
        if "ttl" in respuesta.lower():
            print(f"[+] ¡VIVO! -> {ip}")
            
            # BONUS: RESOLUCIÓN DNS INVERSA
            # Intentamos obtener el Hostname (nombre del equipo).
            try:
                # socket.gethostbyaddr devuelve (hostname, alias, ip_list).
                # Tomamos [0] que es el nombre principal.
                nombre = socket.gethostbyaddr(ip)[0]
                print(f"    └── Hostname: {nombre}")
            except:
                # Si falla (común en redes domésticas), no rompemos el programa.
                print("    └── Hostname: Desconocido")

    print("-" * 60)
    print("[*] Barrido completado.")

# ==========================================
# 4. GESTIÓN DE ERRORES (EXCEPT)
# ==========================================
except KeyboardInterrupt:
    # Este bloque captura EXCLUSIVAMENTE la interrupción de teclado (Ctrl + C).
    print("\n\n[!] Interrupción detectada por el usuario.")
    print("[!] Deteniendo operaciones y saliendo de forma segura...")
    sys.exit() # Cierra el script sin dejar procesos colgados.