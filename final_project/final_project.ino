#include <Arduino_FreeRTOS.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <semphr.h>

/*
    \file:   final_project.ino
    \brief:   
    \author: César Villarreal @4497cv
    \date:   05/12/2019
*/

/* Digital Ports */
#define MQ2_IO_PIN      10        /*     SS/OC1B      */
#define DHT11_IO_PIN    9
/* Analog Ports */
#define LM35DZ_ADC_PIN  A2
#define MQ2_ADC_PIN     A0

#define SERIAL_BAUDRATE 115200

#define REQ_TEMP        '1'
#define REQ_HUM         '2'
#define REQ_GAS         '3'

/* Definitions */
#define xDelay          100
#define NSAMPLES        20

#define NSTATES         3
//#define DEBUG 

static float temperature_samples[NSAMPLES];
static unsigned int samples_counter;
static float g_current_temp;

/* ~~~~~~~~~~ function declarations ~~~~~~~~~~  */
static float LM35DZ_get_temperature_celsius(void);
static void LM35DZ_print_temperature_celsius(void);
static void LM35DZ_get_samples(void);
static void LM35DZ_print_samples(void);
static void LM35DZ_calculate_standard_deviation(void);

/* ~~~~~~~~~~ system tasks ~~~~~~~~~~  */
void LM35DZ_task(void *pvParameters);
void DHT11_task(void *pvParameters);
void MQ2_task(void *pvParameters);
void serial_task(void *pvParameters);

SemaphoreHandle_t xSerialSemaphore; //mutex for serial communication
SemaphoreHandle_t xLM35DZSemaphore;   //semaphore for temperature reading
SemaphoreHandle_t xDHT11Semaphore;
SemaphoreHandle_t xMQ2Semaphore;

static DHT dht(DHT11_IO_PIN, DHT11);

/* ~~~~~~~~~~ system setup (config) ~~~~~~~~~~  */
void setup()
{
  /* configure adc pin for the temperature sensor */
  pinMode(LM35DZ_ADC_PIN, INPUT);
  /* configure adc pin for the gas sensor */
  pinMode(MQ2_ADC_PIN, INPUT);
  
  /* start serial communication (uart) @ 115200 baud/s */
  Serial.begin(SERIAL_BAUDRATE);

  samples_counter = 0;

  /* create mutex semaphore for serial communication */
  xSerialSemaphore = xSemaphoreCreateMutex();
  /* create binary semaphore for tempeature reading */
  xLM35DZSemaphore = xSemaphoreCreateBinary(); 
  /* create binary semaphore for humidity reading */
  xDHT11Semaphore = xSemaphoreCreateBinary(); 
  /* create binary semaphore for gas reading */
  xMQ2Semaphore = xSemaphoreCreateBinary(); 

  /* create tasks fcr serial communication, temperature, humidity, and gas */
  xTaskCreate(LM35DZ_task, "LM35DZ_task", 128, NULL, 2, NULL);
  xTaskCreate(DHT11_task,  "DHT11_task",  128, NULL, 2, NULL);
  xTaskCreate(MQ2_task,    "MQ2_task",    128, NULL, 2, NULL);
  xTaskCreate(serial_task, "serial_task", 128, NULL, 2, NULL);
}

/* ~~~~~~~~~~ infinite loop ~~~~~~~~~~  */
void loop()
{
}

void serial_task(void *pvParameters)
{
  char data;

  for(;;)
  {
    /* verify is serial port is available */
    if(Serial.available() > 0)
    {
      /* ensure atomicity while reading from the serial port */
      xSemaphoreTake(xSerialSemaphore, ( TickType_t ) 5);
      /* read data from serial port */
      data = Serial.read();
      /* release mutex */
      xSemaphoreGive(xSerialSemaphore);
  
      if(REQ_TEMP == data)
      {
         /* read data from serial port */
         xSemaphoreTake(xSerialSemaphore, ( TickType_t ) 5);
         Serial.write("REQ_TEMP_ACK");
         xSemaphoreGive(xSerialSemaphore);
         /* read temperature */
         xSemaphoreGive(xLM35DZSemaphore);
      }
      else if(REQ_HUM == data)
      {
         xSemaphoreTake(xSerialSemaphore, ( TickType_t ) 5);
         Serial.write("REQ_HUM_ACK");
         xSemaphoreGive(xSerialSemaphore);
         /* read temperature */
         xSemaphoreGive(xDHT11Semaphore);
      }
      else if(REQ_GAS == data)
      {
         xSemaphoreTake(xSerialSemaphore, ( TickType_t ) 5);
         Serial.write("REQ_GAS_ACK");
         xSemaphoreGive(xSerialSemaphore);
         /* read temperature */
         xSemaphoreGive(xMQ2Semaphore);
      }
      else if("exit" == data)
      {
        
      }
     }
  }
  
  delay(200); 
}

void LM35DZ_task(void *pvParameters)
{
   for(;;)
   {
    /* wait until the temperature semaphore is released */
    xSemaphoreTake(xLM35DZSemaphore, portMAX_DELAY);
    LM35DZ_get_samples();
    /* send data to GUI*/
    xSemaphoreTake(xSerialSemaphore, ( TickType_t ) 5);
    Serial.print(g_current_temp);
    xSemaphoreGive(xSerialSemaphore);
   }
}

void DHT11_task(void *pvParameters)
{
  float humidity;
   
   for(;;)
   {
    /* wait until the humidity semaphore is released */
    xSemaphoreTake(xDHT11Semaphore, portMAX_DELAY);
    
    xSemaphoreTake(xSerialSemaphore, ( TickType_t ) 5);
    humidity = dht.readHumidity(DHT11_IO_PIN);
    Serial.print(humidity);
    Serial.print("\n\r");
    xSemaphoreGive(xSerialSemaphore);
   }
}

void MQ2_task(void *pvParameters)
{

  for(;;)
  {
    /* wait until the humidity semaphore is released */
    xSemaphoreTake(xMQ2Semaphore, portMAX_DELAY);
//
//    xSemaphoreTake(xSerialSemaphore, ( TickType_t ) 5);
//
//
//    xSemaphoreGive(xSerialSemaphore);
  }  
}

/* ~~~~~~~~~~ LM35DZ functions ~~~~~~~~~~  */

/*  
    \brief      This function returns the actual temperature value in celsius
    \param[in]  void
    \param[out] float
*/  
static float LM35DZ_get_temperature_celsius(void)
{
  volatile float data;
  float celcius_temp;
  float v_out;
  //delay(500);
  /* read analog data from temperature sensor */
  data = analogRead(LM35DZ_ADC_PIN);
  /* The analog values read from the Arduino may have a value between 0 and 1024, 
   *  in which 0 corresponds to 0V and 1024 to 5V. So, we can easily get the output voltage of the sensor in mV */
  v_out = (data*5000)/1024;
  celcius_temp = v_out/10; /* 10 mv division*/
  return celcius_temp;
}

/*  
    \brief      This function prints the actual temperature value in celsius
    \param[in]  void
    \param[out] float
*/  
static void LM35DZ_print_temperature_celsius(void)
{
  float celcius_temp;
  celcius_temp = LM35DZ_get_temperature_celsius();
  Serial.print(LM35DZ_get_temperature_celsius());
  Serial.print(" C");
  Serial.print("\n\r");
}

/*  
    \brief    
    \param[in]  void
    \param[out] void
*/  
static void LM35DZ_get_samples(void)
{
  int s_count;
  int s_flag = 0;
  
  s_count = 0;
  
  do
  {
    if(NSAMPLES == s_count)
    {
      //LM35DZ_print_samples();
      LM35DZ_calculate_standard_deviation();
      s_flag = 1;
    }
    else if(NSAMPLES > s_count)
    {
      /* CAPTURE TEMPERATURE VALUE */
      temperature_samples[s_count] = LM35DZ_get_temperature_celsius();
      s_count++;
    }
  }while(s_flag == 0);
}

/*  
    \brief      This function prints the samples array
    \param[in]  void
    \param[out] void
*/  
static void LM35DZ_print_samples(void)
{
  uint8_t i;
  for(i=0; i < NSAMPLES; i++)
  {
    Serial.print("i = ");
    Serial.print(i);
    Serial.print(" | ");
    Serial.print(temperature_samples[i]);
    Serial.print("\n\r");
  }
}

static void DHT11_read_values()
{
 //  float humidity;
//  
//  humidity = dht.readHumidity(GPIO_PB1);
//  Serial.print("Humidity = ");
//  Serial.print(humidity);
//  Serial.print(" RH \r\n"); 
}

/*  
    \brief      This function calculates the standard deviation for the
                temperature and updates the current global temp. value
    \param[in]  void
    \param[out] void
*/  
static void LM35DZ_calculate_standard_deviation(void)
{
  float total_average;
  float sigma_sqrrt_val_av;
  float std_dev;
  uint8_t i;

  total_average = 0;
  sigma_sqrrt_val_av = 0;
  
  for(i=0; i < NSAMPLES; i++) total_average += temperature_samples[i];

  total_average = total_average/NSAMPLES;

  for(i=0; i < NSAMPLES; i++) sigma_sqrrt_val_av += sqrt(abs((temperature_samples[i] - total_average)));
  
  std_dev = sqrt(sigma_sqrrt_val_av/(NSAMPLES-1));
  
  if(std_dev < 1)
  {
     g_current_temp = total_average;
  }
}


/*  MQ2 Functions */
static void MQ2_warmup_sensor(void)
{
  Serial.print("Warming up....\r\n");
  delay(20000); 
}

static void MQ2_read_RO(void)
{
  float sensorValue = 0;
  const float RL = 1.0;
  const float CLEAN_AIR_RATIO = 9.80;
  float RS;
  float RO;
  float sensor_volt;
  float RS_air;

  for(int i=0; i < 100; i++)
  {
    sensorValue += analogRead(MQ2_ADC_PIN);
  }

  sensorValue = sensorValue/100.0;

  sensor_volt = (sensorValue/1024)*5.0;
  
  RS_air = (5.0 - sensor_volt)/sensor_volt;
  RO = RS_air/9.8;
  
  Serial.print("sensor_volt: ");
  Serial.print(sensor_volt);
  Serial.print("V \n");
  Serial.print("Ro: ");
  Serial.print(RO);
  Serial.print(" \n\r");

  delay(2000);
}

static void MQ2_read_sensor(void)
{
  float sensorValue = 0;
  const float RL = 1.0;
  const float CLEAN_AIR_RATIO = 9.80;
  float RS;
  float RO;
  float sensor_volt;
  float RS_gas;
  float ratio;

  for(int i=0; i < 100; i++)
  {
    sensorValue += analogRead(MQ2_ADC_PIN);
  }

  sensorValue = sensorValue/100.0;

  sensor_volt = (sensorValue/1024)*5.0;
  
  RS_gas = (5.0 - sensor_volt)/sensor_volt;
  ratio= RS_gas/0.44;
  
  Serial.print("sensor_volt: ");
  Serial.print(sensor_volt);
  Serial.print("V \n\r");
  
  Serial.print("rs_ratio = ");
  Serial.print(RS_gas);
  Serial.print(" \n\r");
  Serial.print("Rs/R0 = ");
  Serial.print(ratio);
  Serial.print(" \n\r");

  delay(2000);
}
