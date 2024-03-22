import os
carpeta = 'session'

# Obtener la lista de archivos en la carpeta
archivos = os.listdir(carpeta)

# Crear un archivo de texto para escribir la lista de archivos
with open('lista_archivos.txt', 'w') as archivo_txt:
    # Iterar sobre los archivos y escribir sus nombres en el archivo de texto
    for archivo in archivos:
        nombre_archivo, _ = os.path.splitext(archivo)
        archivo_txt.write(f"{nombre_archivo},??,??\n")