# Nmap Casero (Python) — README

> Herramienta CLI que **escanea puertos TCP** en una dirección IP para determinar cuáles están abiertos o cerrados.

---

## 1. Descripción del módulo

Este proyecto es un escáner de puertos simplificado para la línea de comandos que imita el comportamiento básico de herramientas como Nmap.  Realiza las siguientes operaciones:

- **Validación de dirección IP**: 
  - Comprueba que la IP tenga 4 octetos separados por puntos. 
  - Verifica que cada octeto contenga únicamente dígitos. 
  - Valida que los valores estén dentro del rango válido (0-255).

- **Validación de puertos**:
  - Verifica que los puertos sean valores numéricos enteros.
  - Comprueba que estén dentro del rango permitido (1-65535).
  - Detecta y elimina puertos duplicados.

- **Escaneo de puertos**:
  - Intenta establecer conexiones TCP a los puertos especificados.
  - Determina si cada puerto está "ABIERTO" o "CERRADO". 
  - Muestra un resumen final con estadísticas del escaneo. 

---

## 2. Requisitos

- **Python 3.x**. 
- **No se requieren dependencias externas**. El script utiliza los módulos `sys` y `socket`, que son estándar de Python. 
- Conexión de red activa para realizar el escaneo. 

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
  - **Importante**: En la primera pantalla del instalador, asegúrate de marcar la casilla **"Add Python to PATH"** o **"Agregar Python al PATH"**.  Esto te permitirá ejecutar el script desde cualquier terminal. 
  - Completa la instalación con la opción "Install Now".

- **macOS**:
  - macOS suele incluir una versión de Python, pero puede ser antigua.  Se recomienda instalar una versión más reciente.
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

El script se ejecuta desde la terminal, pasando la dirección IP y opcionalmente una lista de puertos. 

### Sintaxis general

```bash
python3 nmap_casero.py <ip> [-p lista_puertos]
```

- `<ip>`: Dirección IP del host que se desea analizar (obligatorio).
- `[-p lista_puertos]`: Lista de puertos separados por comas (opcional).

> **Nota**: En Windows, es común usar `py` en lugar de `python3`.

### Comportamiento según los argumentos

| Argumentos | Comportamiento |
|------------|----------------|
| Solo IP | Escanea los puertos por defecto:  20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080 |
| IP + `-p` + puertos | Escanea únicamente los puertos especificados |

---

## 5. Ejemplos de uso

### Ejemplo 1: Escaneo con puertos por defecto

```bash
python3 nmap_casero. py 192.168.1.10
```

Salida esperada: 

```text
Escaneando 15 puerto(s) en 192.168.1.10... 

----------------------------------------
Puerto 20: CERRADO
Puerto 21: CERRADO
Puerto 22: ABIERTO
Puerto 23: CERRADO
Puerto 25: CERRADO
Puerto 53: CERRADO
Puerto 80: ABIERTO
Puerto 110: CERRADO
Puerto 143: CERRADO
Puerto 443: ABIERTO
Puerto 445: CERRADO
Puerto 3306: CERRADO
Puerto 3389: CERRADO
Puerto 5432: CERRADO
Puerto 8080: CERRADO
----------------------------------------

=== RESUMEN DEL ESCANEO ===
Total de puertos analizados: 15
Puertos abiertos: 3
Puertos cerrados: 12

Puertos abiertos encontrados: 22, 80, 443
```

### Ejemplo 2: Escaneo con puertos específicos

```bash
python3 nmap_casero.py 192.168.1.10 -p 22,80,443
```

Salida esperada:

```text
Escaneando 3 puerto(s) en 192.168.1.10... 

----------------------------------------
Puerto 22: ABIERTO
Puerto 80: ABIERTO
Puerto 443: CERRADO
----------------------------------------

=== RESUMEN DEL ESCANEO ===
Total de puertos analizados: 3
Puertos abiertos: 2
Puertos cerrados:  1

Puertos abiertos encontrados: 22, 80
```

### Ejemplo 3: Error de estructura de IP (caracteres no numéricos)

```bash
python3 nmap_casero.py 192.168.1.abc
```

Salida esperada:

```text
Error: En la IP 192.168.1.abc, el octeto en la posición 4 no contiene solo dígitos. 
```

### Ejemplo 4: Error de rango en IP (valor fuera de 0-255)

```bash
python3 nmap_casero.py 192.168.300.1
```

Salida esperada:

```text
Error: En la IP 192.168.300.1, el octeto en la posición 3 está fuera de rango (0-255).
```

### Ejemplo 5: Error en lista de puertos (valor no numérico)

```bash
python3 nmap_casero.py 192.168.1.10 -p 22,abc,443
```

Salida esperada: 

```text
Error: 'abc' no es un número de puerto válido. 
```

### Ejemplo 6: Error en lista de puertos (fuera de rango)

```bash
python3 nmap_casero.py 192.168.1.10 -p 22,70000,443
```

Salida esperada: 

```text
Error: El puerto 70000 está fuera del rango permitido (1-65535).
```

### Ejemplo 7: Advertencia de puertos duplicados

```bash
python3 nmap_casero.py 192.168.1.10 -p 22,80,22,443
```

Salida esperada: 

```text
Advertencia: El puerto 22 está duplicado.  Se ignorará el duplicado. 

Escaneando 3 puerto(s) en 192.168.1.10... 
... 
```

### Ejemplo 8: Uso incorrecto (argumentos insuficientes)

```bash
python3 nmap_casero.py
```

Salida esperada: 

```text
Argumentos incorrectos. 
Uso: python3 nmap_casero.py <ip> [-p lista_puertos]

Ejemplos: 
  python3 nmap_casero. py 192.168.1.10
  python3 nmap_casero. py 192.168.1.10 -p 22,80,443
```

---

## 6. Mensajes de salida y errores

El script proporciona mensajes claros sobre el resultado de las validaciones y el escaneo:

### Resultados del escaneo

| Mensaje | Significado |
|---------|-------------|
| `Puerto X: ABIERTO` | El puerto acepta conexiones TCP |
| `Puerto X: CERRADO` | El puerto no responde o rechaza la conexión |

### Errores de validación de IP

| Mensaje | Causa |
|---------|-------|
| `Longitud incorrecta de la IP.  Debe tener solo cuatro octetos. ` | La IP no tiene exactamente 4 partes separadas por puntos |
| `El octeto en la posición X no contiene solo dígitos. ` | Hay caracteres no numéricos en algún octeto |
| `El octeto en la posición X está fuera de rango (0-255).` | El valor del octeto no está entre 0 y 255 |

### Errores de validación de puertos

| Mensaje | Causa |
|---------|-------|
| `'X' no es un número de puerto válido.` | El valor indicado no es un número entero |
| `El puerto X está fuera del rango permitido (1-65535).` | El número de puerto no es válido |
| `Advertencia: El puerto X está duplicado. ` | Se ha repetido un puerto en la lista |

### Errores de ejecución

| Mensaje | Causa |
|---------|-------|
| `Argumentos incorrectos.` | Número incorrecto de parámetros |
| `Opción 'X' no reconocida.  Use '-p' para especificar puertos.` | Se usó una opción diferente a `-p` |

---

## 7. Puertos por defecto

Cuando no se especifica la opción `-p`, el script escanea los siguientes puertos comunes:

| Puerto | Servicio |
|--------|----------|
| 20 | FTP-data |
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |
| 5432 | PostgreSQL |
| 8080 | HTTP alternativo |

---

## 8. Posibles mejoras futuras

- **Escaneo UDP**: Añadir soporte para escanear puertos UDP además de TCP.
- **Multihilo**: Implementar escaneo paralelo para mejorar la velocidad.
- **Detección de servicios**: Identificar qué servicio está corriendo en cada puerto abierto.
- **Rangos de puertos**:  Permitir sintaxis como `1-1000` para escanear rangos. 
- **Exportar resultados**: Guardar los resultados en formatos como JSON o CSV.
- **Escaneo de múltiples hosts**:  Permitir escanear varias IPs o rangos de red.
- **Modo silencioso**: Opción para mostrar solo los puertos abiertos. 
- **Timeout configurable**: Permitir ajustar el tiempo de espera desde la línea de comandos. 
