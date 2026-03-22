// utilities/i2c.h
#pragma once
#include <Arduino.h>

bool    i2c_init();
uint8_t i2c_read(uint8_t addr, uint8_t reg);
bool    i2c_write(uint8_t addr, uint8_t reg, uint8_t val);
bool    i2c_read_multi(uint8_t addr, uint8_t reg, uint8_t* buf, uint8_t len);
void    i2c_identify_devices();