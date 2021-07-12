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


from DISClib.DataStructures.arraylist import addLast, newList
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
def newCatalog(colisionMan: int, loadFactor: float):
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para las categorías,
    una lista vacía para las asociaciones video - categoría y una lista vacía
    para los paises. Retorna el catálogo inicializado. Dependiendo el type pasado inicializa
    las listas con ARRAY_LIST o SINGLE_LINKED

    Args:
        colisionMan: int -- Define el manejo de colisiones para los tad MAP del catalogo
            - 0 para Separate Chaining
            - 1 para Linear Probing
        loadFactor: float -- Factor de carga para los tad MAP del catalogo
    
    Returns:
        Catalogo vacío
    """

    if colisionMan == 0:
        mapType = "CHAINING"
    elif colisionMan == 1:
        mapType = "PROBING"
        if loadFactor >= 1:
            raise Exception("Invalid loadfactor for Linear Probing Map")
    else:
        raise Exception("Invalid colision managment type (colisionMan) in model.newCatalog()")
  
    catalog = {
        "videos": None,
        "catVids": None, #Mapa con <category, list> donde list es una lista de videos con la category
        "categories": None, #Tabla con <id, catName> que relaciona id de categoría con el nombre de la categoría
        "country":None
    }

    catalog["videos"] = lt.newList("ARRAY_LIST")
    catalog["catVids"] = mp.newMap(32, maptype=mapType, loadfactor=loadFactor )
    catalog["categories"] = mp.newMap(32, maptype=mapType, loadfactor=loadFactor )
    catalog["country"]=mp.newMap(197, maptype=mapType, loadfactor=loadFactor )

    
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
    #Añade el libro a la lista de libros en la categoría
    catVidsEntry = mp.get(catalog["catVids"], catName)
    catVids = me.getValue(catVidsEntry)
    lt.addLast(catVids, video) 
    
def addCountry(catalog,video):
    countryvideo=video["country"]
    
    if not mp.contains(catalog["country"],countryvideo):
        new=lt.newList()
        lt.addLast(new,video)
        mp.put(catalog["country"],countryvideo,new)
    if mp.contains(catalog["country"],countryvideo):
        pairs=mp.get(catalog["country"],countryvideo)
        value=me.getValue(pairs)
        lt.addLast(value,video)

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


def trendingVidCountry(catalog, countryName):
   
    mapcountry=catalog["country"]
    
    lista=mp.get(mapcountry,countryName)
    
    value=me.getValue(lista)
    
    hiPerVids = lt.newList("ARRAY_LIST", cmpVideos)
    for video in lt.iterator(value):
        #Evitar división por 0
        if (int(video["dislikes"]) == 0) and (int(video["likes"]) == 0):
            likeDislikeRatio = 0
        elif int(video["dislikes"]) == 0:
            likeDislikeRatio = 30
        else:
            likeDislikeRatio = int(video["likes"]) / int(video["dislikes"])
        #Revisar si el video cumple los criterios
        if (video["country"].lower() == countryName.lower()) and likeDislikeRatio > 10:
            #Revisar si el video ya existe en trendVids
            hiPerVidPos = lt.isPresent(hiPerVids, video["title"])
            if hiPerVidPos > 0:
                hiPerVid = lt.getElement(hiPerVids, hiPerVidPos)
                #Añade 1 a la cuenta de días que ha aparecido el video
                hiPerVid["day_count"] += 1
            else:
                hiPerVid = {
                    "title": video["title"],
                    "channel_title": video["channel_title"],
                    "country": video["country"],
                    "ratio_likes_dislikes": likeDislikeRatio,
                    "day_count": 1
                    }
                lt.addLast(hiPerVids, hiPerVid)
     #Revisa si hay videos que cumplen con la condición
    if lt.isEmpty(hiPerVids):
        return False
    #Ordena los hiPerVids
    srtVidsByTrendDays(hiPerVids)
    #Retorna el video que más días ha sido trend
    return lt.firstElement(hiPerVids)
           
  
  

def cmpVideosByTrendDays(video1, video2) -> bool:
    """
    Devuelve verdadero (True) si los días de tendencia del video 1 son MAYORES que los del video 2
    CUIDADO: los elementos video1 y video2 no son elementos video del catalogo de videos
    deben tener una llave "day_count": int. Ver función trendingVidCat()

    Args:
        video1: información del video 1 que incluye llave day_count
        video2: información del video 2 que incluye llave day_count
    """
    return int(video1["day_count"]) > int(video2["day_count"])


def srtVidsByTrendDays(lst):
    """
    Ordena los videos por días de trend. Retorna la lista ordenada
    La acendencia o decendencia del ordenamiento depende de la
    función cmpVideosByTrendDays().
    ADVERTENCIA: los elementos video1 y video2 NO son elementos video del
    catalogo de videos deben tener una llave "day_count": int.
    Ver función trendingVidCat()

    Args:
        lst -- lista con elementos video que tienen la llave day_count
    """
    return sa.sort(lst, cmpVideosByTrendDays)