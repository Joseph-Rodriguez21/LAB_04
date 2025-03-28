import csv 
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, windows
from scipy.fftpack import fft, fftfreq
from scipy.stats import ttest_ind

# Leer el archivo CSV
filename = "senal_2.csv"
timestamps = []
data = []

with open(filename, mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Saltar encabezado

    for row in reader:
        timestamps.append(float(row[0]))  # Tiempo
        data.append(float(row[1]))  # Voltaje

# Verificar si hay datos
if timestamps:
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

    # Filtro pasa altas
    high_cutoff = 10
    filtered_high = highpass_filter(data, high_cutoff, fs)

    # Filtro pasa bajas
    low_cutoff = 50 
    filtered_low = lowpass_filter(filtered_high, low_cutoff, fs)

    # Graficar señal filtrada y original
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, data, label="Señal EMG Original", color="blue", alpha=0.5)
    plt.plot(timestamps, filtered_low, label="Señal EMG Filtrada", color="red")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.title("Señal EMG Antes y Después del Filtrado")
    plt.legend()
    plt.grid()
    plt.show()

    # Segmentación en ventanas
    tamaño_ventana = 500
    superposicion_ventanas = 250
    pasos = tamaño_ventana - superposicion_ventanas
    aplicar_ventanas = []
    espectros = []
    frecuencias = np.fft.rfftfreq(tamaño_ventana, d=1/fs)
    frecuencias_medias = []

    plt.figure(figsize=(12, 6))
    plt.title("Señal Segmentada en Ventanas de Tiempo")
    plt.xlabel("Muestras")
    plt.ylabel("Amplitud")

    for i in range(0, len(filtered_low) - tamaño_ventana, pasos):
        ventana_señal = filtered_low[i:i+tamaño_ventana] * windows.hamming(tamaño_ventana)
        aplicar_ventanas.append(ventana_señal)

        # Graficar cada ventana en el dominio del tiempo
        plt.plot(range(i, i + tamaño_ventana), ventana_señal, alpha=0.5)
    
    plt.show()
    
    # Análisis espectral de cada ventana
    plt.figure(figsize=(12, 6))
    plt.title("Espectrograma de la Señal EMG")
    plt.xlabel("Ventanas de Tiempo")
    plt.ylabel("Frecuencia (Hz)")
    
    espectrograma = []
    
    for ventana in aplicar_ventanas:
        espectro = np.abs(fft(ventana)[:len(frecuencias)])
        espectros.append(espectro)
        espectrograma.append(espectro)
    
    espectrograma = np.array(espectrograma).T  # Transponer para visualizar correctamente
    plt.imshow(espectrograma, aspect='auto', cmap='jet', origin='lower',
               extent=[0, len(aplicar_ventanas), frecuencias[0], frecuencias[-1]])
    plt.colorbar(label="Amplitud del Espectro")
    plt.show()
    
else:
    print("El archivo está vacío. Verifica la captura de datos.")
