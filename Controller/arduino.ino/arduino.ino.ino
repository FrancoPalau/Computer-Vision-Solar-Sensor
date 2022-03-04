#include <ros.h>


/*
  Stepper Motor Example
  Fersar Corporation 2021
  OpenCR + Pololu Driver + Bipolar Stepper Motor
*/

#include <std_msgs/Float32.h>
#include <anglesarray/discreteAnglesSetpoints.h>


//Timers

HardwareTimer Timer1(TIMER_CH1);
//
//HardwareTimer Timer2(TIMER_CH2);
//
//HardwareTimer Timer3(TIMER_CH3);

int cont1 = 0;
int cont2 = 0;
int cont3 = 0;

// Constants

// Number of steps per motor revolution -- Step: 1.8 degrees
int DivisonStep = 1;
const float STEPS_PER_REV = 200;
const float GRADES_PER_STEP = 1.8;

// Numbers of steps requiered
int RequiredSteps1;
int RequiredSteps2;
int RequiredSteps3;

float PulseTime1 = 100.0;
float PulseTime2 = 100.0;
float PulseTime3 = 100.0;


float SetPoints1;
float SetPoints2;
float SetPoints3;

float Position1 = 0.0;
float Position2 = 0.0;
float Position3 = 0.0;

float lastPos1 = 0.0;
float lastPos2 = 0.0;
float lastPos3 = 0.0;

float reduccion[1];

// Pin out declaration 1st GDL
const int dirPin1 = 2;
const int stepPin1 = 3;

const int microPinM3 = 4;
const int microPinM2 = 5;
const int microPinM1 = 6;


// Pin out declaration 2st GDL
const int dirPin2 = 7;
const int stepPin2 = 9;


// Pin out declaration 3st GDL
const int dirPin3 = 10;
const int stepPin3 = 11;

ros::NodeHandle  nh;


void messageCb1(const fersar_config :: discreteAnglesSetpoints& gdl1_msg) {
  SetPoints1 = gdl1_msg.angle1 - Position1;
  SetPoints2 = gdl1_msg.angle2 - Position2;
  SetPoints3 = gdl1_msg.angle3 - Position3;

  RequiredSteps1 = getNumSteps(SetPoints1);
  RequiredSteps2 = getNumSteps(SetPoints2);
  RequiredSteps3 = getNumSteps(SetPoints3);

  PulseTime1 = ((0.1 / RequiredSteps1) / 2.0) * (1e6);
  PulseTime2 = ((0.1 / RequiredSteps2) / 2.0) * (1e6);
  PulseTime3 = ((0.1 / RequiredSteps3) / 2.0) * (1e6);

  Timer1.setPeriod(PulseTime1);
  Timer2.setPeriod(PulseTime2);
  Timer3.setPeriod(PulseTime3);

  if (SetPoints1 != 0) {
    Timer1.start();
  }
  if (SetPoints2 != 0) {
    Timer2.start();
  }
  if (SetPoints3 != 0) {
    Timer3.start();
  }

  lastPos1 = gdl1_msg.angle1;
  lastPos2 = gdl1_msg.angle2;
  lastPos3 = gdl1_msg.angle3;

}


ros::Subscriber<fersar_config::discreteAnglesSetpoints> sub1("array_angles_gdl", messageCb1 );




void setup() {
  //    GDL1
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  //    GDL2
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  //    GDL3
  pinMode(stepPin3, OUTPUT);
  pinMode(dirPin3, OUTPUT);

  pinMode(microPinM1, OUTPUT);
  pinMode(microPinM2, OUTPUT);
  pinMode(microPinM3, OUTPUT);

  digitalWrite(microPinM1, HIGH);
  DivisonStep = 16;
  digitalWrite(microPinM2, HIGH);
  digitalWrite(microPinM3, HIGH);

  Timer1.stop();
  Timer2.stop();
  Timer3.stop();


  Timer1.attachInterrupt(handler_led1);
  Timer2.attachInterrupt(handler_led2);
  Timer3.attachInterrupt(handler_led3);


  nh.initNode();
  nh.subscribe(sub1);

}

void loop() {
  if (cont1 == RequiredSteps1 * 2) {
    Timer1.stop();
    cont1 = 0;
    Position1 = lastPos1;
  }
  if (cont2 == RequiredSteps2 * 2) {
    Timer2.stop();
    cont2 = 0;
    Position2 = lastPos2;
  }
  if (cont3 == RequiredSteps3 * 2) {
    Timer3.stop();
    cont3 = 0;
    Position3 = lastPos3;

  }
  nh.spinOnce();
}


int getNumSteps(float angleSetPoint) {
  //  nh.getParam("joint_reducion",reduccion,1);
  int result;
  result = abs((angleSetPoint / (GRADES_PER_STEP / DivisonStep)) * 1);
  return result;
}

void handler_led1(void) {
  static uint8_t flag1 = 0;
  if (SetPoints1 < 0) {
    digitalWrite(dirPin1, LOW);
  } else {
    digitalWrite(dirPin1, HIGH);
  }
  digitalWrite(stepPin1, flag1);
  flag1 ^= 1;
  cont1 = cont1 + 1;
}

void handler_led2(void) {
  static uint8_t flag2 = 0;
  if (SetPoints1 < 0) {
    digitalWrite(dirPin2, LOW);
  } else {
    digitalWrite(dirPin2, HIGH);
  }
  digitalWrite(stepPin2, flag2);
  flag2 ^= 1;
  cont2 = cont2 + 1;
}

void handler_led3(void) {
  static uint8_t flag3 = 0;
  if (SetPoints3 < 0) {
    digitalWrite(dirPin3, LOW);
  } else {
    digitalWrite(dirPin3, HIGH);
  }
  digitalWrite(stepPin3, flag3);
  flag3 ^= 1;
  cont3 = cont3 + 1;
}
