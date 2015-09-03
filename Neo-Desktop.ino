#include "Adafruit_NeoPixel.h"

#define COLORPIN 6
#define NUMPIXELS 60

int current_color[] = {0, 0, 0};
int target_color[] = {0, 0, 0};
char message[60];
uint8_t str_postion = 0;
uint16_t red;
uint16_t green;
uint16_t blue;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, COLORPIN, NEO_GRB + NEO_KHZ800);

void setup() {
    Serial.begin(9600);
    pixels.begin();
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
      else if (sscanf(message, "(%u, %u, %u)\n", &red, &green, &blue) == 3)
      {
        target_color[0] = (uint8_t)red;
        target_color[1] = (uint8_t)green;
        target_color[2] = (uint8_t)blue;
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
  delay(10);
  if (current_color[0] != target_color[0] || current_color[1] != target_color[1] || current_color[2] != target_color[2])
  {
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
