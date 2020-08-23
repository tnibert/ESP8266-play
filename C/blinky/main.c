#include "ets_sys.h"
#include "osapi.h"
#include "gpio.h"
#include "os_type.h"

/*
 *  https://hackaday.io/project/160006/instructions section 7
 *  Define the LED as being on GPIO2 - internal LED for Wemos D1 Mini
 *  You will need to change this if your LED is on another pin.
 *  Almost all ESP8266 modules have an LED on BIT2. Check the datasheet for your module!
 */
#define LED BIT2

static os_timer_t ledTimer;

void ICACHE_FLASH_ATTR ledTimer_cb(void *arg) {
  static int ledStatus = 0;
  if (!ledStatus) {
    gpio_output_set(LED, 0, LED, 0);
    ledStatus = 1;
  } else {
    gpio_output_set(0, LED, LED, 0);
    ledStatus = 0;
  }
}

void ICACHE_FLASH_ATTR sdk_init_done_cb(void) {
  os_timer_setfn(&ledTimer, (os_timer_func_t *)ledTimer_cb, NULL);
  os_timer_arm(&ledTimer, 500 , 1);
}

void ICACHE_FLASH_ATTR user_init() {
  gpio_init();
  system_init_done_cb(sdk_init_done_cb);
}
