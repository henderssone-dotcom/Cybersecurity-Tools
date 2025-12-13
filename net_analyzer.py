import socket
import threading
import subprocess
import os
import time
from queue import Queue

# ===============================================
# CÓDIGO DEL ESCÁNER DE PUERTOS MULTIHILO (OPCIÓN 2)
# ===============================================

PORT_RANGE = range(1, 1025)
# Reutilizamos la función de escaneo de un solo puerto
def thread_port_scan(port_list_queue, target_ip, timeout=0.5):
    """Función worker que toma puertos de la cola y realiza la conexión."""
    while True:
        try:
            port = port_list_queue.get(timeout=1)
        except Exception:
            break
            
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        
        try:
            result = s.connect_ex((target_ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = "Desconocido"
                print(f"[+] PUERTO ABIERTO: {port} ({service})")

        except Exception:
            pass
            
        s.close()
        port_list_queue.task_done()

def do_port_scan():
    q_ports = Queue()
    print("\n--- EJECUTANDO ESCÁNER DE PUERTOS ---")
    
    target_ip = input("Introduce la IP de destino a escanear (Ej: 10.0.0.1): ")

    print(f"[!] Escaneando los puertos 1 a 1024 en {target_ip}...")
    for port in PORT_RANGE:
        q_ports.put(port)

    num_threads = 100
    start_time = time.time()
    
    for i in range(num_threads):
        worker = threading.Thread(target=thread_port_scan, args=(q_ports, target_ip))
        worker.setDaemon(True) 
        worker.start()

    q_ports.join()
    end_time = time.time()
    
    print("\n--- RESUMEN DEL ESCANEO ---")
    print(f"IP Escaneada: {target_ip}")
    print(f"Tiempo Total: {end_time - start_time:.2f} segundos")
    print("Escaneo de Puertos Completado.")

# ===============================================
# CÓDIGO DEL BARRIDO DE PING MULTIHILO (OPCIÓN 1)
# ===============================================

IP_RANGE = range(1, 255)

def thread_ping_scan(ip_list_queue, network_prefix):
    """Función worker para el barrido de ping."""
    while True:
        try:
            suffix = ip_list_queue.get(timeout=1)
        except Exception:
            break

        target_ip = f"{network_prefix}.{suffix}"
        command = f"ping -c 1 -W 1 {target_ip}"
        
        # Ocultar la salida normal del ping para solo mostrar los resultados ACTIVO
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"[+] HOST ACTIVO: {target_ip}")

        ip_list_queue.task_done()

def do_ping_sweep():
    q_ips = Queue()
    print("\n--- EJECUTANDO BARRIDO DE PING ---")
    
    network_prefix = input("Introduce la red base (Ej: 10.0.0): ")
    
    for suffix in IP_RANGE:
        q_ips.put(suffix)

    num_threads = 50
    start_time = time.time()
    print(f"[!] Iniciando barrido en la subred {network_prefix}.0/24 con {num_threads} hilos...")
    
    for i in range(num_threads):
        worker = threading.Thread(target=thread_ping_scan, args=(q_ips, network_prefix))
        worker.setDaemon(True)
        worker.start()

    q_ips.join()
    end_time = time.time()
    
    print("\n--- RESUMEN DEL BARRIDO ---")
    print(f"Tiempo Total: {end_time - start_time:.2f} segundos")
    print("Barrido de Ping Completado.")


# ===============================================
# FUNCIÓN DEL MENÚ PRINCIPAL
# ===============================================

def main_menu():
    
    while True:
        print("\n" + "="*40)
        print("     HERRAMIENTA MAESTRA DE ANÁLISIS DE REDES")
        print("="*40)
        print("1. Barrido de Ping de Subred (Ping Sweep)")
        print("2. Escáner Rápido de Puertos (Port Scanner)")
        print("3. Salir")
        print("="*40)
        
        choice = input("Seleccione una opción (1, 2 o 3): ")
        
        if choice == '1':
            do_ping_sweep()
        elif choice == '2':
            do_port_scan()
        elif choice == '3':
            print("\n¡Gracias por usar Net Analyzer! Cerrando.")
            break
        else:
            print("\n[ERROR] Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main_menu()