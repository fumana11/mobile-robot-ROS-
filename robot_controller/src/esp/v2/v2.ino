#include <WiFi.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/UInt16.h>

//const char* ssid = "Guest.UM";
//const char* password = "internetum";
//IPAddress server(10, 60, 201, 5);

const char* ssid = "ROBOTICLAB";
const char* password = "duasatusatu";
IPAddress server(192, 168, 0, 30);   // Set the rosserial socket server IP address

const uint16_t serverPort = 11411;    // Set the rosserial socket server port
int status = WL_IDLE_STATUS;

#define motorKiriA    21  // 16 corresponds to GPIO16
#define motorKiriB    22  // 16 corresponds to GPIO16
#define motorKananA   17  // 16 corresponds to GPIO16
#define motorKananB   16  // 16 corresponds to GPIO16

//Inisialisasi PWM32
const int freq = 5000;
const int ledChannelA = 0;
const int ledChannelB = 1;
const int resolution = 8;

int speedM = 255;

std_msgs::String str_msg;
std_msgs::UInt16 int_msg;

ros::NodeHandle nh;

ros::Publisher robotMove("/robotMove", &str_msg);

void controllerCallback(const std_msgs::String& msg) {

  //Serial.println(msg.data);

  char data = msg.data[0];
  Serial.println(data);

  if (data == 'w') {
    Forward(speedM);
    str_msg.data = "Maju";
    robotMove.publish( &str_msg );
  }

  else if (data == 's') {
    Reverse(speedM);
    str_msg.data = "Mundur";
    robotMove.publish( &str_msg );
  }
  else if (data == 'd') {
    Right(speedM);
    str_msg.data = "Belok Kanan";
    robotMove.publish( &str_msg );
  }
  else if (data == 'a') {
    Left(speedM);
    str_msg.data = "Belok Kiri";
    robotMove.publish( &str_msg );
  }
  else if (data == '3') {
    rotateRight(speedM);
    str_msg.data = "Rotasi Kanan";
    robotMove.publish( &str_msg );
  }
  else if (data == '1') {
    rotateLeft(speedM);
    str_msg.data = "Rotasi Kiri";
    robotMove.publish( &str_msg );
  }
  else if (data == '2') {
    stuck();
    str_msg.data = "Berhenti";
    robotMove.publish( &str_msg );
  }

}

ros::Publisher sensorDepan("/sensorDepan", &int_msg);
ros::Publisher sensorBelakang("/sensorBelakang", &int_msg);

ros::Subscriber<std_msgs::String> sub("/controllerPub", &controllerCallback);

void setup() {
  //WIFI SETUP
  Serial.begin(115200);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //SETUP ESP32 PINOUT
  ledcSetup(ledChannelA, freq, resolution);
  ledcSetup(ledChannelB, freq, resolution);
  
  ledcAttachPin(motorKiriA, ledChannelA);
  ledcAttachPin(motorKananA, ledChannelB);
  
  pinMode(motorKiriB, OUTPUT);
  pinMode(motorKananB, OUTPUT);
  pinMode(39, INPUT);
  pinMode(35, INPUT);

  //ROS SETUP
  delay(2000);

  nh.getHardware()->setConnection(server, serverPort);
  nh.initNode();
  nh.advertise(robotMove);
  nh.advertise(sensorDepan);
  nh.advertise(sensorBelakang);
  nh.subscribe(sub);

}

void loop() {
  int senDepan = analogRead(35);
  int_msg.data = senDepan;
  sensorDepan.publish(&int_msg);

  int senBelakang = analogRead(39);
  int_msg.data = senBelakang;
  sensorBelakang.publish(&int_msg);

  nh.spinOnce();
  delay(500);
}


void analogWrite(int pin, int dc) {
  ledcWrite(pin, dc);
}

void Forward(int speedM) {
  ledcWrite(ledChannelA, speedM); digitalWrite(motorKiriB, LOW);
  ledcWrite(ledChannelB, speedM); digitalWrite(motorKananB, LOW);

  Serial.println("Robot Forward");
}

void Reverse(int speedM) {
  ledcWrite(ledChannelA, 255 - speedM); digitalWrite(motorKiriB, HIGH);
  ledcWrite(ledChannelB, 255 - speedM); digitalWrite(motorKananB, HIGH);

  Serial.println("Robot Reverse");
}

void Right(int speedM) {
  ledcWrite(ledChannelA, 255 - 100); digitalWrite(motorKiriB, HIGH);
  ledcWrite(ledChannelB, speedM); digitalWrite(motorKananB, LOW);

  Serial.println("Robot Right");
}

void Left(int speedM) {
  ledcWrite(ledChannelA, speedM); digitalWrite(motorKiriB, LOW);
  ledcWrite(ledChannelB, 255 - 100); digitalWrite(motorKananB, HIGH);

  Serial.println("Robot Left");
}

void rotateRight(int speedM) {
  ledcWrite(ledChannelA, speedM); digitalWrite(motorKiriB, HIGH);
  ledcWrite(ledChannelB, speedM); digitalWrite(motorKananB, LOW);

  Serial.println("Robot Rotate Right");
}

void rotateLeft(int speedM) {
  ledcWrite(ledChannelA, speedM); digitalWrite(motorKiriB, LOW);
  ledcWrite(ledChannelB, speedM); digitalWrite(motorKananB, HIGH);

  Serial.println("Robot Rotate Left");
}

void stuck() {
  ledcWrite(ledChannelB, 0); digitalWrite(motorKananB, LOW);
  ledcWrite(ledChannelA, 0); digitalWrite(motorKiriB, LOW);

  Serial.println("Robot Stop");
}
