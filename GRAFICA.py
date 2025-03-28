import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, windows
from scipy.fftpack import fft
from scipy.stats import ttest_ind, t


# Leer el archivo CSV
filename = "senal_2.csv"
timestamps, data = [], []

with open(filename, mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Saltar encabezado
    for row in reader:
        timestamps.append(float(row[0]))
        data.append(float(row[1]))

# Verificar si hay datos
if not timestamps:
    print("El archivo está vacío. Verifica la captura de datos.")
    exit()

print("Primeros valores:", list(zip(timestamps, data))[:10])

# Graficar señal original
plt.figure(figsize=(10, 5))
plt.plot(timestamps, data, label="Señal EMG Original", color="blue")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal EMG Guardada")
plt.legend()
plt.grid()
plt.show()

# Filtros
def highpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)

def lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

# Frecuencia de muestreo
fs = 1 / np.mean(np.diff(timestamps))

# Aplicar filtros
high_cutoff, low_cutoff = 10, 50
filtered_signal = lowpass_filter(highpass_filter(data, high_cutoff, fs), low_cutoff, fs)

# Graficar señal filtrada y original
plt.figure(figsize=(10, 5))
plt.plot(timestamps, data, label="Señal EMG Original", color="blue", alpha=0.5)
plt.plot(timestamps, filtered_signal, label="Señal EMG Filtrada", color="red")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal EMG Antes y Después del Filtrado")
plt.legend()
plt.grid()
plt.show()

# Segmentación en ventanas
tamaño_ventana, superposicion_ventanas = 500, 250
pasos = tamaño_ventana - superposicion_ventanas
frecuencias = np.fft.rfftfreq(tamaño_ventana, d=1/fs)
frecuencias_medias, ventanas_procesadas = [], []

plt.figure(figsize=(12, 6))
plt.title("Señal Segmentada en Ventanas de Tiempo")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")

for i in range(0, len(filtered_signal) - tamaño_ventana, pasos):
    ventana = filtered_signal[i:i+tamaño_ventana] * windows.hamming(tamaño_ventana)
    espectro = np.abs(fft(ventana)[:len(frecuencias)])
    frec_mediana = np.median(frecuencias[np.argsort(espectro)[len(espectro)//2:]])
    
    frecuencias_medias.append(frec_mediana)
    ventanas_procesadas.append(espectro)

    # Graficar cada ventana en el dominio del tiempo
    plt.plot(range(i, i + tamaño_ventana), ventana, alpha=0.5)

plt.show()

# Graficar evolución de la frecuencia mediana
plt.figure(figsize=(10, 5))
plt.plot(frecuencias_medias, marker='o', linestyle='-', color='red')
plt.xlabel("Ventanas de tiempo")
plt.ylabel("Frecuencia mediana (Hz)")
plt.title("Evolución de la Frecuencia Mediana")
plt.grid()
plt.show()

# Prueba de hipótesis
division = len(frecuencias_medias) // 2
grupo1, grupo2 = frecuencias_medias[:division], frecuencias_medias[division:]
stat, p_value = ttest_ind(grupo1, grupo2)
alpha = 0.05

print(f"Estadístico t: {stat:.2f}, Valor p: {p_value:.5f}")
if p_value < alpha:
    print("Se detecta un cambio significativo en la frecuencia mediana, indicando posible fatiga muscular.")
else:
    print("No hay evidencia estadística suficiente para afirmar un cambio significativo en la frecuencia mediana.")

# Gráfica de la prueba de hipótesis
t_crit, t_calc, df = 1.96, 15.23, 30
x = np.linspace(-20, 20, 1000)
y = t.pdf(x, df)

plt.figure(figsize=(10, 6))
plt.plot(x, y, color="black", label="Distribución t")
plt.fill_between(x, y, where=(x <= -t_crit) | (x >= t_crit), color="red", alpha=0.5, label="Región de Rechazo")
plt.axvline(-t_crit, linestyle="dashed", color="black", label=r"$t_{crítico} = \pm1.96$")
plt.axvline(t_crit, linestyle="dashed", color="black")
plt.axvline(t_calc, linestyle="dashed", color="blue", label=r"$t_{calculado} = 15.23$")
plt.title("Prueba de Hipótesis de Dos Colas")
plt.xlabel("Valores de t")
plt.ylabel("Densidad de Probabilidad")
plt.legend()
plt.grid()
plt.show()
