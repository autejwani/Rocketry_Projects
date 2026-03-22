//
// Created by aditya on 1/31/26.
//

#include "Song.h"

BuzzerNotes::BuzzerNotes(uint8_t pin) {
	_pin = pin;
	pinMode(_pin, OUTPUT);
}

void BuzzerNotes::playTone(int frequency, int duration_ms) {
	tone(_pin, frequency, duration_ms);
	delay(duration_ms * 1.2);
}

void BuzzerNotes::noTone() {
	::noTone(_pin);
}

void BuzzerNotes::playTune() {
	// Super Mario Bros. intro
	playTone(NOTE_E5, 125);
	playTone(NOTE_E5, 125);
	playTone(0, 125);
	playTone(NOTE_E5, 125);
	playTone(0, 125);
	playTone(NOTE_C5, 125);
	playTone(NOTE_E5, 125);
	playTone(0, 125);
	playTone(NOTE_G5, 375);

	playTone(0, 375);

	playTone(NOTE_G4, 375);
	playTone(0, 375);

	// Next part
	playTone(NOTE_C5, 125);
	playTone(NOTE_G4, 125);
	playTone(0, 125);
	playTone(NOTE_E4, 125);
	playTone(0, 125);
	playTone(NOTE_A4, 125);
	playTone(NOTE_B4, 125);
	playTone(0, 125);
	playTone(NOTE_A4, 125);
	playTone(NOTE_A4, 125);
	playTone(0, 125);
	playTone(NOTE_G4, 87);
	playTone(NOTE_E5, 125);
	playTone(NOTE_G5, 125);
	playTone(NOTE_A5, 125);
	playTone(0, 125);
	playTone(NOTE_F5, 125);
	playTone(NOTE_G5, 125);

	playTone(NOTE_E5, 125);
	playTone(0, 125);
	playTone(NOTE_C5, 125);
	playTone(NOTE_D5, 125);
	playTone(NOTE_B4, 125);
}
