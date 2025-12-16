import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# ===============================================
# CONSTANTES
# ===============================================

# Tamaño del bloque AES. No se modifica.
BLOCK_SIZE = 16 

# ===============================================
# FUNCIONES DE CIFRADO Y DESCIFRADO
# ===============================================

def derive_key(password):
    """
    Deriva una clave criptográfica segura de 16 bytes a partir de la contraseña del usuario.
    
    Usamos SHA-256 para asegurar que la clave sea de 32 bytes (256 bits), 
    y luego la truncamos a 16 bytes (128 bits) para AES-128.
    """
    return hashlib.sha256(password.encode()).digest()[:BLOCK_SIZE]

def encrypt_file():
    """Función para cifrar un archivo."""
    
    file_path = input("Ruta del archivo a cifrar (Ej: documento.txt): ")
    password = input("Introduce la contraseña de cifrado: ")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] Archivo no encontrado en la ruta: {file_path}")
        return

    try:
        # 1. Derivar la clave
        key = derive_key(password)
        
        # 2. Generar un IV (Vector de Inicialización) único
        # El IV es crucial para que el cifrado sea seguro y diferente cada vez.
        iv = get_random_bytes(BLOCK_SIZE)
        
        # 3. Leer el contenido original del archivo
        with open(file_path, 'rb') as f:
            plaintext = f.read()
            
        # 4. Crear el objeto Cipher
        # Usamos AES en modo CBC (Cipher Block Chaining)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # 5. Rellenar y Cifrar
        # Padding (relleno) es necesario para que el tamaño del texto sea múltiplo de 16.
        ciphertext = cipher.encrypt(pad(plaintext, BLOCK_SIZE))
        
        # 6. Escribir el archivo cifrado
        # El archivo cifrado contendrá: [IV] + [Contenido Cifrado]
        encrypted_data = iv + ciphertext
        
        output_path = file_path + ".aes"
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        
        # 7. Opcional: Borrar el archivo original
        # os.remove(file_path)

        print(f"[ÉXITO] Archivo cifrado guardado en: {output_path}")
        print("¡ADVERTENCIA! Si pierdes la contraseña, el archivo será irrecuperable.")

    except Exception as e:
        print(f"[ERROR] Ocurrió un error durante el cifrado: {e}")


def decrypt_file():
    """Función para descifrar un archivo."""
    
    file_path = input("Ruta del archivo a descifrar (Debe terminar en .aes): ")
    password = input("Introduce la contraseña de descifrado: ")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] Archivo no encontrado en la ruta: {file_path}")
        return
    
    if not file_path.endswith('.aes'):
        print("[ERROR] El archivo de entrada debe ser un archivo cifrado (.aes).")
        return

    try:
        # 1. Derivar la clave
        key = derive_key(password)
        
        # 2. Leer datos del archivo cifrado
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
            
        # 3. Separar IV y Ciphertext
        # Los primeros 16 bytes son el IV
        iv = encrypted_data[:BLOCK_SIZE]
        ciphertext = encrypted_data[BLOCK_SIZE:]
        
        # 4. Crear el objeto Cipher
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # 5. Descifrar y Desrellenar (Unpadding)
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, BLOCK_SIZE)
        
        # 6. Escribir el archivo descifrado
        output_path = file_path.replace(".aes", "_decrypted")
        with open(output_path, 'wb') as f:
            f.write(plaintext)
            
        print(f"[ÉXITO] Archivo descifrado guardado en: {output_path}")
        
    except ValueError:
        print("[ERROR] Fallo en el descifrado. ¡Contraseña incorrecta o el archivo está corrupto!")
    except Exception as e:
        print(f"[ERROR] Ocurrió un error: {e}")


# ===============================================
# FUNCIÓN DEL MENÚ PRINCIPAL
# ===============================================

def main_menu():
    
    while True:
        print("\n" + "="*40)
        print("     HERRAMIENTA DE CIFRADO AES (Crypto-Tool)")
        print("="*40)
        print("1. Cifrar Archivo (Encrypt)")
        print("2. Descifrar Archivo (Decrypt)")
        print("3. Salir")
        print("="*40)
        
        choice = input("Seleccione una opción (1, 2 o 3): ")
        
        if choice == '1':
            encrypt_file()
        elif choice == '2':
            decrypt_file()
        elif choice == '3':
            print("\n¡Gracias por usar Crypto-Tool! Cerrando.")
            break
        else:
            print("\n[ERROR] Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main_menu()