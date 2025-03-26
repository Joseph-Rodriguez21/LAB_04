import csv 
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Leer el archivo CSV
filename = "senal_emg_.csv"
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
    def butterworth_filter(data, cutoff, fs, order=4, btype='low'):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        if normal_cutoff <= 0 or normal_cutoff >= 1:
            raise ValueError(f"Frecuencia de corte inválida: {cutoff} Hz (Normalizada: {normal_cutoff})")
        b, a = butter(order, normal_cutoff, btype=btype, analog=False)
        return filtfilt(b, a, data)

    # frecuencia de muestreo estimada 
    fs = 1 / np.mean(np.diff(timestamps))
    nyquist = fs / 2
    
    print(f"Frecuencia de muestreo estimada: {fs} Hz")
    print(f"Frecuencia de Nyquist: {nyquist} Hz")
    
    # frecuencias de corte
    high_cutoff = 20  # Pasa altas
    low_cutoff = 50  # Pasa bajas
    
    if high_cutoff >= nyquist or low_cutoff >= nyquist:
        raise ValueError(f"Las frecuencias de corte deben ser menores que Nyquist ({nyquist} Hz). Ajusta los valores.")
    
    # filtro pasa altas
    filtered_high = butterworth_filter(data, high_cutoff, fs, btype='high')
    
    # filtro pasa bajas
    filtered_low = butterworth_filter(filtered_high, low_cutoff, fs, btype='low')


    # Graficar señal filtrada
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, data, label="Señal EMG Original", color="blue", alpha=0.5)
    plt.plot(timestamps, filtered_low, label="Señal EMG Filtrada", color="red")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.title("Señal EMG Antes y Después del Filtrado")
    plt.legend()
    plt.grid()
    plt.show()

else:
    print("El archivo está vacío. Verifica la captura de datos.")
