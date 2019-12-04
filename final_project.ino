/* DIGITAL PORTS */
#define GPIO_PB0 8   /*   ICP1     */
#define GPIO_PB1 9   /*   OC1A     */
#define GPIO_PB2 10  /*   SS/OC1B  */
#define GPIO_PB3 11  /*   MOSI/OC2 */
#define GPIO_PB4 12  /*   MISO     */
#define GPIO_PB5 13  /*   SCK      */

#define LM35DZ_ADC_PIN A2
#define xDelay   100
#define N_SAMPLES 100

float celcius_temp;
float data;
float vout;

void setup()
{
  pinMode(LM35DZ_ADC_PIN, INPUT);
  Serial.begin(9600);
}

void loop()
{
  LM35DZ_print_temperature_celcius();
}

float LM35DZ_get_temperature_celcius(void)
{
  float celcius_temp;
  float data;
  float vout;
  /* read analog data from temperature sensor */
  data = analogRead(LM35DZ_ADC_PIN);
  /* The analog values read from the Arduino may have a value between 0 and 1024, 
   *  in which 0 corresponds to 0V and 1024 to 5V. So, we can easily get the output voltage of the sensor in mV */
  vout = (data*5000)/1024;
  celcius_temp = vout/10; /* 10 mv division*/
  return celcius_temp;
}

void LM35DZ_print_temperature_celcius(void)
{
  float celcius_temp;
  celcius_temp = LM35DZ_get_temperature_celcius();
  Serial.print(LM35DZ_get_temperature_celcius());
  Serial.print(" °C");
  Serial.print("\n");
}
