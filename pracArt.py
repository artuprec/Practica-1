#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:58:09 2022

@author: mat
"""

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import Array
from random import randint


N = 10
NPROD = 3


def producer(storage, index, empty, non_empty):
    for v in range(N):
        empty[index].acquire()
        storage[index] += randint(0,5)
        print (f"producer {index} produciendo {storage[index]} ")
        non_empty[index].release()
    empty[index].acquire() #Cuando han terminado los procesos mandamos el -1
    storage[index]=-1
    non_empty[index].release() 
    
def consumer(storage,empty, non_empty):
    merge = []
    for i in range(NPROD):
        non_empty[i].acquire()
    while max(storage) != -1:
         data = 5*N*NPROD + 1 #Suma como maximo de 5 en 5 N procesos de N productores
         index = 0
         for i in range(NPROD):
             if data > storage[i] and storage[i] != -1 :
                 data = storage[i]  
                 index = i
         merge.append(data)
         empty[index].release()
         print (f"consumer consumiendo {data} de productor {index} ")            
         non_empty[index].acquire()
    length = N*NPROD
    if len(merge) == length: #Ver si se han producido todos los elementos que se deben
        print("Tamaño de la lista final adecuado (",length," elementos)") 
    else:
        print("NUMERO DE ELEMENTOS PRODUCIDOS INCORRECTO")
    print("Lista final:", merge)
def main():
    storage = Array('i', NPROD)
    non_empty = [Semaphore(0) for i in range(NPROD)] #Creamos un semaforo para cada productor
    empty = [BoundedSemaphore(1) for i in range(NPROD)]
    prodlst = [Process(target = producer, args = (storage, index, empty, non_empty)) for index in range(NPROD)]
    cons= Process(target=consumer,args=(storage, empty, non_empty))
    print("Iniciando proceso con",NPROD,"productores que producen",N,"elementos" )
    for p in prodlst :
        p.start()
    cons.start()
    for p in prodlst :
        p.join()
    cons.join()

if __name__ == '__main__':
    main()