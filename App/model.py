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
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo de libros

    Crea una lista vacia para guardar todos los videos

    Se crean indices (Maps) por los siguientes criterios:
    videos
    categories

    Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'categories': None,
               }
    catalog['videos'] = lt.newList('SINGLE_LINKED', compareCategory) 

    catalog['videos'] = mp.newMap(44,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=cmpVideos)  

    catalog['categories'] = mp.newMap(380000,
                                   maptype='CHAINING',
                                   loadfactor=0.5,
                                   comparefunction=compareCategory)  
    return catalog               



# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

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
# Funciones de ordenamiento
