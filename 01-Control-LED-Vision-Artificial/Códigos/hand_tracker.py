import cv2 # Librería principal de Visión por Computadora (OpenCV)
import controller as cnt # Importamos nuestro archivo controller.py y lo llamamos 'cnt'
from cvzone.HandTrackingModule import HandDetector # Módulo especializado para detectar manos

# Inicializamos el detector de manos. 
# detectionCon=0.8: Exige un 80% de seguridad de que es una mano para no confundirse.
# maxHands=1: Solo buscará y analizará una mano a la vez.
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Encendemos la cámara web (el '0' indica la cámara por defecto de la PC)
video = cv2.VideoCapture(0)

# Bucle infinito para procesar el video cuadro por cuadro (como una película)
while True:
    # Leemos el cuadro (frame) actual de la cámara
    ret, frame = video.read()
    
    # Volteamos el video horizontalmente (efecto espejo) para que sea más intuitivo
    frame = cv2.flip(frame, 1)
    
    # El detector busca manos en el cuadro y las dibuja. Devuelve la información en 'hands'
    hands, img = detector.findHands(frame)
    
    # Si encuentra al menos una mano...
    if hands:
        # Extraemos la información de la primera mano detectada (coordenadas de los 21 puntos)
        lmList = hands[0]
        
        # Le preguntamos al detector cuántos dedos están levantados basándose en los puntos
        # Devuelve una lista de 1s y 0s (ej. [0,1,0,0,0])
        fingerUp = detector.fingersUp(lmList)

        # Mostramos la lista en la consola para depurar
        print(fingerUp)
        
        # ¡Magia! Le enviamos esa lista a nuestro archivo controller.py para que encienda los LEDs
        cnt.led(fingerUp)
        
        # Dependiendo de la lista, dibujamos un texto en la pantalla del video
        # Formato de cv2.putText: (imagen, texto, (posición x,y), fuente, tamaño, (color BGR), grosor, tipo de línea)
        if fingerUp == [0,0,0,0,0]:
            cv2.putText(frame, 'Finger count:0', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        elif fingerUp == [0,1,0,0,0]:
            cv2.putText(frame, 'Finger count:1', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)    
        elif fingerUp == [0,1,1,0,0]:
            cv2.putText(frame, 'Finger count:2', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        elif fingerUp == [0,1,1,1,0]:
            cv2.putText(frame, 'Finger count:3', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        elif fingerUp == [0,1,1,1,1]:
            cv2.putText(frame, 'Finger count:4', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        elif fingerUp == [1,1,1,1,1]:
            cv2.putText(frame, 'Finger count:5', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA) 

    # Mostramos la ventana de video con todos los dibujos y textos agregados
    cv2.imshow("frame", frame)
    
    # Esperamos 1 milisegundo por si el usuario presiona una tecla
    k = cv2.waitKey(1)
    
    # Si el usuario presiona la tecla 'k', rompemos el bucle infinito para salir
    if k == ord("k"):
        break

# Al salir del bucle, apagamos la cámara y cerramos todas las ventanas
video.release()
cv2.destroyAllWindows()
