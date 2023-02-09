import os
import spacy
import math
import sys

pipelineCatala = spacy.load("ca_core_news_trf")

def llegirDades(dades):
    #lista todos los archivos que hay dentro de la carpeta indicada
    contenido = os.listdir(dades)
    diccionario={}
    #dentro de la carpeta va recoriendo todos los archivos para leerlos con utf-8 i quitarle el .txt
    for i in contenido:
        with open(dades + '/' + i, encoding = 'UTF8') as f:
            archivo= f.read()
        diccionario[i.replace('.txt', '')] = archivo
    return diccionario
#le indico cual va a ser la carpeta leida            
dades=llegirDades("./dades")


#analizamos los textos y extraemos las palabras poco comunes con un dicionario en catalan ya creado,
def extreuArrels(analitzar):
    tokens=pipelineCatala(analitzar)
    palabrasPC=[]
    #por cada palabra extraida de la frase analiza si es poco comun o no y si es poco comun la guarda en una lista
    for token in tokens:
        if token.is_stop == False and token.is_punct == False:
            palabrasPC.append(token.lemma_)
    return palabrasPC



# creamos un diccionario para añadir las palabras poco comunes extraidas en la funcion anterior
def creaDiccionari(arrels):
    diccionarioA=[]
    diccionarioF=[]
    for i in arrels:
        diccionarioA.extend(extreuArrels(i))
    for i  in diccionarioA:
        if i not in diccionarioF:
            diccionarioF.append(i)
    return diccionarioF


# de las raices creadas los convertimos en vectores es decir en numeros 
def crearVector (diccionario, frase):
    vector=[]
    arrels=extreuArrels(frase)
    for i in diccionario:
        vector.append(arrels.count(i))
    return vector



# hacemos una raiz cuadrada y una operacion para normalizar los vectores anteriormente creados
def normalitzarVector(vector): # [1,3,0 1,2]
    suma = 0
    vNormalitzat=[]
    for i in vector:
        suma= suma + i*i
    arrel = math.sqrt(suma)
    for i in vector:
        vNormalitzat.append(i/arrel)
    
    return  vNormalitzat



# comparamos los numeros 
def similitudCosinus(v, u):
    suma1= 0
    #en la lengitud de v iremos multipilicando y sumandolo para ver cuanto parecido tienen entre si
    for i in range (len(v)):
        suma1 = suma1 + v[i] * u[i]
    return suma1



# para ver la similitud entre textos basicamente lo que hacemos es ir llamando a las funciones anteriores
def similitudTextos(diccionari, text1, text2):
    vector1=crearVector(diccionari,text1)
    vector2= crearVector(diccionari,text2)
    NrmVecTxt1= normalitzarVector(vector1)
    NrmVecTxt2= normalitzarVector(vector2)
    similitudC= similitudCosinus(NrmVecTxt1, NrmVecTxt2)
    return similitudC



def list (carpeta):
    lista= os.listdir(carpeta)
    return lista



def affinity (persona1, persona2):
    dades=llegirDades("./dades")
    dicionario = creaDiccionari(dades.values())
    similitud=similitudTextos(dicionario, dades[persona1], dades[persona2])
    similitud = int(similitud *100)
    porcentaje = f"{similitud}%"
    return porcentaje


def best(persona):
    max = 0
    dicionari= creaDiccionari(dades.values())
    for nom in dades:
        if nom != persona:
            similitud=similitudTextos(dicionari, dades[persona], dades[nom])
            if max < similitud:
                max = similitud
                maxNom = nom
    return maxNom


def worse (persona):
    min = 100
    dicionari= creaDiccionari(dades.values())
    for nom in dades:
        if nom != persona:
            similitud=similitudTextos(dicionari, dades[persona], dades[nom])
            if min >similitud:
                min = similitud
                minNom = nom
    return minNom