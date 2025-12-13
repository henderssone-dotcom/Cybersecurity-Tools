import socket
import threading
from queue import Queue
import time

# ===============================================
# CONFIGURACIÓN INICIAL
# ===============================================

# Rango de puertos comunes a escanear. 
# Escanearemos los primeros 1024 puertos conocidos.
PORT_RANGE = range(1, 1025)

# Cola para almacenar los números de puerto que vamos a escanear
q = Queue()

# ===============================================
# FUNCIÓN DE ESCANEO DE PUERTO (EJECUTADA POR HILO)
# ===============================================

def thread_port_scan(port_list_queue, target_ip, timeout=0.5):
    """Función worker que toma puertos de la cola y realiza la conexión."""
    while True:
        # Intenta obtener un puerto de la cola. Si la cola está vacía, sale.
        try:
            port = port_list_queue.get(timeout=1)
        except Exception:
            break
            
        # 1. Crear el objeto socket (IPv4 y TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout) # Tiempo máximo para esperar la respuesta
        
        try:
            # 2. Intentar la conexión. connect_ex devuelve 0 si es exitoso.
            result = s.connect_ex((target_ip, port))

            if result == 0:
                try:
                    # Intenta obtener el nombre del servicio para hacerlo más legible
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = "Desconocido"
                
                print(f"[+] PUERTO ABIERTO: {port} ({service})")

        except Exception as e:
            # Manejar errores de red o DNS si ocurren
            pass
            
        s.close()
        
        # Marca la tarea como completada para la cola
        port_list_queue.task_done()

# ===============================================
# FUNCIÓN PRINCIPAL
# ===============================================

def run_multithread_scanner():
    print("--- ESCÁNER DE PUERTOS AVANZADO (Multihilo) ---")
    
    # 1. Pedir la IP de destino
    target_ip = input("Introduce la IP de destino a escanear (Ej: 10.0.0.1): ")

    # 2. Llenar la cola con todos los puertos a escanear
    print(f"[!] Escaneando los puertos 1 a 1024 en {target_ip}...")
    for port in PORT_RANGE:
        q.put(port)

    # 3. Iniciar los hilos (workers)
    # Usaremos 100 hilos para escanear 1024 puertos muy rápidamente.
    num_threads = 100
    threads = []
    
    start_time = time.time()
    
    for i in range(num_threads):
        # Pasar la cola, la IP de destino y el timeout a la función worker
        worker = threading.Thread(target=thread_port_scan, args=(q, target_ip))
        worker.setDaemon(True) 
        worker.start()
        threads.append(worker)

    # 4. Esperar a que la cola termine
    q.join()

    end_time = time.time()
    
    print("\n--- RESUMEN DEL ESCANEO ---")
    print(f"IP Escaneada: {target_ip}")
    print(f"Puertos: 1 a 1024")
    print(f"Tiempo Total: {end_time - start_time:.2f} segundos")
    print("Escaneo Completado.")


if __name__ == "__main__":
    run_multithread_scanner()