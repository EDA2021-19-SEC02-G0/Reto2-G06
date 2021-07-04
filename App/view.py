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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("** ADVERTENCIA: ALGUNAS OPCIONES DEL MENÚ NO HAN SIDO IMPLEMENTADAS **") #TODO Eliminar advertencia
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Top N videos con más likes tendencia en país - categoría")
    print("3- Vídeo que más días ha sido trending en un país")
    print("4- Video que más días ha sido trending en una categoría")
    print("5- N videos con más comentarios en país")
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
    


def initCatalog(type):
    """
    Inicializa el catálogo de videos
    """
    return controller.initCatalog(type)


def loadData(catalog):
    """
    Carga los datos de los videos
    """
    return controller.loadData(catalog)


catalog = None


def categotyInput(catalog) -> int:
    """
    Le pide al usuario que ingrese una categoría (por nombre)
    Devuelve la posición de la categoría en la lista de 
    categorías (int)

    Args:
        catalog -- catálofo de videos
    """
    catPos = 0
    #User category input
    while catPos == 0:
        catName = input("Buscar en categoría: ").strip()
        catPos = controller.catPos(catalog, catName)
        if catPos == 0:
            print("Categoría no encontrada. Intente nuevamente.")
    
    return catPos


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
        #Inicializa el catálogo en modo array_list
        catalog = initCatalog(1)
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])) + "\n")
        #Información del primer video cargado
        firstVid = lt.getElement(catalog["videos"], 1)
        print("Primer video cargado:")
        printRow([[30,20,15,15,10,10,10], ["Titulo", "Canal", "Trend Date", "País", "Vistas", "Likes", "Dislikes"]])
        printRow([
            [30,20,15,15,10,10,10],
            [firstVid["title"], firstVid["channel_title"], firstVid["trending_date"], firstVid["country"], 
            firstVid["views"], firstVid["likes"], firstVid["dislikes"]]
        ])
        print("")
        #Información de categorías cargadas
        print("Categorías cargadas:")
        printRow([
            [4,30],
            ["id", "Nombre"]
        ])
        for i in range(1, lt.size(catalog["categories"]) + 1):
            cat = lt.getElement(catalog["categories"], i)
            printRow([
                [4,30],
                [cat["id"], cat["name"]]
            ])
        input("\nENTER para continuar")

    elif int(inputs[0]) == 2:
        #REQ1
        #User category input
        catPos = categotyInput(catalog)
        #User country input
        countryName = input("Buscar en país: ").strip()
        #User topN input
        topN = topNInput()
        #Exec
        topVideos = controller.topVidsCatCountry(catalog, catPos, countryName,
        topN)
        #Output results
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

