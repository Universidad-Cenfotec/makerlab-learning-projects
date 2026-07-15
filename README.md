# makerlab-learning-projects
Repositorio de proyectos de enseñanza del MakerLab Universidad Cenfotec

> **MakerLab - Universidad Cenfotec**
> Repositorio oficial de mini proyectos desarrollados en el laboratorio Maker de CENFOTEC.

## 🎯 Objetivo

Proveer ejemplos prácticos, replicables y educativos para estudiantes y visitantes del laboratorio. Este espacio está diseñado para demostrar cómo el mundo físico se conecta con el mundo digital, abarcando las siguientes áreas de estudio:

* **IoT (Internet de las Cosas)**
* **Sistemas Embebidos y Microcontroladores**
* **Sensores y Actuadores**
* **Desarrollo Web e Inteligencia Artificial**

---

## Proyectos Disponibles

Actualmente, el repositorio cuenta con los siguientes proyectos funcionales. Navega por las diferentes carpetas para descubrir cada uno:

| Carpeta / Proyecto | Tecnologías Principales | Área de Aprendizaje |
| :--- | :--- | :--- |
| **[1. Control de LEDs mediante Visión Artificial](./01-Control-LED-Vision-Artificial)** | Python, OpenCV, MediaPipe, Arduino | **Inteligencia Artificial:** Hand-tracking y comunicación serial PC-Hardware. |
| **[2. ServoBLE: Portón Inteligente IoT](./02-ServoBLE)** | IdeaBoard (ESP32), Web Bluetooth API, HTML/JS | **Internet of Things (IoT):** Control de actuadores mediante comunicación inalámbrica. |
| **[3. Cenfobot: Control Remoto BLE con Autocorrección](./03-Sumo_Web)** | Sumobot (ESP32), Giroscopio, Control PDI, Web BLE | **Robótica y Control Automático:** Telemetría en tiempo real y corrección matemática de trayectoria. |
| **[4. Radar Ultrasónico Interactivo](./04-Radar_Ultrasonico)** | Arduino, Sensor HC-SR04, Servo SG90, Processing | **Percepción Robótica:** Sensores de distancia y renderizado de interfaces gráficas 2D. |
| **[5. Micro:bit Machine Learning](./05-Microbit_MachineLearning)** | Teachable Machine, MakeCode, Micro:bit, BLE | **Inteligencia Artificial:** Visión computacional conectada a la toma de decisiones físicas. |
| **[6. Arduino-LCD-Minigames](./06-Arduino-LCD-Minigames)** | Arduino C++, LCD 1602 Keypad Shield | **Programación de Videojuegos:** Lógica pura, física 2D, uso de memoria y superación de límites de hardware retro. |

---

## 📂 ¿Qué contiene cada proyecto?

Cada proyecto es 100% independiente y mantiene una estructura estandarizada para facilitar tu aprendizaje. Al entrar a cualquiera de las carpetas de la tabla anterior, encontrarás:

* 📄 **`README.md`:** Las instrucciones detalladas, explicación de las tecnologías y la guía de replicación paso a paso.
* 📁 **`codigos/`:** Los archivos de programación listos para usar (Python, HTML, CircuitPython, C++, etc.).
* 📁 **`imagenes/`:** Fotos del montaje físico, diagramas de conexión y capturas de pantalla para que no te pierdas al armar el circuito.

---

## Cómo usar este repositorio

1. Haz clic en el botón verde **"Code"** en la parte superior derecha de esta página y selecciona **"Download ZIP"** (o clona el repositorio usando Git si prefieres la terminal).
2. Descomprime la carpeta en tu computadora.
3. Entra a la carpeta del proyecto que deseas realizar.
4. Sigue la **Guía de replicación** dentro del `README.md` de esa carpeta específica.

---

## 🛠️ Herramientas Recomendadas

Para sacar el máximo provecho de estos mini proyectos, te sugerimos tener a mano el siguiente software:

* **Arduino IDE:** Esencial para compilar y subir códigos a placas Arduino estándar (usado en el Radar, Consola LCD y para cargar Firmata).
* **Python 3.11:** Requerido para los proyectos de Visión Artificial (Asegúrate de marcar *"Add to PATH"* durante la instalación).
* **Navegador Web Moderno (Chrome o Edge):** Estrictamente necesario para ejecutar los proyectos que utilizan la tecnología *Web Bluetooth API* (ServoBLE y Cenfobot).
* **[IdeaCode Web IDE](https://ideacode.crcibernetica.com/):** Herramienta web recomendada para programar las placas IdeaBoard y Cenfobot directamente desde el navegador, sin instalar nada.
