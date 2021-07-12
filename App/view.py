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
    print("Menú")
    print("1- N videos con mas views de un país y una categoría") #REQ 1
    print("2- Video más días en trending para un país") #REQ 2
    print("3- Video más días en trending para una categoría") #REQ 4
    print("4- Videos con más comentarios de país / tag") #REQ 4
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
Main program
"""
#Carga los datos al iniciar el programa
catalog = None
print("Bienvenido")
print("A continuación se cargará la información en el catálogo",
"ENTER para continuar o 0 para salir")
init = input("> ")
#Termina el programa si el usuario selecciona 0
if init == "0":
    sys.exit(0)
#Carga el catálogo
catalog = controller.initCatalog() #TODO seleccionar manejo de coliciones y factor de carga
controller.loadData(catalog)
#TODO mostrar información del primer video cargado y de categorías.

# Menú principal
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        #REQ 1
        #User input
        catName     = input("Nombre de la categoría: ").lower().strip()
        countryName = input("País: ").lower().strip()
        topN        = topNInput()
        #Program
        topVids = controller.topVidsCatCountry(catalog, catName, countryName, topN)
        #TODO Output

    elif int(inputs[0]) == 2:
        #REQ 2
        #Input del usuario
        countryName = input("Buscar en país: ")
        print("Cargando. Esta operación puede tardar")
        video= controller.trendingVidCountry(catalog, countryName)

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
        pass
    elif int(inputs[0]) == 4:
        #REQ 4
        pass
    else:
        sys.exit(0)

