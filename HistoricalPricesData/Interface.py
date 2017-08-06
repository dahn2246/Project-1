from HistoricalPricesData import Sqlite as sql #@UnresolvedImport #@UnusedVariable
from HistoricalPricesData import Download #@UnresolvedImport
from IndexData import Interface as IndexData #@UnresolvedImport

"""-----------------------------------------------------------------------------------

This method will insert price history into sqlite database called HistoricalPrices.db
An array will be sent in the following table format: 

[0-date, 1-open, 2-high, 3-low, 4-close, 5-adj-price, 6-volume, 7-split-price ]

-----------------------------------------------------------------------------------"""
def insertMechanism(tickerName, data):
    sql.execute('DROP TABLE IF EXISTS ' + tickerName, None)
    sql.execute('CREATE TABLE ' + tickerName + '(CC0 TEXT, CC1 TEXT, CC2 TEXT, CC3 TEXT, CC4 TEXT, CC5 TEXT, CC6 TEXT, CC7 TEXT)', None)
    
    totalText = ''
    for i in data:
        totalText += '('
        for j in i:
            totalText += "'" + str(j) + "',"
        totalText = totalText[0:len(totalText) -1 ]
        totalText += '),'
#             tempArray.append(j)
#         totalText += valuesText + ','
    
    totalText = totalText[0:len(totalText)-1]
    sql.execute('INSERT INTO ' + tickerName + ' VALUES ' + totalText , None)

"""-----------------------------------------------------------------------------------

Inserts historical price data into sqlite database called HistoricalPrice.db. Table will be
named tickerName_Historical and will have the following table format:

[0-date, 1-open, 2-high, 3-low, 4-close, 5-adj-price, 6-volume, 7-split-price ]

-----------------------------------------------------------------------------------"""
# def insertHistoricalPrice(tickerName):
#     data = Download.getHistoricalPrices(tickerName) 
#     insertMechanism(tickerName, data)

# insertHistoricalPrice('AAPL')

"""-----------------------------------------------------------------------------------

Updates Historical Price by scraping Yahoo Finance

-----------------------------------------------------------------------------------"""
def updateHistoricalPrice(tickerName):
    tableName = tickerName
    
    tempData = sql.executeReturn('SELECT * FROM ' + tableName)
    sqlData = []
    for i in tempData:
        temp = []
        for j in i:
            temp.append(j)
        sqlData.append(temp)
        
    newData = Download.updateHistoricalPrice(tickerName, sqlData) #@Unresolved
    
#     for i in newData:
#         print(i)
    insertMechanism(tickerName, newData)
    
# updateHistoricalPrice('BECN')

"""-----------------------------------------------------------------------------------

Returns all historical price data of tickername in the format:
[0-date, 1-open, 2-high, 3-low, 4-close, 5-adj-price, 6-volume, 7-split-price ]

-----------------------------------------------------------------------------------"""
def getHistoricalPrices(tickerName):
    tempData = sql.executeReturn( 'SELECT * FROM ' + tickerName)
    
    data = []
    
    for i in tempData:
        temp = [] 
        for j in i:
            temp.append(j)
        data.append(temp)
    
    return data

# data = getHistoricalPrices('BECN')
# for i in data:
#     print(i)

  
"""-----------------------------------------------------------------------------------
 
Returns all historical price data of tickername in the format:
[0-date, 1-split-price ]
 
-----------------------------------------------------------------------------------"""
def getHistoricalSplit(tickerName):
    tempData = sql.executeReturn('SELECT * FROM ' + tickerName)
    data = []
     
    for i in tempData:
        data.append([i[0], float(i[7])])
     
    return data

  
"""-----------------------------------------------------------------------------------
 
 Update all historical prices

-----------------------------------------------------------------------------------"""
def updateAllHistoricalPrices():
    list = IndexData.getList()
    badlist = []
     
    for i in list:
        try:
            print(i)
            updateHistoricalPrice(i)
        except:
            badlist.append(i)
    print(badlist)

# list = IndexData.getList()
# for i in list:
#     price = getHistoricalPrices(i)
#     for j in price:
#         print(j)


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
        
