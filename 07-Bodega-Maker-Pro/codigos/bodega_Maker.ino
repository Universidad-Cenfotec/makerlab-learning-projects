#include <LiquidCrystal.h>
#include <Servo.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
Servo miServo;

// Pines
const int potPin = A1;
const int trigPin = A2;
const int echoPin = A3;
const int servoPin = A4;

// Memoria
int codigoGuardado = 0;
int distanciaGuardada = 0;
bool sistemaConfigurado = false; 

// Máquina de Estados
enum Estados { 
  MENU_PRINCIPAL, 
  LOGIN_CODIGO, 
  LOGIN_DISTANCIA, 
  ACCESO_CONCEDIDO, 
  CONFIG_NUEVO_CODIGO, 
  CONFIG_NUEVA_DISTANCIA 
};

Estados estadoActual = MENU_PRINCIPAL;
int opcionMenu = 0; 
bool validandoParaConfig = false; 
unsigned long tiempoLectura = 0;
bool estable = false;
int botonAnterior = 0; // Variable crucial para el anti-rebote

// --- Funciones de Seguridad y Estabilidad Visual ---

void mostrarMensaje(String l1, String l2) {
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print(l1);
  lcd.setCursor(0, 1); lcd.print(l2);
}

// Esta función ahora dibuja la parte superior inmediatamente para que la pantalla nunca quede vacía
void cambiarEstado(Estados nuevo) {
  estadoActual = nuevo;
  lcd.clear();
  switch(nuevo) {
    case MENU_PRINCIPAL:       lcd.setCursor(0,0); lcd.print("> MENU PRINCIPAL"); break;
    case LOGIN_CODIGO:         lcd.setCursor(0,0); lcd.print("Paso 1: CODIGO  "); break;
    case LOGIN_DISTANCIA:      lcd.setCursor(0,0); lcd.print("Paso 2: BIO-SCAN"); break;
    case CONFIG_NUEVO_CODIGO:  lcd.setCursor(0,0); lcd.print("SET NUEVO COD:  "); break;
    case CONFIG_NUEVA_DISTANCIA:lcd.setCursor(0,0);lcd.print("SET NUEVA DIST: "); break;
    case ACCESO_CONCEDIDO:     lcd.setCursor(0,0); lcd.print("ACCESO TOTAL    "); break;
  }
}

int leerBotonSeguro() {
  analogRead(A0); // Lectura "falsa" para limpiar la interferencia del potenciómetro
  delay(2);       // Le damos tiempo al chip para estabilizarse
  int a = analogRead(A0);
  if (a > 1000) return 0; // Ningún botón presionado
  if (a < 50) return 5;   // RIGHT
  if (a < 250) return 1;  // UP
  if (a < 450) return 2;  // DOWN
  if (a < 650) return 3;  // LEFT
  if (a < 850) return 4;  // SELECT
  return 0;
}

long obtenerDistancia() {
  digitalWrite(trigPin, LOW); delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Timeout de 20ms (20000us) agregado. Si el sensor falla, el Arduino NO se congela.
  long d = pulseIn(echoPin, HIGH, 20000) * 0.034 / 2; 
  return (d > 0 && d < 100) ? d : 0;
}

// --- SETUP ---
void setup() {
  lcd.begin(16, 2);
  miServo.attach(servoPin);
  miServo.write(0); 
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  mostrarMensaje("BOVEDA MAKER", "Iniciando...");
  delay(1500);
  cambiarEstado(MENU_PRINCIPAL);
}

// --- LOOP PRINCIPAL ---
void loop() {
  // 1. Antirrebote Físico: Convierte clics largos o sucios en un solo pulso exacto
  int botonActual = leerBotonSeguro();
  int btn = 0; 
  if (botonActual != botonAnterior && botonActual != 0) {
    btn = botonActual; // btn solo tendrá valor durante un milisegundo exacto
  }
  botonAnterior = botonActual;

  // 2. Lectura Segura del Potenciómetro aislada de los botones
  analogRead(potPin); delay(2);
  int potVal = analogRead(potPin);
  int potMapeado = map(potVal, 0, 1023, 100, 999);

  // 3. Máquina de Estados
  switch (estadoActual) {

    case MENU_PRINCIPAL:
      lcd.setCursor(0, 1);
      if (opcionMenu == 0) lcd.print(" [DESBLOQUEAR]  ");
      else                 lcd.print(" [CONFIGURAR]   ");

      if (btn == 1) opcionMenu = 0; // UP
      if (btn == 2) opcionMenu = 1; // DOWN
      
      if (btn == 4) { // SELECT
        if (opcionMenu == 0) {
          if (!sistemaConfigurado) {
            mostrarMensaje("NO CONFIGURADO", "Ir a Setup...");
            delay(1500);
            cambiarEstado(CONFIG_NUEVO_CODIGO);
          } else {
            validandoParaConfig = false;
            cambiarEstado(LOGIN_CODIGO);
          }
        } 
        else { 
          if (!sistemaConfigurado) {
            mostrarMensaje("MODO: SETUP", "Primera vez...");
            delay(1500);
            cambiarEstado(CONFIG_NUEVO_CODIGO);
          } else {
            mostrarMensaje("SEGURIDAD:", "Validar Admin...");
            delay(1500);
            validandoParaConfig = true;
            cambiarEstado(LOGIN_CODIGO);
          }
        }
      }
      break;

    case LOGIN_CODIGO:
      lcd.setCursor(0, 1);
      lcd.print("Valor: "); lcd.print(potMapeado); lcd.print("    ");

      if (btn == 4) {
        if (abs(potMapeado - codigoGuardado) < 15) {
          mostrarMensaje("CODIGO OK", "Siguiente...");
          delay(1000);
          cambiarEstado(LOGIN_DISTANCIA);
        } else {
          mostrarMensaje("ERROR", "Clave Invalida");
          delay(1500);
          cambiarEstado(MENU_PRINCIPAL);
        }
      }
      break;

    case LOGIN_DISTANCIA:
      {
        long dist = obtenerDistancia();
        lcd.setCursor(0, 1);
        lcd.print("D:"); lcd.print(dist); lcd.print("cm O:"); lcd.print(distanciaGuardada); lcd.print("cm  ");

        if (abs(dist - distanciaGuardada) <= 1) {
          if (!estable) { tiempoLectura = millis(); estable = true; }
          if (millis() - tiempoLectura > 3000) {
            estable = false;
            if (validandoParaConfig) cambiarEstado(CONFIG_NUEVO_CODIGO); 
            else                     cambiarEstado(ACCESO_CONCEDIDO);    
          }
        } else { estable = false; }
      }
      break;

    case ACCESO_CONCEDIDO:
      mostrarMensaje("ACCESO TOTAL", "Puerta Abierta");
      miServo.write(90);
      delay(5000);
      miServo.write(0);
      cambiarEstado(MENU_PRINCIPAL);
      break;

    case CONFIG_NUEVO_CODIGO:
      lcd.setCursor(0, 1);
      lcd.print("Cod:"); lcd.print(potMapeado); lcd.print(" [SELECT] ");
      
      if (btn == 4) {
        codigoGuardado = potMapeado;
        mostrarMensaje("CODIGO GUARDADO", "Siguiente...");
        delay(1500);
        cambiarEstado(CONFIG_NUEVA_DISTANCIA);
      }
      break;

    case CONFIG_NUEVA_DISTANCIA:
      {
        long d2 = obtenerDistancia();
        lcd.setCursor(0, 1);
        lcd.print("Dist:"); lcd.print(d2); lcd.print("cm [SEL] ");
        
        if (btn == 4) {
          distanciaGuardada = d2;
          sistemaConfigurado = true; 
          mostrarMensaje("GUARDADO OK!", "Boveda Activa");
          delay(2000);
          cambiarEstado(MENU_PRINCIPAL);
        }
      }
      break;
  }
  
  delay(50); // Pausa para no saturar los cristales líquidos de la pantalla
}
