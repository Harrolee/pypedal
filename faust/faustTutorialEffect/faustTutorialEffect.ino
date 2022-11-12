#include <Audio.h>
#include "FaustZita.h"
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>

FaustZita faustZita;
AudioInputI2S in;
AudioOutputI2S out;
AudioControlSGTL5000 audioShield;

AudioConnection patchCord0(in, 1, faustZita, 1);
AudioConnection patchCord1(faustZita,1,out,1);

const int myInput = AUDIO_INPUT_LINEIN;

void setup() {
  AudioMemory(15);
  
  audioShield.enable();
  audioShield.inputSelect(myInput);
  audioShield.volume(0.5);
  
  faustZita.setParamValue("level",50);
}

elapsedMillis volmsec=0;

void loop() {
  //float dw = analogRead(A0)/512 - 1;
  faustZita.setParamValue("dryWet",3);
  delay(10);

  if (volmsec > 50) {
    float vol = analogRead(15);
    vol = vol / 1023.0;
    volmsec = 0;
  }
}
