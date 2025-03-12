#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>   // LiquidCrystal

#define DHTPIN 2          // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11     // DHT 11 sensor type
#define MQ135_PIN A2      // MQ-135 متصل بالمخرج A2

DHT dht(DHTPIN, DHTTYPE); // DHT11
LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD (عنوان I2C: 0x27، حجم 16x2)

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  
  Serial.println("SYSTEM TEST");
  dht.begin();

  pinMode(2, INPUT); // DHT11
  pinMode(MQ135_PIN, INPUT); // MQ-135


  lcd.setCursor(0, 0);
  lcd.print("SYSTEM CUALITY AIR");
  lcd.setCursor(0, 1);
  lcd.print("SYSTEM IS ON ");
  delay(2000);
  lcd.clear();


  Serial.println("LABEL,Time,Humidity,Temperature,AirQuality,CO2");  // تسمية الأعمدة
}

void loop() {
  int CO2 = analogRead(A0); // CO2

  int airQuality = analogRead(MQ135_PIN); // قراءة مستشعر MQ-135

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // تنظيف الشاشة قبل الطباعة
  lcd.clear();

  // طباعة القيم على LCD
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C");

  lcd.setCursor(0, 1);
  lcd.print("Hum: ");
  lcd.print(humidity);
  lcd.print(" %");

  delay(3000);
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Air Q: ");
  lcd.print(airQuality);

  lcd.setCursor(0, 1);
  lcd.print("CO2 : ");
  lcd.print(CO2);



    // إرسال البيانات إلى Excel
  Serial.print("DATA,"); 
  Serial.print(millis() / 1000); Serial.print(","); // الوقت بالثواني
  Serial.print(humidity); Serial.print(",");
  Serial.print(temperature); Serial.print(",");
  Serial.print(airQuality); Serial.print(",");
  Serial.println(CO2); 

  delay(3000); // تأخير 2 ثانية قبل تحديث القيم
}