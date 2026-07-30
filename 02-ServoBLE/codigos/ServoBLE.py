import time
import board
from ideaboard import IdeaBoard
from hcsr04 import HCSR04

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

# ==================================================
# INICIALIZACIÓN
# ==================================================
ib = IdeaBoard()

# Servo
servo = ib.Servo(board.IO4)
REPOSO = 90
ABIERTO = 0
servo.angle = REPOSO

# Ultrasonico
sonar = HCSR04(board.IO26, board.IO25)

# BLE
ble = BLERadio()
ble.name = "Porton_Sumobot"

uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

print("Sistema listo")

# ==================================================
# VARIABLES
# ==================================================
objeto_detectado = False
contador = 0

# ==================================================
# LOOP PRINCIPAL
# ==================================================
while True:

    # 🔵 Esperando conexión
    ib.pixel = (0,0,255)
    ble.start_advertising(advertisement)

    while not ble.connected:
        try:
            distancia = sonar.dist_cm()

            if distancia != -1 and distancia < 50:
                objeto_detectado = True
            else:
                objeto_detectado = False

        except RuntimeError:
            pass

        time.sleep(0.2)

    # 🟢 Conectado
    ble.stop_advertising()
    ib.pixel = (0,255,0)
    uart.write("CONECTADO\n")

    while ble.connected:

        # ==============================
        # 1️⃣ Leer ultrasónico
        # ==============================
        try:
            distancia = sonar.dist_cm()

            if distancia != -1 and distancia < 50:
                objeto_detectado = True
            else:
                objeto_detectado = False

        except RuntimeError:
            pass

        # ==============================
        # 2️⃣ Enviar estado cada cierto tiempo
        # ==============================
        contador += 1

        if contador >= 3:  # cada ~1 segundo
            if objeto_detectado:
                uart.write("OBJETO_DETECTADO\n")
            else:
                uart.write("AREA_LIBRE\n")

            contador = 0

        # ==============================
        # 3️⃣ Recibir comandos BLE
        # ==============================
        data = uart.readline()
        if data:
            texto = data.decode("utf-8").strip()
            print("Recibido:", texto)

            if texto == "ABRIR" and objeto_detectado:
                servo.angle = ABIERTO
                uart.write("PORTON_ABIERTO\n")

            elif texto == "CERRAR":
                servo.angle = REPOSO
                uart.write("PORTON_CERRADO\n")

        time.sleep(0.2)

    # 🔴 Desconectado
    servo.angle = REPOSO
    ib.pixel = (0,0,0)
    print("BLE desconectado")
