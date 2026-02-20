#objetivo.
Caracterizar una señal biomédica utilizando parámetros estadísticos.

#Diagrama de flujo parte A.
#Parte A.

#Diagrama de flujo parte B.
#Parte B.

#Diagrama de flujo parte C.
#Parte C.

#Análisis de resultados.
#Conclusiones.
#Discusión.
Para responder a estas preguntas de discusión en tu informe de laboratorio, puedes basarte en los conceptos de adquisición de señales y procesamiento estadístico tratados en las fuentes:

## **1. ¿Son los valores estadísticos de la señal sintética exactamente iguales a los de la señal real?**

**No, generalmente no son exactamente iguales.** Aunque intente generar una señal del mismo tipo, existen varias razones fisiológicas y técnicas para esta discrepancia:

* **Ruido de adquisición:** Las señales medidas en entornos reales (Parte A) o capturadas mediante hardware como ESP32 (Parte B) están contaminadas por ruido del equipo y del ambiente, lo que altera la dispersión y los valores centrales.
* **Variabilidad fisiológica:** Una señal real de una base de datos captura la complejidad de un organismo, mientras que un generador de señales biológicas produce artefactos.
* **Sensibilidad de los parámetros:** Magnitudes como la **curtosis** y la **asimetría** son muy sensibles a pequeñas variaciones en la distribución de los puntos de la señal; cualquier diferencia mínima en la forma de la onda entre la señal sintética y la real se reflejará en estos valores.

---

## **2. ¿Afecta el tipo de ruido al valor de la SNR calculada? ¿Cuáles podrían ser las razones?**

**Sí, el tipo de ruido afecta significativamente el valor de la SNR (Relación Señal-Ruido).** Las razones principales son:

* **Distribución de la potencia del ruido:** La SNR se basa en la relación entre la potencia de la señal y la potencia del ruido. El **ruido gaussiano** distribuye su energía de manera uniforme, mientras que el **ruido impulso** concentra mucha energía en periodos de tiempo muy cortos (picos), lo que altera la potencia total calculada de forma distinta.
* **Naturaleza del artefacto:** Los ruidos tipo **artefacto** suelen tener componentes de frecuencia específicas o amplitudes mayores que el ruido térmico o gaussiano, lo que puede degradar la calidad de la señal de manera más agresiva, disminuyendo restrictivamente el valor de la SNR.
* **Impacto en la calidad:** Diferentes ruidos afectan la "limpieza" de la señal de formas diversas. Por ejemplo, un ruido tipo artefacto puede desplazar el medio de la señal, mientras que un ruido gaussiano afecta principalmente la desviación estándar.
