# 🖐️ Ejemplos Extra: Visión Artificial y Hand Tracking (Software Puro)

> **MakerLab - Universidad Cenfotec**
> Esta sección contiene proyectos exploratorios que demuestran el poder de la visión por computadora. A diferencia del proyecto principal, estos ejemplos no utilizan hardware (Arduino), sino que interactúan directamente con el software de tu computadora.

En esta carpeta encontrarás 4 scripts de Python que llevan el reconocimiento de manos al siguiente nivel: desde dibujar en la pantalla hasta controlar el cursor de tu computadora al estilo "Minority Report".

---

## 🛠️ Requisitos e Instalación de Librerías

Para correr estos ejemplos, asegúrate de tener instalada la versión **Python 3.11** (marcando la opción "Add to PATH" al instalar). Además de las librerías base (OpenCV y MediaPipe), ocuparemos un par extra para controlar el sistema operativo y realizar cálculos.

Abre tu terminal (CMD o PowerShell) y ejecuta este comando para instalar todo lo necesario:

```bash
pip install opencv-python mediapipe pyautogui numpy
```


# 🧠 Entendiendo las Librerías Extra
Entender qué hace cada herramienta es vital en la filosofía del MakerLab para no quedarse solo en el "copiar y pegar". En estos códigos extra, introdujimos dos librerías nuevas muy poderosas y, de forma deliberada, dejamos de usar una (cvzone).

🖱️ **1. PyAutoGUI (pyautogui)**
¿Qué es? Es una librería de automatización para la Interfaz Gráfica de Usuario (GUI).

Su rol: Es el "Fantasma en la Máquina". Le da a tu código Python el permiso y la capacidad de tomar el control físico de tu mouse y tu teclado.

En el script 2-hand_mouse.py, usamos MediaPipe para saber dónde está tu dedo, pero usamos PyAutoGUI para que el sistema operativo de tu computadora obedezca a ese dedo.

pyautogui.size(): Le pregunta a tu computadora cuál es la resolución exacta de tu monitor.

pyautogui.moveTo(x, y): Mueve la flecha de tu mouse físicamente a ese punto de la pantalla.

pyautogui.click(): Simula el clic izquierdo de un mouse físico.

🧮 **2. NumPy (numpy)**
¿Qué es? Significa Numerical Python. Es la librería matemática más importante de todo el ecosistema de Python, diseñada para hacer cálculos complejos y manejar matrices a altísima velocidad.

Su rol: Es la "Calculadora Científica". Una imagen no es más que una matriz matemática gigante llena de números (píxeles), y NumPy es el experto en manejarlos.

Interpolación (np.interp): Hace una "regla de tres" matemática instantánea para mapear y expandir los movimientos pequeños captados por la cámara a la resolución total de tu pantalla.

Geometría (np.hypot): Calcula la hipotenusa (distancia en línea recta) entre las coordenadas de tus dedos para detectar gestos como "pellizcos".

Lienzos (np.zeros_like): Crea una matriz de ceros (una imagen totalmente negra/transparente) exactamente del mismo tamaño que la imagen de tu cámara para poder pintar sobre ella.

🎓 **El Detalle Educativo**: ¿Por qué ya no usamos cvzone aquí?
En el proyecto principal de Arduino usamos cvzone.HandTrackingModule porque nos hacía la vida muy fácil. Sin embargo, en los scripts 3 y 4 de esta carpeta no la usamos. ¿Por qué? Porque queremos ver cómo funcionan las matemáticas por debajo.

El script 3-hand_tracking.py incluye una función manual. En lugar de depender de una librería mágica, aquí hacemos el trabajo duro: le decimos a Python que compare la coordenada Y de la punta de tu dedo (tip) con la coordenada Y de tu nudillo medio (pip). Si la punta está más alta que el nudillo, ¡significa que el dedo está estirado!

## 🚀 ¿Cómo descargar y ejecutar los scripts?
Mantenemos el mismo estándar que en nuestros proyectos principales. Sigue estos pasos:

- Ve al inicio del repositorio y descarga todo el proyecto (Code > Download ZIP) y descomprímelo.

- Abre una terminal (CMD o PowerShell).

- Navega hasta la carpeta codigos que se encuentra dentro de esta sección de ejemplos extra.

- Ejecuta el script que desees utilizando el comando específico para forzar la versión 3.11 de Python. Por ejemplo:

```Bash
py -3.11 1-hand_detector.py
```
(Recuerda que para cerrar la ventana de la cámara de forma segura y detener el programa, debes presionar la tecla q en tu teclado o ctl+c).

📂 Catálogo de Códigos
A continuación, se explica qué hace cada archivo. ¡Haz clic en el título de cada proyecto para ver su código fuente!

# 1️⃣ Detector Básico de Manos (01-hand_detector.py)!
[Detector Básico de Manos](https://github.com/Aggy2025/makerlab-mini-proyectos/blob/main/01-Control-LED-Vision-Artificial/ejemplos_extra/codigos/01-hand_detector.py)
**¿Qué hace?** Es el "Hola Mundo" de MediaPipe. Abre tu cámara y dibuja el esqueleto digital (los 21 puntos clave o landmarks) sobre cualquier mano que aparezca en pantalla.

# 2️⃣ Control de Mouse con la Mano (02-hand_mouse.py)
[Control de Mouse con la Mano](https://github.com/Aggy2025/makerlab-mini-proyectos/blob/main/01-Control-LED-Vision-Artificial/ejemplos_extra/codigos/02-hand_mouse.py)
**¿Qué hace?** Transforma tu dedo índice en el cursor de tu computadora. El script interpola la posición de tu dedo en la cámara con la resolución de tu monitor. Si bajas el dedo medio, el programa simula un "clic izquierdo". ¡Prueba cerrar ventanas o abrir carpetas sin tocar tu mouse físico!

# 3️⃣ Contador de Dedos Matemático (03-hand_tracking.py)
[Contador de Dedos Matemático](https://github.com/Aggy2025/makerlab-mini-proyectos/blob/main/01-Control-LED-Vision-Artificial/ejemplos_extra/codigos/03-hand_tracking.py)
**¿Qué hace?** En lugar de usar herramientas de terceros, este código incluye una función matemática nativa llamada fingers_up. Calcula si las puntas de tus dedos (tips) están por encima de tus nudillos para saber si están estirados o doblados, y muestra en tiempo real cuántos dedos estás levantando.

# 4️⃣ Pizarra Virtual / Finger Paint (04-finger_paint.py)
[Pizarra Virtual / Finger Paint](https://github.com/Aggy2025/makerlab-mini-proyectos/blob/main/01-Control-LED-Vision-Artificial/ejemplos_extra/codigos/04-finger_paint.py)
**¿Qué hace?** Convierte el aire en un lienzo. Usa tu dedo índice para dibujar en la pantalla en tiempo real. Utiliza geometría para medir la distancia entre tu pulgar y tu índice: si los juntas (haciendo una pinza o chasquido), la pantalla se borra instantáneamente.
