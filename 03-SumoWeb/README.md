# 🤖 Cenfobot: Control Remoto BLE con Autocorrección (Giroscopio + PDI)

> **MakerLab - Universidad Cenfotec**
> Este proyecto demuestra cómo integrar robótica móvil, control automático y desarrollo web. Es el ejemplo perfecto para entender cómo un navegador web puede controlar hardware complejo de forma inalámbrica sin instalar aplicaciones.

Este proyecto permite controlar un **Sumobot (Cenfobot)** de forma remota utilizando Bluetooth Low Energy (BLE) a través de una página web interactiva. A diferencia de un carro a control remoto tradicional, este robot es "consciente" de su entorno: utiliza un giroscopio y un controlador matemático (PDI) para mantener líneas perfectamente rectas al avanzar o retroceder, compensando en tiempo real cualquier diferencia de fuerza entre sus motores.

---

## 🏎️ El Hardware Base: Sumobot Cenfotec

Este proyecto utiliza exactamente el mismo chasis, motores y placa electrónica que usamos para las competencias universitarias. 

🔗 **[Ver Repositorio Oficial del Sumobot (Materiales y Ensamblaje)](https://github.com/Universidad-Cenfotec/Sumobot/blob/main/README.md)**

**🔄 El Cambio de Enfoque (Autónomo vs. Teleoperado):**
Mientras que en la competencia el robot es 100% autónomo y utiliza sensores infrarrojos para buscar y empujar a su oponente, en este proyecto le damos un enfoque de **Teleoperación Asistida e IoT (Internet of Things)**. 

Apagamos sus "instintos de batalla" y activamos su antena Bluetooth. Ahora el robot obedece comandos humanos enviados desde un navegador web, utilizando su giroscopio interno como asistencia de conducción para que el usuario no tenga que lidiar con las desviaciones mecánicas de los motores.

---

## 🧠 Tecnologías y Conceptos Clave

Para lograr que el robot navegue con precisión y se comunique con tu teléfono, usamos estos conceptos:

* **📡 Bluetooth Low Energy (El Puente Invisible):** Un protocolo de comunicación de ultra bajo consumo. Permite enviar comandos instantáneos desde la web al robot.
* **🌐 Web Bluetooth API (El Mando Universal):** Una tecnología que rompe barreras. Permite que navegadores como Chrome o Edge se conecten directamente al hardware por Bluetooth. ¡Cero descargas, cero instalaciones!
* **⚖️ Giroscopio / IMU (El Oído Interno):** Un sensor que detecta la rotación y el equilibrio. Le dice al robot: *"Te estás desviando 2 grados a la izquierda"*.
* **🧮 Controlador PDI (El Piloto Automático):** Un algoritmo matemático (Proporcional-Derivativo-Integral) que ajusta dinámicamente la velocidad de las llantas. Si el robot se desvía, el PDI frena un motor y acelera el otro en milisegundos para volver al rumbo recto.
* **🚦 LED NeoPixel (El Semáforo de Estado):** Un indicador visual inteligente que nos muestra qué acción está ejecutando o pensando el robot en ese momento.

---

## 🖼️ Galería y Centro de Control Web

Para controlar el robot, no necesitas descargar nada. La interfaz está alojada de forma pública y es 100% *responsive* (se adapta a la pantalla de tu computadora, tablet o celular).

1. **Desde tu computadora:** Ingresa al siguiente enlace usando Google Chrome o Microsoft Edge:
   🔗 **[Interfaz Web Cenfobot Control](https://universidad-cenfotec.github.io/makerlab-learning-projects/)**

2. **Desde tu teléfono móvil:** Escanea este código QR con tu cámara para abrir el control al instante:

   ![Sumobot](https://github.com/Universidad-Cenfotec/makerlab-learning-projects/blob/main/docs/imagenes/MakerLab_QR.svg) 
   


*(Nota: Actualmente el navegador Safari en iOS no soporta Web Bluetooth nativo. Recomendamos usar Chrome en Android o en PC).*

---

## 💻 Configuración del Software y Archivos

Este proyecto está dividido en dos partes: el código que vive en la placa (Hardware) y la interfaz gráfica (Web).

### 1. El Cerebro Físico (Hardware)
La placa de nuestro Sumobot utiliza **CircuitPython**. Para programarla, no necesitas instalar programas pesados, ¡podemos hacerlo todo desde el navegador web!

Utilizaremos el **IdeaCode Web IDE**, una herramienta que te permite ver y editar directamente los archivos dentro del IdeaBoard(cerebro del sumobot):
🔗 **[Acceder a IdeaCode (Editor Web)](https://ideacode.crcibernetica.com/)**

**Pasos para cargar el código:**
1. Conecta tu robot a la computadora mediante un cable USB.
2. Abre IdeaCode en Google Chrome o Edge, haz clic en el botón de conexión serial y selecciona el puerto en el que esta conectada la placa.
3. A la izquierda verás los archivos de tu robot. Tienes dos opciones para cargar nuestro sistema BLE:
   * **Opción A (Recomendada):** Crea un archivo llamado `sumobot_ble.py`, pega ahí el código fuente de nuestro proyecto y guárdalo. Luego, abre el archivo maestro llamado `code.py` (este es el archivo que la placa ejecuta automáticamente al encender) y escribe únicamente esta línea: `import sumobot_ble`.
   * **Opción B (Directa):** Abre el archivo `code.py` y pega directamente todo el código del proyecto ahí.

### 2. El Centro de Control (Web)
El código de la interfaz gráfica se encuentra en `codigos/index.html`. No necesitas modificarlo para jugar, ya que está subido a GitHub Pages, pero puedes abrirlo en tu editor de código favorito si deseas personalizar los botones o los colores de tu control remoto.

### 🚀 ¿Cómo iniciar la conexión?
1. Enciende tu Cenfobot (o desconéctalo del USB y ponle baterías). El NeoPixel parpadeará indicando que está listo para emparejarse.
2. Abre la interfaz web en tu dispositivo (usando el link o el QR).
3. Haz clic en el botón de conexión BLE y selecciona tu robot en el menú del navegador.
4. Usa los botones en pantalla para mover el robot. ¡Observa cómo corrige su rumbo automáticamente si intentas empujarlo hacia los lados!

---

## 🎮 Comandos y Telemetría

### 1. Protocolo de Comunicación
El navegador web y el robot se comunican usando un formato de texto muy simple: `COMANDO,VELOCIDAD`.
* Ejemplo: Si la web envía `F,0.5`, el robot entiende: **"Avanzar (Forward) al 50% de mi capacidad máxima"**.
* Ejemplo: Si envía `B,0.7`, el robot entiende: **"Retroceder (Backward) al 70%"**.

| Comando | Letra Clave | Acción en el Robot |
| :---: | :---: | :--- |
| **Avanzar** | `F` | Motores adelante + Control PDI activo |
| **Retroceder** | `B` | Motores en reversa + Control PDI activo |
| **Girar Izquierda** | `L` | Rotación sobre su propio eje |
| **Girar Derecha** | `R` | Rotación sobre su propio eje |
| **Detener** | `S` | Freno total de motores |

### 2. Estados Visuales (NeoPixel)
El robot te hablará a través de la luz. La página web también tiene un LED virtual que se sincroniza con estos colores:

| Color del LED | Estado del Cenfobot |
| :--- | :--- |
| 🟢 **Verde** | Avanzando en línea recta. |
| 🔴 **Rojo** | Retrocediendo. |
| 🔵 **Cian** | Girando (Izquierda / Derecha). |
| 🟡 **Amarillo** | Sistema en espera / Detenido. |
| 🟠 **Naranja** | Calibración inicial del Giroscopio (¡No lo muevas!). |

---

## 🔬 Aprendizajes Clave MakerLab

Este proyecto lleva las bases de la robótica al siguiente nivel:

**1. El mundo físico no es perfecto:**
Si le das la misma energía a dos motores idénticos, un robot nunca irá en línea recta perfecta por culpa de la fricción, el peso y el polvo. Aprender a implementar un **Control PDI con Giroscopio** es la solución profesional de la ingeniería: el robot mide su propio error y se autocorrige cientos de veces por segundo.

**2. Web Bluetooth democratiza el hardware:**
Programar aplicaciones nativas para Android y para iOS toma meses. Al usar la Web API, creamos un control remoto multiplataforma en un solo archivo `HTML`, haciendo la tecnología mucho más accesible para fines educativos.

**3. Telemetría y Feedback:**
Un buen prototipo no solo obedece órdenes, también informa su estado. Sincronizar el estado de conexión y los colores del LED entre el hardware físico y la interfaz de usuario web cierra el ciclo completo de la **Interacción Humano-Máquina (HCI)**.
