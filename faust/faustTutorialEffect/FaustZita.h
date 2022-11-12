#ifndef faust_FaustZita_h_
#define faust_FaustZita_h_

#include <string>
#include "Arduino.h"
#include "AudioStream.h"
#include "Audio.h"

class dsp;
class MapUI;

class FaustZita : public AudioStream
{
public:
	FaustZita();
	~FaustZita();
	virtual void update(void);
	void setParamValue(const std::string& path, float value);
private:
	float** fInChannel;
	float** fOutChannel;
	MapUI* UI;
	dsp* fDSP;
};

#endif
