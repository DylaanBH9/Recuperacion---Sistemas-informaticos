import sys
import hashlib
import time
import itertools  # Importamos itertools para generar las combinaciones de forma iterativa


# Función para validar que la longitud introducida sea un número entero
def comprobar_longitud(longitud_contrasena):
    if longitud_contrasena.isdigit():
        return True
    else:
        return False


# Función para verificar que el hash tenga el tamaño correcto de un SHA256
def comprobar_hash(hash):
    if len(hash) == 64:
        return True
    else:
        return False


# Aquí creamos el "abecedario" con todos los caracteres posibles que vamos a probar
def crear_conjunto_caracteres():
    minusculas = "abcdefghijklmnñopqrstuvwxyz"
    mayusculas = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    numeros = "0123456789"
    simbolos = "!@#$%&/()="

    # Devolvemos todo junto en una sola cadena de texto
    return minusculas + mayusculas + numeros + simbolos


# Busca la contraseña sin usar recursividad pura
def encontrar_contrasena(longitud, conjunto_caracteres, hash_objetivo):
    for intento in itertools.product(conjunto_caracteres, repeat=longitud):
        intento_contrasena = "".join(intento)

        contrasena_codificada = intento_contrasena.encode('utf-8')
        contrasena_hasheada = hashlib.sha256(contrasena_codificada).hexdigest()

        if contrasena_hasheada == hash_objetivo:
            return intento_contrasena

    return None


# Mensajes en pantalla para que la interfaz quede ordenada al empezar
def mensaje_comienzo(hash_objetivo, longitud, tamano_conjunto):
    print("CONTRASEÑA FUERZA BRUTA")
    print(f"- HASH A ENCONTRAR: {hash_objetivo[:20]}...")
    print(f"- LONGITUD PALABRA: {longitud}")
    print(f"- TAMAÑO CONJUNTO PALABRAS: {tamano_conjunto}")


# Mensaje final con el resultado y el tiempo que ha tardado el script
def mensaje_final(contrasena_encontrada, longitud, tiempo_ejecucion):
    if contrasena_encontrada:
        print(f"\n- EXITO: Contraseña encontrada! -> {contrasena_encontrada}")
    else:
        print(f"\n- ERROR: La contraseña de longitud {longitud} no fue encontrada.")

    print(f"- Tiempo total: {tiempo_ejecucion:.2f} segundos")


def main():
    # Controlamos que se pasen exactamente los argumentos necesarios por la terminal
    if len(sys.argv) == 3:
        longitud_contrasena = sys.argv[1]
        hash_encontrar = sys.argv[2]

        # Validaciones de los datos de entrada antes de lanzar el bucle
        if comprobar_longitud(longitud_contrasena):
            longitud_contrasena = int(longitud_contrasena)  # Lo pasamos a entero tras comprobarlo
            if comprobar_hash(hash_encontrar):
                conjunto_caracteres = crear_conjunto_caracteres()

                mensaje_comienzo(hash_encontrar, longitud_contrasena, len(conjunto_caracteres))

                # Medimos el tiempo con perf_counter para ver el rendimiento total
                tiempo_inicio = time.perf_counter()
                contrasena_encontrada = encontrar_contrasena(longitud_contrasena, conjunto_caracteres, hash_encontrar)
                tiempo_final = time.perf_counter()

                tiempo_total = tiempo_final - tiempo_inicio

                mensaje_final(contrasena_encontrada, longitud_contrasena, tiempo_total)

            else:
                print(f"Error: El hash {hash_encontrar[:20]}... introducido es incorrecto")
        else:
            print(f"Error: La longitud {longitud_contrasena} introducida no es un digito")
    else:
        print("Argumentos incorrectos.")
        print(f"Uso: python3 {sys.argv[0]} <longitud> <hash>")
        print("Ejemplos:")
        print(f"  python3 {sys.argv[0]} 4 7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834")


if __name__ == "__main__":
    main()