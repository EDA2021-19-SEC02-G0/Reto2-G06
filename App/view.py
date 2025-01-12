﻿"""
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
from typing import Any
import config as cf
import controller
assert cf
from DISClib.ADT import list as lt #TAD Lista
from DISClib.ADT import map as mp #TAD map
from DISClib.DataStructures import mapentry as me #TAD map
from time import process_time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#Desactiva el seguimiento de memoria para mejorar rendimiento
controller.mtTrace.trace_memory = False

def printMenu():
    print("Menú")
    print("1- N videos con mas views de un país y una categoría") #REQ 1
    print("2- Video más días en trending para un país") #REQ 2
    print("3- Video más días en trending para una categoría") #REQ 4
    print("4- Videos con más comentarios de país / tag") #REQ 4
    print("0- Salir")


def printTrace(trace, processDesc: str = "Proceso en") -> None:
    controller.mtTrace.printTrace(trace, processDesc)


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


def initProgram() -> None:
    #Carga los datos al iniciar el programa
    print("Bienvenido")
    print("A continuación se cargará la información en el catálogo")
    init = input("ENTER para continuar o 0 para salir: ")
    #Termina el programa si el usuario selecciona 0
    if init == "0":
        sys.exit(0)
    #Carga el catálogo
    print("Cargando...")
    catalog, trace1 = controller.initCatalog(0, 2)
    trace2 = controller.loadData(catalog)
    trace1["time"] += trace2["time"]
    if trace1["memory"] is not None:
        trace1["memory"] += trace2["memory"]

    #Información de catalogo cargado
    printTrace(trace1,
    str(lt.size(catalog["videos"])) + " videos cargados en")
    input("ENTER para continuar ")
    mainMenu(catalog)


def mainMenu(catalog):
    # Menú principal
    while True:
        print("")
        printMenu()
        inputs = input('Seleccione una opción para continuar\n> ')
        if int(inputs[0]) == 1:
            #REQ 1
            #User input
            catName     = input("Nombre de la categoría: ").lower().strip()
            countryName = input("País: ").lower().strip()
            topN        = topNInput()
            #Program
            topVids, trace = controller.topVidsCatCountry(catalog, catName, countryName, topN)
            # Output
            printTrace(trace)
            if topVids == False:
                print("Ningún video cumple con los filtros de busqueda")
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
                for video in lt.iterator(topVids):
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
                if topVids["size"] < topN:
                    print("Solo", topVids["size"], "cumplen las condiciones de búsqueda")
            input("\nENTRE para continuar")

        elif int(inputs[0]) == 2:
            #REQ 2
            #User input
            countryName = input("Buscar en país: ").strip().lower()
            print("Cargando. Esta operación puede tardar")
            #Program
            video, trace = controller.trendingVidCountry(catalog, countryName)
            #Output
            printTrace(trace)
            if video == False :
                print("Ningún video cumple con los parámetros de busqueda")
            else:
                print("\nEl video del pais", countryName, "con persepción positiva es\n")
                print("Titulo:", video["title"])
                print("Canal:", video["channel_title"])
                print("Pais:", video["country"])
                print("Likes/dislikes:", round(video["ratio_likes_dislikes"], 2))
                print("Días en trend:", video["day_count"], "\n")
            input("ENTER para continuar")

        elif int(inputs[0]) == 3:
            #REQ 3
            #User input
            catName = input("Buscar en categoría: ").strip().lower()
            print("Cargando. Esta operación puede tardar")
            #Program
            video, trace = controller.trendingVidCat(catalog, catName)
            #Output
            printTrace(trace)
            if video == False :
                print("Ningún video cumple con los parámetros de busqueda")
            else:
                print("\nEl video de la categoría", catName, "con persepción positiva es\n")
                print("Titulo:", video["title"])
                print("Canal:", video["channel_title"])
                print("Category Id:", video["category_id"])
                print("Likes/dislikes:", round(video["ratio_likes_dislikes"], 2))
                print("Días en trend:", video["day_count"], "\n")
            input("\nENTER para continuar")

        elif int(inputs[0]) == 4:
            #REQ 4
            #User input
            tagName = input("Tag a buscar: ")
            countryName = input("Buscar en país: ")
            topN = topNInput()
            #program
            mostComVids, trace = controller.mostCommentedVids(catalog, countryName, tagName, topN)
            #Output
            printTrace(trace)
            if mostComVids == False:
                print("Ningún video cumple con los filtros de búsqueda")
            else:
                if mostComVids["size"] < topN:
                    print("Solo", mostComVids["size"], "videos cumplen las condiciones de búsqueda")
                for video in lt.iterator(mostComVids):
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



"""
Main program
"""
initProgram()


