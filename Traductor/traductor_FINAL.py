import tkinter as tk
from tkinter import messagebox
import csv
import subprocess

# Función para cargar vocabulario desde un archivo CSV
def cargar_vocabulario_csv(nombre_archivo):
    vocabulario = {
        'espanol': {'palabras': [], 'etiquetas': []},
        'ingles': {'palabras': [], 'etiquetas': []}
    }
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:
            vocabulario['espanol']['palabras'].append(row['palabra_espanol'])
            vocabulario['espanol']['etiquetas'].append(row['etiqueta_espanol'])
            vocabulario['ingles']['palabras'].append(row['palabra_ingles'])
            vocabulario['ingles']['etiquetas'].append(row['etiqueta_ingles'])
    return vocabulario

# Cargar el vocabulario desde el archivo CSV
vocabulario = cargar_vocabulario_csv("/Users/aldoescamillaresendiz/Documents/Python/5to Semestre/Lenguaje Natural/yolo.csv")

palabrasEspanol = vocabulario['espanol']['palabras']
etiquetasEspanol = vocabulario['espanol']['etiquetas']
palabrasIngles = vocabulario['ingles']['palabras']
etiquetasIngles = vocabulario['ingles']['etiquetas']

# Función para encontrar la etiqueta de una palabra dada
def buscar_etiqueta(palabra, idioma):
    palabra = palabra.lower().capitalize()  # Normalizar la palabra a capitalización estándar
    if palabra in vocabulario[idioma]['palabras']:
        indice = vocabulario[idioma]['palabras'].index(palabra)
        return vocabulario[idioma]['etiquetas'][indice]
    return None

# Función para traducir una palabra dada
def traducir_palabra(palabra, idioma_origen, idioma_destino):
    palabra = palabra.lower().capitalize()
    if palabra in vocabulario[idioma_origen]['palabras']:
        indice = vocabulario[idioma_origen]['palabras'].index(palabra)
        return vocabulario[idioma_destino]['palabras'][indice]
    return palabra  # Si no se encuentra la traducción, retornar la palabra original

# Función para traducir una oración
def traducir_oracion(oracion, idioma_origen, idioma_destino):
    palabras = oracion.split()
    traduccion = [traducir_palabra(palabra, idioma_origen, idioma_destino) for palabra in palabras]
    return " ".join(traduccion)

# Función para cargar reglas desde un archivo
def cargar_reglas(nombre_archivo="reglas.txt"):
    reglas = {}
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.replace('-->', '->').strip()
            if "->" in linea:
                secuencia_es, secuencia_en = linea.split("->")
                reglas[secuencia_es.strip()] = secuencia_en.strip()
                reglas[secuencia_en.strip()] = secuencia_es.strip()  # Añadir regla inversa
    return reglas

# Función para procesar oraciones y extraer reglas
def procesar_oraciones(oracion_es, oracion_en):
    palabras_es = oracion_es.split()
    palabras_en = oracion_en.split()
    etiquetas_es = [buscar_etiqueta(palabra, 'espanol') for palabra in palabras_es]
    etiquetas_en = [buscar_etiqueta(palabra, 'ingles') for palabra in palabras_en]
    
    if None in etiquetas_es or None in etiquetas_en:
        messagebox.showerror("Error", "Algunas palabras no tienen etiqueta. Revisa las oraciones.")
    else:
        secuencia_es = " ".join(etiquetas_es)
        secuencia_en = " ".join(etiquetas_en)
        regla = f"{secuencia_es} --> {secuencia_en}"
        messagebox.showinfo("Regla extraída", f"Regla: {regla}")
        guardar_regla(regla)

# Función para guardar las reglas en un archivo
def guardar_regla(regla):
    with open("reglas.txt", "a", encoding="utf-8") as archivo:
        archivo.write(regla + "\n")

# Función para agregar nuevas palabras y etiquetas
def agregar_palabra(palabra_es, etiqueta_es, palabra_en, etiqueta_en):
    if palabra_es not in palabrasEspanol:
        palabrasEspanol.append(palabra_es.capitalize())
        etiquetasEspanol.append(etiqueta_es)
    if palabra_en not in palabrasIngles:
        palabrasIngles.append(palabra_en.capitalize())
        etiquetasIngles.append(etiqueta_en)
    # Actualizar el vocabulario
    vocabulario['espanol']['palabras'] = palabrasEspanol
    vocabulario['espanol']['etiquetas'] = etiquetasEspanol
    vocabulario['ingles']['palabras'] = palabrasIngles
    vocabulario['ingles']['etiquetas'] = etiquetasIngles
    messagebox.showinfo("Éxito", f"Palabras y etiquetas agregadas: {palabra_es} - {etiqueta_es}, {palabra_en} - {etiqueta_en}")

# Función para guardar vocabulario en un archivo CSV
def guardar_vocabulario_csv():
    with open("vocabulario.csv", "w", newline='', encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["palabra_espanol", "etiqueta_espanol", "palabra_ingles", "etiqueta_ingles"])
        for i in range(len(palabrasEspanol)):
            palabra_es = palabrasEspanol[i]
            etiqueta_es = etiquetasEspanol[i]
            palabra_en = palabrasIngles[i] if i < len(palabrasIngles) else ""
            etiqueta_en = etiquetasIngles[i] if i < len(etiquetasIngles) else ""
            writer.writerow([palabra_es, etiqueta_es, palabra_en, etiqueta_en])
    messagebox.showinfo("Éxito", "Vocabulario guardado en vocabulario.csv")

# Función para traducir usando las reglas gramaticales avanzadas
def traducir_con_P6(oracion, idioma_origen, idioma_destino):
    # Llamar al archivo Python externo
    subprocess.run(["python3", "p6gui.py"])

# Función para cargar y ejecutar el script adjunto
def ejecutar_parte3():
    script_path = "/Users/aldoescamillaresendiz/Documents/Python/5to Semestre/Lenguaje Natural/traductormodificado.py"
    subprocess.run(["python3", script_path])

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Procesador de Oraciones")

# Widgets para la entrada de oraciones en inglés y su traducción
tk.Label(root, text="Oración en Inglés:").grid(row=0, column=0)
entrada_en_es = tk.Entry(root, width=50)
entrada_en_es.grid(row=0, column=1)

tk.Label(root, text="Traducción en Español:").grid(row=1, column=0)
traduccion_es = tk.Entry(root, width=50)
traduccion_es.grid(row=1, column=1)

# Widgets para la entrada de oraciones en español y su traducción
tk.Label(root, text="Oración en Español:").grid(row=2, column=0)
entrada_es = tk.Entry(root, width=50)
entrada_es.grid(row=2, column=1)

tk.Label(root, text="Traducción en Inglés:").grid(row=3, column=0)
entrada_en = tk.Entry(root, width=50)
entrada_en.grid(row=3, column=1)

# Botón para procesar oraciones
btn_procesar = tk.Button(root, text="Procesar Oraciones", command=lambda: procesar_oraciones(entrada_es.get(), entrada_en.get()))
btn_procesar.grid(row=4, column=0, columnspan=2)

# Widgets para agregar nuevas palabras
tk.Label(root, text="Nueva palabra en Español:").grid(row=5, column=0)
nueva_palabra_es = tk.Entry(root, width=20)
nueva_palabra_es.grid(row=5, column=1)

tk.Label(root, text="Etiqueta:").grid(row=6, column=0)
nueva_etiqueta_es = tk.Entry(root, width=20)
nueva_etiqueta_es.grid(row=6, column=1)

tk.Label(root, text="Nueva palabra en Inglés:").grid(row=7, column=0)
nueva_palabra_en = tk.Entry(root, width=20)
nueva_palabra_en.grid(row=7, column=1)

tk.Label(root, text="Etiqueta:").grid(row=8, column=0)
nueva_etiqueta_en = tk.Entry(root, width=20)
nueva_etiqueta_en.grid(row=8, column=1)

# Botón para agregar palabras
btn_agregar = tk.Button(root, text="Agregar Palabras", command=lambda: agregar_palabra(nueva_palabra_es.get(), nueva_etiqueta_es.get(), nueva_palabra_en.get(), nueva_etiqueta_en.get()))
btn_agregar.grid(row=9, column=0, columnspan=2)

# Botón para guardar vocabulario en CSV
btn_guardar_csv = tk.Button(root, text="Guardar Vocabulario en CSV", command=guardar_vocabulario_csv)
btn_guardar_csv.grid(row=10, column=0, columnspan=2)

# Botón para traducir oración del español al inglés
btn_traducir_en = tk.Button(root, text="Traducir al Inglés Sin Gramatica", command=lambda: messagebox.showinfo("Traducción", traducir_oracion(entrada_es.get(), 'espanol', 'ingles')))
btn_traducir_en.grid(row=11, column=0, columnspan=2)

# Botón para traducir oración del inglés al español
btn_traducir_es = tk.Button(root, text="Traducir al Español Sin Gramatica", command=lambda: messagebox.showinfo("Traducción", traducir_oracion(entrada_en_es.get(), 'ingles', 'espanol')))
btn_traducir_es.grid(row=12, column=0, columnspan=2)

# Botón para traducir usando las reglas gramaticales avanzadas
btn_traducir_con_P6 = tk.Button(root, text="Traducir Gramaticalmente", command=lambda: traducir_con_P6(entrada_en_es.get(), 'ingles', 'espanol'))
btn_traducir_con_P6.grid(row=13, column=0, columnspan=2)

# Botón para regresar a la parte 3
btn_regresar_parte3 = tk.Button(root, text="Regresar a la Parte 3", command=ejecutar_parte3)
btn_regresar_parte3.grid(row=14, column=0, columnspan=2)

root.mainloop()
