import serial
import numpy as np
import wfdb
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import time
import os

# =========================
# PARTE B – SEÑAL ADQUIRIDA (ESP32)
# =========================
PUERTO = "COM3"
BAUDIOS = 115200
FS = 360
DURACION = 10
N = FS * DURACION

BASE_PATH = r"C:\Users\amaya\Desktop\universidad\2026-1\procesamiento digital de señales\lab 1\señal"
RECORD_NAME = "datos_ana"
os.chdir(BASE_PATH)

# =========================
# CAPTURA
# =========================
ser = serial.Serial(PUERTO, BAUDIOS)
time.sleep(2)

datos = []
while len(datos) < N:
    linea = ser.readline().decode(errors="ignore").strip()
    if linea.isdigit():
        datos.append(int(linea))
ser.close()

signal = np.array(datos, dtype=float)

# Normalización
signal = (signal - np.mean(signal)) * (3.3 / 4095)

t = np.arange(N) / FS

# =========================
# GUARDAR WFDB
# =========================
wfdb.wrsamp(
    RECORD_NAME,
    fs=FS,
    units=["mV"],
    sig_name=["ECG"],
    p_signal=signal.reshape(-1,1)
)

# =========================
# VISUALIZACIÓN
# =========================
plt.figure(figsize=(10,4))
plt.plot(t, signal)
plt.title("ECG adquirido – ESP32")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [mV]")
plt.grid()
plt.tight_layout()

# Zoom
plt.figure(figsize=(10,4))
plt.plot(t[:FS*5], signal[:FS*5])
plt.title("ECG ESP32 – Zoom 5 s")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [mV]")
plt.grid()
plt.tight_layout()

# =========================
# MÉTODO A – MANUAL
# =========================

N = len(signal)

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
# RESULTADOS
# =========================
print("\nPARTE B – ECG ESP32")
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
plt.title("Histograma – ECG ESP32")
plt.xlabel("Amplitud [mV]")
plt.ylabel("Densidad de probabilidad")
plt.grid()
plt.tight_layout()
# =========================
# PARTE C – RELACIÓN SEÑAL RUIDO (SNR)
# =========================

def calcular_snr(signal_limpia, signal_ruidosa):
    ruido = signal_ruidosa - signal_limpia
    P_signal = np.mean(signal_limpia**2)
    P_ruido = np.mean(ruido**2)
    return 10 * np.log10(P_signal / P_ruido)

# =========================
# a) RUIDO GAUSSIANO
# =========================
sigma = 0.05 * np.std(signal)      # nivel de ruido (5%)
ruido_gauss = np.random.normal(0, sigma, N)
signal_gauss = signal + ruido_gauss

snr_gauss = calcular_snr(signal, signal_gauss)

# =========================
# b) RUIDO IMPULSO
# =========================
signal_impulso = signal.copy()
num_impulsos = int(0.01 * N)       # 1% de muestras
indices = np.random.randint(0, N, num_impulsos)

signal_impulso[indices] += 5 * np.max(np.abs(signal))

snr_impulso = calcular_snr(signal, signal_impulso)

# =========================
# c) RUIDO TIPO ARTEFACTO
# =========================
artefacto = 0.3 * np.sin(2 * np.pi * 0.5 * t)  # baja frecuencia
signal_artefacto = signal + artefacto

snr_artefacto = calcular_snr(signal, signal_artefacto)

# =========================
# RESULTADOS SNR
# =========================
print("\nPARTE C – RELACIÓN SEÑAL RUIDO (SNR)")
print(f"SNR con ruido gaussiano : {snr_gauss:.2f} dB")
print(f"SNR con ruido impulso  : {snr_impulso:.2f} dB")
print(f"SNR con ruido artefacto: {snr_artefacto:.2f} dB")

# =========================
# GRÁFICAS PARTE C
# =========================
plt.figure(figsize=(10,4))
plt.plot(t, signal, label="Señal limpia")
plt.plot(t, signal_gauss, alpha=0.6, label="Ruido gaussiano")
plt.title("ECG + Ruido Gaussiano")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [mV]")
plt.legend()
plt.grid()
plt.tight_layout()

plt.figure(figsize=(10,4))
plt.plot(t, signal_impulso, color="r")
plt.title("ECG + Ruido Impulso")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [mV]")
plt.grid()
plt.tight_layout()

plt.figure(figsize=(10,4))
plt.plot(t, signal_artefacto, color="g")
plt.title("ECG + Ruido Tipo Artefacto")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud [mV]")
plt.grid()
plt.tight_layout()

plt.show()
