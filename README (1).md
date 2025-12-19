
## Calculadora de Análisis Matemático y Visualización Gráfica

## Descripción del Proyecto

Este software es una herramienta de escritorio desarrollada en Python que integra el cálculo simbólico avanzado con la visualización gráfica interactiva. Su propósito principal es servir como entorno unificado para el estudio de funciones matemáticas, permitiendo al usuario obtener resultados analíticos exactos (derivadas e integrales) y visualizar simultáneamente su interpretación geométrica.

A diferencia de las calculadoras gráficas estándar, este programa implementa un motor de álgebra computacional (CAS) que manipula las ecuaciones matemáticas en su forma exacta antes de convertirlas en representaciones numéricas para su graficado.

## Características Principales

### 1. Motor Matemático Simbólico
* **Derivación Analítica:** Calcula la función derivada exacta f'(x) de cualquier expresión algebraica.
* **Integración Simbólica:** Resuelve integrales indefinidas mostrando la primitiva F(x) + C.
* **Interpretación de Sintaxis:** Capacidad para entender notación humana (como "sen", "ln") y convertirla automáticamente a la sintaxis técnica de Python.

### 2. Visualización Gráfica Avanzada
* **Graficado de Alta Fidelidad:** Representación de funciones f(x) utilizando la librería Matplotlib.
* **Interpretación Geométrica de la Derivada:** Dibuja la recta tangente a la curva en un punto definido por el usuario, calculando la pendiente exacta en tiempo real.
* **Interpretación Geométrica de la Integral:** Sombrea el área bajo la curva entre dos límites definidos (Integral Definida), permitiendo visualizar la acumulación de la función.

### 3. Interfaz y Experiencia de Usuario
* **Panel Unificado:** Diseño de ventana única que separa los controles de entrada (izquierda) de la visualización de resultados (derecha).
* **Navegación Interactiva:** Incorpora una barra de herramientas profesional que permite realizar Zoom (acercar/alejar), Pan (desplazamiento) y guardar la gráfica como imagen (PNG/JPG).
* **Resolución Dinámica:** El algoritmo ajusta automáticamente la cantidad de puntos de muestreo según el rango de visualización para evitar gráficos pixelados o líneas quebradas.
* **Escalado Inteligente:** Ajuste automático del eje Y para ignorar valores asintóticos o infinitos, manteniendo la gráfica siempre legible.

---

## Requisitos Técnicos

Para ejecutar este software, es necesario disponer de un entorno Python (versión 3.8 o superior).

### Librerías Dependientes
El proyecto se basa en las siguientes librerías de código abierto:

* **Tkinter:** Para la construcción de la interfaz gráfica de usuario (GUI).
* **SymPy:** Para el procesamiento matemático simbólico y álgebra computacional.
* **NumPy:** Para la generación de arrays numéricos y cálculo vectorial de alto rendimiento.
* **Matplotlib:** Para la generación de gráficos 2D y la integración del lienzo en la interfaz.

---

## Instalación y Ejecución

Siga estos pasos para poner en marcha la aplicación en su sistema local:

1.  **Clonar el repositorio o descargar el código:**
    Descargue el archivo `calculadora.py` en un directorio de su elección.

2.  **Instalar dependencias:**
    Abra su terminal o consola de comandos y ejecute el siguiente comando para instalar las librerías necesarias:
    ```bash
    pip install sympy numpy matplotlib
    ```
    *Nota: Tkinter suele venir preinstalado con Python. En sistemas Linux, si recibe un error, ejecute: `sudo apt-get install python3-tk`.*

3.  **Ejecutar el programa:**
    Desde la terminal, navegue a la carpeta del proyecto y ejecute:
    ```bash
    python calculadora.py
    ```

---

## Manual de Usuario

### Panel de Control (Izquierda)

1.  **Entrada de Función:**
    Introduzca la expresión matemática en el campo "Función f(x)". Consulte la tabla de sintaxis más abajo para asegurar un formato correcto.

2.  **Cálculo de Texto:**
    * Botón **Derivada (Texto):** Muestra la expresión algebraica de la derivada en el campo de resultados.
    * Botón **Integral (Texto):** Muestra la expresión algebraica de la integral indefinida.

3.  **Configuración Gráfica:**
    * **Área (Límites X):** Introduzca los valores "Min" y "Max". Estos valores definen dos cosas: el rango del eje X que se mostrará en la gráfica y los límites de integración para el sombreado del área.
    * **Tangente (Punto X):** Introduzca el valor de X donde desea visualizar la recta tangente.

4.  **Botón Actualizar:**
    Pulse el botón verde **"GRAFICAR / REINICIAR VISTA"** para procesar todos los datos. Esto limpiará el gráfico anterior y generará uno nuevo con los parámetros actualizados.

### Panel Gráfico (Derecha)

El gráfico mostrará:
* **Línea Azul:** La función original.
* **Sombreado Morado:** El área bajo la curva (si se definieron límites).
* **Línea Punteada Roja:** La recta tangente en el punto seleccionado.

Utilice la barra de herramientas gris situada en la parte inferior para interactuar con el gráfico (hacer zoom, mover o guardar).

---

## Guía de Sintaxis Matemática

El programa utiliza un sistema de normalización de entrada que permite cierta flexibilidad, pero se recomienda seguir estas normas para evitar errores de interpretación:

| Operación Matemática | Sintaxis en el Programa | Ejemplo Correcto | Notas Importantes |
| :--- | :--- | :--- | :--- |
| **Suma / Resta** | `+`, `-` | `x + 5` | |
| **Multiplicación** | `*` | `3*x` | **Obligatorio** usar el asterisco. `3x` dará error. |
| **División** | `/` | `x / 2` | |
| **Potencia** | `**` o `^` | `x**2` o `x^2` | Ambos símbolos son aceptados. |
| **Raíz Cuadrada** | `sqrt()` | `sqrt(x)` | |
| **Funciones Trigonométricas** | `sin`, `cos`, `tan` | `sin(x)` | Admite `sen` (español) y lo traduce a `sin`. |
| **Trigonométricas Inversas** | `asin`, `acos`, `atan` | `atan(x)` | Admite `arctan`, `arcsin`, etc. |
| **Logaritmo Natural** | `ln()` | `ln(x)` | Base e. |
| **Logaritmo Decimal** | `log()` | `log(x)` | Base 10. |
| **Constante Euler** | `e` | `e**x` | |
| **Constante Pi** | `pi` | `2*pi` | |

---

## Arquitectura del Código

El software está estructurado bajo el paradigma de Programación Orientada a Objetos (POO) en una única clase principal `SuperCalculadoraMatematica`.

El flujo de datos es el siguiente:
1.  **Entrada:** Se captura el string del usuario y se normaliza (reemplazo de caracteres).
2.  **Procesamiento Simbólico (SymPy):** El string se convierte en una expresión de SymPy. Aquí se realizan las operaciones de cálculo diferencial e integral.
3.  **Conversión Numérica (Lambdify):** La expresión simbólica se compila en una función lambda de Python optimizada para trabajar con arrays de NumPy.
4.  **Generación de Datos:** Se crea un dominio de puntos X (dinámico según el zoom) y se evalúa la función para obtener Y.
5.  **Renderizado (Matplotlib):** Se dibuja la figura y se incrusta en el widget Canvas de Tkinter.

## Licencia

Este proyecto se distribuye como código abierto. Usted es libre de modificarlo, estudiarlo y distribuirlo para fines educativos o comerciales.