#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define MQ135_PIN A2

#define RL 10.0
#define R0_CALIBRATED 76.63

// معاملات معايرة معدلة ل CO₂ (لإخراج بالمئات)
#define A 110.23
#define B -2.6

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

float R0 = R0_CALIBRATED;
bool showRanges = false;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  dht.begin();
  
  lcd.clear();
  lcd.print("Calibrating...");
  
  // معايرة R0 مع تحسينات
  float avg = 0;
  for(int i = 0; i < 100; i++) {
    avg += analogRead(MQ135_PIN);
    delay(10);
  }
  avg /= 100;
  float voltage = avg * (5.0 / 1023.0);
  float RS_AIR = ((5.0 - voltage) / voltage) * RL;
  R0 = RS_AIR / 3.6; // قيمة معايرة مثبتة تجريبياً

  lcd.clear();


  Serial.println("LABEL,Time,Humidity,Temperature,CO2");  // تسمية الأعمدة
}

void loop() {
  int sensorValue = analogRead(MQ135_PIN);
  float voltage = sensorValue * (5.0 / 1023.0);
  float RS = ((5.0 - voltage) / voltage) * RL;
  float ratio = RS / R0;
  
  // معادلة معدلة ل CO₂ (تضخيم النتيجة)
  float CO2_ppm = A * pow(ratio, B) * 100; // الضرب في 100 للحصول على قيم بالمئات
  
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  lcd.clear();
  if(showRanges) {
    // عرض النطاقات كاملة مع محاذاة
    lcd.setCursor(0, 0);
    lcd.print("CO2 Ranges:");
    lcd.setCursor(0, 1);
    lcd.print("Out:400-450ppm");
  } else {
    // عرض القراءات مع إشارات المقارنة
    lcd.setCursor(0, 0);
    lcd.print("T:");
    lcd.print(temperature,1);
    lcd.print("C H:");
    lcd.print(humidity,0);
    lcd.print("%");
    
    lcd.setCursor(0, 1);
    lcd.print("CO2:");
    lcd.print(CO2_ppm,0);
    lcd.print("ppm ");
    
    // إضافة مؤشرات المقارنة
    if(CO2_ppm < 400) lcd.print("LOW");
    else if(CO2_ppm > 1000) lcd.print("HIGH!");
    else lcd.print("OK");
  }
  showRanges = !showRanges;

  // إرسال البيانات
  Serial.print("DATA,");
  Serial.print(millis()/1000);Serial.print(",");
  Serial.print(humidity/100);Serial.print(",");
  Serial.print(temperature);Serial.print(",");
  Serial.println(CO2_ppm);

  delay(3000);
}