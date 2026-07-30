#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

byte bird[8] = {0x00, 0x00, 0x0E, 0x1B, 0x1F, 0x18, 0x00, 0x00}; 
byte birdWing[8] = {0x00, 0x06, 0x0E, 0x1B, 0x1F, 0x18, 0x00, 0x00}; 
byte pipe[8] = {0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F};

float birdY = 0.5;
float velocity = 0;
float gravity = 0.2; // Gravedad ajustada
float jump = -0.5;   // Salto ajustado
int pipeX = 15;
int gapY = 0;
int score = 0;
bool playing = true;

void setup() {
  lcd.begin(16, 2);
  lcd.createChar(0, bird);
  lcd.createChar(1, birdWing);
  lcd.createChar(2, pipe);
}

void loop() {
  if (!playing) return;

  int btn = analogRead(0);
  if (btn < 400) velocity = jump; // Salta con UP o RIGHT

  // Física
  velocity += gravity;
  birdY += velocity;

  // FIX: Límites matemáticos estrictos
  if (birdY > 1.0) { birdY = 1.0; velocity = 0; }
  if (birdY < 0.0) { birdY = 0.0; velocity = 0; }

  // Tuberías
  pipeX--;
  if (pipeX < 0) {
    pipeX = 15;
    gapY = random(0, 2);
    score++;
  }

  // FIX: Conversión segura a coordenadas LCD
  int visualY = (birdY >= 0.5) ? 1 : 0;

  // Colisión real (Solo si el pájaro y la tubería comparten columna y fila)
  if (pipeX == 2 && visualY != gapY) {
    playing = false;
    lcd.clear(); lcd.print("CRASH!"); 
    lcd.setCursor(0,1); lcd.print("Score: "); lcd.print(score);
    delay(2000); 
    // Reset variables
    birdY = 0.5; velocity = 0; score = 0; pipeX = 15;
    playing = true;
    return;
  }

  // Dibujo
  lcd.clear();
  lcd.setCursor(2, visualY);
  lcd.write(velocity < 0 ? byte(1) : byte(0)); 

  lcd.setCursor(pipeX, 1 - gapY);
  lcd.write(byte(2)); 
  
  delay(150); // Velocidad del juego
}