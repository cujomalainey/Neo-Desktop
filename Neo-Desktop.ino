#include "Adafruit_NeoPixel.h"

#define COLORPIN 6
#define NUMPIXELS 60

uint8_t current_color[] = {0, 0, 0};
uint8_t target_color[] = {0, 0, 0};
char message[60];
char debug[30];
uint8_t str_postion = 0;
uint8_t red;
uint8_t green;
uint8_t blue;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, COLORPIN, NEO_GRB + NEO_KHZ800);

void setup() {
    Serial.begin(9600);
    message[59] = '\0';
}

void loop() {
  while (Serial.available() > 0)
  {
    message[str_postion] = Serial.read();
    if (message[str_postion] == '\n')
    {
      message[str_postion + 1] = '\0';
      str_postion = 0;
      if (message[0] == 'T')
      {
        Serial.print("GREEN!\n");
      }
      else if (sscanf(message, "(%d, %d, %d)\n", &red, &green, &blue) == 3)
      {
        sprintf(debug, "got (%d, %d, %d)\n", red, green, blue);
        Serial.println(message);
        Serial.print(debug);
        target_color[0] = red;
        target_color[1] = green;
        target_color[2] = blue;
      }
      else
      {
        Serial.print("PARSE\n");
      }
    }
    else
    {
      str_postion++;
    }
  }
  delay(0.01);
  if (current_color[0] != target_color[0] || current_color[1] != target_color[1] || current_color[2] != target_color[2])
  {
    // sprintf(debug, "(%d, %d, %d)\n", current_color[0], current_color[1], current_color[2]);
    // Serial.print(debug);
    for (int i; i < 3; i++)
    {
      if (target_color[i] > current_color[i])
      {
        current_color[i]++;
      } 
      else if (target_color[i] < current_color[i])
      {
        current_color[i]--;
      }
    }
    for (int i; i < NUMPIXELS; i++)
    {
      pixels.setPixelColor(i, pixels.Color(current_color[0], current_color[1], current_color[2]));
    }
    pixels.show();
  }
}
