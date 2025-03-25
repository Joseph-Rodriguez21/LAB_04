import nidaqmx
import matplotlib.pyplot as plt
import csv
import time

# Configuración
num_samples = 10000
sampling_rate = 10000  # Hz
filename = "senal_emg.csv"

# Inicializar archivo CSV y escribir encabezado
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Tiempo (s)", "Voltaje (V)"])

# Captura y guardado de la señal
data = []
start_time = time.time()

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev2/ai0")

    for i in range(num_samples):
        value = task.read()
        timestamp = time.time() - start_time
        data.append((timestamp, value))

        # Guardar en el archivo CSV
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, value])

print("Datos guardados en", filename)
