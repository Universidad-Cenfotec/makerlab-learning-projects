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

# ---------------- Servo ----------------
servo = ib.Servo(board.IO4)

REPOSO = 0
ABIERTO = 90

servo.angle = REPOSO

# ---------------- Ultrasonico ----------------
sonar = HCSR04(board.IO26, board.IO25)

# ---------------- BLE ----------------
ble = BLERadio()
ble.name = "Porton_Sumobot"

uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

print("====================================")
print(" Sistema listo")
print(" Servo inicializado")
print(" BLE listo")
print("====================================")

objeto_detectado = False
ultimo_envio = time.monotonic()

# ==================================================
# LOOP PRINCIPAL
# ==================================================

while True:

    # Esperando conexión
    ib.pixel = (0, 0, 255)

    ble.start_advertising(advertisement)

    print("Esperando conexión BLE...")

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

    # Conectado
    ble.stop_advertising()

    ib.pixel = (0, 255, 0)

    uart.write("CONECTADO\n")

    print("Cliente conectado")

    while ble.connected:

        # =====================================
        # Leer sensor
        # =====================================

        try:

            distancia = sonar.dist_cm()

            if distancia != -1 and distancia < 50:
                objeto_detectado = True
            else:
                objeto_detectado = False

        except RuntimeError:
            pass

        # =====================================
        # Enviar estado cada segundo
        # =====================================

        if time.monotonic() - ultimo_envio >= 1:

            if objeto_detectado:
                uart.write("OBJETO_DETECTADO\n")
            else:
                uart.write("AREA_LIBRE\n")

            ultimo_envio = time.monotonic()

        # =====================================
        # Leer comandos BLE
        # =====================================

        data = uart.readline()

        if data:

            try:

                texto = data.decode("utf-8").strip()

                print("Comando recibido:", texto)

                if texto == "ABRIR":

                    print("Abriendo portón")

                    servo.angle = ABIERTO

                    time.sleep(1)

                    uart.write("PORTON_ABIERTO\n")

                elif texto == "CERRAR":

                    print("Cerrando portón")

                    servo.angle = REPOSO

                    time.sleep(1)

                    uart.write("PORTON_CERRADO\n")

            except Exception as e:

                print("Error:", e)

        time.sleep(0.05)

    # =====================================
    # Desconectado
    # =====================================

    print("Cliente desconectado")

    servo.angle = REPOSO

    ib.pixel = (0, 0, 0)

    time.sleep(0.5)
