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
import time
import tracemalloc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de videos

def initCatalog(colisionMan = 0, loadFactor = 1):
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog(colisionMan, loadFactor)
    return catalog

    
# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadCategories(catalog)
    loadVideos(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory

def loadCategories(catalog):
    catfile = cf.data_dir + "category-id.csv"
    input_file = csv.DictReader(open(catfile,encoding='utf-8'), delimiter="\t")
    for category in input_file:
        model.loadCategory(catalog, category)

def loadVideos(catalog):
    # TODO Cambiar a videos-large.csv para producción
    vidsfile = cf.data_dir + "videos-large.csv"
    input_file = csv.DictReader(open(vidsfile,encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog, video)
        model.addCountry(catalog,video)

# Funciones de ordenamiento
def srtVidsByLikes(catalog, srtType):
    """
    Llama a la función sortVidsByLikes del model.py
    """
    return model.srtVidsByLikes(catalog, srtType)


# Funciones de consulta sobre el catálogo

def catPos(catalog, catName):
    """
    Llama a la función catPos del model.py
    """
    return model.catPos(catalog, catName)


def trendingVidCat(catalog, catPos):
    """
    Llama a la función model.trendingVidCat()
    """
    return model.trendingVidCat(catalog, catPos)


def topVidsCatCountry(catalog, catPos, countryName, topN):
    """
    Llama a la función topVidsCatCountry del model.py
    """
    return model.topVidsCatCountry(catalog, catPos, countryName,
    topN)


def mostCommentedVids(catalog, country, tagName, topN):
    """
    Llama a la función model.mostCommentedVids()
    """
    return model.mostCommentedVid(catalog, country, tagName, topN)

def trendingVidCountry(catalog, country):
    return model.trendingVidCountry(catalog, country)

#TODO Eliminar función para Reto (solo se utiliza para labs)
def topVidsCat(catalog, catName: str, topN: int):
    return model.topVidsCat(catalog, catName, topN)

# =====================================
# Funciones para medir tiempo y memoria
# =====================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory