import csv
import random
from collections import Counter, defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def construir_ngramas(palabras, n):
    ngramas = defaultdict(list)
    for i in range(len(palabras) - n):
        key = tuple(palabras[i:i+n])
        next_word = palabras[i + n]
        ngramas[key].append(next_word)
    return ngramas

def contar_frecuencias_ngramas(ngramas):
    frecuencias = defaultdict(Counter)
    for key, words in ngramas.items():
        frecuencias[key] = Counter(words)
    return frecuencias

def predecir_palabra(ngramas, historial):
    key = tuple(historial)
    if key in ngramas:
        return random.choice(ngramas[key])
    else:
        return random.choice(list(ngramas.keys()))[0]

def cargar_archivo():
    ruta_archivo = filedialog.askopenfilename()
    if ruta_archivo:
        letras = []
        with open(ruta_archivo, newline='', encoding='ISO-8859-1') as csvfile:
            lector = csv.DictReader(csvfile)
            for fila in lector:
                letras.append(fila['cuento'])

        linea = ' '.join(letras)
        palabras = linea.split()

        frecuencias = Counter(palabras)

        palabra_mas_comun = frecuencias.most_common(1)[0]
        
        numero_palabras = simpledialog.askinteger("Input", "¿Cuántas palabras más usadas quiere ver?")
        palabras_mas_comunes = frecuencias.most_common(numero_palabras)

        result_text.set(f"Las {numero_palabras} palabras más usadas y sus frecuencias:\n" +
                        '\n'.join([f"{palabra}: {frecuencia} veces" for palabra, frecuencia in palabras_mas_comunes]))

        n = simpledialog.askinteger("Input", "Gramas para la predicción (1-5):")
        tamaño = simpledialog.askinteger("Input", "¿Cuántas palabras se generarán?:")

        ngramas = construir_ngramas(palabras, n)
        frecuencias_ngramas = contar_frecuencias_ngramas(ngramas)

        imprimir = 'Había'
        historial = [imprimir] * n

        with open('resultado.txt', 'w', encoding='utf-8') as archivo:
            
            # Escribir las palabras más comunes
            archivo.write(f"Las {numero_palabras} palabras más usadas y sus frecuencias:\n")
            for palabra, frecuencia in palabras_mas_comunes:
                archivo.write(f"{palabra}: {frecuencia} veces\n")
            
            # Generar el texto y escribirlo
            archivo.write("\nTexto generado:\n")
            archivo.write(imprimir + ' ')
            for _ in range(tamaño - 1):
                siguiente = predecir_palabra(ngramas, historial[-n:])
                historial.append(siguiente)
                archivo.write(siguiente + ' ')
            archivo.write("\n\n")

            # Escribir las frecuencias de los n-gramas
            archivo.write("Frecuencias de los n-gramas:\n")
            for key, counter in frecuencias_ngramas.items():
                archivo.write(f"{' '.join(key)}:\n")
                for word, freq in counter.items():
                    archivo.write(f"  {word}: {freq} veces\n")

        messagebox.showinfo("Éxito", "El texto generado y las estadísticas se han guardado correctamente en 'resultado.txt'.")

app = tk.Tk()
app.title("Generador de Texto con N-gramas")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

cargar_btn = tk.Button(frame, text="Cargar archivo CSV", command=cargar_archivo)
cargar_btn.pack(pady=5)

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, justify="left")
result_label.pack(pady=5)

app.mainloop()
