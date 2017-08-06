from FundamentalsData import Sqlite as sql #@UnresolvedImport #@UnusedVariable
from Variables import *
from IndexData import Interface as IndexData #@UnresolvedImport

"""-----------------------------------------------------------------------------------

Inserts into tickername (in stock.db) data variable. Data variable contains dates/
price/earnings data. Data will be fed into sqldata base as something like.

(dates, Revenue-Q,......etc)
(11/9/2016, 855000,......etc)

-----------------------------------------------------------------------------------"""
def insertSQL(tickerName, data):      
    """IF read directly from excel, data comes in like this:
    date...9/16/2016
    Revenue... 5000
    etc. """
    
    """If it is the other way around ex:
    date revenue etc...
    9/16/2016 """
    """Flip it so that it is input correctly """
    if('Price' in data[0]):
        tempData = data
        data = []
        for i in range(0,len(tempData[0])):
            tempArray = []
            for j in range(0,len(tempData)):
                tempArray.append(tempData[j][i])
#             print(tempArray)
            data.append(tempArray)
             
#     for i in data:
#         print(i)
              
    '''Data should be in the following format. MUST HAVE rowID AS FIRST COLUMN'''
    '''rowID | revenues | etc '''
    '''1 | 500 | etc'''
    columnLength = len(data[0])
    temp1 = []
    temp1.append('rowID')
    for i in range(1,columnLength):
        temp1.append(i)
        
    tempData = data
    data = []
    data.append(temp1)
    for i in tempData:
        data.append(i)
            
    ''' Make text CC1 TEXT, CC2 TEXT, .... '''
    columnText = ""
    questionText = ""
              
    for i in range(0,len(data)):
        columnText += 'CC' + str(i) + ' TEXT,'
        questionText += '?,'
    columnText = columnText[0:len(columnText)-1]
    questionText = questionText[0:len(questionText)-1]
        
#     for i in data:
#         print(i)
    
    previousData = getData(tickerName)
    sql.execute('DROP TABLE IF EXISTS ' + tickerName, None)
    sql.execute('CREATE TABLE ' + tickerName + '(' + columnText + ')', None)
               
    try: 
        totalText = ''
        for i in range(0, len(data[0])):
            totalText += '('
            for j in range(0, len(data)):
                totalText += "'" + str(data[j][i]) + "',"
            totalText = totalText[0:len(totalText) -1 ]
            totalText += '),'
     
        
        totalText = totalText[0:len(totalText)-1]
        sql.execute('INSERT INTO ' + tickerName + ' VALUES ' + totalText , None)
    except:
        data = previousData
        totalText = ''
        for i in range(0, len(data[0])):
            totalText += '('
            for j in range(0, len(data)):
                totalText += "'" + str(data[j][i]) + "',"
            totalText = totalText[0:len(totalText) -1 ]
            totalText += '),'
     
        
        totalText = totalText[0:len(totalText)-1]
        sql.execute('INSERT INTO ' + tickerName + ' VALUES ' + totalText , None)


"""-----------------------------------------------------------------------------------

Returns fundamental data from Fundamentals.db

-----------------------------------------------------------------------------------"""
def getData(tickerName):   
#     print(tickerName)
    tempData = sql.executeReturn('SELECT * FROM ' + tickerName)
    data = []
    
    for i in tempData:
        temp = i[1:len(i)]
        tempArr = []
        for j in temp:
            tempArr.append(j)
        data.append(tempArr)
    
    return data


""" 
Dow30 Conversion 
"""

def removeTable(tickerName):
    sql.execute('DROP TABLE IF EXISTS ' + tickerName, None)
    

def getAllTables():
    allTables = sql.executeReturn("SELECT name FROM sqlite_master WHERE type = 'table';")
    tables = []
    
    for i in allTables:
        print(i)
        
    for i in allTables:
        tables.append(i[0])
    
    return tables

def removeExtra():
    dow30 = IndexData.getList()
    regression = getAllTables()
     
    
    for i in regression:
       if(i not in dow30):
           removeTable(i)


