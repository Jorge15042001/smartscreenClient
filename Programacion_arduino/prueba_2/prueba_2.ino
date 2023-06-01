

const uint8_t cantidad_grados_libertad = 6; //Cantidad de ejes x, y, z; cantidad angulos Roll, Pitch, Yaw
char nombre_grados_libertad[cantidad_grados_libertad]={'x','y','z','R','P','Y'};
char delimitador1 = ',';
char delimitador2 = ':';
String string_eje[cantidad_grados_libertad];
int posicion_delimitadores[cantidad_grados_libertad-1];
float coordenadas_xyz_RPY[cantidad_grados_libertad]; //[mm] distancia del usuario en x, y, z.
String serial; //Comando recibido por el serial
float altura_pantalla_actual = 0;
String comando = "altura"; 


void enviar_altura(){
  if(serial.compareTo(comando) == 0){
    Serial.println(String(altura_pantalla_actual));
  }
}

void actualizar_coordenadas_xyz_RPY(){
  if(Serial.available() > 0){
    serial = Serial.readString();
    if (serial.compareTo(comando) != 0){
      for (uint8_t i=0; i<cantidad_grados_libertad; i++){
        if(i==0){
          posicion_delimitadores[i] = serial.indexOf(delimitador1);
          string_eje[i] = serial.substring(0,posicion_delimitadores[i]);
        }else if(i==cantidad_grados_libertad){
          string_eje[i] = serial.substring(posicion_delimitadores[i-1]+1);
        }else{
          posicion_delimitadores[i] = serial.indexOf(delimitador1, posicion_delimitadores[i-1]+1);
          string_eje[i] = serial.substring(posicion_delimitadores[i-1]+1, posicion_delimitadores[i]);
        }
        coordenadas_xyz_RPY[i] = string_eje[i].substring(string_eje[i].indexOf(delimitador2)+1).toFloat();
        /*Serial.print("coordenada: ");
        Serial.println(coordenadas_xyz_RPY[i]);*/
      }
    }else{
      //enviar_altura();
    }
  }
}

void setup() {
  Serial.begin(115200);

}

void loop() {
  actualizar_coordenadas_xyz_RPY();

}
