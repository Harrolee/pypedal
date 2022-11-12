#include <Audio.h>
#include "faustEcho.h"

faustEcho faustEcho;
AudioInputI2S in;
AudioOutputI2S out;
AudioControlSGTL5000 audioShield;
AudioConnection patchCord0(in,0,faustEcho,0);
AudioConnection patchCord1(in,1,faustEcho,1);
AudioConnection patchCord2(faustEcho,0,out,0);
AudioConnection patchCord3(faustEcho,1,out,1);

void setup() {
  AudioMemory(6);
  audioShield.enable();
  faustEcho.setParamValue("del",22000);
  faustEcho.setParamValue("feedback",0.6);
}

void loop() {
}