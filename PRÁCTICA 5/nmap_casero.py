import sys
import socket

# Puertos por defecto a escanear.
PUERTOS_POR_DEFECTO = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080]

# Tiempo de espera para la conexión
TIMEOUT = 1


def comprobar_ip_estructura(ip: str) -> bool:
    """
    Se encarga de comprobar si la estructura de la IP es válida.

    Args:
        ip (str): La dirección IP a comprobar.

    Returns:
        bool: True si la estructura de la IP es válida, False en caso contrario.
    """
    octetos = ip.split(".")
    if len(octetos) != 4:
        print("Error:  Longitud incorrecta de la IP.  Debe tener solo cuatro octetos.  Ej: 192.168.1.1")
        return False

    for posicion, octeto in enumerate(octetos, 1):
        if not octeto.isdigit():
            print(f"Error: En la IP {ip}, el octeto en la posición {posicion} no contiene solo dígitos.")
            return False
        valor = int(octeto)
        if valor < 0 or valor > 255:
            print(f"Error: En la IP {ip}, el octeto en la posición {posicion} está fuera de rango (0-255).")
            return False
    return True


def validar_puertos(lista_puertos_str: str) -> list | None:
    """
    Valida y convierte una cadena de puertos separados por comas en una lista de enteros.

    Args:
        lista_puertos_str (str): Cadena con los puertos separados por comas.

    Returns:
        list: Lista de puertos válidos o None si hay algún error.
    """
    puertos = []
    elementos = lista_puertos_str.split(",")

    for elemento in elementos:
        elemento = elemento.strip()

        # Verificar que sea un número entero
        if not elemento.isdigit():
            print(f"Error: '{elemento}' no es un número de puerto válido.")
            return

        puerto = int(elemento)

        if puerto < 1 or puerto > 65535:
            print(f"Error: El puerto {puerto} está fuera del rango permitido (1-65535).")
            return

        # Verificar duplicados
        if puerto in puertos:
            print(f"Advertencia: El puerto {puerto} está duplicado.  Se ignorará el duplicado.")
        else:
            puertos.append(puerto)

    return puertos


def escanear_puerto(ip: str, puerto: int) -> bool:
    """
    Intenta establecer una conexión TCP con el puerto especificado.

    Args:
        ip (str): La dirección IP del host.
        puerto (int): El número de puerto a escanear.

    Returns:
        bool: True si el puerto está abierto, False si está cerrado o no accesible.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        # Intentar conectar al puerto
        resultado = sock.connect_ex((ip, puerto))
        sock.close()

        # Si resultado es 0, la conexión fue exitosa (puerto abierto)
        return resultado == 0

    except socket.error:
        return False
    except:
        return False


def escanear_puertos(ip: str, puertos: list) -> dict:
    """
    Escanea una lista de puertos en la IP especificada.

    Args:
        ip (str): La dirección IP del host.
        puertos (list): Lista de puertos a escanear.

    Returns:
        dict: Diccionario con los resultados del escaneo.
    """
    resultados = {"abiertos": [], "cerrados": []}

    print(f"\nEscaneando {len(puertos)} puerto(s) en {ip}.. .\n")

    for puerto in puertos:
        if escanear_puerto(ip, puerto):
            print(f"Puerto {puerto}:  ABIERTO")
            resultados["abiertos"].append(puerto)
        else:
            print(f"Puerto {puerto}: CERRADO")
            resultados["cerrados"].append(puerto)

    return resultados


def mostrar_resumen(resultados: dict) -> None:
    """
    Muestra un resumen del escaneo realizado.

    Args:
        resultados (dict): Diccionario con los resultados del escaneo.
    """
    total = len(resultados["abiertos"]) + len(resultados["cerrados"])
    abiertos = len(resultados["abiertos"])

    print(f"\n=== RESUMEN DEL ESCANEO ===")
    print(f"Total de puertos analizados: {total}")
    print(f"Puertos abiertos: {abiertos}")
    print(f"Puertos cerrados: {total - abiertos}")

    if resultados["abiertos"]:
        print(f"\nPuertos abiertos encontrados: {', '.join(map(str, resultados['abiertos']))}")


def mostrar_uso() -> None:
    """
    Muestra el mensaje de uso del programa.
    """
    print("Argumentos incorrectos.")
    print(f"Uso:  python3 {sys.argv[0]} <ip> [-p lista_puertos]")
    print("\nEjemplos:")
    print(f"  python3 {sys.argv[0]} 192.168.1.10")
    print(f"  python3 {sys.argv[0]} 192.168.1.10 -p 22,80,443")


def procesar_argumentos() -> tuple:
    """
    Procesa los argumentos de línea de comandos.

    Returns:
        tuple: (ip, puertos) o None, None si hay error.
    """
    argc = len(sys.argv)

    if argc == 2:
        ip = sys.argv[1]
        return (ip, PUERTOS_POR_DEFECTO)

    elif argc == 4:
        ip = sys.argv[1]
        opcion = sys.argv[2]
        lista_puertos_str = sys.argv[3]

        if opcion != "-p":
            print(f"Error:  Opción '{opcion}' no reconocida. Use '-p' para especificar puertos.")
            return None, None

        puertos = validar_puertos(lista_puertos_str)
        if puertos is None:
            return None, None

        if len(puertos) == 0:
            print("Error: No se especificaron puertos válidos.")
            return None, None

        return (ip, puertos)

    else:
        mostrar_uso()
        return None, None


def main() -> None:
    """
    Función principal que hace funcionar el escaneo de puertos.
    """
    # Procesar argumentos
    ip, puertos = procesar_argumentos()

    if ip is None or puertos is None:
        return

    # Validar estructura de la IP
    if not comprobar_ip_estructura(ip):
        return

    # Realizar el escaneo de puertos
    resultados = escanear_puertos(ip, puertos)

    # Mostrar resumen
    mostrar_resumen(resultados)


if __name__ == '__main__':
    main()