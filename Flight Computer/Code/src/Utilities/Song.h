//
// Created by aditya on 1/31/26.
//

#ifndef SONG_H
#define SONG_H

#include <Arduino.h>

class BuzzerNotes
{
	public:
		BuzzerNotes(uint8_t pin);

		void playTone(int frequency, int duration_ms);
		void noTone();

		void playTune();

		// Common notes with octave labels
		static const int NOTE_C4  = 262;   // C, 4th octave
		static const int NOTE_D4  = 294;   // D, 4th octave
		static const int NOTE_E4  = 330;   // E, 4th octave
		static const int NOTE_F4  = 349;   // F, 4th octave
		static const int NOTE_G4  = 392;   // G, 4th octave
		static const int NOTE_A4  = 440;   // A, 4th octave
		static const int NOTE_B4  = 494;   // B, 4th octave

		static const int NOTE_C5  = 523;   // C, 5th octave
		static const int NOTE_D5  = 587;   // D, 5th octave
		static const int NOTE_E5  = 659;   // E, 5th octave
		static const int NOTE_F5  = 698;   // F, 5th octave
		static const int NOTE_G5  = 784;   // G, 5th octave
		static const int NOTE_A5  = 880;   // A, 5th octave
		static const int NOTE_B5  = 988;   // B, 5th octave

		static const int NOTE_C6  = 1047;  // C, 6th octave

	private:
		uint8_t _pin;
};

#endif
