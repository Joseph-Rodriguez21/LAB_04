
import csv
import matplotlib.pyplot as plt

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

    # Graficar
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, data, label="Señal EMG", color="blue")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.title("Señal EMG Guardada")
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("El archivo está vacío. Verifica la captura de datos.")
