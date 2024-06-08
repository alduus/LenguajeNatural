import pandas as pd

# Datos de los cuentos
cuentos = {
    "Nombre del cuento": ["El Bosque Encantado", "La Princesa y el Dragón", "El Reloj Mágico", "La Isla Misteriosa", "El Gato y la Luna"],
    "Cuento": [
        "Había una vez un bosque encantado donde los árboles hablaban y los animales podían volar. Un día, un joven aventurero llamado Lucas se adentró en el bosque y descubrió un árbol mágico que le concedía deseos. Lucas deseó poder volar y, al instante, se elevó por los aires, explorando el bosque desde arriba y viviendo emocionantes aventuras.",
        "En un lejano reino, una valiente princesa llamada Isabel decidió enfrentarse a un temible dragón que aterrorizaba a su pueblo. Armada con su espada y su valentía, Isabel logró derrotar al dragón y liberó al reino de su amenaza. El rey, en agradecimiento, la nombró caballera y celebraron una gran fiesta en su honor.",
        "Un anciano relojero encontró un reloj mágico en una tienda de antigüedades. Cada vez que el reloj marcaba la medianoche, transportaba al relojero a un momento diferente en la historia. Viajó a la época de los dinosaurios, al antiguo Egipto y al futuro, aprendiendo valiosas lecciones en cada viaje y haciendo nuevos amigos en cada era.",
        "Un grupo de amigos encontró un mapa antiguo que los llevó a una isla misteriosa en medio del océano. En la isla, descubrieron tesoros escondidos y secretos olvidados. Con la ayuda de los habitantes locales, los amigos desentrañaron los misterios de la isla y regresaron a casa con historias increíbles y nuevas amistades.",
        "Una noche, un gato callejero llamado Felix se encontró con la Luna, que había descendido a la Tierra para jugar. Juntos, el gato y la Luna vivieron una noche mágica, corriendo por los tejados y saltando entre las estrellas. Al amanecer, la Luna regresó al cielo, prometiendo a Felix que siempre estaría allí para iluminar sus noches."
    ]
}

# Crear el DataFrame
df_cuentos = pd.DataFrame(cuentos)

# Guardar en un archivo CSV
df_cuentos.to_csv("/Users/aldoescamillaresendiz/Documents/Python/5to Semestre/Lenguaje Natural/cuentos.csv", index=False)

