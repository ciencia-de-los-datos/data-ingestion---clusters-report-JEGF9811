"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd

import re  #libreria para manejo de expresiones regulares

def cambiar_espacio(texto):
    patron=re.compile(r'\s+')
    texto=re.sub(pattern=patron,repl=' ',string=texto) #busco espacios (1 o +) y reemplazo con uno ' '
    texto=re.sub(pattern='\.',repl='',string=texto) #busco . y reemplazo con nada ''
    return texto

def cambiar_porcentaje(texto):
    patron=re.compile(r'(\d+),(\d+)\s%') #busca una secuencia digito + ,+ digito + espacio + %
    texto=re.sub(pattern=patron,repl=r'\1.\2',string=texto) #busco % y lo reemplazo con nada
    texto=float(texto)
    return texto

def quitar_decimal(num):
    num=int(num)
    return num

def ingest_data():

    df=pd.read_fwf('clusters_report.txt',skiprows=4,header=None) #evito las primeras 4 filas
    df.columns=['cluster','cantidad_de_palabras_clave','porcentaje_de_palabras_clave',
                'principales_palabras_clave']

    #definir las acciones de agrupacion y formateo de la columna de palabras clave
    df['principales_palabras_clave']=df.ffill().groupby('cluster')['principales_palabras_clave'].transform(lambda x:' '.join(x))
    df=df.dropna().reset_index(drop=True) #borrar vacios y reiniciar conteo

    df['principales_palabras_clave']=df['principales_palabras_clave'].apply(cambiar_espacio)

    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].apply(cambiar_porcentaje)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].apply(quitar_decimal)

    return df
