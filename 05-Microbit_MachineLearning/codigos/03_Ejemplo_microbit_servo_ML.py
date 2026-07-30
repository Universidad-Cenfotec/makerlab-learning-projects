def on_bluetooth_connected():
    basic.show_icon(IconNames.YES)
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_icon(IconNames.NO)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def on_uart_data_received():
    global receivedString
    receivedString = bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE))
    if receivedString == "Rojo":
        basic.show_string("R")
        pins.servo_write_pin(AnalogPin.P0, 90)
    # Abrir
    if receivedString == "Verde":
        basic.show_string("V")
        pins.servo_write_pin(AnalogPin.P0, 90)
    # Abrir
    if receivedString == "Minion1":
        basic.show_string("M1")
        pins.servo_write_pin(AnalogPin.P0, 0)
    # Cerrar
    if receivedString == "Minion2":
        basic.show_string("M2")
        pins.servo_write_pin(AnalogPin.P0, 0)
    # Cerrar
    if receivedString == "Nulo":
        pins.servo_write_pin(AnalogPin.P0, 0)
        basic.clear_screen()
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),
    on_uart_data_received)

receivedString = ""
bluetooth.start_uart_service()
basic.show_icon(IconNames.SILLY)
