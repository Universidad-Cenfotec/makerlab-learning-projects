import cv2
import mediapipe as mp

# Cargar los módulos de dibujo y detección de manos de MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

def run_hand_tracking():
    # Iniciar la captura de video (0 suele ser la cámara web principal)
    cam = cv2.VideoCapture(0)

    # Configurar el modelo de Inteligencia Artificial
    with mp_hands.Hands(
        model_complexity=0,         # 0 es más rápido, 1 es más preciso
        max_num_hands=2,            # Número máximo de manos a detectar
        min_detection_confidence=0.5, # Umbral de confianza para detectar (50%)
        min_tracking_confidence=0.5   # Umbral de confianza para seguir el movimiento (50%)
    ) as hands:

        # Bucle principal: se ejecuta mientras la cámara esté abierta
        while cam.isOpened():
            success, frame = cam.read() # Leer un cuadro (foto) de la cámara

            if not success:
                print("Ignoring empty camera frame.")
                continue

            # MediaPipe requiere colores en formato RGB, pero OpenCV usa BGR por defecto.
            # Aquí hacemos la conversión para que la IA entienda la imagen.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Procesar la imagen y buscar manos
            results = hands.process(frame_rgb)

            # Si se encontraron manos en la imagen...
            if results.multi_hand_landmarks:
                # Recorrer cada mano detectada
                for hand_landmarks in results.multi_hand_landmarks:
                    # Dibujar los puntos (landmarks) y las líneas que los conectan
                    mp_drawing.draw_landmarks(
                        frame, # Imagen donde vamos a dibujar
                        hand_landmarks, # Coordenadas de los puntos de la mano
                        mp_hands.HAND_CONNECTIONS, # Conexiones (huesos)
                        mp_styles.get_default_hand_landmarks_style(), # Estilo de los puntos
                        mp_styles.get_default_hand_connections_style(), # Estilo de las líneas
                    )

            # Mostrar el resultado en una ventana (cv2.flip crea un efecto espejo)
            cv2.imshow("Detector de manos", cv2.flip(frame, 1))

            # Esperar 1 milisegundo por si el usuario presiona la tecla 'q' para salir
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # Liberar la cámara y cerrar todas las ventanas al terminar
    cam.release()
    cv2.destroyAllWindows()

# Ejecutar la función
run_hand_tracking()
