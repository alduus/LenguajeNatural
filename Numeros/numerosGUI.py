from PIL import Image, ImageTk
import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox

# Función para comparar las imágenes de manera exhaustiva
def exhaustiva(original, prueba):
    image1 = Image.open(original)
    image2 = Image.open(prueba)

    if image1.size != image2.size:
        messagebox.showerror("Error", "Las imágenes no tienen el tamaño esperado")
        return

    for x in range(image1.width):
        for y in range(image1.height):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))

            if pixel1 != pixel2:
                messagebox.showinfo("Resultado", "La imagen no coincide con la original.")
                return

    messagebox.showinfo("Resultado", "La imagen ingresada es la misma que la original")

# Función para comparar las imágenes
def comparar_imagenes(original, prueba):
    image1 = Image.open(original)
    image2 = Image.open(prueba)

    if image1.size != image2.size:
        messagebox.showerror("Error", "Las imágenes no tienen el tamaño esperado")
        return

    coincidencias = 0
    total_pixeles = image1.width * image1.height

    for x in range(image1.width):
        for y in range(image1.height):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))

            if pixel1 == pixel2:
                coincidencias += 1

    porcentaje_coincidencia = (coincidencias / total_pixeles) * 100

    messagebox.showinfo("Resultado", f"Porcentaje de coincidencia entre las imágenes: {porcentaje_coincidencia:.2f}%")

def leerImagenBmp(nombre_archivo):
    with open(nombre_archivo, 'rb') as archivo:
        # Cabecera BMP (los primeros 54 bytes)
        cabecera = archivo.read(54)

        # Obteniendo el ancho y alto de la imagen
        ancho = int.from_bytes(cabecera[18:22], byteorder='little')
        alto = int.from_bytes(cabecera[22:26], byteorder='little')

        # Saltar al inicio de los datos de la imagen
        archivo.seek(int.from_bytes(cabecera[10:14], byteorder='little'))

        # Leer los datos de la imagen
        datosImagen = archivo.read()

    return ancho, alto, datosImagen

def leerImagenesBmpEnCarpeta(carpeta):
    imagenes_bmp = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".bmp"):
            ruta_completa = os.path.join(carpeta, archivo)
            ancho, alto, datos = leerImagenBmp(ruta_completa)
            imagenes_bmp.append((ruta_completa, ancho, alto, datos))

    return imagenes_bmp

def validar_dimensiones(imagenes):
    for i in range(len(imagenes) - 1):  # Iterar hasta el penúltimo elemento
        ancho, alto, _ = imagenes[i][1:]  # Obtener dimensiones de la imagen actual
        siguiente_ancho, siguiente_alto, _ = imagenes[i + 1][1:]  # Obtener dimensiones de la siguiente imagen
        if (ancho, alto) != (siguiente_ancho, siguiente_alto):
            print("Las imágenes no tienen las mismas dimensiones")
            return False
    return True

# Función para convertir una imagen BMP en un vector de características
def convertir_aCaracteristicas(ruta_imagen):
    # Leer la imagen BMP y extraer características relevantes
    ancho, alto, datos = leerImagenBmp(ruta_imagen)
    return [ancho, alto]

# Función para obtener la función de pérdida durante el entrenamiento
def obtener_funcion_perdida(datos_entrenamiento, pesos, tasa_aprendizaje, iteraciones_max):
    iteraciones = []
    perdidas = []

    for iteracion in range(iteraciones_max):
        aprendiendo = False
        perdida_iteracion = 0
        random.shuffle(datos_entrenamiento)  # Mezcla los datos en cada iteración

        for datos in datos_entrenamiento:
            entradas = datos[:-1]  # Todas las características excepto la última (etiqueta)
            etiqueta_real = datos[-1]

            # Calcular salida del perceptrón
            suma_ponderada = sum(w * x for w, x in zip(pesos[:-1], entradas)) + pesos[-1]
            salida = 1 if suma_ponderada > 0 else 0

            # Calcular pérdida
            perdida_iteracion += (etiqueta_real - salida) ** 2

            # Actualizar pesos si es necesario
            if salida != etiqueta_real:
                error = etiqueta_real - salida
                for i in range(len(entradas)):
                    pesos[i] += tasa_aprendizaje * error * entradas[i]
                pesos[-1] += tasa_aprendizaje * error
                aprendiendo = True

        # Almacenar la pérdida de esta iteración
        iteraciones.append(iteracion)
        perdidas.append(perdida_iteracion)

        # Salir del bucle si no hay errores de clasificación
        if not aprendiendo or iteracion >= iteraciones_max:
            break

    return iteraciones, perdidas

def perceptron():
    carpeta_con_imagenes = filedialog.askdirectory(title="Selecciona la carpeta con las imágenes de prueba")  # Seleccionar carpeta
    if not carpeta_con_imagenes:
        return

    original = entrada_original.get()
    if not original:
        messagebox.showwarning("Advertencia", "Por favor, seleccione la imagen original.")
        return
    
    imagenes_bmp_en_carpeta = leerImagenesBmpEnCarpeta(carpeta_con_imagenes)
    datos_entrenamiento = []

    original_caracteristicas = convertir_aCaracteristicas(original)
    if not validar_dimensiones([original_caracteristicas] + imagenes_bmp_en_carpeta):
        messagebox.showerror("Error", "Las imágenes no tienen las mismas dimensiones")
        return

    # Preparar datos de entrenamiento
    for ruta_imagen, _, _, _ in imagenes_bmp_en_carpeta:
        caracteristicas = convertir_aCaracteristicas(ruta_imagen)
        etiqueta = 1 if ruta_imagen == original else 0  # Etiqueta 1 para la imagen original, 0 para las demás
        datos_entrenamiento.append(caracteristicas + [etiqueta])

    # Inicializar pesos aleatorios
    num_caracteristicas = len(datos_entrenamiento[0]) - 1  
    pesos = [random.uniform(-1, 1) for _ in range(num_caracteristicas + 1)]  # +1 para el sesgo

    # Parámetros del perceptrón
    tasa_aprendizaje = 0.3
    iteraciones_max = 1000

    # Obtener la función de pérdida durante el entrenamiento
    iteraciones, perdidas = obtener_funcion_perdida(datos_entrenamiento, pesos, tasa_aprendizaje, iteraciones_max)

    # Mostrar pesos finales
    messagebox.showinfo("Resultado", f"Pesos finales: {pesos}")

    # Clasificación de nuevas imágenes
    pruebas = leerImagenesBmpEnCarpeta(carpeta_con_imagenes)
    resultados = ""
    for ruta_imagen, _, _, _ in pruebas:
        caracteristicas = convertir_aCaracteristicas(ruta_imagen)
        suma_ponderada = sum(w * x for w, x in zip(pesos[:-1], caracteristicas)) + pesos[-1]
        salida = 1 if suma_ponderada > 0 else 0
        resultados += f"Imagen: {ruta_imagen}, Predicción: {salida}, Suma ponderada: {suma_ponderada}\n"
    
    messagebox.showinfo("Resultado", resultados)

def seleccionar_imagen(tipo):
    archivo = filedialog.askopenfilename(filetypes=[("Image files", "*.bmp")])
    if archivo:
        if tipo == "original":
            entrada_original.set(archivo)
        elif tipo == "prueba":
            entrada_prueba.set(archivo)

def ejecutar_exhaustiva():
    original = entrada_original.get()
    prueba = entrada_prueba.get()
    if original and prueba:
        exhaustiva(original, prueba)
    else:
        messagebox.showwarning("Advertencia", "Por favor, seleccione ambas imágenes.")

def ejecutar_comparar():
    original = entrada_original.get()
    prueba = entrada_prueba.get()
    if original and prueba:
        comparar_imagenes(original, prueba)
    else:
        messagebox.showwarning("Advertencia", "Por favor, seleccione ambas imágenes.")

# Crear la ventana principal
root = tk.Tk()
root.title("Comparación de Imágenes BMP")

# Variables para las rutas de las imágenes
entrada_original = tk.StringVar()
entrada_prueba = tk.StringVar()

# Crear y organizar los widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label_original = tk.Label(frame, text="Imagen Original:")
label_original.grid(row=0, column=0, sticky="e")
entry_original = tk.Entry(frame, textvariable=entrada_original, width=50)
entry_original.grid(row=0, column=1, padx=5)
button_original = tk.Button(frame, text="Seleccionar", command=lambda: seleccionar_imagen("original"))
button_original.grid(row=0, column=2, padx=5)

label_prueba = tk.Label(frame, text="Imagen de Prueba:")
label_prueba.grid(row=1, column=0, sticky="e")
entry_prueba = tk.Entry(frame, textvariable=entrada_prueba, width=50)
entry_prueba.grid(row=1, column=1, padx=5)
button_prueba = tk.Button(frame, text="Seleccionar", command=lambda: seleccionar_imagen("prueba"))
button_prueba.grid(row=1, column=2, padx=5)

button_exhaustiva = tk.Button(frame, text="Comparación Exhaustiva", command=ejecutar_exhaustiva)
button_exhaustiva.grid(row=2, column=0, columnspan=3, pady=5)

button_comparar = tk.Button(frame, text="Comparar Porcentaje", command=ejecutar_comparar)
button_comparar.grid(row=3, column=0, columnspan=3, pady=5)

button_perceptron = tk.Button(frame, text="Ejecutar Perceptrón", command=perceptron)
button_perceptron.grid(row=4, column=0, columnspan=3, pady=5)

# Iniciar el bucle principal de la interfaz
root.mainloop()
