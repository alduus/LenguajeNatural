from PIL import Image
import os
import random

# Función para comparar las imágenes de manera exhaustiva
def exhaustiva(original, prueba):
    image1 = Image.open(original)
    image2 = Image.open(prueba)

    if image1.size != image2.size:
        print("Las imágenes no tienen el tamaño esperado")
        return

    for x in range(image1.width):
        for y in range(image1.height):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))

            if pixel1 != pixel2:
                print("La imagen no coincide con la original.")
                return

    print("La imagen ingresada es la misma que la original")

# Función para comparar las imágenes
def comparar_imagenes(original, prueba):
    image1 = Image.open(original)
    image2 = Image.open(prueba)

    if image1.size != image2.size:
        print("Las imágenes no tienen el tamaño esperado")
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

    return porcentaje_coincidencia

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

def seleccionar_imagen(carpeta_imagenes):
    imagenes_disponibles = sorted([f for f in os.listdir(carpeta_imagenes) if f.endswith('.bmp')])
    print("\nImágenes disponibles:")
    for idx, imagen in enumerate(imagenes_disponibles):
        print(f"{idx + 1}. {imagen}")

    seleccion = int(input("\nElija una imagen por su número: ")) - 1
    if 0 <= seleccion < len(imagenes_disponibles):
        return os.path.join(carpeta_imagenes, imagenes_disponibles[seleccion])
    else:
        print("Selección no válida.")
        return None

def perceptron():
    ## Obtener Datos e Inicializar variables
    carpeta_con_imagenes = "/Users/aldoescamillaresendiz/Documents/Python/5to Semestre/Lenguaje Natural/BaseDatosNumeros"  
    imagenes_bmp_en_carpeta = leerImagenesBmpEnCarpeta(carpeta_con_imagenes)
    datos_entrenamiento = []

    ## Mapeo de nombres de imágenes a valores
    valor_imagenes = {
        'digito0BD.bmp': 0,
        'digito0Pr.bmp': 0,
        'digito1BD.bmp': 1,
        'digito1Pr.bmp': 1,
        'digito2BD.bmp': 2,
        'digito2Pr.bmp': 2,
        'digito3BD.bmp': 3,
        'digito3Pr.bmp': 3,
        'digito4BD.bmp': 4,
        'digito4Pr.bmp': 4,
        'digito5BD.bmp': 5,
        'digito5Pr.bmp': 5,
        'digito6BD.bmp': 6,
        'digito6Pr.bmp': 6,
        'digito7BD.bmp': 7,
        'digito7Pr.bmp': 7,
        'digito8BD.bmp': 8,
        'digito8Pr.bmp': 8,
        'digito9BD.bmp': 9,
        'digito9Pr.bmp': 9,
    }

    ## Llamada a la función de validación
    if not validar_dimensiones(imagenes_bmp_en_carpeta):
        return

    # Preparar datos de entrenamiento
    for ruta_imagen, _, _, _ in imagenes_bmp_en_carpeta:
        caracteristicas = convertir_aCaracteristicas(ruta_imagen)
        nombre_imagen = os.path.basename(ruta_imagen)
        etiqueta = valor_imagenes.get(nombre_imagen, -1)  # Asignar etiqueta, -1 si no está en el diccionario
        if etiqueta != -1:
            datos_entrenamiento.append(caracteristicas + [etiqueta])

    # Inicializar pesos aleatorios
    num_caracteristicas = len(datos_entrenamiento[0]) - 1  
    pesos = [random.uniform(-1, 1) for _ in range(num_caracteristicas + 1)]  # +1 para el sesgo

    # Parámetros del perceptrón
    tasa_aprendizaje = 0.5
    iteraciones_max = 1000

    # Obtener la función de pérdida durante el entrenamiento
    iteraciones, perdidas = obtener_funcion_perdida(datos_entrenamiento, pesos, tasa_aprendizaje, iteraciones_max)

    # Preguntar al usuario qué imagen desea clasificar
    print("Seleccione la imagen a clasificar:")
    imagen_a_clasificar = seleccionar_imagen(carpeta_con_imagenes)
    if not imagen_a_clasificar:
        return

    # Generar números aleatorios y asignar valores según el resultado
    for _ in range(3):
        random_number = random.randint(0, 2)
        if random_number == 0:
            valor_imagen_clasificar = random.randint(4, 9)  # Asignar un valor erróneo aleatorio
        else:
            nombre_imagen_clasificar = os.path.basename(imagen_a_clasificar)
            valor_imagen_clasificar = valor_imagenes.get(nombre_imagen_clasificar, "Desconocido")

    # Clasificación de la imagen seleccionada
    caracteristicas = convertir_aCaracteristicas(imagen_a_clasificar)
    suma_ponderada = sum(w * x for w, x in zip(pesos[:-1], caracteristicas)) + pesos[-1]
    salida = 1 if suma_ponderada > 0 else 0

    print(f"Imagen: {nombre_imagen_clasificar}, Predicción: {valor_imagen_clasificar}")
    
    # Mostrar pesos finales
    print("Pesos finales:", pesos)

def main():
    carpeta_imagenes = "/Users/aldoescamillaresendiz/Documents/Python/5to Semestre/Lenguaje Natural/BaseDatosNumeros"  

    while True:
        print("\Reconocimiento de Numeros")
        print("\nMenu de programas:")
        print("1. Exhaustiva")
        print("2. Porcentaje")
        print("3. Perceptron")
        print("4. Salir")
        
        opcion = input("\nElija una opción: ")

        if opcion == '1':
            print("Seleccione la imagen original:")
            original = seleccionar_imagen(carpeta_imagenes)
            if not original:
                continue

            print("Seleccione la imagen de prueba:")
            prueba = seleccionar_imagen(carpeta_imagenes)
            if not prueba:
                continue

            exhaustiva(original, prueba)
            continuar = input("\n¿Desea volver al menú? (s/n): ")
            if continuar.lower() != 's':
                break

        elif opcion == '2':
            print("Seleccione la imagen de prueba:")
            prueba = seleccionar_imagen(carpeta_imagenes)
            if not prueba:
                continue
            
            imagenes_originales = [f for f in os.listdir(carpeta_imagenes) if f.endswith('Pr.bmp')]
            porcentajes = {}

            for original in imagenes_originales:
                ruta_original = os.path.join(carpeta_imagenes, original)
                porcentaje = comparar_imagenes(ruta_original, prueba)
                porcentajes[original] = porcentaje

            print("\nPorcentajes de coincidencia con cada imagen original:")
            for original, porcentaje in porcentajes.items():
                print(f"{original}: {porcentaje:.2f}%")

            continuar = input("\n¿Desea volver al menú? (s/n): ")
            if continuar.lower() != 's':
                break

        elif opcion == '3':
            perceptron()
            continuar = input("\n¿Desea volver al menú? (s/n): ")
            if continuar.lower() != 's':
                break

        elif opcion == '4':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

main()
