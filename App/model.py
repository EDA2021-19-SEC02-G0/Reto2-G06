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
        "categories": None,
        "categories_id": None,
        "countries": None
    }

    catalog["videos"] = lt.newList("ARRAY_LIST")
    """
    Crea un mapa para obtener una lista de videos en una categoría a partir
    del nombre de la categoría
    """
    catalog["categories"] = mp.newMap(32, maptype=mapType, loadfactor=loadFactor)
    """
    Crea un mapa utilizado para obtener el nombre de la categoría a paritr del
    id de esta.
    """
    catalog["categories_id"] = mp.newMap(32, maptype=mapType, loadfactor=loadFactor)
    """
    Crea un mapa utilizado para obtener una lista de videos de un país dado el nombre
    de este
    """
    catalog["countries"] = mp.newMap(20, maptype=mapType, loadfactor=loadFactor) #TODO corregir tamaño del map
    
    return catalog        


# Funciones para agregar informacion al catalogo

# -- Para cargar categorías
def loadCategory(catalog, category):
    """
    Añade una categoría al mapa de categorías del catálogo creando
    la estructura de categoría que contiene el nombre de la
    categoría, el id, y una lista para incluir los videos
    de dicha categoría.
    Adicionalmente añade la pareja <llave, valor> <category id, category name>
    al mapa categories_id del catálogo
    Args:
        catalog -- catálogo de videos
        category: dict -- información de la categoría a agregar
    """
    catName     = category["name"].strip().lower()
    catId       = int(category["id"])
    # Añade al mapa catalog["categories"] (crea una lista vacía para agregar
    # videos posteriormente)
    mp.put(catalog["categories"], catName, lt.newList("ARRAY_LIST"))
    #Añade al mapa catalog["categories_id"]
    mp.put(catalog["categories_id"], catId, catName)
    

# -- Para añadir videos
def addVideo(catalog, video):
    """
    Añade un video a la lista de videos, y a la lista de videos
    de la categoría a la que pertenece.
    Args:
        catalog -- catálogo de videos
        video: dict -- información del video a agregar
    """
    lt.addLast(catalog["videos"], video)
    #Obtener nombre de la categoría del video
    catName = getMapValue(catalog["categories_id"], int(video["category_id"]))
    #Añade el video a la lista de videos en la categoría
    catVids = getMapValue(catalog["categories"], catName)
    lt.addLast(catVids, video) 
    #Añade el video a la lista de videos del país
    addCountryVideo(catalog, video)


def addCountryVideo(catalog, video):
    """
    Añade un video al map de videos de un país específico (catalog["countries"])
    Si no existe el país crea la llave-valor en el mapa, y añade el video

    Args:
        catalog -- catálogo de videos
        video -- video con llave "country"
    """
    countryName = video["country"].strip().lower()
    countryVids = getMapValue(catalog["countries"], countryName)
    #Revisa si ya se añadió la llave
    if countryVids is not None:
        lt.addLast(countryVids, video)
    else:
        mp.put(catalog["countries"], countryName, lt.newList("ARRAY_LIST"))
        countryVids = getMapValue(catalog["countries"], countryName)
        lt.addLast(countryVids, video)


# Funciones para creacion de datos

# Funciones de consulta

def topVidsCatCountry(catalog, catName: str, countryName: str, topN: int):
    """
    Devuelve una lista con el top n videos con mas likes en un determinado
    país y de una categoría específica

    Args:
        catalog -- catálogo de videos
        catName: str -- Nombre de la categoría para filtrar
        countryName: str -- Nombre del país para filtrar
        topN: int -- Número de videos a listar
    
    Returns: TAD lista | bool
        TAD lista el top n videos o Falso si no encuentra videos que coincidan
        con los filtros o FALSE si no se encutentra ningún video con las
        filtros
    """
    catName = catName.strip().lower()
    countryName = countryName.lower().strip()
    topVids = lt.newList("ARRAY_LIST")
    # Get list with countryVids
    countryVids = getMapValue(catalog["countries"], countryName)
    # Get list with catVids
    catVids = getMapValue(catalog["categories"], catName)

    # Check if keys exist
    if countryVids is None or catVids is None:
        return False
    
    #Revisa que lista es mas pequeña para ver por cual hace el recorrido
    if lt.size(catVids) <= lt.size(countryVids):
        #Itera por videos en catVids
        for video in lt.iterator(catVids):
            if video["country"].strip().lower() == countryName:
                lt.addLast(topVids, video)
    else:
        #Itera por los videos de countryVids
        for video in lt.iterator(countryVids):
            # Get video's catName
            vidCatName = getMapValue(catalog["categories_id"], int(video["category_id"])).strip().lower()
            if vidCatName == catName:
                lt.addLast(topVids, video)
    
    # Checks if topVids is empty
    if lt.isEmpty(topVids):
        return False
    
    #Sorts vids by likes
    srtVidsByLikes(topVids)

    #Retorna los n videos a listar
    return lt.subList(topVids, 1, topN)


def trendingVidCountry(catalog, countryName: str):
    """
    Devuelve el video que más días ha sido trending en un país específico
    Solo cuenta las ocurrencias de dias en trending de aquellos videos que
    tienen una persepción altamente positiva (ratio likes / dislikes > 10)

    Args:
        catalog -- catálogo de videos
        countryName: str -- Nombre del país para filtrar
    
    Returns: dict | Bool
        Diccionario con informaicón del video o False si no se encuentra
        ningún video que cumpla con los filtros.        
    """
    countryVids = getMapValue(catalog["countries"], countryName.strip().lower())
    if countryVids is None:
        return False
    #Crea mapa para almacenar videos que cumplen con los filtros
    hiPerVids = mp.newMap(100000, maptype="CHAINING", loadfactor=2) #TODO determinar tipo de mapa y factor de carga

    for video in lt.iterator(countryVids):
        #Evitar división por 0
        if (int(video["dislikes"]) == 0) and (int(video["likes"]) == 0):
            likeDislikeRatio = 0
        elif int(video["dislikes"]) == 0:
            likeDislikeRatio = "Infinito"
        else:
            likeDislikeRatio = int(video["likes"]) / int(video["dislikes"])
        #Revisar si el video cumple los criterios
        if (str(likeDislikeRatio) == "Infinito") or (likeDislikeRatio > 10):
            #Revisar si el video ya existe en hiPerVids
            hiPerVid = getMapValue(hiPerVids, video["title"])
            if hiPerVid is not None:
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
                mp.put(hiPerVids, video["title"], hiPerVid)
                
    #Convierte el mapa en una lista de los valores
    hiPerVids = mp.valueSet(hiPerVids)

    # Revisa si hay videos que cumplen con la condición
    if lt.isEmpty(hiPerVids):
        return False
    
    #Ordena los hiPerVids
    srtVidsByTrendDays(hiPerVids)

    #Retorna el video que más días ha sido trend
    return lt.firstElement(hiPerVids)


def trendingVidCat(catalog, catName: str):
    """
    Devuelve el video que más días ha sido trending en un país específico
    Solo cuenta las ocurrencias de dias en trending de aquellos videos que
    tienen una persepción altamente positiva (ratio likes / dislikes > 20)

    Args:
        catalog -- catálogo de videos
        catName: str -- Nombre de la categoría para filtrar
    
    Returns: dict | Bool
        Diccionario con informaicón del video o False si no se encuentra
        ningún video que cumpla con los filtros.
    """
    catVids = getMapValue(catalog["categories"], catName.strip().lower())
    if catVids is None:
        return False
    #Crea mapa para almacenar videos que cumplen con los filtros
    hiPerVids = mp.newMap(100000, maptype="CHAINING", loadfactor=2) #TODO determinar tipo de mapa y factor de carga

    for video in lt.iterator(catVids):
        #Evitar división por 0
        if (int(video["dislikes"]) == 0) and (int(video["likes"]) == 0):
            likeDislikeRatio = 0
        elif int(video["dislikes"]) == 0:
            likeDislikeRatio = "Infinito"
        else:
            likeDislikeRatio = int(video["likes"]) / int(video["dislikes"])
        #Revisar si el video cumple los criterios
        if (str(likeDislikeRatio) == "Infinito") or (likeDislikeRatio > 20):
            #Revisar si el video ya existe en hiPerVids
            hiPerVid = getMapValue(hiPerVids, video["title"])
            if hiPerVid is not None:
                #Añade 1 a la cuenta de días que ha aparecido el video
                hiPerVid["day_count"] += 1
            else:
                hiPerVid = {
                    "title": video["title"],
                    "channel_title": video["channel_title"],
                    "category_id": video["category_id"],
                    "ratio_likes_dislikes": likeDislikeRatio,
                    "day_count": 1
                    }
                mp.put(hiPerVids, video["title"], hiPerVid)
                
    #Convierte el mapa en una lista de los valores
    hiPerVids = mp.valueSet(hiPerVids)

    # Revisa si hay videos que cumplen con la condición
    if lt.isEmpty(hiPerVids):
        return False
    
    #Ordena los hiPerVids
    srtVidsByTrendDays(hiPerVids)

    #Retorna el video que más días ha sido trend
    return lt.firstElement(hiPerVids)



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


def cmpVideosByLikes(video1, video2) -> bool:
    """
    Devuelve verdadero (True) si los likes de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'likes'
    video2: informacion del segundo video que incluye su valor 'likes'
    """
    return int(video1["likes"]) > int(video2["likes"])


# Funciones de ordenamiento

def srtVidsByLikes(lst):
    """
    Ordena los videos del catálogo por likes. La acendencia o
    decendencia del orden depende de la función de comparación
    cmpVideosByLikes(). Utiliza la función de ordenamiento importada
    como "sa"

    Args:
        lst -- Lista con elementos video a ordenar
    
    Returns:
        Tad Lista con los videos ordenados.
    """
    sortedList = sa.sort(lst, cmpVideosByLikes)

    return sortedList


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


# ================================
#       Otras funciones
# ================================

def getMapValue(map, key):
    """
    Devuelve el valor en un mapa que corresponde a la llave pasada
    por parámetro

    Returns:
        El valor correspondiente a la llave pasada o None
        si no encuentra la llave especificada
    """
    valueEntry = mp.get(map, key)
    if valueEntry is None:
        return None
    value = me.getValue(valueEntry)
    
    return value
