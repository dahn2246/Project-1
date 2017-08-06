from IndexData import Sqlite as sql #@UnresolvedImport
from IndexData import GetSector #@UnresolvedImport

"""-----------------------------------------------------------------------

Database is called IndexData.db 

This database has a table called "list" with column
(CC0)

Database called dow30 with dow jones 30 industrial stocks

This list contains stocks to be actively analyzed.
Contains tickers > 2B market cap

Table: listIndustry with [tickerName, Sector, Industry, Empty, Empty] 
(C1 TEXT, C2 TEXT, C3 TEXT, C4 TEXT, C5 TEXT)

------------------------------------------------------------------------"""
def getList():
    returnArray = []
    
    tempData = sql.executeReturn("SELECT * FROM 'dow30'")
    
    for i in tempData:
        returnArray.append(i[0])
    
    return returnArray

def getIndustry():
    returnArray = []
    
    tempData = sql.executeReturn("SELECT * FROM 'listIndustry'")
    
    for i in tempData:
        returnArray.append(i)
    
    return returnArray

"""-----------------------------------------------------------------------

Returns all tables in the database

------------------------------------------------------------------------"""
def getAllTables():
    allTables = sql.executeReturn("SELECT name FROM sqlite_master WHERE type = 'table';")
    
    for i in allTables:
        print(i)

# getAllTables()

def removeTicker(tickerName):
    sql.execute("DELETE FROM list WHERE CC0 = ?", [tickerName])

def addList(tableName, data):
    sql.execute('DROP TABLE IF EXISTS ' + tableName, None)
    sql.execute('CREATE TABLE ' + tableName + '(CC0 TEXT)', None)
    
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
    sql.execute('INSERT INTO ' + tableName + ' VALUES ' + totalText , None)


def getCompetitors(tickerName):    
    industry = getIndustry()
    ticker = ''
    competitors = []
    
    for i in industry:
        if(i[0] == tickerName):
            ticker = i
    
    if(ticker == ''):
        return []
    
    for i in industry:
        if(i[1] == ticker[1] and i[2] == ticker[2]):
            competitors.append(i)
    
    return competitors
         
# sql.execute("CREATE TABLE dow30 (C1 TEXT)", None)
# print('hello')
# getAllTables()
# dow30 = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DIS', 'DD', 'XOM', 'GE', 'GS', 'HD', 
#          'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UTX', 'UNH',
#           'VZ', 'V', 'WMT']
# 
# for i in dow30:
#     sql.execute("INSERT INTO dow30 VALUES (?)", ([i]))
    
    
# dow30 = getList()
# regression = HistoricalPricesData.getAllTables()
#  
# 
# for i in regression:
#     if(i not in dow30):
#         HistoricalPricesData.removeTable(i)
         
# industry = getIndustry()
# 
# for i in industry:
#     print(i)

# getAllTables()   
    
    
    
    
    
    
    