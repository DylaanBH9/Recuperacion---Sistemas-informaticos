# Descubridor de MAC y Comprobador de Conectividad (Python) — README

> Herramienta CLI que **valida** una dirección IP, **comprueba su conectividad** en la red usando `ping` y **obtiene su dirección MAC** usando `arp`.

---

## 1. Descripción del módulo

Este proyecto es una herramienta para la línea de comandos que realiza las siguientes operaciones con una dirección IP en la red local:

- **Validación de estructura**:
  - Comprueba que la IP tenga 4 octetos separados por puntos.
  - Verifica que cada octeto contenga únicamente dígitos.
- **Validación de rango**:
  - Verifica que los valores de los octetos estén dentro del rango válido (0-255).
- **Comprobación de conectividad**:
  - Ejecuta el comando `ping` para determinar si el host con la IP especificada es accesible en la red.
- **Obtención de la dirección MAC**:
  - Si el host es accesible, ejecuta el comando `arp` para buscar la dirección MAC asociada a la IP en la tabla ARP del sistema.
  - Adapta los comandos `ping` y `arp` según el sistema operativo del usuario (`windows`, `linux` o `macos`).

---

## 2. Requisitos

- **Python 3.x**.
- **No se requieren dependencias externas**. El script utiliza los módulos `sys` y `subprocess`, que son estándar de Python.
- Los comandos `ping` y `arp` deben estar disponibles en el PATH del sistema.

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

El script se ejecuta desde la terminal, pasando el sistema operativo y la dirección IP como argumentos.

### Sintaxis general

```bash
python3 descubrir_mac.py <sistema_operativo> <ip_decimal>
```

- `<sistema_operativo>`: Sistema operativo desde el que se ejecuta el script. Valores aceptados: `windows`, `linux`, `macos`.
- `<ip_decimal>`: Dirección IP local que se desea comprobar.

> **Nota**: En Windows, es común usar `py` en lugar de `python3`.

### Ejemplos de uso

#### Ejemplo 1: Host accesible y MAC encontrada (Linux/macOS)

```bash
python3 descubrir_mac.py linux 192.168.1.1
```

Salida esperada:

```text
Trabajando, por favor espera...

Éxito: La MAC para la IP '192.168.1.1' es: 00-1A-2B-3C-4D-5E
```

#### Ejemplo 2: Host accesible, pero MAC no encontrada (Windows)

```bash
py descubrir_mac.py windows 8.8.8.8
```

Salida esperada:

```text
Trabajando, por favor espera...

Fallo: No se pudo obtener la MAC para '8.8.8.8'.
Asegúrate de que está en la misma red local.
```

#### Ejemplo 3: Host inaccesible

```bash
py descubrir_mac.py windows 192.168.1.254
```

Salida esperada:

```text
Trabajando, por favor espera...

Fallo: La máquina '192.168.1.254' no está accesible.
```

#### Ejemplo 4: Error de estructura (caracteres no numéricos)

```bash
python3 descubrir_mac.py linux 192.168.1.abc
```

Salida esperada:

```text
En la IP 192.168.1.abc, el octeto en la posicion 4 no contiene solo digitos
```

#### Ejemplo 5: Uso incorrecto (argumentos insuficientes)

```bash
python3 descubrir_mac.py linux
```

Salida esperada:

```text
Argumentos incorrectos.
python3 descubrir_mac.py <windows|linux|macos> <ip>
Ejemplos:
  python3 descubrir_mac.py windows 192.168.1.1
  python3 descubrir_mac.py linux 192.168.1.54
```

---

## 5. Mensajes de salida y errores

El script proporciona mensajes claros sobre el resultado de las validaciones y las pruebas:

- **Resultados de obtención de MAC**:
  - `Éxito: La MAC para la IP 'X.X.X.X' es: YY-YY-YY-YY-YY-YY`
  - `Fallo: No se pudo obtener la MAC para 'X.X.X.X'.` (seguido de una sugerencia)

- **Resultados de conectividad**:
  - `Fallo: La máquina 'X.X.X.X' no está accesible.`

- **Errores de validación de IP**:
  - `Longitud incorrecta de la ip. Debe tener solo cuatro octetos. Ej: 192.168.1.1`
  - `En la IP X.X.X.X, el octeto en la posicion Y no contiene solo digitos`
  - `En la IP X.X.X.X, el octeto en la posicion Y esta fuera de rango`

- **Errores de ejecución**:
  - `Argumentos incorrectos.` (seguido de la sintaxis correcta)
  - `El comando 'ping' no se pudo encontrar.`
  - `El comando 'arp' no se pudo encontrar.`
  - `Sistema operativo '{sistema_operativo}' no reconocido. Usa 'windows', 'linux' o 'macos'.`