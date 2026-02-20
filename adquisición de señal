// =========================
// CONFIGURACIÓN
// =========================
const int ECG_PIN = 13;      // GPIO13 = ADC2_4
const int FS = 360;          // Frecuencia de muestreo (Hz)
unsigned long periodo_us;

void setup() {
  Serial.begin(115200);
  delay(2000);

  periodo_us = 1000000UL / FS;

  // Configuración ADC
  analogReadResolution(12);              // 0–4095
  analogSetPinAttenuation(ECG_PIN, ADC_11db); // hasta 3.3V

  Serial.println("ESP32 ECG listo");
}

void loop() {
  unsigned long t0 = micros();

  int valor_adc = analogRead(ECG_PIN);
  Serial.println(valor_adc);

  // Mantener frecuencia de muestreo estable
  while (micros() - t0 < periodo_us) {
    // espera activa
  }
}
