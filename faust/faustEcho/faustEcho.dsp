import("stdfaust.lib");
del = hslider("del",20000,1,30000,1);
feedback = hslider("feedback",0.5,0,1,0.01);
echo = +~de.delay(30000,del)*feedback;
process = par(i,2,echo);