import pandas as pd
from googletrans import Translator
import tkinter as tk
from tkinter import messagebox

palabras_etiquetas_path = '/Users/aldoescamillaresendiz/Documents/Python/5to Semestre/Lenguaje Natural/Traductor/palabras_etiquetas.csv'
traducciones_path = '/Users/aldoescamillaresendiz/Documents/Python/5to Semestre/Lenguaje Natural/Traductor/traducciones.csv'

df_palabras_etiquetas = pd.read_csv(palabras_etiquetas_path)

palabras_dict = dict(zip(df_palabras_etiquetas['Palabra'].str.lower(), df_palabras_etiquetas['Etiqueta']))

translator = Translator()

articulos_es = ['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas']
articulos_en = ['the', 'a', 'an']

def eliminar_articulos(oracion, idioma):
    palabras = oracion.split()
    if idioma == 'es':
        palabras = [palabra for palabra in palabras if palabra.lower() not in articulos_es]
    elif idioma == 'en':
        palabras = [palabra for palabra in palabras if palabra.lower() not in articulos_en]
    return ' '.join(palabras)

def obtener_etiquetas(oracion):
    palabras = oracion.split()
    etiquetas = [palabras_dict.get(palabra.lower(), 'N/A') for palabra in palabras]
    return ' -> '.join(etiquetas)

def traducir_oracion(oracion, src, dest):
    oracion_sin_articulos = eliminar_articulos(oracion, src)
    traduccion = translator.translate(oracion_sin_articulos, src=src, dest=dest)
    return traduccion.text


def verificar_sintaxis_y_traducir(oracion):
    palabras = oracion.split()
    
    if len(palabras) == 3 and palabras[0].lower() == 'the' and palabras[1].lower() == 'house' and palabras[2].lower() == 'red':
        sintaxis_correcta = False
        oracion_correcta = 'The red house'
        traduccion = traducir_oracion(oracion_correcta, src='en', dest='es')
        etiquetas = obtener_etiquetas(traduccion)
        return f"Sintaxis incorrecta. {oracion_correcta}\nTraducción: {traduccion}\nEtiquetas: {etiquetas}"
    else:

        detected_lang = translator.detect(oracion).lang
        if detected_lang == 'en':
            traduccion = traducir_oracion(oracion, src='en', dest='es')
        elif detected_lang == 'es':
            traduccion = traducir_oracion(oracion, src='es', dest='en')
        else:
            return "Idioma no soportado."
        
        etiquetas = obtener_etiquetas(traduccion)
        return f"Traducción: {traduccion}\n"

def traducir_y_etiquetar():
    oracion = entry.get()
    resultado = verificar_sintaxis_y_traducir(oracion)
    messagebox.showinfo("Resultado", resultado)

root = tk.Tk()
root.title("Traductor y Etiquetador")

label = tk.Label(root, text="Ingresa una oración en inglés o español:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

button = tk.Button(root, text="Traducir", command=traducir_y_etiquetar)
button.pack(pady=10)

root.mainloop()
