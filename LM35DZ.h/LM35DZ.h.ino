
#ifndef LM35DZ_h
#define LM35DZ_h

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

#endif
