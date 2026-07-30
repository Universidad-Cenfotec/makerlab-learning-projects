#include <LiquidCrystal.h>

LiquidCrystal lcd(8,9,4,5,6,7);

// ===== SPRITES =====

// Dino correr 1
byte dino1[8]={
B00110,
B00111,
B00110,
B01110,
B11110,
B00110,
B01010,
B10001
};

// Dino correr 2
byte dino2[8]={
B00110,
B00111,
B00110,
B01110,
B11110,
B00110,
B10001,
B01010
};

// Cactus
byte cactus[8]={
B00100,
B00101,
B10101,
B10101,
B11101,
B00100,
B00100,
B00100
};

int dinoY=1;
bool saltando=false;
unsigned long saltoTiempo;

int cactusX=15;

bool gameOver=false;
int score=0;
int velocidad=200;
bool anim=0;


// ===== BOTONES =====
int leerBoton(){
int v=analogRead(A0);

if(v<50)return 1;
if(v<200)return 2; // UP
if(v<400)return 3;
if(v<600)return 4;
if(v<800)return 5;
return 0;
}


// ===== MENU =====
void menu(){
lcd.clear();
lcd.setCursor(0,0);
lcd.print("DINO GAME :)");
lcd.setCursor(0,1);
lcd.print("UP para jugar");

while(leerBoton()!=2){
delay(50);
}
}


// ===== SETUP =====
void setup(){

lcd.begin(16,2);

lcd.createChar(0,dino1);
lcd.createChar(1,dino2);
lcd.createChar(2,cactus);

menu();
}


// ===== LOOP =====
void loop(){

if(gameOver){

lcd.clear();
lcd.setCursor(3,0);
lcd.print("GAME OVER");

lcd.setCursor(2,1);
lcd.print("Score:");
lcd.print(score);

delay(2500);

score=0;
velocidad=200;
cactusX=15;
gameOver=false;

menu();
}


// ===== SALTO =====
int boton=leerBoton();

if(boton==2 && !saltando){
saltando=true;
dinoY=0;
saltoTiempo=millis();
}

if(saltando && millis()-saltoTiempo>400){
saltando=false;
dinoY=1;
}


// ===== MOVER CACTUS =====
cactusX--;

if(cactusX<0){
cactusX=15;
score++;

if(velocidad>80)
velocidad-=5;
}


// ===== COLISION =====
if(cactusX==0 && dinoY==1){
gameOver=true;
}


// ===== DIBUJO =====
lcd.clear();

lcd.setCursor(0,dinoY);
lcd.write(byte(anim?0:1));

lcd.setCursor(cactusX,1);
lcd.write(byte(2));

lcd.setCursor(11,0);
lcd.print(score);

anim=!anim;

delay(velocidad);
}