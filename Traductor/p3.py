import tkinter as tk
from tkinter import simpledialog, messagebox, StringVar
import csv
import os

def cargar_traducciones(archivo):
    traducciones = {}
    with open(archivo, 'r', encoding='utf-8') as file:
        next(file)  # Saltar la cabecera del archivo
        for linea in file:
            ingles, espanol = linea.strip().split(',')
            traducciones[ingles] = espanol
            traducciones[espanol] = ingles  
    return traducciones

def cargar_selecciones(archivo):
    selecciones = {}
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for fila in reader:
                palabra, count = fila
                selecciones[palabra] = int(count)
    return selecciones

def guardar_selecciones(selecciones, archivo):
    with open(archivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for palabra, count in selecciones.items():
            writer.writerow([palabra, count])

def obtener_etiquetas(oracion, traducciones):
    palabras = oracion.lower().split()
    etiquetas = [traducciones.get(palabra, "No se encontró etiqueta") for palabra in palabras]
    return " -> ".join(etiquetas)

def mostrar_etiquetas():
    oracion = simpledialog.askstring("Ingresar oración", "Ingresa una oración:")
    if oracion:
        etiquetas = obtener_etiquetas(oracion, traducciones)
        messagebox.showinfo("Etiquetas", f"Etiquetas: {etiquetas}")

def distancia_levenshtein(s1, s2):
    if len(s1) < len(s2):
        return distancia_levenshtein(s2, s1)
    if not s1:
        return len(s2)
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        prev_row = current_row
    return prev_row[-1]

def actualizar_traduccion(palabra=None):
    if palabra:
        variable_palabra.set(palabra)
    traduccion = traducciones.get(variable_palabra.get().lower(), "No se encontró la traducción")
    etiqueta_traduccion.config(text=f"Traducción: {traduccion}")

def sugerir_palabras(palabra, diccionario):
    sugerencias = []
    distancia_minima = float('inf')
    for key in diccionario.keys():
        distancia = distancia_levenshtein(palabra, key)
        if distancia < distancia_minima:
            distancia_minima = distancia
            sugerencias = [key]
        elif distancia == distancia_minima:
            sugerencias.append(key)
    return sugerencias if distancia_minima <= 2 else []

def actualizar_menu_sugerencias(sugerencias):
    sugerencias.sort(key=lambda s: selecciones.get(s, 0), reverse=True)
    menu_sugerencias['menu'].delete(0, 'end')
    for s in sugerencias:
        menu_sugerencias['menu'].add_command(label=s, command=lambda s=s: seleccionar_sugerencia(s))

def seleccionar_sugerencia(sugerencia):
    selecciones[sugerencia] = selecciones.get(sugerencia, 0) + 1
    guardar_selecciones(selecciones, archivo_selecciones)
    actualizar_traduccion(sugerencia)

def traducir():
    palabra = entrada_palabra.get().lower()
    if palabra not in traducciones:
        guardar_palabra_incorrecta(palabra)
        sugerencias = sugerir_palabras(palabra, traducciones)
        if sugerencias:
            actualizar_menu_sugerencias(sugerencias)
            variable_palabra.set("Selecciona una palabra sugerida")
            return
    actualizar_traduccion(palabra)

def agregar_palabra():
    nueva_palabra = simpledialog.askstring("Nueva Palabra", "Ingresa la palabra en inglés:")
    nueva_traduccion = simpledialog.askstring("Nueva Traducción", "Ingresa la traducción en español:")
    if nueva_palabra and nueva_traduccion:
        with open('traducciones.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([nueva_palabra.lower(), nueva_traduccion.lower()])
        traducciones[nueva_palabra.lower()] = nueva_traduccion.lower()
        traducciones[nueva_traduccion.lower()] = nueva_palabra.lower()
        messagebox.showinfo("Guardado", "Palabra y traducción añadidas correctamente.")
    else:
        messagebox.showerror("Error", "Ambos campos deben ser llenados.")

def guardar_palabra_incorrecta(palabra):
    archivo_incorrectas = 'palabras_incorrectas.csv'
    if os.path.exists(archivo_incorrectas):
        with open(archivo_incorrectas, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            palabras = {rows[0]: int(rows[1]) for rows in reader}
    else:
        palabras = {}

    if palabra in palabras:
        palabras[palabra] += 1
    else:
        palabras[palabra] = 1

    with open(archivo_incorrectas, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in palabras.items():
            writer.writerow([key, value])

archivo_selecciones = 'selecciones.csv'
traducciones = cargar_traducciones('/Users/aldoescamillaresendiz/Documents/Python/5to Semestre/Lenguaje Natural/TraductorChido/traducciones.csv')
selecciones = cargar_selecciones(archivo_selecciones)

root = tk.Tk()
root.title("Traductor Inglés-Español")
root.geometry("400x350")

variable_palabra = StringVar(root)
variable_palabra.trace("w", lambda *args: actualizar_traduccion())

etiqueta_intro = tk.Label(root, text="Ingresa la palabra que quieres traducir:")
etiqueta_intro.pack(pady=5)

entrada_palabra = tk.Entry(root, width=50)
entrada_palabra.pack(pady=5)

boton_traducir = tk.Button(root, text="Traducir", command=traducir)
boton_traducir.pack(pady=5)

etiqueta_traduccion = tk.Label(root, text="Traducción: ")
etiqueta_traduccion.pack(pady=5)

menu_sugerencias = tk.OptionMenu(root, variable_palabra, "Selecciona una palabra sugerida")
menu_sugerencias.pack(pady=5)

boton_agregar = tk.Button(root, text="Agregar Nueva Palabra", command=agregar_palabra)
boton_agregar.pack(pady=5)

root.mainloop()
