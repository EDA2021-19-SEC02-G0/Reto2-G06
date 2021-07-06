"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import sys
import config as cf
import controller
assert cf
from DISClib.ADT import list as lt #TAD Lista
from DISClib.ADT import map as mp #TAD map
from DISClib.DataStructures import mapentry as me #TAD map


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    #TODO corregir menú a requerimientos
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- N videos con mas views de una categoría")
    print("0- Salir")


def printRow(row: list) -> None:
    """
    Imprime la fila de una tabla. Si el largo de los datos supera el ancho de la columna,
    imprime el dato incompleto con ...

    Args:
        row: Lista de listas. Row debe ser de la forma [<lens>, <data>]
            <lens>: (list) Lista con ancho de las columnas
            <data>: (list) Lista con datos de las columnas

    TODO Manejo de ancho y caracteres asiaticos
    """
    rowFormat = ""
    for i in range(0, len(row[0])):
        colWidth = row[0][i]
        cell = str(row[1][i])
        #Añade la columna al formato
        rowFormat += "{:<" + str(colWidth) + "}"
        #Revisa y corrige si el tamaño de los datos es más grande que la columna
        if len(cell) > colWidth:
            row[1][i] = cell[0:colWidth - 3] + "..."
    
    #Imrpime la fila
    print(rowFormat.format(*row[1]))
    


def initCatalog():
    """
    Inicializa el catálogo de videos
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los datos de los videos
    """
    return controller.loadData(catalog)


catalog = None

def topNInput() -> int:
    """
    Le pide al usuario que ingrese un int, que corresponde al
    top de videos que quiere que se listen
    """
    topN = 0
    while topN < 1:
        topN = int(input("Número de video a listar: "))
        if topN < 1:
            print("Entrada inválida, intente nuevamente.")
    
    return topN

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = initCatalog()
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])) + "\n")
        print("Categorías cargadas:", str(mp.size(catalog["catVids"])))
        for catName in lt.iterator(mp.keySet(catalog["catVids"])):
            print(catName, ":", lt.size(me.getValue(mp.get(catalog["catVids"], catName))))
        input("\nENTER para continuar")

    elif int(inputs[0]) == 2:
        #Top n videos con mas vistas de una categoría
        #User category input
        catName = input("Buscar en categoría: ")
        #User topN input
        topN = topNInput()
        #Consulta
        topVideos = controller.topVidsCat(catalog, catName, topN)
        #Output results
        #Check if category was found
        if not topVideos:
            print("Categoría no encontrada")
        else:
            printRow([
                [15, 40, 20, 25, 10, 10, 10],
                [
                    "Trending date",
                    "Title",
                    "Channel title",
                    "Publish time",
                    "Views",
                    "likes",
                    "dislikes"
                ]
            ])
            for video in lt.iterator(topVideos):
                printRow([
                [15, 40, 20, 25, 10, 10, 10],
                [
                    video["trending_date"],
                    video["title"],
                    video["channel_title"],
                    video["publish_time"],
                    video["views"],
                    video["likes"],
                    video["dislikes"]
                ]
            ])
            #Check if requested more videos that they are
            if topVideos["size"] < topN:
                print("Solo", topVideos["size"], "cumplen las condiciones de búsqueda")
        input("\nENTRE para continuar")
    
    elif int(inputs[0]) == 3:
        #REQ 2
        #Input del usuario
        countryName = input("Buscar en país: ")
        print("Cargando. Esta operación puede tardar")
        video= controller.trendingVidCountry(catalog, countryName)
        if video == False:
            print("Ningún video cumple con los parámetros de busqueda")
        else:
            print("\nEl video del pais", countryName, "con persepción positiva es\n")
            print("Titulo:", video["title"])
            print("Canal:", video["channel_title"])
            print("Pais:", video["country"])
            print("Likes/dislikes:", round(video["ratio_likes_dislikes"], 2))
            print("Días en trend:", video["day_count"], "\n")
            input("ENTER para continuar")
    elif int(inputs[0]) == 4:
        #REQ3
        #User category input
        catPos = categotyInput(catalog)
        print("Cargando. Esta operación puede tardar")
        video = controller.trendingVidCat(catalog, catPos)
        if video == False:
            print("Nungún video cumple con los parámetros de busqueda")
        else:
            print("\nEl video de la categoría ingresada con persepción sumamente positiva es, que más días ha sido trend es\n")
            print("Titulo:", video["title"])
            print("Canal:", video["channel_title"])
            print("Id categoría:", video["category_id"])
            print("Likes/dislikes:", round(video["ratio_likes_dislikes"], 2))
            print("Días en trend:", video["day_count"], "\n")
            input("ENTER para continuar")

    elif int(inputs[0]) == 5:
        #REQ4
        countryName = input("Buscar en país: ")
        tagName = input("Etiqueta (tag) a buscar: ")
        topN = topNInput()
        print("Cargando. Esta operación puede targar.")
        videos = controller.mostCommentedVids(catalog, countryName, tagName, topN)
        if videos["size"] == 0:
            print("No se ecnontró ningún video que cumpla con las condiciones de búsqueda")
        elif videos["size"] < topN:
            print("Solo", videos["size"], "videos cumplen las condiciones de búsqueda")
            print("resultados a continuación:")
        else:
            print("Resulatados a continuación:")
        for video in lt.iterator(videos):
            print("")
            printRow([
                [40, 20, 20, 10, 10, 10, 11],
                [
                    "Title",
                    "Channel title",
                    "Publish time",
                    "Views",
                    "likes",
                    "dislikes",
                    "Comment cnt"
                ]
            ])
            printRow([
                [40, 20, 20, 10, 10, 10, 11],
                [
                    video["title"],
                    video["channel_title"],
                    video["publish_time"],
                    video["views"],
                    video["likes"],
                    video["dislikes"],
                    video["comment_count"]
                ]
            ])
            print("\nTAGS:", video["tags"], "\n")
        input("\nENTER para continuar")
    else:
        sys.exit(0)

