# 🛡️ Bóveda Maker Pro (Caja Fuerte Inteligente)

> **MakerLab - Universidad Cenfotec**
> Este proyecto es ideal para dar tus primeros pasos en el mundo del hardware (electrónica) y el software (programación). ¡Aprenderás cómo los códigos le dan vida a los objetos físicos!

Este proyecto te enseña a construir una cerradura de doble seguridad, ¡como las de las películas de espías! Para abrir el cerrojo, necesitas dos cosas: ingresar una contraseña numérica girando una perilla y usar una "llave invisible", colocando tu mano a una distancia secreta que solo tú conoces.

---

## 🧠 ¿Qué aprenderemos aquí?

En el mundo de la tecnología, las computadoras necesitan "sentidos" para entender el mundo real. En este proyecto exploraremos:

* **🧠 El Cerebro (Microcontrolador):** Cómo usar una placa Arduino para tomar decisiones basadas en lo que le dicen los sensores.
* **🦇 Eco-Localización (Ultrasonido):** Descubriremos cómo usar el sonido que no podemos escuchar para medir distancias, ¡exactamente igual que hacen los murciélagos!
* **⚡ Señales Analógicas vs Digitales:** Aprenderemos cómo traducir algo físico (como girar una perilla) en un cambio de electricidad, y luego convertirlo en un número digital del 100 al 999.
* **🚦 Multitarea Básica:** Cómo programar el Arduino para que pueda hacer varias cosas a la vez (como leer la pantalla, escuchar la perilla y mover el motor) sin quedarse "pegado".

---

## 🛠️ Materiales Necesarios

| Cantidad | Componente | ¿Para qué sirve? |
| :---: | :--- | :--- |
| 1 | Placa Arduino | Es el cerebro de nuestra bóveda. |
| 1 | Shield LCD 16x2 | Es nuestra pantalla y teclado (trae 5 botones). |
| 1 | Sensor HC-SR04 | Los "ojos" que miden la distancia de tu mano. |
| 1 | Potenciómetro (10k) | La perilla de caja fuerte para meter la clave. |
| 1 | Micro Servo SG90 | Un pequeño motor que funcionará como el cerrojo. |
| Varios | Cables Jumper | Para conectar todo (Macho-Macho y Macho-Hembra). |

---

## 🔌 Cómo conectar todo (Hardware)

Armar el circuito es como armar un rompecabezas de LEGO. Como usamos una pantalla tipo "Shield", esta se encaja directamente encima del Arduino, como si fuera un sombrero.

1. **Montaje:** Encaja el Shield LCD directamente sobre los pines del Arduino.
2. **Energía:** Conecta los pines de VCC y GND (energía y tierra) del sensor ultrasónico, el potenciómetro y el motor a los pines de 5V y GND del Arduino.
3. **Señales:** Conecta los cables de datos (los que llevan la información) siguiendo esta tabla:

| Componente | Pin del Componente | Pin del Arduino |
| :--- | :--- | :---: |
| Botones de Pantalla | Interno | **Pin A0** |
| Potenciómetro (Perilla) | Pata del Centro | **Pin A1** |
| Ultrasonido (Radar) | Trig (El que grita) | **Pin A2** |
| Ultrasonido (Radar) | Echo (El que escucha)| **Pin A3** |
| Servo Motor (Cerrojo) | Señal (Cable Amarillo) | **Pin A4** |

---

### Galería de Componentes

**El Cerebro y la Pantalla**
![Shield LCD y Arduino](imagenes/Shield_LCD_Arduino.jpeg)

**Los Sensores (Perilla y Radar)**
![Sensores](imagenes/Sensores_Boveda.jpeg)

**El Motor (Cerrojo)**
![Servo](imagenes/Servo_SG90.jpeg)

**Todo Conectado**
![Circuito Final](imagenes/Circuito_Boveda_Final.jpeg)

---

## 💻 Configuración del Software

### 1. Preparar la Computadora
1. Descarga e instala el programa **Arduino IDE** (es gratuito).
2. ¡Buenas noticias! No hay que instalar librerías extra, las que necesitamos para la pantalla y el motor ya vienen incluidas.

### 2. Descargar el Código
1. Ve al inicio de esta página en GitHub.
2. Haz clic en el botón verde **"Code"** y luego en **"Download ZIP"**.
3. Descomprime la carpeta y abre el archivo `codigos/boveda_maker.ino`.

### 3. Subir el Código al Arduino
1. Conecta tu Arduino a la computadora con el cable USB.
2. En el programa Arduino, ve a `Herramientas` > `Placa` y elige tu modelo (ej. Arduino Uno).
3. En `Herramientas` > `Puerto`, selecciona el puerto de tu placa.
4. Haz clic en el botón redondo con una flecha hacia la derecha (**Subir**).

⚙️ **Un tip secreto:** Si la pantalla enciende pero se ve en blanco (sin letras), busca un tornillito azul en la esquina de la pantalla y gíralo despacio con un destornillador. ¡Eso ajusta el brillo de las letras!

---

# 🚀 ¡A jugar con la Bóveda!

Una vez que el código esté adentro, el Arduino hará todo por sí solo:

1. **Paso 1 (Crear tu clave):** Como es la primera vez que se enciende, te pedirá configurar una clave. Gira el potenciómetro para elegir un número de 3 dígitos y presiona el botón `SELECT`. 
2. **Paso 2 (Llave invisible):** Pon tu mano frente al sensor del radar a la distancia que quieras y presiona `SELECT` para guardarla.
3. **Paso 3 (¡Desbloquear!):** Ve al menú principal, selecciona "Desbloquear". Ingresa tu clave numérica y luego mantén tu mano exactamente a la distancia secreta durante 3 segundos. ¡Escucharás el motor abrir el cerrojo!

# ¡LISTO!
🎉      ╰(*°▽°*)╯         🎉

![Boveda_Funcionando](imagenes/Boveda_Funcionando.gif)

---

# 🤓 Para los curiosos: ¿Cómo funciona la magia del código?

Si quieres saber cómo logramos que todo esto funcione sin fallar, aquí te explicamos tres trucos de programación que usamos:

**1. El truco de los "Estados" (Como un videojuego)**
Si le decimos al Arduino "espera 3 segundos", se queda totalmente dormido y no responde a los botones. Para evitarlo, programamos el código por "Estados" (Menú Principal, Configurando, Abierto). Así el Arduino siempre está despierto, revisando en qué nivel del "juego" está y qué debe mostrar en pantalla.

**2. Limpiando el Ruido Eléctrico (Antirrebote)**
Cuando presionas un botón físico, los metales por dentro chocan y rebotan a nivel microscópico. Como el Arduino piensa súper rápido, a veces cree que presionaste el botón 5 veces en lugar de una. En el código, le enseñamos a ignorar esos rebotes y registrar un solo "clic" limpio.

**3. El límite de espera del Radar**
El sensor ultrasónico funciona gritando un sonido y esperando a que rebote para medir el tiempo. Pero, ¿qué pasa si el sonido no choca contra nada y se pierde en el aire? ¡El Arduino se quedaría esperando para siempre! Para evitarlo, le pusimos un cronómetro límite: "Si en 20 milisegundos no escuchas el rebote, asume que no hay nada ahí y sigue trabajando".

💻 **[>> CLIC AQUÍ PARA VER Y DESCARGAR EL CÓDIGO (.ino) <<](codigos/bodega_Maker.ino)**
