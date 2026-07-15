import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Definir una lista de colores (Formato BGR de OpenCV: Azul, Verde, Rojo)
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]  # Rojo, Azul, Verde
color_index = 0
brush_color = colors[color_index]
brush_thickness = 5

# Variable global que actuará como nuestro lienzo transparente
canvas = None

def finger_paint():
    global canvas, brush_color, color_index

    cam = cv2.VideoCapture(0)
    cam.set(3, 1280)  # Establecer resolución HD para tener más espacio de dibujo
    cam.set(4, 720)

    # Variables para recordar dónde estaba el dedo un instante atrás y poder trazar una línea
    prev_x, prev_y = None, None

    with mp_hands.Hands(
        model_complexity=1, # Subimos la complejidad para más precisión al dibujar
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        while cam.isOpened():
            success, frame = cam.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)  # Espejo

            # Si es la primera vez que corre, crear un lienzo negro del mismo tamaño que la cámara
            if canvas is None:
                canvas = np.zeros_like(frame)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 1. Extraer las coordenadas del índice (pincel)
                    x = int(hand_landmarks.landmark[8].x * frame.shape[1])
                    y = int(hand_landmarks.landmark[8].y * frame.shape[0])

                    # 2. Extraer los puntos del pulgar y el índice para calcular distancia
                    thumb_tip = hand_landmarks.landmark[4]
                    index_tip = hand_landmarks.landmark[8]

                    # GEOMETRÍA: Calcular la distancia (Hipotenusa) entre pulgar e índice
                    dist = np.hypot((thumb_tip.x - index_tip.x) * frame.shape[1],
                                    (thumb_tip.y - index_tip.y) * frame.shape[0])

                    # 3. GESTO DE BORRAR: Si la distancia es menor a 40 píxeles (dedos tocándose)
                    if dist < 40:
                        canvas = np.zeros_like(frame) # Resetear el lienzo a negro
                        prev_x, prev_y = None, None   # Soltar el trazo

                    # 4. GESTO CAMBIO DE COLOR: Si abres toda la mano (dedo medio estirado)
                    # Cambia de color iterando por la lista de forma cíclica
                    if hand_landmarks.landmark[12].y < hand_landmarks.landmark[9].y:
                        color_index = (color_index + 1) % len(colors)
                        brush_color = colors[color_index]

                    # 5. DIBUJAR: Si ya teníamos un punto anterior, trazar una línea hasta el nuevo punto
                    if prev_x is not None and prev_y is not None:
                        cv2.line(canvas, (prev_x, prev_y), (x, y), brush_color, brush_thickness)

                    # Guardar la posición actual como la "anterior" para el siguiente ciclo
                    prev_x, prev_y = x, y

                    # Dibujar el esqueleto (opcional, ayuda a ver la detección)
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            else:
                # Si no hay manos en pantalla, soltar el trazo para que no se dibujen líneas rectas feas al regresar
                prev_x, prev_y = None, None

            # FUSIÓN: Combinar el cuadro de la cámara real (frame) con el lienzo de dibujo (canvas)
            # addWeighted mezcla las imágenes (70% cámara, 30% dibujos) para que parezca un holograma
            frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

            cv2.imshow("Finger Paint MakerLab", frame)
            
            # Presionar 'q' para salir
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cam.release()
    cv2.destroyAllWindows()

finger_paint()
