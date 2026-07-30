#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

// Definición de botones para el Shield
#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   -1

int sequence[50];       // Guarda la secuencia de pasos
int userSequence[50];   // Guarda lo que el usuario presiona
int level = 1;

void setup() {
  lcd.begin(16, 2);
  randomSeed(analogRead(1)); // Semilla aleatoria
  showStartMessage();
}

void loop() {
  // 1. Añadir nuevo paso a la secuencia
  sequence[level - 1] = random(0, 4); // 0 a 3 (Right, Up, Down, Left)
  
  // 2. Mostrar la secuencia al jugador
  showSequence();
  
  // 3. Obtener respuesta del jugador
  if (getUserInput()) {
    level++;
    lcd.clear();
    lcd.print("CORRECTO :)");
    lcd.setCursor(0, 1);
    lcd.print("Pasando a nivel "); lcd.print(level);
    delay(1500); // Tiempo para celebrar el acierto
  } else {
    gameOver();
  }
}

// --- Funciones de Juego ---

void showStartMessage() {
  lcd.clear();
  lcd.print("MakerLab Simon");
  lcd.setCursor(0, 1);
  lcd.print("Presiona SELECT");
  
  while(read_buttons() != btnSELECT) { delay(10); } // Espera el botón
  while(read_buttons() != btnNONE) { delay(10); }   // Espera a que lo suelte
  
  lcd.clear();
  lcd.print("PREPARATE :)");
  delay(1000);
}

void showSequence() {
  lcd.clear();
  lcd.print("Observa...");
  delay(1000);
  
  for (int i = 0; i < level; i++) {
    lcd.clear();
    lcd.setCursor(0, 0);
    printButtonName(sequence[i]);
    
    // El tiempo que el botón se muestra en pantalla
    delay(800); 
    
    lcd.clear();
    // Pausa visual entre botones (clave si se repite el mismo botón 2 veces)
    delay(350); 
  }
}

bool getUserInput() {
  for (int i = 0; i < level; i++) {
    int pressed = btnNONE;
    
    lcd.clear();
    lcd.print("Tu turno: "); lcd.print(i + 1); 
    lcd.print("/"); lcd.print(level); // Estética extra: Ej "Tu turno: 1/3"
    
    // 1. Asegurarnos de que el usuario no esté tocando nada antes de empezar
    while (read_buttons() != btnNONE) { delay(10); }
    
    // 2. Esperar a que presione un botón
    while (pressed == btnNONE) {
      pressed = read_buttons();
      delay(10); // Estabilidad de lectura
    }
    
    // 3. Mostrar lo que presionó en la segunda línea
    lcd.setCursor(0, 1);
    printButtonName(pressed);
    
    // 4. EL SECRETO: Pausa para que el jugador PUEDA VER lo que presionó
    delay(400); 
    
    // 5. Verificar si es correcto
    if (pressed != sequence[i]) {
      delay(600); // Deja el error en pantalla un momento para que sepa en qué falló
      return false; // Retorna falso, lo que dispara el Game Over
    }
    
    // 6. Esperar a que suelte el botón para evitar que un solo toque cuente como dos
    while (read_buttons() != btnNONE) { delay(10); } 
  }
  
  return true; // Superó toda la secuencia
}

void printButtonName(int b) {
  switch (b) {
    case btnRIGHT: lcd.print("DERECHA >"); break;
    case btnUP:    lcd.print("ARRIBA ^"); break;
    case btnDOWN:  lcd.print("ABAJO v"); break;
    case btnLEFT:  lcd.print("< IZQUIERDA"); break;
  }
}

int read_buttons() {
  int adc = analogRead(0);
  if (adc < 50)   return btnRIGHT;
  if (adc < 250)  return btnUP;
  if (adc < 450)  return btnDOWN;
  if (adc < 650)  return btnLEFT;
  if (adc < 850)  return btnSELECT;
  return btnNONE;
}

void gameOver() {
  lcd.clear();
  lcd.print("GAME OVER :(");
  lcd.setCursor(0, 1);
  lcd.print("Nivel: "); lcd.print(level);
  level = 1; // Reiniciar nivel
  delay(3500); // Pausa larga para lamentar la derrota
  showStartMessage();
}