import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tqdm import tqdm
from time import sleep

def extraer_info_atrezzo_vazquez(numero_paginas):
    """
    Extrae información de productos de la página web Atrezzo Vázquez.

    Esta función realiza web scraping de las primeras `numero_paginas` páginas
    del sitio web de Atrezzo Vázquez, extrayendo información relevante
    sobre los productos disponibles. La información extraída incluye
    nombre, categoría, sección, descripción, dimensiones y enlace a la imagen.

    Args:
        numero_paginas (int): Número de páginas a extraer. Por defecto es 100.

    Returns:
        pandas.DataFrame: DataFrame con la información de los productos extraídos.
    """
    lista_datos = []

    # Bucle que recorre las páginas desde 1 hasta numero_paginas
    for pagina in tqdm(range(1, numero_paginas + 1), desc="Procesando páginas"):
        # URL para la página actual
        url = f"https://atrezzovazquez.es/shop.php?search_type=-1&search_terms=&limit=48&page={pagina}"
        
        # Realizar la solicitud HTTP GET
        res_atrezzo = requests.get(url)

        # Comprobamos el estado de la petición
        print(f"La respuesta de la petición es: {res_atrezzo.status_code}")
        
        if res_atrezzo.status_code == 200:
            # Creamos el objeto BeautifulSoup para acceder al contenido
            sopa = BeautifulSoup(res_atrezzo.content, 'html.parser')
             
            # Encontramos todos los contenedores de productos
            productos = sopa.find_all("div", class_="col-md-3 col-sm-4 shop-grid-item")
            
            # Iteramos sobre cada producto de la página
            for producto in productos:
                # Inicializamos un diccionario para cada producto
                diccionario = {}

                # Extraemos los datos de nombre, categoría, sección, descripción, dimensiones e imagen
                try:
                    diccionario["nombre"] = producto.find("a", class_="title").get_text(strip=True)
                except:
                    diccionario["nombre"] = np.nan
                try:
                    diccionario["categoria"] = producto.find("a", class_="tag").get_text(strip=True)
                except:
                    diccionario["categoria"] = np.nan
                try:
                    diccionario["seccion"] = producto.find("div", class_="cat-sec").get_text(strip=True)
                except:
                    diccionario["seccion"] = np.nan
                try:
                    diccionario["descripcion"] = producto.find("div", class_="article-container style-1").get_text(strip=True)
                except:
                    diccionario["descripcion"] = np.nan
                try:
                    diccionario["dimensiones"] = producto.find("div", class_="price").get_text(strip=True)
                except:
                    diccionario["dimensiones"] = np.nan
                try:
                    imagen_src = producto.find('img').get('src')
                    diccionario["imagen"] = "https://atrezzovazquez.es/" + imagen_src if imagen_src else np.nan
                except:
                    diccionario["imagen"] = np.nan
                                
                # Añadimos a lista_datos los datos del producto
                lista_datos.append(diccionario)
            
            # Introducimos un retraso para no sobrecargar el servidor
            sleep(1)
        else:
            print(f"No se ha podido recuperar la página {pagina}. Código de estado: {res_atrezzo.status_code}")
            break  # Se detiene la ejecución si no se puede recuperar la página

    # Creamos un DataFrame con la lista de diccionarios que hemos obtenido
    df_atrezzo = pd.DataFrame(lista_datos)
    return df_atrezzo
