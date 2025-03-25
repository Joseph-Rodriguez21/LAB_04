# Laboratorio 04 Señales electromiográficas EMG

1. Introducción:

El electromiograma (EMG) registra la actividad eléctrica de los músculos, con dos tipos principales: superficial e intramuscular. Para captar estas señales, se usan electrodos activos y de tierra. Los electrodos superficiales se colocan sobre la piel, mientras que el de tierra se conecta a una parte eléctricamente activa del cuerpo. La señal EMG se obtiene a partir de la diferencia de potencial entre los electrodos activos.

2. Metodología, desarrollo y analisis:

Primero se descargaron los correspondientes programas para la adquisicion de datos DAQ NI USB, en el cual instalamos una aplicacion y ampliacion en Python, luego se conectan los electrodos al amplificador y al sistema DAQ.
Seleccionamos un músculo a estudiar y calcular la frecuencia de muestreo necesaria para realizar la captura de la señal.
Nuestro grupo de trabajo realizo el siguiente montaje:

![image](https://github.com/user-attachments/assets/2d0b261c-eee7-46fc-bde9-1f8ca6d57a81)

Imagen referencia de montaje, Lab 04 señales electromiográficas PDS.

Se realiza contracción muscular continua hasta llegar a la fatiga mientras a su vez registramos la señal EMG en tiempo real.

3. Montaje:

Se conectaron los electrodos al sensor y este a su vez al dispositivo NU, el cual de igual manera proporcionaba la energia suficiente para su correcto funcionamiento.

![Imagen de WhatsApp 2025-03-25 a las 17 13 46_1581254b](https://github.com/user-attachments/assets/4950648b-405d-4d9d-bf2a-a0800cedf1e9)

La captura de los datos de la señal de EMG fueron capturados en tiempo real mediante el siguiente código, el cual al finalizar los guardaba en un archivo .csv con el que más adelante mostraremos su grafica y sus correspondientes filtros.
En este tramo de código, se llaman diferentes librerias importantes, tales como 'nidaqmx' con la cual interactuamos con dispositivos de adquision de datos (DAQ), tambien tenemos 'csv' para manejar archivos CSV y guardar los datos de la señal y por otro lado 'time' para medir el tiempo de adquisición de datos y generar marcas de tiempo.
Luego configuramos los rangos de la captura de datos, en este caso vamos a registrar 10000 muestras a una frecuencia en Hertz de (10,000 muestras por segundo), y por ultimo definimos el nombre del archivo en el que guardaremos los datos.

![image](https://github.com/user-attachments/assets/8f4600e3-1abb-4acf-8a28-ea8bcf1d662c)


Ahora se realiza la creación del archivo CSV y estritura del encabezado, en este caso "Tiempo (s)", "Voltaje (V)", se abre el archivo en modo escritura, lo cual sobreescribirá los datos de la señal que vamos a capturar mediante el siguiente paso que es la inicialización.

![image](https://github.com/user-attachments/assets/4a313887-1932-4488-877c-7096235a890b)


El siguiente paso es la captura y guardado de la señal, en la cual principalmente realizaremos la inicialización de la captura de datos, en la cual se inicializa una lista vacia para almacenar temporalmente los datos adquiridos 'data = []', para luego guardar el tiempo de incio en segundos, para asi calcular el tiempo transcurrido en cada medición.

![image](https://github.com/user-attachments/assets/e4d37802-3f49-47ad-9bc9-7ef32ca28283)


Luego se realiza la adquisición de datos en las que se crea un objeto Task, el cual representa una tarea de adquisición de datos, a este agregamos el canal por el cual se adquirirán los datos provenientes del sensor recibidos en un canal de entrada analógica del dispositivo DAQ, en este caso 'Dev2/ai0', lo cual significa que se realizada en el dispositivo Dev2, canal analógico 0 (ai0).

![image](https://github.com/user-attachments/assets/6112a18a-76f2-445d-bb86-ff75f9d4577c)


Ahora creamos un for en forma de bucle para la captura de datos, se inicia un bucle que se ejecuta en 'num_samples' veces (lo cual corresponde a lo ya definido anteriormente, 10.000 iteraciones), ahora mediante 'value = task.read()' se lee el voltaje actual del canal 'ai0', también se calcula el tiempo transcurrido desde que comenzo la adquisición y por último se guarda la tabla en la lista 'data' para almacenamiento temporal.

![image](https://github.com/user-attachments/assets/1b0d354b-0482-434f-bc3e-83ee8c01679e)


Por último se realiza la esctirua de datos en el archivo CSV, en este se abre el archico en modo "append" "a", luego se crea un objeto 'writer' para escribir en el archivo y mediante 'writer.writerow([timestamp, value])'se escribe en una nueva fila el tiempo transcurrido y el voltaje capturado en esa iteración, para terminar imprime en pantalla un mensaje de confirmación y guardado correcto.

![image](https://github.com/user-attachments/assets/d7b97482-993f-41a7-98b1-35c64f8b4895)


Para este punto ya hemos capturado y guardado la señal de EMG en un archivo de CSV, por lo cual ahora vamos a realizar la gráfica para terminar nuestra señal y empezar a trabajar sobre ella y realizar los diferentes filtros y análisis.

Ahora se realiza un código para leer el archivo CSV de la señal de EMG y graficar sus datos.

Llamamos librerias que nos ayudan a leer archivos CSV donde se almacenaron los datos y hacer su respectiva gráfica. Luego llamaremos el nombre del archivo que se leerá, posteriormenrte se mencionan dos listas vacias para almacenar los datos de valores de voltaje y tiempo.
Ahora se realiza a lectura de los datos en archivo CSV, primero se abre el archivo en modo de lectura 'r', se crea un objeto que lee lina por linea 'csv.reader(file)'

![image](https://github.com/user-attachments/assets/553deb18-3fe3-47d8-97a3-03ecf5e6f4db)


Luego se almacenan los datos en listas, esto lo hacemos mediante un ciclo for que recorre cada fila del archivo CSV, 'row[0]' (primer valor de la fila), se convierte ea 'float' y se guarda en 'timestamps' (lista de tiempos), de igual manera con 'row[1]' y se guarda en 'data' (lista de voltajes)
También se realiza una verificación de datos para comprobar que se esta realizando un correcto intercambio de datos.

![image](https://github.com/user-attachments/assets/e5767a96-e3b2-4480-ba51-6cc3a48852e1)

Por último, una vez verificado vamos a realizar su correspondiente grafica, se añaden titulos de ejes y cuadrilla para mejor analisis e identificación.

![image](https://github.com/user-attachments/assets/65ac99ed-8a0f-49cb-b04b-8b94c0454b18)


hecho esto obtenemos la siguiente gráfica sobre la que vamos a trabajar y realizar los correspondientes filtros.

![image](https://github.com/user-attachments/assets/e4754c9d-2218-4875-b4a3-f5231d816c02)


   
