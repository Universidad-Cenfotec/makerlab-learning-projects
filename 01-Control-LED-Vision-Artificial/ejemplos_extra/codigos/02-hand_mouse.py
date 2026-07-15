import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Inicializar módulos de MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Obtener la resolución exacta de tu monitor (ej. 1920x1080)
screen_w, screen_h = pyautogui.size()

def hand_mouse_control():
    cam = cv2.VideoCapture(0)
    # Ajustar la resolución de la cámara para que el proceso sea rápido
    cam.set(3, 640)  # ancho
    cam.set(4, 480)  # alto

    with mp_hands.Hands(
        max_num_hands=1, # Solo queremos controlar el mouse con 1 mano a la vez
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        while cam.isOpened():
            success, frame = cam.read()
            if not success:
                continue

            # Crear efecto espejo inmediatamente para coordinar mejor los movimientos
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                # Tomar los datos de la primera mano detectada
                hand_landmarks = results.multi_hand_landmarks[0]

                # Obtener las coordenadas del PUNTO 8 (Punta del dedo índice)
                index_finger_tip = hand_landmarks.landmark[8]
                # Multiplicar por el tamaño del frame porque MediaPipe devuelve valores entre 0 y 1
                x = int(index_finger_tip.x * frame.shape[1])
                y = int(index_finger_tip.y * frame.shape[0])

                # MATEMÁTICAS: Regla de tres (Interpolación)
                # Convertir las coordenadas de la cámara (pequeñas) a las de la pantalla (grandes)
                mouse_x = np.interp(x, [0, frame.shape[1]], [0, screen_w])
                mouse_y = np.interp(y, [0, frame.shape[0]], [0, screen_h])

                # Mover el mouse real de la computadora
                pyautogui.moveTo(mouse_x, mouse_y)

                # DETECCIÓN DE CLIC:
                # Obtener las coordenadas del dedo medio
                middle_finger_tip = hand_landmarks.landmark[12]
                
                # Si la punta del índice está ARRIBA de su nudillo (dedo estirado)
                # Y la punta del medio está ABAJO de su nudillo (dedo doblado hacia abajo)
                if index_finger_tip.y < hand_landmarks.landmark[6].y and \
                   middle_finger_tip.y > hand_landmarks.landmark[10].y:
                    pyautogui.click()  # Simular clic izquierdo

                # Dibujar esqueleto para visualizar
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow("Hand Mouse Control", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cam.release()
    cv2.destroyAllWindows()

hand_mouse_control()
