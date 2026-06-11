import sys
import subprocess

def obtener_parametro_ping(so_usuario: str) -> str | bool:
    """
    Determina el parámetro de conteo para el comando ping basado en el SO.

    Args:
        so_usuario (str): El sistema operativo indicado por el usuario ('windows', 'linux', 'macos').

    Returns:
        str | bool: '-n' para Windows, '-c' para otros sistemas. False si el SO no es reconocido.
    """
    so_usuario = so_usuario.lower()
    if so_usuario.lower() == "windows":
        return "-n"
    elif so_usuario.lower() == "linux" or so_usuario.lower() == "macos":
        return "-c"
    else:
        return False

def comprobar_ip_estructura(ip: str) -> bool:
    """
    Se encarga de comprobar si la estructura de la IP es válida.

    Args:
        ip (str): La dirección IP a comprobar.

    Returns:
        bool: True si la estructura de la IP es válida, False en caso contrario.
    """
    octetos = ip.split(".")
    posicion_octeto = 1
    if len(octetos) != 4:
        print("Longitud incorrecta de la ip. Debe tener solo cuatro octetos. Ej: 192.168.1.1")
        return False
    for octeto in octetos:
        if not octeto.isdigit():
            print(f"En la IP {ip}, el octeto en la posicion {posicion_octeto} no contiene solo digitos")
            return False
        posicion_octeto += 1
    return True

def comprobar_ip_rango(ip: str) -> bool:
    """
    Se encarga de comprobar si el rango de la IP es válida.

    Args:
        ip (str): La dirección IP a comprobar.

    Returns:
        bool: True si el rango de la IP es válida, False en caso contrario.
    """
    octetos = ip.split(".")
    posicion_octeto = 1
    for octeto in octetos:
        if not (0 <= int(octeto) <= 255):
            print(f"En la IP {ip}, el octeto en la posicion {posicion_octeto} esta fuera de rango")
            return False
        posicion_octeto += 1
    return True

def comprobar_conectividad(ip: str, parametro_ping: str) -> bool:
    """
    Ejecuta el comando ping para un host para asegurar que esté en la tabla ARP.

    Args:
        ip (str): La dirección IP a comprobar.
        parametro_ping (str): El parámetro a usar para limitar a un paquete ('-n' o '-c').

    Returns:
        bool: True si el host responde al ping, False en caso contrario.
    """
    comando = ['ping', parametro_ping, '1', ip]
    print("Trabajando, por favor espera...")

    try:
        resultado = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return resultado.returncode == 0
    except FileNotFoundError:
        print("El comando 'ping' no se pudo encontrar.")
        return False


def obtener_mac_remota(ip: str, so_usuario: str) -> str | None:
    """
    Ejecuta el comando ARP y busca en su salida la dirección MAC asociada a una IP.

    Args:
        ip (str): La IP del host remoto cuya MAC se quiere obtener.
        so_usuario (str): El sistema operativo del equipo local ('windows', 'linux', 'macos').

    Returns:
        str | None: La dirección MAC si se encuentra, o None si no.
    """
    if so_usuario.lower() == "windows":
        arg_arp = "-a"
    else:
        arg_arp = "-n"
    comando = ['arp', arg_arp]

    try:
        # Ejecutamos el comando 'arp' y capturamos su salida de texto
        proceso_arp = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            check=True
        )
        # Dividimos la salida en líneas para procesarla una por una
        for linea in proceso_arp.stdout.splitlines():
            # Buscamos la línea que contiene la IP que nos interesa
            if ip in linea:
                # Dividimos la línea en columnas
                partes = linea.split()
                # Buscamos la "palabra" que parece una MAC (contiene '-' o ':')
                for parte in partes:
                    if '-' in parte or ':' in parte:
                        return parte
        return None
    except FileNotFoundError:
        print("El comando 'arp' no se pudo encontrar.")
        return None
    except subprocess.CalledProcessError:
        print(f"Fallo al ejecutar 'arp'. La IP {ip} puede no estar en la tabla ARP.")
        return None

def main() -> None:
    """
    Función principal que llama al resto de funciones.
    """
    if len(sys.argv) == 3:
        sistema_operativo = sys.argv[1]
        ip_remota = sys.argv[2]

        parametro = obtener_parametro_ping(sistema_operativo)

        if parametro:
            if comprobar_ip_estructura(ip_remota):
                if comprobar_ip_rango(ip_remota):
                    if comprobar_conectividad(ip_remota, parametro):
                        mac_encontrada = obtener_mac_remota(ip_remota, sistema_operativo)
                        if mac_encontrada:
                            print(f"Éxito: La MAC para la IP '{ip_remota}' es: {mac_encontrada.upper()}")
                        else:
                            print(f"Fallo: No se pudo obtener la MAC para '{ip_remota}'.")
                            print("Asegúrate de que está en la misma red local.")
                    else:
                        print(f"Fallo: La máquina '{ip_remota}' no está accesible.")
        else:
            print(f"Sistema operativo '{sistema_operativo}' no reconocido. Usa 'windows', 'linux' o 'macos'.")
    else:
        print("Argumentos incorrectos.")
        print(f"python3 {sys.argv[0]} <windows|linux|macos> <ip>")
        print("Ejemplos:")
        print(f"  python3 {sys.argv[0]} windows 192.168.1.1")
        print(f"  python3 {sys.argv[0]} linux 192.168.1.54")

if __name__ == "__main__":
    main()