#include <math.h>
#include "ets_sys.h"
#include "osapi.h"
#include "gpio.h"
#include "pwm.h"
#include "os_type.h"

/*
 * This currently uses pulse width modulation to fade the on board LED
 * todo: modify this to output different frequencies to KY-006 passive buzzer module
 */

// LED on GPIO2. Change to another GPIO
// for other boards.
//static const int pin = 2;
static os_timer_t ledTimer;
bool ascending = true;
static const uint32_t frequency = 5000; // in hz, so 5kHz
uint32_t maxDuty = 0;
uint8_t ledDutyPercent = 10;
uint8_t *pLedDutyPercent = &ledDutyPercent;
uint32_t ledDuty = 0;
uint32_t *pLedDuty = &ledDuty;

/**
 * PWM control function
 */
void ICACHE_FLASH_ATTR ledTimer_f(void *args) {
  if(*pLedDutyPercent == 100) {
    ascending = false;
  } else if (*pLedDutyPercent == 0) {
    ascending = true;
  }
  if(ascending == true) {
    (*pLedDutyPercent)++;
  } else if(ascending == false) {
    (*pLedDutyPercent)--;
  }
  *pLedDuty = (uint32_t)((*pLedDutyPercent/100.0) * (float)maxDuty);
  pwm_set_duty(*pLedDuty, 0);
  pwm_start();
}

/**
 * entry point
 */
void ICACHE_FLASH_ATTR user_init() {
  // init gpio subsytem
  gpio_init();
  maxDuty = (frequency * 1000)/45;
  uint32_t pwmInfo[1][3] = {{PERIPHS_IO_MUX_GPIO2_U,FUNC_GPIO2,2}};
  *pLedDuty = (uint32_t)((float)(ledDutyPercent/100.0) * (float)maxDuty);
  pwm_init(frequency, pLedDuty, 1, pwmInfo);

  // setup timer (20ms, repeating)
  os_timer_setfn(&ledTimer, (os_timer_func_t *)ledTimer_f, NULL);
  os_timer_arm(&ledTimer, 20, 1);
}
