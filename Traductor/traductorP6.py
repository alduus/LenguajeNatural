import tkinter as tk
from tkinter import messagebox
import csv

# Vocabulario en español e inglés con sus correspondientes etiquetas
vocabulario = {
    'espanol': {
        'palabras': ["El", "La", "Los", "Las", "Un", "Una", "Unos", "Unas", "Yo", "Tú", "Él", "Ella", "Nosotros", "Nosotras", "Vosotros", "Vosotras", "Ellos", "Ellas", "Casa", "Roja", "Sol", "Y", "Arcoiris", "Son", "Luz", "Flor", "Grande", "Amarillo",
                     "Perro", "Gato", "Coche", "Pequeño", "Azul", "Cielo", "Nube", "Llueve", "Verde", "Árbol", "Río", 
                     "Montaña", "Nieve", "Frío", "Calor", "Mar", "Playa", "Nadar", "Correr", "Jugar", "Feliz", 
                     "Triste", "Pájaro", "Cantar", "Bailar", "Amigo", "Familia", "Escuela", "Trabajo", "Comida", 
                     "Bebida", "Libro", "Música", "Película", "Deporte", "Viajar", "Vuelo", "Tren", "Autobús", 
                     "Parque", "Ciudad", "País", "Continente", "Océano", "Universo", "Estrella", "Luna", "Planeta", 
                     "Galaxia", "Espacio", "Tiempo", "Reloj", "Calendario", "Historia", "Cultura", "Arte", "Pintura", 
                     "Escultura", "Museo", "Teatro", "Cine", "Biblioteca", "Pluma", "Papel", "Escribir", "Leer", 
                     "Estudiar", "Examen", "Notas", "Clase", "Profesor", "Alumno", "Escuchar", "Hablar", "Ver", 
                     "Oír", "Sentir", "Pensar", "Creer", "Entender", "Aprender", "Conocer", "Descubrir", "Inventar"],
        'etiquetas': ["Ar", "Ar", "Ar", "Ar", "Ar", "Ar", "Ar", "Ar", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "S", "Ad", "S", "C", "S", "V", "V", "S", "Ad", "Ad",
                      "S", "S", "S", "Ad", "Ad", "S", "S", "V", "Ad", "S", "S", "S", "S", "Ad", "S", "S", "S", "S", "V", "V", "V", 
                      "V", "Ad", "Ad", "S", "V", "V", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "V", "S", "S", 
                      "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", 
                      "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "V", 
                      "V", "V", "V", "V", "V", "V", "V"]
    },
    'ingles': {
        'palabras': ["The", "The", "The", "The", "A", "An", "Some", "Some", "I", "You", "He", "She", "We", "We", "You", "You", "They", "They", "House", "Red", "Sun", "And", "Rainbow", "Are", "Light", "Flower", "Big", "Yellow",
                     "Dog", "Cat", "Car", "Small", "Blue", "Sky", "Cloud", "Rain", "Green", "Tree", "River", "Mountain", 
                     "Snow", "Cold", "Heat", "Sea", "Beach", "Swim", "Run", "Play", "Happy", "Sad", "Bird", "Sing", 
                     "Dance", "Friend", "Family", "School", "Work", "Food", "Drink", "Book", "Music", "Movie", "Sport", 
                     "Travel", "Flight", "Train", "Bus", "Park", "City", "Country", "Continent", "Ocean", "Universe", 
                     "Star", "Moon", "Planet", "Galaxy", "Space", "Time", "Clock", "Calendar", "History", "Culture", 
                     "Art", "Painting", "Sculpture", "Museum", "Theater", "Cinema", "Library", "Pen", "Paper", "Write", 
                     "Read", "Study", "Exam", "Grades", "Class", "Teacher", "Student", "Listen", "Speak", "See", "Hear", 
                     "Feel", "Think", "Believe", "Understand", "Learn", "Know", "Discover", "Invent"],
        'etiquetas': ["Ar", "Ar", "Ar", "Ar", "Ar", "Ar", "Ar", "Ar", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "Pr", "S", "Ad", "S", "C", "S", "V", "V", "S", "Ad", "Ad",
                      "S", "S", "S", "Ad", "Ad", "S", "S", "V", "Ad", "S", "S", "S", "S", "Ad", "S", "S", "S", "S", "V", 
                      "V", "V", "V", "Ad", "Ad", "S", "V", "V", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "V", 
                      "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", 
                      "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", 
                      "V", "V", "V", "V", "V", "V", "V", "V"]
    }
}

palabrasEspanol = vocabulario['espanol']['palabras']
etiquetasEspanol = vocabulario['espanol']['etiquetas']
palabrasIngles = vocabulario['ingles']['palabras']
etiquetasIngles = vocabulario['ingles']['etiquetas']

# Función para encontrar la etiqueta de una palabra dada
def buscar_etiqueta(palabra, idioma):
    if palabra in vocabulario[idioma]['palabras']:
        indice = vocabulario[idioma]['palabras'].index(palabra)
        return vocabulario[idioma]['etiquetas'][indice]
    return None

# Función para cargar reglas desde un archivo
def cargar_reglas(nombre_archivo="reglas.txt"):
    reglas = {}
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.replace('-->', '->').strip()
            if "->" in linea:
                secuencia_es, secuencia_en = linea.split("->")
                reglas[secuencia_es.strip()] = secuencia_en.strip()
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
        palabrasEspanol.append(palabra_es)
        etiquetasEspanol.append(etiqueta_es)
    if palabra_en not in palabrasIngles:
        palabrasIngles.append(palabra_en)
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
        writer.writerow(["Palabra (Español)", "Etiqueta (Español)", "Palabra (Inglés)", "Etiqueta (Inglés)"])
        for i in range(len(palabrasEspanol)):
            palabra_es = palabrasEspanol[i]
            etiqueta_es = etiquetasEspanol[i]
            palabra_en = palabrasIngles[i] if i < len(palabrasIngles) else ""
            etiqueta_en = etiquetasIngles[i] if i < len(etiquetasIngles) else ""
            writer.writerow([palabra_es, etiqueta_es, palabra_en, etiqueta_en])
    messagebox.showinfo("Éxito", "Vocabulario guardado en vocabulario.csv")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Procesador de Oraciones")

# Widgets para la entrada de oraciones
tk.Label(root, text="Oración en Español:").grid(row=0, column=0)
entrada_es = tk.Entry(root, width=50)
entrada_es.grid(row=0, column=1)

tk.Label(root, text="Traducción en Inglés:").grid(row=1, column=0)
entrada_en = tk.Entry(root, width=50)
entrada_en.grid(row=1, column=1)

# Botón para procesar oraciones
btn_procesar = tk.Button(root, text="Procesar Oraciones", command=lambda: procesar_oraciones(entrada_es.get(), entrada_en.get()))
btn_procesar.grid(row=2, column=0, columnspan=2)

# Widgets para agregar nuevas palabras
tk.Label(root, text="Nueva palabra en Español:").grid(row=3, column=0)
nueva_palabra_es = tk.Entry(root, width=20)
nueva_palabra_es.grid(row=3, column=1)

tk.Label(root, text="Etiqueta:").grid(row=4, column=0)
nueva_etiqueta_es = tk.Entry(root, width=20)
nueva_etiqueta_es.grid(row=4, column=1)

tk.Label(root, text="Nueva palabra en Inglés:").grid(row=5, column=0)
nueva_palabra_en = tk.Entry(root, width=20)
nueva_palabra_en.grid(row=5, column=1)

tk.Label(root, text="Etiqueta:").grid(row=6, column=0)
nueva_etiqueta_en = tk.Entry(root, width=20)
nueva_etiqueta_en.grid(row=6, column=1)

# Botón para agregar palabras
btn_agregar = tk.Button(root, text="Agregar Palabras", command=lambda: agregar_palabra(nueva_palabra_es.get(), nueva_etiqueta_es.get(), nueva_palabra_en.get(), nueva_etiqueta_en.get()))
btn_agregar.grid(row=7, column=0, columnspan=2)

# Botón para guardar vocabulario en CSV
btn_guardar_csv = tk.Button(root, text="Guardar Vocabulario en CSV", command=guardar_vocabulario_csv)
btn_guardar_csv.grid(row=8, column=0, columnspan=2)

root.mainloop()
