#include <Servo.h> // Librería para controlar el "cuello" del radar

#define trigPin 8  // Pin que emite el sonido
#define echoPin 9  // Pin que escucha el rebote
#define ledPin 7   // Pin del LED de alerta física

Servo myservo;     // Creamos el objeto servo

long duration;
int distance;

int servoPos = 15; // Ángulo inicial del servo
int direccion = 1; // 1 = avanza, -1 = retrocede

bool tracking = false;
bool radarActivo = true;

// ---------- SENSOR (Los Ojos) ----------
int calculateDistance()
{
  // Limpiamos el pin por 2 microsegundos
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Disparamos un pulso ultrasónico inaudible por 10 microsegundos
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Medimos cuánto tardó en volver el eco
  duration = pulseIn(echoPin, HIGH, 30000);

  if(duration == 0) return -1; // Si no hay rebote, ignoramos

  // Fórmula mágica: tiempo * velocidad del sonido / 2 (ida y vuelta)
  return duration * 0.034 / 2;
}

// ---------- COMANDOS ----------
void leerComando()
{
  // Si la computadora (Processing) nos manda un mensaje...
  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // Podemos detener o arrancar el radar a distancia
    if(cmd == "STOP") radarActivo = false;
    if(cmd == "START") radarActivo = true;
  }
}

// ---------- SCAN (Barrido Normal) ----------
void scanRadar()
{
  myservo.write(servoPos); // Movemos el motor al ángulo actual

  int d = calculateDistance(); // Medimos qué hay al frente
  distance = d;

  // ⭐ FORMATO OBLIGATORIO PARA PROCESSING (El Puente)
  // Mandamos los datos así: "angulo,distancia."
  Serial.print(servoPos);
  Serial.print(",");
  Serial.print(distance);
  Serial.print(".");

  // Si hay un objeto a menos de 10cm, ¡Alerta!
  if(d > 0 && d < 10)
  {
    tracking = true; // Entramos en modo persecución
    digitalWrite(ledPin, HIGH); // Encendemos LED
    return;
  }

  // Movemos el radar un paso
  servoPos += direccion;

  // Si llegamos a los extremos, cambiamos de dirección (efecto parabrisas)
  if(servoPos >= 165 || servoPos <= 15)
    direccion *= -1;

  delay(20); // Pequeña pausa para que el motor llegue a su posición
}

// ---------- TRACKING (Persecución de objeto) ----------
void trackObject()
{
  digitalWrite(ledPin, HIGH); // LED rojo encendido

  // Hacemos un micro-barrido solo en la zona donde detectamos algo
  for(int offset=-8; offset<=8; offset++)
  {
    leerComando();
    if(!radarActivo) return;

    myservo.write(servoPos + offset);

    int d = calculateDistance();
    distance = d;

    // ⭐ SIEMPRE enviar datos al radar (Processing necesita saber)
    Serial.print(servoPos + offset);
    Serial.print(",");
    Serial.print(distance);
    Serial.print(".");

    // Si el objeto se aleja a más de 10cm, volvemos a barrido normal
    if(!(d > 0 && d < 10))
    {
      tracking = false;
      digitalWrite(ledPin, LOW);
      return;
    }

    delay(40);
  }
}

// ---------- SETUP (Configuración inicial) ----------
void setup()
{
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);

  myservo.attach(11); // Conectamos el servo al pin 11

  Serial.begin(9600); // Abrimos el canal de comunicación USB a 9600 baudios
}

// ---------- LOOP (Ciclo infinito) ----------
void loop()
{
  leerComando();

  if(!radarActivo) return; // Si nos mandaron a parar, no hacemos nada

  // Decidimos qué hacer: perseguir o buscar
  if(tracking)
    trackObject();
  else
    scanRadar();
}
