from RegressionData import Sqlite as sql #@UnresolvedImport #@UnusedVariable

def insertRegressionData(tickerName, multipleLinear):
    tableName = tickerName 
    
    sql.execute('DROP TABLE IF EXISTS ' + tableName, None)
    sql.execute('CREATE TABLE ' + tableName + '(CC0 REAL, CC1 REAL, CC2 TEXT)', None)
    
    for i in multipleLinear:
        tempArray = [i[0],i[1],str(i[2])]
        sql.execute('INSERT INTO ' + tableName + ' VALUES (?,?,?)', tempArray)
        
        
def getRegressionData(tickerName):
    tableName = tickerName
    
    tempData = sql.executeReturn('SELECT * FROM ' + tableName)
    ML = []

    """Each i should have 
    [radjusted (float), regPrice (float), keywords (str) """
    for i in tempData:
        data = []
        data.append(float(i[0]))
        data.append(float(i[1]))
        
        keywordAdd = []
        stringToList = str(i[2])
        stringToList = stringToList[1:len(stringToList) - 2]
        
        keywordStr = stringToList.split("',")
    
        for keywords in keywordStr:
            tempKeywords = keywords.strip()[1:]

            keywordAdd.append(tempKeywords)
            
        data.append(keywordAdd)
        ML.append(data)
    
    return ML

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
    
        
# getAllTables()