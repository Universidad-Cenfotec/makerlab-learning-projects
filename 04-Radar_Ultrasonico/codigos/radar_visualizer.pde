import processing.serial.*;
import processing.sound.*;   // ⭐ Librería para reproducir el sonido de alarma

Serial myPort;          // Objeto para la comunicación USB
SoundFile alarma;       // Objeto para guardar nuestro archivo .wav

String datos="";        // Aquí guardaremos el texto que llega de Arduino

int angulo=0;
int distancia=0;

boolean detectando=false; // ¿Hay un intruso cerca?

void setup(){
  size(1200,700);            // Tamaño de la ventana del radar
  surface.setResizable(true);
  smooth();                  // Suavizado de bordes

  // Imprime en consola todos los puertos disponibles. ¡Útil para debugear!
  println(Serial.list());

  // ⭐ IMPORTANTE: Cambia "COM9" por el puerto que use tu Arduino (ej. COM3)
  myPort = new Serial(this,"COM9",9600);
  myPort.bufferUntil('.');   // Lee hasta encontrar el punto que mandó Arduino

  // ⭐ Cargar sonido (Debe estar en una carpeta llamada "data")
  alarma = new SoundFile(this,"alarm-sfx-sound.wav");
}

void draw(){
  // ⭐ Efecto "memoria de radar" (estela verde que se desvanece)
  noStroke();
  fill(0,35); // Rectángulo negro casi transparente
  rect(0,0,width,height); 

  dibujarRadar();
  dibujarLineaRadar();
  dibujarTexto();
}

// ================= SERIAL (El Traductor) =================
void serialEvent(Serial myPort){
  // Leemos la ráfaga de datos hasta el punto "."
  datos=myPort.readStringUntil('.');

  if(datos==null) return; // Si no hay nada, salimos

  datos=trim(datos); // Limpiamos espacios en blanco

  int coma=datos.indexOf(','); // Buscamos dónde está la coma

  if(coma<0) return; // Si la trama llegó rota, la ignoramos

  // Partimos el texto en dos usando la coma como separador
  int a=int(datos.substring(0,coma)); 
  int d=int(datos.substring(coma+1));

  // Filtro de ruido (si la distancia es irreal, ignoramos)
  if(d<=0 || d>60) return;

  angulo=a;
  distancia=d;

  // ⭐ Lógica de detección: intruso a 10cm o menos
  detectando = distancia <= 10;

  // ⭐ Lógica de sonido alarma
  if(detectando && !alarma.isPlaying()){
    alarma.loop();   // Suena de forma continua
  }

  if(!detectando && alarma.isPlaying()){
    alarma.stop();   // Se calla si el objeto se va
  }
}

// ================= RADAR BASE =================
void dibujarRadar(){
  pushMatrix(); // Guardamos el sistema de coordenadas
  translate(width/2,height*0.9); // Movemos el centro abajo a la mitad

  noFill();
  stroke(0,255,70); // Verde estilo Matrix/Radar
  strokeWeight(2);

  float r=width*0.9;

  // Dibujamos los semicírculos concéntricos
  arc(0,0,r,r,PI,TWO_PI);
  arc(0,0,r*0.75,r*0.75,PI,TWO_PI);
  arc(0,0,r*0.5,r*0.5,PI,TWO_PI);
  arc(0,0,r*0.25,r*0.25,PI,TWO_PI);

  // Dibujamos las líneas guía cada 30 grados
  for(int i=0;i<=180;i+=30){
    line(0,0,
      -r/2*cos(radians(i)),
      -r/2*sin(radians(i)));
  }
  popMatrix(); // Restauramos coordenadas
}

// ================= LINEA RADAR =================
void dibujarLineaRadar(){
  pushMatrix();
  translate(width/2,height*0.9);

  float largo = height*0.8;

  // ⭐ EFECTO ESPEJO (clave para que la pantalla y el motor giren igual)
  float anguloEspejo = 180 - angulo;

  // ⭐ Cambio de color si detecta objeto
  if(detectando){
    stroke(255,0,0); // Rojo peligro
    strokeWeight(5);
  }else{
    stroke(0,255,80); // Verde seguro
    strokeWeight(3);
  }

  // Matemáticas trigonométricas para dibujar la línea en ángulo
  line(
    0,0,
    largo*cos(radians(anguloEspejo)),
    -largo*sin(radians(anguloEspejo))
  );
  popMatrix();
}

// ================= TEXTO =================
void dibujarTexto(){
  // Panel negro en la base para tapar el radar residual
  fill(0);
  noStroke();
  rect(0,height-90,width,90);

  fill(0,255,70);
  textSize(26);

  // Textos de telemetría en vivo
  text("RADAR MAKERLAB",20,height-55);
  text("Ángulo: "+angulo+"°",320,height-55);
  text("Distancia: "+distancia+" cm",620,height-55);

  // Mensaje de estado dinámico
  if(detectando){
    fill(255,0,0);
    text("⚠ OBJETO DETECTADO",920,height-55);
  }else{
    fill(0,255,70);
    text("Escaneando...",920,height-55);
  }
}
