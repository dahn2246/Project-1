import sqlite3
import os
from Variables import *

def execute(commands, input):
    directory = Variables.preDirectory + '\\HistoricalPricesData\\HistoricalPrices.db'
    conn = sqlite3.connect(directory)
    c = conn.cursor()
    
    if(input == None or input == False):
        c.execute(commands)
    else:
        c.execute(commands,input)
    
    conn.commit()
    conn.close()


def executeReturn(commands):
    directory = Variables.preDirectory + '\\HistoricalPricesData\\HistoricalPrices.db'
    returnArray = []
    conn = sqlite3.connect(directory) 
    c = conn.cursor()
    
    cursor = c.execute(commands)
    
    for i in cursor:
        returnArray.append(i)
    
    conn.commit()
    conn.close()
    
    return returnArray    

