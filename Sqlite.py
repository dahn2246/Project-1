import sqlite3

'''----------------------------------------------------------------------
Table called list
Contains list of tickers that are actively analyzed 
TICKER | TEXT
As of 26 April 2017, 1483 tickers
Contains tickers > 2B market cap

All stocks that have been analyzed have the following:
table with tickerName - contains earnings data
table with tickerName + '_ML'- contains ML data
table with tickerName + '_Historical' - contains historical data

OTHER: 
Table called allstocks
-Stocks that have not yet have data downloaded
rowID INTEGER, TICKER TEXT, NAME TEXT, MARKETCAP TEXT

Table called SP500list
Contains S&P 500 stocks as of 1/3/2017


**************Important sqlite queries:***************************
Create table : CREATE TABLE tablename (date TEXT)

Insert : INSERT INTO tablename (variable) VALUES ()
    ex. INSERT INTO stocktable (TICKER) VALUES ('AAPL')

Get all tables from database : "SELECT name FROM sqlite_master WHERE type = 'table';" 

Delete table : "DROP TABLE IF EXISTS " + tablename

Delete row in table : "DELETE FROM tablename WHERE column = columnname
    ex. DELETE FROM stocklist WHERE TICKER = SWKS 

Delete duplicates inside table : "DELETE FROM stocklist WHERE rowid NOT IN (SELECT MAX(rowid) FROM stocklist GROUP BY TICKER)"

Get Column Names : PRAGMA table_info('table_name') 

Update Entries : UPDATE table SET variable = ? WHERE rowid = 5

-----------------------------------------------------------------------'''
def execute(commands, input):
    conn = sqlite3.connect('dow30.db')
    c = conn.cursor()
    
    if(input == None or input == False):
        c.execute(commands)
    else:
        c.execute(commands,input)
    
    conn.commit()
    conn.close()


def executeReturn(commands):
    returnArray = []
    conn = sqlite3.connect('dow30.db')
    c = conn.cursor()
    
    cursor = c.execute(commands)
    
    for i in cursor:
        returnArray.append(i)
    
    conn.commit()
    conn.close()
    
    return returnArray     

# data = executeReturn("SELECT name FROM sqlite_master WHERE type = 'table';") 
# for i in data:
#     print(i)


'''-----------------------------------------------------------------------------

Retrieving data from sql tables. 
getData - returns all earnings data
getML - returns muliple linear regression data
getHistorical & get HistoricalClose - gets price data. 

-----------------------------------------------------------------------------'''    
def getData(tickerName):
    price, priceAvg = [], []
    ones = []
    
    ''' Data about stock ticker '''
    ''' Will remove rowId and numbers in rowID column'''
    tempData = executeReturn('SELECT * FROM ' + tickerName)
    variables = tempData[0][1:len(tempData[0])]
    tempData = tempData[1:len(tempData)]
    data = []
    data.append(variables)
    
    for i in tempData:
        data.append(i[1:len(i)])
        
    return data

def getML(tickerName):
    tableName = tickerName + '_ML'
    
    tempData = executeReturn('SELECT * FROM ' + tableName)
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

def getHistorical(tickerName):
    tempData = executeReturn('SELECT * FROM ' + tickerName + '_Historical')
    data = []
    
    for i in tempData:
        temp = [] 
        for j in i:
            temp.append(j)
        data.append(temp)
    
    return data

def getHistoricalClose(tickerName):
    tempData = executeReturn('SELECT * FROM ' + tickerName + '_Historical')
    data = []
    
    for i in tempData:
        data.append([i[0], float(i[5])])
    
    return data
 
# data = getHistoricalClose('HES')
# for i in data:
#     print(i)

'''-----------------------------------------------------------------------------

Inserts into tickername (in stock.db) data variable. Data variable contains dates/
price/earnings data. Data will be fed into sqldata base as something like.

(dates, Revenue-Q,......etc)
(11/9/2016, 855000,......etc)

-----------------------------------------------------------------------------'''
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
        
    execute('DROP TABLE IF EXISTS ' + tickerName, None)
    execute('CREATE TABLE ' + tickerName + '(' + columnText + ')', None)
                
            
    '''Feed data into sqlite'''
    for i in range(0,len(data[1])):
        tempArray = []
        for  j in range(0,len(data)):
            tempArray.append(data[j][i])
#         print(tempArray)
        execute('INSERT INTO ' + tickerName + ' VALUES (' + questionText + ')', tempArray)

'''-----------------------------------------------------------------------------

Inserts multiple linear analysis information such as regressed price, r^2 adj,
and keywords used for regression. This is called by the analyze() function which is
faster than performing actual ML analysis.

-----------------------------------------------------------------------------'''

def insertML(tickerName, multipleLinear):
    tableName = tickerName + '_ML'
    
    execute('DROP TABLE IF EXISTS ' + tableName, None)
    execute('CREATE TABLE ' + tableName + '(CC0 REAL, CC1 REAL, CC2 TEXT)', None)
    
    for i in multipleLinear:
        tempArray = [i[0],i[1],str(i[2])]
        execute('INSERT INTO ' + tableName + ' VALUES (?,?,?)', tempArray)
        
'''-----------------------------------------------------------------------------

Inserts historical price information from yahoo finance. As of MAy 2017, automated
download of yahoo finance stock tickers does not work. Therefore, the historical 
prices spanning ~ last 10 years is stored into sql. 

-----------------------------------------------------------------------------'''
def insertHistorical(tickerName, data):
    tableName = tickerName + '_Historical'
    
    execute('DROP TABLE IF EXISTS ' + tableName, None)
    execute('CREATE TABLE ' + tableName + '(CC0 TEXT, CC1 TEXT, CC2 TEXT, CC3 TEXT, CC4 TEXT, CC5 TEXT, CC6 TEXT)', None)
    
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
#     print(totalText)
    execute('INSERT INTO ' + tableName + ' VALUES ' + totalText , None)
    

# dow30 = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DIS', 'DD', 'XOM', 'GE', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 
#          'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'UTX', 'UNH', 'VZ', 'V', 'WMT']

# for i in range(10,len(dow30)):
#     print(i)
#     data = getData(dow30[i])
#     insertSQL(dow30[i], data)
#     
#     ML = getML(dow30[i])
#     insertML(dow30[i], ML)
#     
#     historical = getHistorical(dow30[i])
#     insertHistorical(dow30[i], historical)

