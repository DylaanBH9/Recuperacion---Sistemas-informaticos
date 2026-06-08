# Descifrador de Contraseñas por Fuerza Bruta (Python) — README

> Herramienta CLI que busca una contraseña a partir de un **hash SHA256** mediante un ataque de **fuerza bruta**.
> La salida muestra la contraseña encontrada (si tiene éxito) y el tiempo que ha tardado en descubrirla.

---

## 1. Descripción del módulo

Este proyecto es un **descifrador de contraseñas por fuerza bruta** para la línea de comandos que realiza las siguientes operaciones:

- **Validación de entradas**:
  - Comprueba que la `longitud` sea un número.
  - Verifica que el `hash` tenga el formato correcto de SHA256 (64 caracteres hexadecimales).
- **Generación de contraseñas**:
  - Crea un conjunto de caracteres predefinido que incluye:
    - Letras minúsculas (`a-z`, `ñ`).
    - Letras mayúsculas (`A-Z`, `Ñ`).
    - Números (`0-9`).
    - Símbolos (`!@#$%&/()=`).
- **Búsqueda por fuerza bruta**:
  - Genera de forma iterativa y eficiente (utilizando itertools.product) todas las combinaciones posibles de contraseñas con la longitud especificada, evitando así los límites de profundidad de recursión.
  - Para cada combinación, calcula su hash SHA256 y lo compara con el hash objetivo.
  - Si encuentra una coincidencia, devuelve la contraseña y finaliza.

---

## 2. Requisitos

- **Python 3.x**.
- **No se requieren dependencias externas**. El script utiliza los módulos `sys`, `hashlib`, `itertools` y `time`, que son estándar de Python.

---

## 3. Instalación

No se necesita instalación del script, solo tener Python disponible en el sistema.

### Verificar versión de Python

Puedes verificar si ya tienes Python y qué versión es con los siguientes comandos:

```bash
# Linux / macOS
python3 --version

# Windows
py --version
```

### Cómo instalar Python

Si no tienes Python instalado, puedes descargarlo desde su sitio web oficial:

1. Ve a [python.org/downloads/](https://www.python.org/downloads/).
2. Descarga la última versión estable para tu sistema operativo.

#### Recomendaciones por sistema operativo

- **Windows**:
  - Ejecuta el instalador que descargaste.
  - **Importante**: En la primera pantalla del instalador, asegúrate de marcar la casilla **"Add Python to PATH"** o **"Agregar Python al PATH"**. Esto te permitirá ejecutar el script desde cualquier terminal.
  - Completa la instalación con la opción "Install Now".

- **macOS**:
  - macOS suele incluir una versión de Python, pero puede ser antigua. Se recomienda instalar una versión más reciente.
  - Puedes descargar el instalador oficial desde [python.org](https://www.python.org/downloads/).
  - Si usas el gestor de paquetes [Homebrew](https://brew.sh/), puedes instalarlo con el comando: `brew install python3`.

- **Linux**:
  - La mayoría de distribuciones modernas ya incluyen Python 3. Si no es tu caso, usa el gestor de paquetes de tu sistema:
    - **Para Debian/Ubuntu**:
      ```bash
      sudo apt update
      sudo apt install python3
      ```
    - **Para Fedora/CentOS**:
      ```bash
      sudo dnf install python3
      ```

---

## 4. Ejecución del módulo

El script se ejecuta desde la terminal, pasando la longitud de la contraseña y el hash SHA256 como argumentos.

### Sintaxis general

```bash
python3 contraseña_fuerza_bruta.py <longitud> <hash>
```

- `<longitud>`: El número de caracteres que tiene la contraseña a buscar.
- `<hash>`: El hash SHA256 de 64 caracteres de la contraseña.

> **Nota**: En Windows, es común usar `py` en lugar de `python3`. En Linux y macOS, `python3` es más explícito.

### Ejemplos de uso

#### Ejemplo 1: Encontrar una contraseña de 3 caracteres ("sol")

```bash
# El hash de "sol" es 15d310a26932d398d8a77a9404c534c7a65d3362145e69e0b82f8d8376e43899
python3 contraseña_fuerza_bruta.py 3 15d310a26932d398d8a77a9404c534c7a65d3362145e69e0b82f8d8376e43899
```

Salida esperada:

```text
CONTRASEÑA FUERZA BRUTA
- HASH A ENCONTRAR: 15d310a26932d398d8a...
- LONGITUD PALABRA: 3
- TAMAÑO CONJUNTO PALABRAS: 75
-------------------------

- EXITO: Contraseña encontrada! -> sol
- Tiempo total: X.XX segundos
```

#### Ejemplo 2: Encontrar una contraseña de 4 caracteres ("Py1!")

```bash
# El hash de "Py1!" es 7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834
python3 contraseña_fuerza_bruta.py 4 7c9e7c1494b2684ab7c19d6aff737e460fa9e98d5a234da1310c97ddf5691834
```

Salida esperada:

```text
CONTRASEÑA FUERZA BRUTA
- HASH A ENCONTRAR: 7c9e7c1494b2684ab7c...
- LONGITUD PALABRA: 4
- TAMAÑO CONJUNTO PALABRAS: 75
-------------------------

- EXITO: Contraseña encontrada! -> Py1!
- Tiempo total: X.XX segundos
```

> **Advertencia**: El tiempo de ejecución aumenta exponencialmente con la longitud de la contraseña. Contraseñas de más de 5 o 6 caracteres pueden tardar mucho tiempo en ser descubiertas.

---

## 5. Mensajes de error y validaciones

El script valida las entradas antes de realizar cualquier operación:

- **Número incorrecto de argumentos**:
  - `Argumentos incorrectos.`
  - `Uso: python3 contraseña_fuerza_bruta.py <longitud> <hash>`
  - `Ejemplo: python3 contraseña_fuerza_bruta.py 4 7c9e...`

- **Longitud no numérica**:
  - `Error: La longitud X introducida no es un digito`

- **Formato de hash incorrecto**:
  - `Error: El hash X... introducido es incorrecto`

- **Contraseña no encontrada**:
  - Si el script termina sin encontrar una coincidencia (por ejemplo, si la contraseña contiene caracteres no incluidos en el conjunto), mostrará un mensaje de error:
  - `ERROR: La contraseña de longitud X no fue encontrada.`