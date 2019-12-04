/* DIGITAL PORTS */
#define GPIO_PB0 8   /*   ICP1     */
#define GPIO_PB1 9   /*   OC1A     */
#define GPIO_PB2 10  /*   SS/OC1B  */
#define GPIO_PB3 11  /*   MOSI/OC2 */
#define GPIO_PB4 12  /*   MISO     */
#define GPIO_PB5 13  /*   SCK      */

/* Analog Ports */
#define LM35DZ_ADC_PIN A2

/* Definitions */
#define xDelay   100
#define N_SAMPLES 100

#define NSTATES 3

enum fsm_states
{
  GET_SAMPLES,
  CALC_VARIANCE,
  PRINT_RESULT
};

struct fsm_sys_t
{
  void(*fptr)();
  fsm_states next[NSTATES];
};

float celcius_temp;
float data;
float vout;
static fsm_states current_st = CALC_VARIANCE;

void LM35DZ_print_temperature_celsius(void);
float LM35DZ_get_temperature_celsius(void);
void LM35DZ_calc_variance(void);

static fsm_sys_t FSM_SYSTEM[NSTATES]=
{
  {LM35DZ_print_temperature_celsius, {CALC_VARIANCE, PRINT_RESULT,   GET_SAMPLES}},
  {LM35DZ_calc_variance,             {PRINT_RESULT,   GET_SAMPLES, CALC_VARIANCE}},
  {LM35DZ_print_temperature_celsius, {GET_SAMPLES,  CALC_VARIANCE,  PRINT_RESULT}}
};


void setup()
{
  pinMode(LM35DZ_ADC_PIN, INPUT);
  Serial.begin(9600);
}

void loop()
{
    FSM_SYSTEM[current_st].fptr();
    current_st = FSM_SYSTEM[current_st].next[0];
      //LM35DZ_print_temperature_celcius();
}

float LM35DZ_get_temperature_celsius(void)
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

void LM35DZ_print_temperature_celsius(void)
{
  float celcius_temp;
  celcius_temp = LM35DZ_get_temperature_celsius();
  Serial.print(LM35DZ_get_temperature_celsius());
  Serial.print(" °C");
  Serial.print("\n");
}

void LM35DZ_calc_variance(void)
{
  
}
