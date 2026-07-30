def on_uart_data_received():
    global receivedString
    receivedString = bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE))
    if receivedString == "Feliz":
        basic.show_icon(IconNames.HAPPY)
    if receivedString == "Triste":
        basic.show_icon(IconNames.SAD)
    if receivedString == "Nada":
        basic.show_icon(IconNames.ASLEEP)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),
    on_uart_data_received)

receivedString = ""
bluetooth.start_uart_service()
basic.show_icon(IconNames.ASLEEP)
