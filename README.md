## Objetivo.

Caracterizar una señal biomédica tipo electrocardiograma (ECG) utilizando parámetros estadísticos descriptivos, a partir de una señal digital de referencia y de una señal adquirida experimentalmente mediante una plataforma ESP32, con el fin de analizar sus propiedades estadísticas, evaluar el impacto del ruido y comparar el 
comportamiento entre una señal estándar y una señal medida en condiciones reales.

## Diagrama de flujo parte A.

<img width="2880" height="4224" alt="ecg_flowchart" src="https://github.com/user-attachments/assets/2ea79d4e-3fc4-4220-945e-17e7bef5d56d" />

## Parte A.

En esta parte se trabajó con una señal ECG digital proveniente de la base de datos MIT-BIH Arrhythmia Database, específicamente el registro 100. La señal fue cargada en Python mediante la librería wfdb, la cual permite leer archivos biomédicos en formato estándar (.dat, .hea, .atr). A partir del archivo de encabezado se extrajeron el canal correspondiente al ECG y la frecuencia de muestreo asociada.

Con la frecuencia de muestreo se construyó un vector de tiempo que permitió representar la señal en función del tiempo. Se realizaron dos visualizaciones principales: una gráfica de la señal completa y una gráfica con un zoom de los primeros cinco segundos, lo que facilitó la observación detallada de la morfología típica del ECG, incluyendo complejos QRS, ondas P y T.

Posteriormente, se calcularon parámetros estadísticos descriptivos mediante dos enfoques. En el primer enfoque, denominado Método A, los cálculos se realizaron manualmente, siguiendo paso a paso las definiciones matemáticas de media, varianza, desviación estándar, coeficiente de variación, asimetría (skewness) y curtosis. Este procedimiento permitió reforzar la comprensión conceptual de cada estadístico.

En el segundo enfoque, Método B, se utilizaron funciones estadísticas provistas por las librerías numpy y scipy.stats, con el objetivo de validar los resultados obtenidos manualmente. Finalmente, se construyó un histograma de amplitudes de la señal ECG, lo que permitió analizar la distribución estadística de los valores y su relación con los parámetros calculados.

<img width="849" height="561" alt="image" src="https://github.com/user-attachments/assets/5ed8bf93-aed2-42be-a316-5e539a9d9468" />

<img width="1425" height="561" alt="image" src="https://github.com/user-attachments/assets/ba2c71d6-0a00-4d30-8677-25eb6470f7db" />

<img width="1425" height="561" alt="image" src="https://github.com/user-attachments/assets/e884b453-fd91-4ba1-b476-b075736168b5" />

## Diagrama de flujo parte B y C

<img width="2880" height="5832" alt="ecg_esp32_flowchart" src="https://github.com/user-attachments/assets/e8935972-34b2-4705-b76a-b7de7bcb45bc" />

## Parte B.

En esta etapa se adquirió una señal ECG analógica utilizando un módulo AD8232 y una placa ESP32 Dev Kit. La ESP32 fue configurada para muestrear la señal a una frecuencia de 360 Hz, empleando un canal ADC con resolución de 12 bits. La placa se encargó exclusivamente de la adquisición de la señal y de la transmisión de los valores del convertidor analógico-digital a través de comunicación serial.

Un único script en Python se encargó de establecer la comunicación serial con la ESP32, recibir los datos adquiridos, almacenarlos y realizar tanto el procesamiento estadístico como el análisis posterior del efecto del ruido sobre la señal.

Dentro de este mismo código se integraron las rutinas correspondientes a la Parte B (adquisición y caracterización estadística de la señal) y a la Parte C (contaminación con distintos tipos de ruido y cálculo de la Relación Señal-Ruido, SNR), garantizando coherencia en el manejo de los datos y evitando la duplicación de procesos.

La señal adquirida fue almacenada en formato WFDB, lo que permitió tratarla de manera equivalente a una señal biomédica estándar proveniente de una base de datos. Esto facilitó la reutilización del mismo procedimiento de visualización y análisis estadístico aplicado en la Parte A.

De forma análoga, se generaron las gráficas de la señal completa y un zoom de los primeros cinco segundos. Asimismo, se calcularon los parámetros estadísticos descriptivos tanto mediante el método manual como utilizando funciones de Python, y se construyó el histograma de amplitudes. Esto permitió comparar directamente los resultados obtenidos con los de la señal digital de referencia.

## Parte C.

En esta parte se analizó el efecto del ruido sobre la señal ECG adquirida en la Parte B, utilizando el mismo script de procesamiento desarrollado previamente, en el cual se integraron tanto la adquisición como el análisis estadístico y de ruido.

La señal obtenida experimentalmente fue reutilizada directamente dentro del código para generar versiones contaminadas con diferentes tipos de ruido, lo que permitió calcular la Relación Señal-Ruido (SNR) sin necesidad de recargar ni reprocesar la señal desde cero, garantizando coherencia en el tratamiento de los datos.

A partir de la señal original adquirida con la ESP32, se generaron tres versiones contaminadas con distintos tipos de ruido:

Ruido gaussiano, modelado como una señal aleatoria de distribución normal con media cero y una desviación estándar proporcional a la de la señal original.

Ruido impulso, implementado mediante la inserción de picos de alta amplitud en un pequeño porcentaje de las muestras, simulando interferencias abruptas.

Ruido tipo artefacto, simulado como una interferencia de baja frecuencia que altera la línea base de la señal, representando efectos como movimiento del paciente o mala colocación de los electrodos.

Para cada caso se calculó la SNR utilizando la diferencia entre la señal contaminada y la señal original como estimación del ruido. Asimismo, se realizaron representaciones gráficas que permitieron visualizar el impacto de cada tipo de ruido sobre la morfología de la señal ECG.

## Análisis de resultados.

Los resultados obtenidos muestran que los parámetros estadísticos calculados manualmente coinciden estrechamente con los obtenidos mediante funciones de Python, validando la correcta implementación de los algoritmos y la consistencia de los datos.

Al comparar la señal digital de la Parte A con la señal adquirida en la Parte B, se observaron diferencias en la dispersión y en los estadísticos de orden superior, especialmente en la asimetría y la curtosis. Estas diferencias se atribuyen principalmente al ruido presente en la adquisición real y a la variabilidad inherente al sistema de medición.

En la Parte C se evidenció que la SNR depende fuertemente del tipo de ruido aplicado. El ruido impulso produjo una degradación más severa de la SNR debido a la alta energía concentrada en picos aislados, mientras que el ruido gaussiano afectó de manera más uniforme la señal. El ruido tipo artefacto alteró significativamente la 
forma global del ECG, afectando su interpretación aun cuando la SNR no fuese la más baja.

## Conclusiones.

Se logró caracterizar una señal ECG utilizando parámetros estadísticos descriptivos tanto a partir de una señal digital de referencia como de una señal adquirida experimentalmente con una ESP32. El uso de cálculos manuales permitió reforzar la comprensión teórica de los estadísticos, mientras que el uso de funciones de Python facilitó la validación de los resultados.

La adquisición experimental introdujo ruido y variabilidad que se reflejaron en los parámetros estadísticos, evidenciando la diferencia entre señales ideales y señales reales. Finalmente, el análisis de la SNR permitió demostrar que distintos tipos de ruido afectan de manera diferente la calidad de la señal ECG, lo cual es fundamental en el procesamiento de señales biomédicas.

Desde el punto de vista de implementación, el uso de un único script para las Partes B y C permitió mantener un flujo de procesamiento continuo, reduciendo errores asociados a conversiones intermedias y garantizando que el análisis de ruido se realizara exactamente sobre la señal adquirida experimentalmente. Esta estrategia mejora la trazabilidad de los resultados y refleja un enfoque más cercano a sistemas reales de procesamiento biomédico.

## Discusión.

El desarrollo del laboratorio permitió integrar conceptos de estadística, procesamiento digital de señales y adquisición de datos biomédicos en un entorno práctico. La comparación entre señales digitales y señales adquiridas experimentalmente resalta la importancia del acondicionamiento de señal y del análisis de ruido en aplicaciones biomédicas reales.

El uso de herramientas abiertas como Python, WFDB y plataformas de hardware de bajo costo como la ESP32 demuestra que es posible realizar análisis biomédicos robustos con recursos accesibles, siempre que se comprendan adecuadamente las limitaciones y fuentes de error del sistema.

## 1. ¿Son los valores estadísticos de la señal sintética exactamente iguales a los de la señal real?

No son exactamente iguales. Aunque se intente trabajar con señales del mismo tipo, existen varias razones fisiológicas y técnicas que explican estas diferencias.

El ruido de adquisición presente en señales reales o capturadas mediante hardware introduce variaciones que afectan la dispersión y los valores centrales. Además, la variabilidad fisiológica hace que una señal real contenga irregularidades que no están presentes en señales sintéticas o idealizadas. Por último, parámetros como la curtosis y la asimetría son altamente sensibles a pequeñas variaciones en la distribución de los datos, por lo que cualquier diferencia mínima en la forma de la señal se refleja en estos valores.

## 2. ¿Afecta el tipo de ruido al valor de la SNR calculada? ¿Cuáles podrían ser las razones?

Sí, el tipo de ruido afecta significativamente el valor de la SNR. Esto se debe a que la SNR depende directamente de la relación entre la potencia de la señal y la potencia del ruido.

El ruido gaussiano distribuye su energía de forma uniforme a lo largo del tiempo, mientras que el ruido impulso concentra grandes cantidades de energía en intervalos muy cortos, reduciendo de manera más drástica la SNR. Por su parte, el ruido tipo artefacto introduce componentes de baja frecuencia o desplazamientos de la línea base, lo que puede degradar la calidad de la señal de manera considerable, incluso cuando la potencia total del ruido no es máxima.
