


//enum fsm_states
//{
//  GET_SAMPLES,
//  CALC_VARIANCE,
//  PRINT_VARIANCE,
//};

//struct fsm_sys_t
//{
//  void(*fptr)();
//  fsm_states next[NSTATES];
//};

//static fsm_states current_st = CALC_VARIANCE;

//static fsm_sys_t FSM_SYSTEM[NSTATES]=
//{
//  {LM35DZ_print_temperature_celsius, {CALC_VARIANCE, PRINT_RESULT,   GET_SAMPLES}},
//  {LM35DZ_calc_variance,             {PRINT_RESULT,   GET_SAMPLES, CALC_VARIANCE}},
//  {LM35DZ_print_temperature_celsius, {GET_SAMPLES,  CALC_VARIANCE,  PRINT_RESULT}}
//};
