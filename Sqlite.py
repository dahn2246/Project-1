import sqlite3
from time import sleep
import threading

'''----------------------------------------------------------------------
Table name is stocklist

Variables - TICKER : name of stock ticker name
            DATE : date when stock was updated
            INDEX_NUM : Index # of stock 
            REGRESSION : If value = 1, regression value is > .75
            DATEFIX : If value = 1, Dates are messed up so fix it
                    : If value = 0, dates are ok
            
Also contains tables of all stocks with earnings information
Variables - CC1, CC2, ...

Table called SP500list
Contains S&P 500 stocks as of 1/3/2017

Table called list
Contains list of tickers that analysis works
TICKER | TEXT
As of 29 March 2017, 1483 tickers
Contains tickers > 2B market cap

Table called allstocks
-Stocks that have not yet have data downloaded
rowID INTEGER, TICKER TEXT, NAME TEXT, MARKETCAP TEXT


**************Important sqlite queries:***************************
Create table : CREATE TABLE tablename (date TEXT)

Insert : INSERT INTO tablename (variable) VALUES ()
    ex. INSERT INTO stocktable (TICKER) VALUES ('AAPL')

Get all tables from database : "SELECT name FROM sqlite_master WHERE type = 'table';" 

Delete table : "DROP TABLE IF EXISTS " + tablename

Delete row in table : "DELETE FROM tablename WHERE column = columnname
    ex. DELETE FROM stocklist WHERE TICKER = SWKS 

Delete duplicates inside table : "DELETE FROM stocklist WHERE rowid NOT IN (SELECT MAX(rowid) FROM stocklist GROUP BY TICKER)"

Get All tables : "SELECT name FROM sqlite_master WHERE type = 'table';"

Get Column Names : PRAGMA table_info('table_name') 

Update Entries : UPDATE table SET variable = ? WHERE rowid = 5

-----------------------------------------------------------------------'''

def execute(commands, input):
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    
    if(input == None or input == False):
        c.execute(commands)
    else:
        c.execute(commands,input)
    
    conn.commit()
    conn.close()


def executeReturn(commands):
    returnArray = []
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    
    cursor = c.execute(commands)
    
    for i in cursor:
        returnArray.append(i)
    
    conn.commit()
    conn.close()
    
    return returnArray    

'''-----------------------------------------------------------------------------

Testing / Manipulating tables

-----------------------------------------------------------------------------'''

'''-----------------------UTILITY METHODS---------------'''        
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

fixSQL "fixes" SQL databases. If priceAvg or price is empty, drops row. 
OR, if more than 20% of database is empty, drops row. 

-----------------------------------------------------------------------------'''
def fixSQL(tickerName):
    stockdata = getData(tickerName)
    
    fixedData = []    
    
    for j in stockdata:        
        """First check to see if price and priceavg are there. If not, don't add. """
        priceAvg = j[len(j)-1]
        price = j[len(j)-2]
        goodLen = len(j)-5
        badCount = 0
        
        if(priceAvg == '' or priceAvg == ' '):
            continue
        elif(price == '' or price == ' '):
            continue
        
        for i in range(2,len(j)-3):
            if(j[i] == '' or j[i] == ' '):
                badCount += 1
        
        if(badCount > (0.20 * goodLen)):
            continue
    
        fixedData.append(j)
    
    
    insertSQL(tickerName,fixedData)


def insertML(tickerName, multipleLinear):
    tableName = tickerName + '_ML'
    
    execute('DROP TABLE IF EXISTS ' + tableName, None)
    execute('CREATE TABLE ' + tableName + '(CC0 REAL, CC1 REAL, CC2 TEXT)', None)
    
    for i in multipleLinear:
        tempArray = [i[0],i[1],str(i[2])]
        execute('INSERT INTO ' + tableName + ' VALUES (?,?,?)', tempArray)

# keywords = [[5.5,3.53,[["Revenues-Q","Dividends per Basic Common Share-Q", "Revenue Growth-QG"] ,
#                     ["Revenues-T", "Dividends per Basic Common Share-T"] ,
#                     ["Earnings per Diluted Share-Q","Book Value per Share-QM"] ,
#                     ["Weighted Average Shares-T", "Operating Expenses-Q", "Cash and Equivalents-QB", "Investments-QB"]
#     ]]]    
#   
# insertML('TEST', keywords)
#   
# for i in getML('TEST'):
#     print(i)
# #     for j in i:
# #         print(j)

'''-----------------------------------------------------------------------------

Cleans stock ticker data so that tables have
Variables...
Data.....
ONLY

-----------------------------------------------------------------------------'''

def cleanDataInsert():
    temp1 = executeReturn('SELECT * FROM list')         
    list = []
          
    for i in temp1:
        list.append(i[0])
        
#     list = ['CMCSA']
    
    letspass = False    
    
    for ticker in list:
        letspass = False
        print(ticker)
        temp1 = executeReturn('SELECT * FROM ' + ticker)
        sqlData = []
        clean = []
    
        for i in temp1:
            sqlData.append(i) 
#             print(i)
        
#         for i in sqlData:
#             print(i)
        
        counter = 0 
        '''------ First one sees if data is in rowID format  ----'''
        for i in sqlData:
            print(i)
            if(i[0] == 'rowID'):
                letspass = True
                print('done')
                print(letspass)
                break
             
            elif(i[0] == 'dates' and counter == 0):
                print('doneeee')
                temp2 = []
                temp2.append('rowID')
                 
                for j in i:
                    temp2.append(j)
                 
                clean.append(temp2)
             
            elif(i[0] == 'dates' and counter != 0):
                continue
             
            elif(i[0] == ' ' or i[0] == '' or i[0] == '0'):
                continue
             
            else:
                temp2 = []
                temp2.append(counter)
                 
                for j in i:
                    temp2.append(j)
                 
                clean.append(temp2)
             
            counter += 1
            
         
#         print('cleannnn')
#         for i in clean:
#             print(i)
#         print(letspass)
        
        if(letspass == False):
            insert = []
             
            rows = len(clean)
            columns = len(clean[0])
             
            for i in range(0,columns):
                temp2 = []
                for j in range(0,rows):
                    temp2.append(clean[j][i])
                     
                insert.append(temp2)
            
#             print('Hello lets pass')
#             for i in insert:
#                 print(i)
#             print('setting into sql')

            insertSQL(ticker, insert)
        

def cleanData(data): 
    counter = 0
    clean = []
    
    for i in data:
        print(i)
    
    for i in data:
        if(i[0] == 'dates' and counter == 0):
            temp2 = []
            
            for j in i:
                temp2.append(j)
            
            clean.append(temp2)
    
        elif(i[0] == 'dates' and counter != 0):
            continue
    
        elif(i[0] == ' ' or i[0] == '' or i[0] == '0'):
            continue
    
        else:
            temp2 = []
            temp2.append(counter)
    
            for j in i:
                temp2.append(j)
    
            clean.append(temp2)
    
        counter += 1
    
    insert = []
    rows = len(clean)
    columns = len(clean[0])
    
    for i in range(0,columns):
        temp2 = []
        for j in range(0,rows):
            temp2.append(clean[j][i])
             
        insert.append(temp2)
        
    for i in insert:
        print(i)
    
    return insert
    
#     nolist = ['ASML', 'CSAL', 'FHB', 'GWPH', 'ICLR','NTNX', 'QGEN', 'TIVO', 'AGU', 'AA', 'ABEV', 'AZN', 'CWH', 'CNI', 'CHL', 'COTV', 'DEO', 'GGB', 'GSK', 'IHG', 'KGC', 'MFC', 'NMR', 'NORD', 'NVS', 'IX', 'PSO', 'RIO', 'RCI', 'SHI', 'SNN', 'TWLO', 'VVV', 'VSM', 'WBK', 'WIT']
#     

# cleanData()
       
# bad = 'AAPL'
# ticker = bad
#                     
# temp1 = executeReturn('SELECT * FROM ' + ticker)
# for i in temp1:
#     print(i)
       


''' --This bit of code took data from nyse.csv, nasdaq.csv etc and then
        put them into table called allstocks. - '''
#nasdaq - done
#amex - done
#nyse - done
# execute('DROP TABLE IF EXISTS allstocks',None)
# execute('CREATE TABLE allstocks (rowid INTEGER, TICKER TEXT, NAME TEXT, MARKETCAP TEXT)', None)
# stfile = ['D:/cmsc/Stock Analysis/nasdaq.csv',
#           'D:/cmsc/Stock Analysis/amex.csv',
#           'D:/cmsc/Stock Analysis/nyse.csv']

# count = 0 
# 
# temp1 = executeReturn('SELECT * from allstocks')
# allstock = []
# allnames = []
# 
# for i in temp1:
#     allnames.append(i[1])
#     allstock.append(i)
#     print(i)
#     
# ID = allstock[len(allstock)-1][0]
# ID += 1
# 
# for kk in stfile:
#     data = ReadExcel.readCSV(kk)
#         
#     for i in data:
#         ticker = i[0].strip()
#         raw = i[3].strip()
#         marketCap = raw[1:len(raw)-1]
#         MorB = raw[len(raw)-1]
#          
#                         
#         if(len(marketCap) > 0 and marketCap[len(marketCap)-1] == '.'):
#             marketCap = marketCap[0:len(marketCap)-1]
#         try:
#             marketCap = float(marketCap)
#             print(marketCap)
#         except:
#             continue
#          
#         marketCap = str(marketCap) + MorB
#         print(ticker + " : " + marketCap)
#      
#         if(ticker in allnames):
#             execute("UPDATE allstocks SET MARKETCAP = ? WHERE TICKER = '" + ticker + "'", [marketCap])
#         elif(ticker not in allnames):
#             execute("INSERT INTO allstocks (rowid, TICKER, NAME, MARKETCAP) VALUES (?,?,?,?)",[ID, str(i[0]).strip(), str(i[1]).strip(), str(i[2]).strip()])
#             ID += 1

#         if ticker not in list:
#         print(ticker)
#         execute("INSERT INTO allstocks (rowid, TICKER, NAME, MARKETCAP) VALUES (?,?,?,?)",[count, str(i[0]).strip(), str(i[1]).strip(), str(i[2]).strip()])
#              
#         print(str(i[0]) + " " + str(i[3]))
          




