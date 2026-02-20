# ============================================================
# IMPORTANTE:
# Este script debe ejecutarse en el MISMO directorio donde se
# encuentran los archivos del registro MIT-BIH descargados
# desde PhysioNet (.dat, .hea y .atr).
#
# Ejemplo:
#   100.dat
#   100.hea
#   100.atr
#
# De lo contrario, la librería wfdb no podrá cargar la señal.
# ============================================================

import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

# =========================
# PARTE A – SEÑAL REAL (PHYSIONET)
# =========================

record = wfdb.rdrecord('100')
signal = record.p_signal[:, 0]      # ECG canal 1
fs = record.fs

# Normalización (comparabilidad con ESP32)
signal = signal - np.mean(signal)

t = np.arange(len(signal)) / fs
N = len(signal)

# =========================
# VISUALIZACIÓN
# =========================
plt.figure(figsize=(10,4))
plt.plot(t, signal)
plt.title("ECG real – MIT-BIH (señal completa)")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [mV]")
plt.grid()
plt.tight_layout()

# Zoom
zoom_s = 5
plt.figure(figsize=(10,4))
plt.plot(t[:int(fs*zoom_s)], signal[:int(fs*zoom_s)])
plt.title("ECG real – Zoom 5 s")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [mV]")
plt.grid()
plt.tight_layout()

# =========================
# MÉTODO A – CÁLCULO MANUAL
# =========================
# Número total de muestras de la señal
N = len(signal)

# =========================
# MEDIA
# =========================
# Inicializamos una variable para acumular la suma
suma_total = 0

# Recorremos la señal muestra por muestra
for muestra in signal:
    suma_total = suma_total + muestra

# Calculamos la media dividiendo entre el número de muestras
media_m = suma_total / N


# =========================
# VARIANZA
# =========================
# La varianza mide qué tan alejados están los valores de la media
suma_diferencias_cuadradas = 0

for muestra in signal:
    diferencia = muestra - media_m          # distancia a la media
    diferencia_cuadrada = diferencia ** 2   # elevamos al cuadrado
    suma_diferencias_cuadradas += diferencia_cuadrada

# Dividimos entre el total de muestras
var_m = suma_diferencias_cuadradas / N


# =========================
# DESVIACIÓN ESTÁNDAR
# =========================
# Es simplemente la raíz cuadrada de la varianza
std_m = np.sqrt(var_m)


# =========================
# COEFICIENTE DE VARIACIÓN
# =========================
# Relaciona la dispersión con el valor promedio
cv_m = std_m / abs(media_m)


# =========================
# SKEWNESS (asimetría)
# =========================
# Indica si la distribución está inclinada a la izquierda o derecha
suma_cubos = 0

for muestra in signal:
    diferencia = muestra - media_m
    suma_cubos += diferencia ** 3

skew_m = suma_cubos / (N * std_m ** 3)


# =========================
# CURTOSIS
# =========================
# Indica qué tan puntiaguda o plana es la distribución
suma_cuartas = 0

for muestra in signal:
    diferencia = muestra - media_m
    suma_cuartas += diferencia ** 4

kurt_m = suma_cuartas / (N * std_m ** 4)


# =========================
# MÉTODO B – PYTHON
# =========================
media_p = np.mean(signal)
std_p = np.std(signal)
cv_p = std_p / abs(media_p)
skew_p = skew(signal)
kurt_p = kurtosis(signal, fisher=False)

# =========================
# RESULTADOS COMPARATIVOS
# =========================
print("\nPARTE A – ECG REAL (PHYSIONET)")
print("Estadístico        Manual        Python")
print(f"Media           {media_m:.5f}     {media_p:.5f}")
print(f"Varianza        {var_m:.5f}     {std_p**2:.5f}")
print(f"Desv. estándar  {std_m:.5f}     {std_p:.5f}")
print(f"Coef. variación {cv_m:.5f}     {cv_p:.5f}")
print(f"Skewness        {skew_m:.5f}     {skew_p:.5f}")
print(f"Curtosis        {kurt_m:.5f}     {kurt_p:.5f}")

# =========================
# HISTOGRAMA
# =========================
plt.figure(figsize=(6,4))
plt.hist(signal, bins=100, density=True)
plt.title("Histograma – ECG real")
plt.xlabel("Amplitud [mV]")
plt.ylabel("Densidad de probabilidad")
plt.grid()
plt.tight_layout()

plt.show()
