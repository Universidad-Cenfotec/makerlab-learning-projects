#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

byte snakeBody[8] = {0x0E, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0E}; 
byte foodIcon[8]  = {0x04, 0x0A, 0x04, 0x00, 0x0E, 0x1F, 0x1F, 0x0E}; 

int snakeX[32], snakeY[32], length, dir, fX, fY;
int lastHDir = 0; // Guarda la última dirección horizontal
bool running = false;
unsigned long prevMillis = 0;
int speed = 350;

void setup() {
  lcd.begin(16, 2);
  lcd.createChar(0, snakeBody);
  lcd.createChar(1, foodIcon);
  showIntro("SNAKE MAKER");
}

void showIntro(String title) {
  lcd.clear();
  lcd.setCursor(2, 0); lcd.print(">> " + title + " <<");
  lcd.setCursor(0, 1); lcd.print("Press SELECT...");
  while(analogRead(0) > 800); 
  delay(300); // Anti-rebote
  initGame();
}

void initGame() {
  length = 3; 
  dir = 0;      // Inicia moviéndose a la derecha
  lastHDir = 0; // Memoria de movimiento horizontal
  for(int i=0; i<length; i++) { snakeX[i] = 5-i; snakeY[i] = 0; }
  spawnFood();
  running = true;
  speed = 350;
}

void spawnFood() {
  fX = random(0, 16); fY = random(0, 2);
}

void loop() {
  if(!running) return;

  int btn = analogRead(0);
  
  // Guardamos siempre hacia dónde íbamos horizontalmente
  if (dir == 0 || dir == 3) lastHDir = dir;

  // Lógica de botones
  if (btn < 60) { if (lastHDir != 3) dir = 0; }       // RIGHT
  else if (btn < 200) { dir = 1; }                    // UP
  else if (btn < 400) { dir = 2; }                    // DOWN
  else if (btn < 600) { if (lastHDir != 0) dir = 3; } // LEFT

  if(millis() - prevMillis > speed) {
    prevMillis = millis();
    
    int nextX = snakeX[0];
    int nextY = snakeY[0];

    // Lógica de Movimiento en Escalera
    if (dir == 0) nextX++;
    else if (dir == 3) nextX--;
    else if (dir == 1) { 
      nextY--; 
      dir = lastHDir; // Tras cambiar de carril, sigue hacia adelante
    } 
    else if (dir == 2) { 
      nextY++; 
      dir = lastHDir; // Tras cambiar de carril, sigue hacia adelante
    }

    // Teleport en bordes
    if(nextX > 15) nextX = 0; else if(nextX < 0) nextX = 15;
    if(nextY > 1) nextY = 0; else if(nextY < 0) nextY = 1;

    // Colisión mejorada
    for(int i=0; i<length-1; i++) {
      if(nextX == snakeX[i] && nextY == snakeY[i]) {
        gameOver(); return;
      }
    }

    // Comer
    if(nextX == fX && nextY == fY) {
      length++;
      speed = max(100, speed - 15);
      spawnFood();
    }

    // Desplazar cuerpo
    for(int i = length-1; i > 0; i--) {
      snakeX[i] = snakeX[i-1];
      snakeY[i] = snakeY[i-1];
    }
    snakeX[0] = nextX; snakeY[0] = nextY;

    draw();
  }
}

void draw() {
  lcd.clear();
  lcd.setCursor(fX, fY); lcd.write(byte(1)); 
  for(int i=0; i<length; i++) {
    lcd.setCursor(snakeX[i], snakeY[i]);
    lcd.write(byte(0)); 
  }
}

void gameOver() {
  running = false;
  lcd.clear();
  lcd.print("GAME OVER!");
  lcd.setCursor(0,1);
  lcd.print("Score: "); lcd.print(length-3);
  delay(2000);
  showIntro("REINTENTAR?");
}