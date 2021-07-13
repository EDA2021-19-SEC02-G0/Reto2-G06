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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de videos

def initCatalog(colisionMan = 0, loadFactor = 1):
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
    catalog = model.newCatalog(colisionMan, loadFactor)
    return catalog

    
# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    __loadCategories(catalog)
    __loadVideos(catalog)


def __loadCategories(catalog):
    """
    Lee el archivo category-id.csv y carga las categorías en el catálogo

    Args:
        Catalog -- catalogo de videos
    """
    catfile = cf.data_dir + "category-id.csv"
    input_file = csv.DictReader(open(catfile,encoding='utf-8'), delimiter="\t")
    for category in input_file:
        model.loadCategory(catalog, category)


def __loadVideos(catalog):
    """
    Lee el archivo videos-large.csv y carga los videos al catálogo

    Args:
        Catalog -- catalogo de videos
    """
    # TODO Cambiar a videos-large.csv para producción
    vidsfile = cf.data_dir + "videos-large.csv"
    input_file = csv.DictReader(open(vidsfile,encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)
       


# Funciones de ordenamiento
def srtVidsByLikes(catalog, srtType):
    """
    Llama a la función sortVidsByLikes del model.py
    """
    return model.srtVidsByLikes(catalog, srtType)


# Funciones de consulta sobre el catálogo

def trendingVidCat(catalog, catName: str):
    """
    Devuelve el video que más días ha sido trending en una categoría específica
    Solo cuenta las ocurrencias de dias en trending de aquellos videos que
    tienen una persepción altamente positiva (ratio likes / dislikes > 20)

    Args:
        catalog -- catálogo de videos
        catName: str -- Nombre de la categoría para filtrar
    
    Returns: dict | Bool
        Diccionario con informaicón del video o False si no se encuentra
        ningún video que cumpla con los filtros.
    """
    return model.trendingVidCat(catalog, catName)


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
        con los filtros
    """
    return model.topVidsCatCountry(catalog, catName, countryName,
    topN)


def mostCommentedVids(catalog, countryName, tagName, topN):
    """
    Llama a la función model.mostCommentedVids()
    """
    return model.mostCommentedVid(catalog, countryName, tagName, topN)

def trendingVidCountry(catalog, country):
    return model.trendingVidCountry(catalog, country)