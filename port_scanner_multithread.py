import socket       # Para las conexiones de red (la "puerta")
import threading    # Para crear hilos (trabajadores paralelos)
from queue import Queue # Estructura de datos "Thread-Safe" (segura para hilos)
import sys          # Para salir del programa limpiamente si hay error

# ==========================================
# 1. CONFIGURACIÓN INTERACTIVA (INPUTS)
# ==========================================
print("--- ESCÁNER MULTIHILO (THREADED) ---\n")
print("[*] Modo Educativo: Activado\n")

# Pedimos la IP al usuario. 
target = input("Introduce la IP a escanear (Ej: 192.168.0.50): ")

# Pedimos el rango de puertos y validamos que sean números.
try:
    start_port = int(input("Puerto inicial (Ej: 1): "))
    end_port = int(input("Puerto final (Ej: 1000): "))
except ValueError:
    print("\n[!] Error: Debes introducir números enteros.")
    sys.exit() # Cierra el programa si el usuario escribe letras en vez de números

# ==========================================
# 2. PREPARACIÓN DE HERRAMIENTAS
# ==========================================

# Creamos la COLA (Queue).
# Diferencia con una lista normal []:
# Una lista normal puede corromperse si 100 hilos intentan leerla a la vez.
# La Queue gestiona el tráfico automáticamente ("Pase usted, luego usted...").
queue = Queue()

# Lista normal para guardar los resultados (puertos abiertos).
open_ports = []

# ==========================================
# 3. DEFINICIÓN DEL TRABAJO (WORKER)
# ==========================================

def port_scan(port):
    """
    Función que hace el trabajo sucio: intenta conectar a UN puerto.
    Es la misma lógica que usaste en scanner_v2.py.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) # Esperamos máximo 1 segundo
        result = s.connect_ex((target, port))
        
        if result == 0:
            # Si conecta, guardamos el puerto en la lista de hallazgos
            open_ports.append(port)
            
        s.close() # Siempre cerramos el socket
    except:
        pass

def worker():
    """
    Esta es la vida de cada Hilo (Cajero).
    Es un bucle infinito que solo para cuando se apaga el programa.
    """
    while not queue.empty():
        # 1. Obtener tarea: Saca un número de puerto de la cola
        port = queue.get()
        
        # 2. Trabajar: Llama a la función de escaneo
        port_scan(port)
        
        # 3. Avisar: Le dice a la Queue "Ya terminé con este puerto, dame otro o táchalo"
        queue.task_done()

# ==========================================
# 4. EJECUCIÓN PRINCIPAL (EL JEFE DE OBRA)
# ==========================================

# LLENADO DE LA COLA:
# Metemos todas las tareas (puertos) en la cola antes de empezar.
# range(start, end + 1) es necesario porque Python excluye el último número por defecto.
for port in range(start_port, end_port + 1):
    queue.put(port)

print(f"\n[*] Iniciando escaneo en {target} con 100 hilos paralelos...")

# CONTRATACIÓN DE HILOS:
# Creamos 100 hilos para procesar la cola rápidamente.
for t in range(100):
    thread = threading.Thread(target=worker)
    
    # Daemon = True es VITAL.
    # Significa: "Si el programa principal termina, mata a este hilo inmediatamente".
    # Sin esto, el programa se quedaría colgado esperando eternamente aunque el trabajo haya terminado.
    thread.daemon = True
    
    thread.start() # ¡A trabajar!

# ESPERA FINAL (JOIN):
# queue.join() bloquea el script principal.
# Le dice al programa: "No te cierres hasta que la cola esté vacía".
queue.join()

print("----------------------------------------------------")
# Imprimimos la lista ordenada (sorted) para que se vea bonito
print(f"Puertos abiertos en {target}: {sorted(open_ports)}")
print("----------------------------------------------------")
print("[*] Escaneo finalizado.")