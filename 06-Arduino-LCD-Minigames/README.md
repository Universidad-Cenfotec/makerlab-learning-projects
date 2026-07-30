# 🕹️ Arduino-LCD-Minigames

> **MakerLab - Universidad Cenfotec**
> ¡Convierte tu Arduino en una mini-consola de videojuegos! Este proyecto es ideal para dar tus primeros pasos en la programación de juegos y descubrir cómo usar la imaginación para crear mucha diversión utilizando componentes súper básicos.

El **LCD 1602 Keypad Shield** es una placa clásica e indispensable en el mundo de la electrónica. Tradicionalmente, es la herramienta perfecta para mostrar información clave, como las mediciones de tus sensores, o para navegar por menús de configuración usando sus 5 botones. ¡Pero en el MakerLab nos gusta llevar los componentes más allá de su propósito original! En lugar de usar esta pantalla solo como un monitor de datos serios, aquí te enseñaremos a "hackear" su uso para transformarla y jugar 4 minijuegos retro completos.

---

## 🧠 ¿Qué vas a aprender jugando?

Aunque el objetivo es divertirse, detrás de cada juego hay conceptos geniales de programación que aprenderás sin darte cuenta:

* **Lógica de Videojuegos:** Entenderás cómo funciona el "cerebro" de un juego, separando los gráficos que ves en pantalla de la matemática que ocurre en el fondo.
* **Manejo del Tiempo:** Aprenderás a usar el reloj interno del Arduino para que los juegos no vayan ni muy rápido ni muy lento (evitando que la pantalla parpadee).
* **Uso de Memoria:** Juegos como *Snake* o *Simon Dice* te enseñarán a guardar historiales de datos (como por dónde pasó la serpiente) usando listas de información (Arrays).
* **Ilusiones Ópticas Maker:** Descubrirás cómo engañar al hardware para dibujar personajes personalizados (como dinosaurios o pájaros) en una pantalla que fue diseñada originalmente solo para mostrar letras del alfabeto.

---

## 🛠️ Materiales Necesarios

| Cantidad | Componente | Función |
| :---: | :--- | :--- |
| 1 | Placa Arduino UNO (o compatible) | El microcontrolador que procesará el juego. |
| 1 | LCD 1602 Keypad Shield v1.0 | La pantalla y los controles de tu consola. |
| 1 | Cable USB (Tipo A a B) | Para programar y darle energía al Arduino. |

*¡Lo mejor de este proyecto es que no necesitas cables sueltos, protoboards ni soldar absolutamente nada!*

---

## 🖼️ Galería de Componentes

Para que reconozcas fácilmente los componentes antes de armar la consola:

* **Arduino UNO y LCD Keypad Shield :** El cerebro del proyecto.
  ![Arduino UNO](imagenes/arduino_uno_lcd_shield.jpeg)`)

---

## 🔌 Conexiones (Plug and Play)

Armar tu consola toma menos de 10 segundos:

1. Toma tu pantalla (LCD Keypad Shield) y alinea sus pines de metal con los agujeros negros del Arduino UNO.
2. Presiona firmemente hacia abajo hasta que encaje como una pieza de Lego.
3. Conecta el cable USB del Arduino a tu computadora.
4. *Tip Maker:* Si ves la pantalla encendida pero no logras leer nada, busca un cuadrito azul en la esquina superior izquierda de la placa. Usa un destornillador pequeño para girarlo suavemente; esto ajustará el contraste de la pantalla.

![Consola Ensamblada](imagenes/consola_ensamblada.jpeg))*

---

## 🧪 Código de Prueba: "Hola MakerLab"

Antes de cargar los juegos, es crucial verificar que tu pantalla y tus botones funcionen correctamente. Abre tu **Arduino IDE**, copia este código y súbelo a la placa. 

Al ejecutarlo, la pantalla te saludará y, cuando presiones los botones, te mostrará el valor analógico que está leyendo y el nombre del botón detectado.

```cpp
#include <LiquidCrystal.h>

// Pines estándar usados por el Shield v1.0
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Hola MakerLab!");
  lcd.setCursor(0, 1);
  lcd.print("Prueba un boton.");
  delay(2000);
}

void loop() {
  int valorADC = analogRead(A0); // Leemos el pin analógico 0
  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("ADC: "); 
  lcd.print(valorADC);
  
  lcd.setCursor(0, 1);
  if (valorADC < 50)       { lcd.print("Boton: DERECHA"); }
  else if (valorADC < 250) { lcd.print("Boton: ARRIBA"); }
  else if (valorADC < 450) { lcd.print("Boton: ABAJO"); }
  else if (valorADC < 650) { lcd.print("Boton: IZQUIERDA"); }
  else if (valorADC < 850) { lcd.print("Boton: SELECT"); }
  else                     { lcd.print("Esperando..."); }
  
  delay(150); // Pequeña pausa para no parpadear tan rápido
}
```

## 🎮 Catálogo de Juegos

Dentro de la carpeta `codigos/` encontrarás 4 juegos listos para usar. Solo puedes cargar un juego a la vez en el Arduino. Haz clic en el nombre del juego que desees para ver su código fuente y súbelo a la placa.

### 1. 🟢 [Simon Dice](./codigos/01_Simon_Dice.ino)
**El clásico juego de memoria.** El Arduino generará una secuencia aleatoria de botones (Arriba, Abajo, Izquierda, Derecha). Debes observarla y repetirla exactamente en el mismo orden. Cada nivel suma un paso extra a la secuencia.

* **Qué aprenderás:** Uso de arreglos temporales (`arrays`) para guardar el historial del jugador, generación de semillas aleatorias (`randomSeed`) y programación de "pausas estratégicas" para adaptar la velocidad de la máquina a los reflejos humanos.

### 2. 🐦 [Flappy Maker](./codigos/02_Bird_Game.ino)
**Sobrevive volando.** Controla a un pequeño pájaro que debe esquivar las tuberías atravesando los huecos. Presiona el botón `UP` o `RIGHT` para dar aleteos cortos y evitar caer al suelo o chocar contra el techo.

* **Qué aprenderás:** Creación de píxeles personalizados para dibujar al personaje, implementación de fórmulas matemáticas simples para simular "gravedad" y programación de hitboxes (zonas de colisión).

### 3. 🦖 [Dino Game](./codigos/03_Dino_Game.ino)
**La carrera sin internet.** Nuestra versión del famoso minijuego de Google Chrome. Un cactus se acerca constantemente de derecha a izquierda; presiona el botón `UP` para saltarlo a tiempo. Cada vez que esquivas un cactus, el juego se vuelve un poco más rápido.

* **Qué aprenderás:** Animación de personajes mediante el cambio rápido de dos fotogramas (sprites) y el uso de la función `millis()` para hacer que el dinosaurio salte sin congelar el movimiento del cactus.

### 4. 🐍 [Snake Game](./codigos/04_Snake_Game.ino)
**Efecto Pac-Man.** Controla una serpiente usando los botones de dirección. Tu objetivo es comer el ícono que aparece aleatoriamente en la pantalla para crecer y sumar puntos. Si sales por un borde de la pantalla, aparecerás por el lado opuesto. ¡Pero cuidado con morderte a ti mismo!

* **Qué aprenderás:** Manipulación avanzada de matrices para lograr que cada segmento del cuerpo siga exactamente los pasos de la cabeza de la serpiente, actualizando coordenadas (X, Y) en un espacio de cuadrícula bidimensional.
