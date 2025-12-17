import socket

def get_banner(ip, port):
    """
    Intenta conectarse a una IP y puerto específicos para capturar
    el mensaje de bienvenida (banner) del servicio.
    """
    try:
        # 1. Crear el objeto socket
        s = socket.socket()
        # 2. Establecer un tiempo de espera corto (2 segundos)
        s.settimeout(2)
        # 3. Intentar conectar
        s.connect((ip, port))
        
        # Enviamos un saludo genérico para que el servicio responda
        s.send# Enviamos una petición HTTP básica (Método HEAD)
        # Esto es como preguntar: "¿Quién eres?" sin pedir toda la página.
        s.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        
        # 4. Recibir el banner
        banner = s.recv(1024)
        # Algunos servicios requieren que envíes algo primero para responder,
        # pero muchos lo envían al conectar.
        banner = s.recv(1024)
        return banner.decode().strip()
    
    except socket.timeout:
        return "No se recibió respuesta (Timeout)"
    except ConnectionRefusedError:
        return "Conexión rechazada (Puerto cerrado)"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("--- ESCÁNER DE BANNER (VULNERABILITY RECON) ---")
    target = input("Introduce la IP a escanear (Ej: 10.0.0.1): ")
    ports = [21, 22, 25, 80, 443] # Puertos comunes: FTP, SSH, SMTP, HTTP, HTTPS

    print(f"\n[!] Analizando banners en {target}...\n")

    for port in ports:
        banner = get_banner(target, port)
        if banner:
            print(f"[+] Puerto {port}: {banner}")

if __name__ == "__main__":
    main()