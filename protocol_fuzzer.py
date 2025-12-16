import socket
import time
import sys

# ===============================================
# CONFIGURACIÓN DEL FUZZER
# ===============================================

# El comando de un protocolo que vamos a fuzzer. 
# En este caso, simularemos un comando de protocolo simple (Ej: HTTP, FTP)
FUZZ_COMMAND = "OVERFLOW "

# Carácter a usar en el payload (la 'A' es el estándar en fuzzing)
FUZZ_CHAR = "A"

# Rango del payload (de 100 en 100 hasta 5000 bytes)
START_SIZE = 100
END_SIZE = 5000
STEP = 100

# ===============================================
# FUNCIÓN DE FUZZING
# ===============================================

def run_fuzzer():
    print("--- PROTOCOL FUZZER BÁSICO ---")
    
    # 1. Pedir la configuración de destino
    target_ip = input("Introduce la IP de destino (Ej: 10.0.0.1): ")
    try:
        target_port = int(input("Introduce el Puerto de destino (Ej: 80): "))
    except ValueError:
        print("[ERROR] El puerto debe ser un número entero.")
        return

    print(f"\n[!] Iniciando fuzzing en {target_ip}:{target_port} con incrementos de {STEP} bytes...")

    # 2. Bucle principal del fuzzing
    for size in range(START_SIZE, END_SIZE, STEP):
        
        # 3. Crear el payload
        # El payload es el comando más las 'A' repetidas (ej: "OVERFLOW AAAAA...")
        payload = FUZZ_COMMAND + (FUZZ_CHAR * size)
        
        # Convertir el payload a bytes (necesario para la conexión de socket)
        payload_bytes = payload.encode('latin-1') + b'\r\n' # \r\n es el salto de línea HTTP/FTP
        
        print(f"[>] Enviando payload de tamaño: {len(payload_bytes)} bytes...")

        try:
            # 4. Crear y conectar el socket (Timeout bajo)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2) # Esperar 2 segundos para la respuesta
            s.connect((target_ip, target_port))
            
            # 5. Enviar el payload
            s.send(payload_bytes)
            
            # 6. Recibir la respuesta del servidor (Opcional, solo para confirmar que sigue vivo)
            response = s.recv(1024)
            s.close()

            # Esperar un poco para que el servidor se recupere entre intentos
            time.sleep(1) 

        except socket.timeout:
            print(f"[CRASH DETECTADO] El host {target_ip} no respondió después de enviar {len(payload_bytes)} bytes.")
            print("El servicio puede haber colapsado o estar sobrecargado.")
            return # Detener el fuzzer
            
        except ConnectionRefusedError:
            print(f"[CRASH DETECTADO] Conexión rechazada después de enviar {len(payload_bytes)} bytes.")
            print("El servicio se cerró o reinició abruptamente.")
            return # Detener el fuzzer
            
        except Exception as e:
            print(f"[CRASH/ERROR] Un error inesperado ocurrió en {len(payload_bytes)} bytes: {e}")
            return # Detener el fuzzer

    print("\n[ÉXITO] El servicio parece robusto. No se detectó un crash hasta 5000 bytes.")

# ===============================================
# EJECUCIÓN
# ===============================================

if __name__ == "__main__":
    run_fuzzer()