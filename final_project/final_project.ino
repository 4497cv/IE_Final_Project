#
/* DIGITAL PORTS */
#define GPIO_PB0 8   /*   ICP1     */
#define GPIO_PB1 9   /*   OC1A     */
#define GPIO_PB2 10  /*   SS/OC1B  */
#define GPIO_PB3 11  /*   MOSI/OC2 */
#define GPIO_PB4 12  /*   MISO     */
#define GPIO_PB5 13  /*   SCK      */

/* Analog Ports */
#define LM35DZ_ADC_PIN A2
#define DHT11_ADC_PIN  A1
#define MQ2_ADC_PIN    A0

/* Definitions */
#define xDelay   100
#define NSAMPLES 50

#define NSTATES 3
//#define DEBUG 

static float temperature_samples[NSAMPLES];
static unsigned int samples_counter;
static float g_current_temp;

void LM35DZ_print_temperature_celsius(void);
float LM35DZ_get_temperature_celsius(void);
void LM35DZ_calc_variance(void);
void LM35DZ_print_samples(void);

enum fsm_states
{
  GET_SAMPLES,
  CALC_VARIANCE,
  PRINT_VARIANCE,
};

struct fsm_sys_t
{
  void(*fptr)();
  fsm_states next[NSTATES];
};

static fsm_states current_st = CALC_VARIANCE;

//static fsm_sys_t FSM_SYSTEM[NSTATES]=
//{
//  {LM35DZ_print_temperature_celsius, {CALC_VARIANCE, PRINT_RESULT,   GET_SAMPLES}},
//  {LM35DZ_calc_variance,             {PRINT_RESULT,   GET_SAMPLES, CALC_VARIANCE}},
//  {LM35DZ_print_temperature_celsius, {GET_SAMPLES,  CALC_VARIANCE,  PRINT_RESULT}}
//};

void setup()
{
  pinMode(LM35DZ_ADC_PIN, INPUT);

  samples_counter = 0;
  
  Serial.begin(115200);
}

void loop()
{
  //LM35DZ_get_samples();
  LM35DZ_print_temperature_celsius();
}

/*  ---------- LM35DZ functions ------------- */


float LM35DZ_get_temperature_celsius(void)
{
  float celcius_temp;
  float data;
  float vout;
  //delay(500);
  /* read analog data from temperature sensor */
  data = analogRead(LM35DZ_ADC_PIN);
  /* The analog values read from the Arduino may have a value between 0 and 1024, 
   *  in which 0 corresponds to 0V and 1024 to 5V. So, we can easily get the output voltage of the sensor in mV */
  vout = (data*5000)/1024;
  celcius_temp = vout/10; /* 10 mv division*/
  return celcius_temp;
}

void LM35DZ_print_temperature_celsius(void)
{
  float celcius_temp;
  celcius_temp = LM35DZ_get_temperature_celsius();
  Serial.print(LM35DZ_get_temperature_celsius());
  Serial.print(" C");
  Serial.print("\n\r");
}

void  LM35DZ_get_samples(void)
{
  if(NSAMPLES == samples_counter)
  {
    //LM35DZ_print_samples();
    LM35DZ_calc_variance();
    Serial.print(g_current_temp);
    Serial.print(" C");
    Serial.print("\n\r");
    samples_counter = 0;
  }
  else if(NSAMPLES > samples_counter)
  {
    /* CAPTURE TEMPERATURE VALUE */
    temperature_samples[samples_counter] = LM35DZ_get_temperature_celsius();
    samples_counter++;
  }
  else
  {
    samples_counter = 0;
  }
}

void LM35DZ_print_samples(void)
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

void LM35DZ_calc_std_(void)
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

#ifdef DEBUG
  Serial.print("the total variance is: ");
  Serial.print(variance);
  Serial.print("| Number of samples: ");
  Serial.print(NSAMPLES);
  Serial.print("\n\r");
#endif

  if(std_dev < 0.8)
  {
     g_current_temp = total_average;
  }
}
