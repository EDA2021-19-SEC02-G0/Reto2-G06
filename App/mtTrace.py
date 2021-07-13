from time import process_time
import tracemalloc

class mtTrace:
    """
    Permite hacer seguimiento de tiempo y memoria consumida
    """
    __start_time = None
    __start_memory = None
    __stop_time = None
    __stop_memory = None
    def __init__(self):
        """
        Inicializa tracemalloc y las variables __start_time y __start_memory
        """
        tracemalloc.start()
        self.__start_time = process_time()
        self.__start_memory = tracemalloc.take_snapshot()
    
    def stop(self):
        """
        Devuelve el tiempo transcurrido desde que se inicializó
        la variable __start_time, y la memoria consumida desde
        que se inicializó la variable __start_memory

        Returns: dict -- Diccionario con llave time en donde se
        encuentra el tiempo transcurrido en segundos y con llave
        memory en donde se encuentra la memoria utilizada en Mb
        """
        self.__stop_time = process_time()
        self.__stop_memory = tracemalloc.take_snapshot()
        delta_time = self.__stop_time - self.__start_time
        delta_memory = self.deltaMem()
        returnDict = {
            "time": delta_time,
            "memory": delta_memory
        }

        return returnDict



    def deltaMem(self):
        """
        calcula la diferencia en memoria alocada del programa entre dos
        instantes de tiempo y devuelve el resultado en Mb
        """
        memory_diff = self.__stop_memory.compare_to(self.__start_memory, "filename")
        delta_memory = 0.0

        # suma de las diferencias en uso de memoria
        for stat in memory_diff:
            delta_memory = delta_memory + stat.size_diff
        # de Byte -> kByte
        delta_memory = delta_memory * 1024
        return delta_memory 



