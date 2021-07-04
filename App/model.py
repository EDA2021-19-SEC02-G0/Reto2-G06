"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog(type):
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para las categorías,
    una lista vacía para las asociaciones video - categoría y una lista vacía
    para los paises. Retorna el catálogo inicializado. Dependiendo el type pasado inicializa
    las listas con ARRAY_LIST o SINGLE_LINKED

    Args:
        type: int -- 1 para cargar los datos en ARRAY_LIST, 2 para cargar los datos en SINGLE_LINKED
    """
    if type == 1:
        lstType = "ARRAY_LIST"
    elif type == 2:
        lstType = "SINGLE_LINKED"
    else:
        raise Exception("Invalid type in model.newCatalog()")
        
    catalog = {
        "videos": None,
        "catVids": None, #Mapa con <category, list> donde list es una lista de videos con la category
        "categories": None #Tabla con <id, catName> que relaciona id de categoría con el nombre de la categoría
    }

    catalog["videos"] = lt.newList(lstType)
    catalog["catVids"] = mp.newMap(1000, 
    loadfactor=4, comparefunction=compareCategory)
    catalog["categories"] = mp.newMap(32, loadfactor=4, comparefunction=compareCategory)
    
    return catalog        


# Funciones para agregar informacion al catalogo

# -- Para cargar categorías
def loadCategory(catalog, category):
    """
    Añade una categoría a la lista de categorías.
    """
    #Añade <id, catName> a la tabla que relaciona el id de la categoría
    #con el nombre de esta
    mp.put(catalog["categories"], int(category["id"]), category["name"].strip())
    #Crea la estructura de datos para listar los videos
    #que aparecen en una categoría
    mp.put(catalog["catVids"], category["name"].strip(), lt.newList())
    

# -- Para añadir videos
def addVideo(catalog, video):
    """
    Añade un video a la lista de videos.
    """
    lt.addLast(catalog["videos"], video)
    #Obtener nombre de la categoría del video
    catEntry = mp.get(catalog["categories"], int(video["category_id"]))
    catName = me.getValue(catEntry)
    #Añade el libro a la 
    catVidsEntry = mp.get(catalog["catVids"], catName)
    catVids = me.get(catVidsEntry)
    lt.addLast(catVids, video) 

# Funciones para creacion de datos

# Funciones de consulta

def topVidsCat(catalog, catName: str, topN: int):
    """
    Retorna los n videos con mas vistas de una categoría.
    TODO mejorar documentación
    """
    #Revisa si la llave está en el mapa
    if not mp.contains(catalog["catVids"], catName):
        return False
    catVidsEntry = mp.get(catalog["catVids"], catName)
    catVids = me.getValue(catVidsEntry)
    #Revisa si hay videos que cumplen la condición
    if lt.isEmpty(catVids):
        return False
    #Ordena los videos
    srtVidsByViews(catVids)
    #Retorna los primeros n videos
    return lt.subList(catVids, 1, topN)
    

# Funciones utilizadas para comparar elementos dentro de una lista

def compareCategory(catName,cat):
    if (catName.lower() in cat["name"].lower()):
        return 0
    return -1


def cmpVideos(videoTitle, video) -> int:
    """
    Compara un str con el nombre de un elemento video

    Args:
        videoTitle: str a comparar
        video: elemento video a comparar
    
    Returns:
        0 (int): si el str es igual al id del elemento video
        -1 (int): si son diferentes  
    """
    if (videoTitle == video["title"]):
        return 0
    return -1


def cmpVidsByViews(video1, video2):
    """
    Devuelve verdadero (True) si las vistas de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'views'
    video2: informacion del segundo video que incluye su valor 'views'
    """
    return int(video1["views"]) > int(video2["views"])


# Funciones de ordenamiento

def srtVidsByViews(lst):
    """
    Ordena los videos del lst por viwews. La acendencia o
    decendencia del orden depende de la función de comparación
    cmpVidsByViews(). Utiliza la función de ordenamiento importada
    como "sa"

    Args:
        lst -- Lista con elementos video a ordenar
    
    Returns:
        Tad Lista con los videos ordenados.
    """
    return sa.sort(lst, cmpVidsByViews)
