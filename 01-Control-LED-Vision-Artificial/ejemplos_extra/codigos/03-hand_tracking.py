import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

# Función personalizada para saber qué dedos están levantados
def fingers_up(hand_landmarks, hand_label):
    fingers = []

    # Identificadores de las puntas de los dedos: índice(8), medio(12), anular(16), meñique(20)
    tips_ids = [8, 12, 16, 20]
    
    # Evaluar los 4 dedos largos
    for tip_id in tips_ids:
        # En la pantalla, la coordenada Y aumenta hacia abajo. 
        # Si la Y de la punta es MENOR que la Y de dos nudillos más abajo, el dedo está levantado.
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            fingers.append(1) # Levantado
        else:
            fingers.append(0) # Doblado

    # Evaluar el pulgar (su mecánica es diferente, se mueve en el eje X, no en el Y)
    if hand_label == "Right": # Si es la mano derecha
        # Compara la posición horizontal de la punta (4) con el nudillo (3)
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else: # Si es la mano izquierda
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

    # Retorna una lista de 5 números (ej. [1, 0, 0, 0, 0] significa solo pulgar levantado)
    return fingers

def run_hand_tracking():
    cam = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:

        while cam.isOpened():
            success, frame = cam.read()
            if not success:
                print("Ignorando frame vacío")
                continue

            frame = cv2.flip(frame, 1) # Efecto espejo vital para la lógica del pulgar
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            total_fingers = 0

            if results.multi_hand_landmarks:
                # zip une las coordenadas de la mano con la etiqueta (Izquierda/Derecha)
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    hand_label = handedness.classification[0].label # "Left" o "Right"
                    
                    # Dibujar puntos
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_styles.get_default_hand_landmarks_style(),
                        mp_styles.get_default_hand_connections_style()
                    )

                    # Llamar a nuestra función matemática
                    fingers = fingers_up(hand_landmarks, hand_label)
                    # Sumar los 1s de la lista para saber el total de dedos levantados
                    total_fingers += sum(fingers)

                    # Obtener la coordenada de la muñeca (punto 0) para escribir el número encima de cada mano
                    wrist = hand_landmarks.landmark[0]
                    h, w, _ = frame.shape
                    cx, cy = int(wrist.x * w), int(wrist.y * h)

                    # Escribir el número de dedos de cada mano cerca de su muñeca
                    cv2.putText(frame, f"{sum(fingers)}", (cx, cy - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            # Escribir el total sumado de ambas manos en la esquina superior izquierda
            cv2.putText(frame, f"Total dedos: {total_fingers}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

            cv2.imshow("Contador Matematico", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cam.release()
    cv2.destroyAllWindows()

run_hand_tracking()
