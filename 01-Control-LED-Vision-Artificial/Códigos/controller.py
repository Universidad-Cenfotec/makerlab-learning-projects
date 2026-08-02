# Importamos la librería pyfirmata2 para hablar con el Arduino
from pyfirmata2 import Arduino

# Definimos el puerto donde está conectado el Arduino (¡Cámbialo si es necesario!)
comport = 'COM9'
board = Arduino(comport)

# Configuramos los pines del Arduino como salidas digitales ('d': digital, número de pin, 'o': output)
led_1 = board.get_pin('d:8:o')
led_2 = board.get_pin('d:9:o')
led_3 = board.get_pin('d:10:o')
led_4 = board.get_pin('d:11:o')
led_5 = board.get_pin('d:12:o')

# Esta función recibe una lista llamada 'fingerUp' (ej. [0,1,0,0,0])
# Cada posición de la lista representa un dedo: [Pulgar, Índice, Medio, Anular, Meñique]
# 1 significa dedo levantado, 0 significa dedo bajado.
def led(fingerUp):
    # Si la mano está cerrada (0 dedos) -> Apaga todos los LEDs
    if fingerUp == [0,0,0,0,0]:
        led_1.write(0)
        led_2.write(0)
        led_3.write(0)
        led_4.write(0)
        led_5.write(0)

    # Si solo el índice está levantado -> Enciende LED 1
    elif fingerUp == [0,1,0,0,0]:
        led_1.write(1)
        led_2.write(0)
        led_3.write(0)
        led_4.write(0)
        led_5.write(0)
        
    # Si índice y medio están levantados -> Enciende LED 1 y 2
    elif fingerUp == [0,1,1,0,0]:
        led_1.write(1)
        led_2.write(1)
        led_3.write(0)
        led_4.write(0)
        led_5.write(0)    
        
    # Si índice, medio y anular están levantados -> Enciende LED 1, 2 y 3
    elif fingerUp == [0,1,1,1,0]:
        led_1.write(1)
        led_2.write(1)
        led_3.write(1)
        led_4.write(0)
        led_5.write(0)
        
    # Si todos menos el pulgar están levantados -> Enciende LED 1, 2, 3 y 4
    elif fingerUp == [0,1,1,1,1]:
        led_1.write(1)
        led_2.write(1)
        led_3.write(1)
        led_4.write(1)
        led_5.write(0)
        
    # Si los 5 dedos están levantados -> Enciende todos los LEDs
    elif fingerUp == [1,1,1,1,1]:
        led_1.write(1)
        led_2.write(1)
        led_3.write(1)
        led_4.write(1)
        led_5.write(1)
