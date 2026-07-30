# 🔵 ServoBLE: Portón Inteligente IoT (IdeaBoard + Web)

> **MakerLab - Universidad Cenfotec**
> Este proyecto es ideal para entender la integración completa entre el hardware físico (sensores y motores) y el mundo digital (Interfaces Web), utilizando **Internet of Things (IoT)** y comunicación inalámbrica.

El sistema ServoBLE simula un acceso de seguridad inteligente. Utiliza una placa **IdeaBoard (basada en el potente ESP32)** para leer un sensor ultrasónico frontal. Cuando el sistema detecta que una persona o vehículo se acerca, envía una notificación silenciosa e inalámbrica a una página web interactiva. Desde esa web, el usuario recibe la alerta y puede decidir presionar un botón para abrir o cerrar el portón físicamente.

---

## 🧠 Tecnologías y Conceptos Clave

Para lograr que una página web mueva un motor físico en tu escritorio, combinamos estas tecnologías:

* **🧠 IdeaBoard ESP32 (El Cerebro Conectado):** A diferencia de un Arduino tradicional, esta placa tiene antenas Wi-Fi y Bluetooth incorporadas, permitiéndole hablar con el mundo exterior.
* **🦇 Sensor Ultrasónico (Los Ojos):** Mide la distancia enviando pulsos de sonido para detectar si hay "alguien en la puerta".
* **🦾 Servo Motor (El Músculo / El Portón):** El actuador físico que ejecutará la orden de abrir o cerrar el acceso.
* **📡 Bluetooth Low Energy / BLE (El Mensajero Invisible):** Un protocolo de comunicación diseñado para gastar muy poca batería. A diferencia del Bluetooth clásico, BLE envía mensajes cortos y rápidos.
* **🌐 Web Bluetooth API (El Centro de Control):** Una tecnología moderna que permite que tu navegador web (Chrome, Edge) se conecte directamente al hardware por Bluetooth, ¡sin necesidad de programar ni instalar aplicaciones móviles!

---

## 🛠️ Materiales Necesarios

| Cantidad | Componente | Función |
| :---: | :--- | :--- |
| 1 | IdeaBoard (ESP32) | Microcontrolador principal con BLE. |
| 1 | Sensor Ultrasónico HC-SR04 | Detección de presencia física. |
| 1 | Servo Motor SG90 | Actuador para mover el portón. |
| 1 | Caja de Baterías 4xAA | **Fuente externa** para el motor. |
| 1 | Protoboard y Jumpers | Para realizar las conexiones. |
| 1 | PC o Teléfono móvil | Para ejecutar la página Web remota. |

---

## 🔌 Conexiones de Hardware (MUY IMPORTANTE)

Como aprendimos en proyectos anteriores del MakerLab, los motores consumen mucha energía. Alimentaremos el IdeaBoard vía USB, pero el **Servo Motor** se alimentará de las baterías.

**⚠️ REGLA DE ORO MAKER:** ¡Debes conectar el cable negro (GND) de las baterías a un pin **GND** de la IdeaBoard! Si no comparten la misma "tierra", el sistema no funcionará o se comportará de forma errática.

### 1. Conexión del Servo Motor (Alimentación Externa)
| Cable del Servo | Conexión Física |
| :--- | :--- |
| **Rojo (VCC)** | Positivo (+) de las Baterías 4xAA |
| **Negro / Marrón (GND)** | Negativo (-) de las Baterías **Y** GND de IdeaBoard |
| **Amarillo / Naranja (Señal)**| Pin **IO4** de la IdeaBoard |

### 2. Conexión del Sensor Ultrasónico
*Nota: El IdeaBoard proporciona salidas de 5V perfectas para este sensor.*
| Pin del Sensor | Pin en IdeaBoard |
| :--- | :--- |
| **VCC** | **5V** |
| **GND** | **GND** |
| **TRIG** | **IO26** |
| **ECHO** | **IO25** |

---

## 🖼️ Galería de Componentes

Para replicar este proyecto y armar tu propio portón, guíate con estas imágenes de referencia:

* **Montaje del Portón Físico:** `imagenes/porton_terminado.jpg`
* **Circuito IdeaBoard y Baterías:** `imagenes/circuito_ideaboard.jpg`
* **Interfaz Web Funcionando:** `imagenes/interfaz_web.jpg`

---

## 💻 Configuración del Software

Este proyecto está dividido en dos partes: el código que vive en la placa (Hardware) y la interfaz gráfica (Web).

### 1. El Cerebro Físico (Hardware)
1. Conecta tu IdeaBoard a la computadora mediante USB.
2. Abre el archivo de código fuente ubicado en la carpeta `codigos/code.py`.
3. Carga este código dentro de tu IdeaBoard (usualmente copiándolo a la unidad virtual `CIRCUITPY` o a través de tu entorno de desarrollo habitual).

### 2. El Centro de Control (Web y Código QR)
¡No necesitas instalar aplicaciones ni descargar archivos para controlar el portón! La interfaz está alojada en la nube gracias a GitHub Pages.

1. **Desde tu computadora:** Ingresa directamente al siguiente enlace utilizando Google Chrome o Microsoft Edge:
   🔗 **[Aplicación Web ServoBLE](https://aggy2025.github.io/Servo-BLE/)**

2. **Desde tu teléfono móvil:** Simplemente escanea este código QR para abrir la aplicación de control al instante:
   
   ![QR ServoBLE](imagenes/qr_ServoBLE.svg)

---

## 🚀 Ejecución y Uso

1. **Encendido:** Conecta la alimentación de tu IdeaBoard y asegúrate de que las baterías del servo estén encendidas. El sistema iniciará su antena BLE automáticamente.
2. **Emparejamiento:** En la página web oficial, presiona el botón **"Conectar BLE"**.
3. Aparecerá una ventana de tu navegador buscando dispositivos. Selecciona el que dice **`Porton_Sumobot`** (o el nombre que hayas configurado) y dale a "Emparejar".
4. **Interacción:** * Pasa tu mano frente al sensor ultrasónico. La página web cambiará su estado a **"Objeto Detectado"**.
   * Haz clic en el botón de **"Abrir Portón"** en la web. El mensaje viajará de forma inalámbrica hasta la IdeaBoard y el servomotor abrirá el acceso.

---

## 🧪 Tabla de Estados del Sistema

Durante la ejecución, la interfaz web te mostrará exactamente qué está pensando el microcontrolador:

| Estado Visual | Significado en el Sistema |
| :--- | :--- |
| 🔴 **Desconectado** | No hay enlace Bluetooth activo. |
| 🔵 **Conectado** | Sistema emparejado, antena BLE sincronizada. |
| 🟡 **Objeto Detectado** | Sensor midió presencia física (persona/vehículo). |
| 🟢 **Área Libre** | Sensor no detecta obstáculos cercanos. |
| 🔓 **Portón Abierto** | Se envió la orden al Servo para abrir el paso. |

---

## 🔬 Aprendizajes Clave MakerLab

Este proyecto es una excelente demostración de la arquitectura real del Internet de las Cosas:

**1. Interacción Bidireccional:**
Aprendimos que la comunicación no es de una sola vía. El hardware le envía datos a la web ("*Hay un objeto aquí*") y la web le envía órdenes al hardware ("*Abre el portón*").

**2. El poder del Web Bluetooth API:**
Históricamente, controlar hardware desde un teléfono requería programar una App para Android y otra para iOS. Hoy, programando un simple archivo web y alojándolo en GitHub Pages, logramos controlar hardware desde cualquier dispositivo con un navegador compatible.

**3. Prototipado y Fabricación Digital:**
Este proyecto es la excusa perfecta para usar las **impresoras 3D** del MakerLab. Diseñar una base para el IdeaBoard, un soporte frontal para el ultrasonido y la barrera plástica del portón completa el ciclo de "Idea a Producto".

