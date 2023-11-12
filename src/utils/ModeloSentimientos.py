from src.utils.frecuenciasSentimientos import frecuencias

def Clasifica(texto: str) -> str: # Input - un string con la oracion a clasificar
    # Preprocesado
    textoProcesado = []
    for palabra in texto.split(): #tokenizando
        # eliminando stopwords
        stopwords = ["de", "en", "a", "y", "la", "el", "muy", "me", "un"]
        if palabra in stopwords: 
            continue
        # pasando a minusculas
        palabra = palabra.lower() 
        # limpiando tildes, puntuaciones, etc
        palabra = palabra.replace("á", "a")
        palabra = palabra.replace("é", "e")
        palabra = palabra.replace("í", "i")
        palabra = palabra.replace("ó", "o")
        palabra = palabra.replace("ú", "u")
        palabra = palabra.replace(".", "")
        palabra = palabra.replace("!", "")
        palabra = palabra.replace("?", "")
        palabra = palabra.replace("¿", "")
        palabra = palabra.replace("¡", "")
        # chequeo final
        if not palabra.isalpha():
            continue 
        # texto final
        textoProcesado.append(palabra)

    # Modelo
    frecuenciasPositivas = 0 # textos 
    frecuenciasNegativas = 0
    frecuenciasAgresivas = 0

    for palabra in textoProcesado:
        lista = frecuencias.get(palabra, [0, 0, 0])
        frecuenciasPositivas += lista[0]/42000
        frecuenciasNegativas += lista[1]/42000
        frecuenciasAgresivas += lista[2]/42000

    w = [4.286724389731548, 2.088413170199017, 14.188418043863404]
    b = [0.0080000000020, 0.000000000010, 0.0000000000012]
    
    z1 = frecuenciasPositivas*w[0]+b[0] # sumatoria
    z2 = frecuenciasNegativas*w[1]+b[1]
    z3 = frecuenciasAgresivas*w[2]+b[2]

    a1 = 1/(1+1.71828**-z1) # sigmoid
    a2 = 1/(1+1.71828**-z2)
    a3 = 1/(1+1.71828**-z3)

    sentimiento = ""
    score = 0.0
    # regreso el numero? ej 0 es positivo, 1 es negativo y 2 agresivo. o un string?
    if   (a1 >= a2 and a1 >= a3): sentimiento, score = 1, a1 * 100 
    elif (a2 >= a1 and a2 >= a3): sentimiento, score = 2, a2 * 100
    elif (a3 >= a1 and a3 >= a2): sentimiento, score = 3, a3 * 100
    
    return sentimiento, score

if __name__=='__main__':
    message = 'No me gusta'
    print(message, Clasifica(message))