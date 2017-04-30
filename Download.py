import urllib
from urllib import request
from bs4 import BeautifulSoup
import os
import Text
import Utility
import Sqlite as sql
import ReadExcel as excel
from Variables import *            
            

'''-----------------------------------------------------------------------------

Downloads price data from Yahoo finance and stockrow.com. Also adds file ending
to excel files. 

--------------------------------------------------------------------------------'''
def downloadAll(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    urlList = fileVariables.returnUrlList(tickerName)
    
#     print(urlList)
    
    counter = 0
    for i in urlList:
        try:
            request.urlretrieve(i,directory + fileEnding[counter])
            counter += 1
        
        except Exception as inst:
            print(i)
            print(inst)


                 
'''-----------------------------------------------------------------------------

Delete all files related to tickerName

--------------------------------------------------------------------------------'''
def deleteAll(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)
    
    for i in fileEnding:
        try:
            os.remove(directory+i)
        except:
            pass
    
    
'''-----------------------------------------------------
Downloads stocks from stockrow, yahoo. 
Extracts Data 
Puts into sqlite

Note: This is not for updating. It will delete sql table with ticker name
and recreate it. 

-------------------------------------------------------'''   
def dlAdd(tickerName): 
    deleteAll(tickerName)
    downloadAll(tickerName)
    data = excel.getData(tickerName)
    sql.insertSQL(tickerName, data)

# list = ['ASBB', 'AMTX', 'AGEN', 'ALGT', 'AHGP', 'ARLP', 'GOOGL', 'AMDA', 'AMWD', 'AMGN', 'ANIK','ANSS','ANTH','AAPL','ASBB']
# for ticker in list:
# #     dlAdd(ticker)
#     print(ticker)
# for i in list:
#     ticker = i
#     dlAdd(ticker)
#     stockdata = sql.executeReturn("SELECT * from " + ticker)
#      
#     for i in stockdata:
#         print(i)


# ticker = 'AAPL'
# dlAdd(ticker)
# stockdata = sql.executeReturn("SELECT * from " + ticker)
#   
# for i in stockdata:
#     print(i)
        
'''-----------------------------------------------------

UpdateTicker function will do following:
- Delete Excel files associated with tickerName from stockrow.com and yahoo finance.
- Download new Excel files
- Retrieve current data in sql and extract data from new Excel files. 
- Determine difference between current sql data and new data from Excel files. 
- Perform partial update or total update

-------------------------------------------------------'''   
def updateTicker(tickerName):
    deleteAll(tickerName)
    downloadAll(tickerName)
    
    '''Delete and download excel files. Then gets information off excel files'''
    data = excel.getData(tickerName)
    '''Will get SQL data too '''
    sqlData = sql.getData(tickerName)
    
#     for i in data:
#         print(i)
#            
#     for i in sqlData:
#         print(i)
    
    '''Compare data with sqlData'''
    newDates = data[0]
    newDates = newDates[1:len(newDates)]
    oldDates = []
    addDates = []
    
    for i in sqlData:
        oldDates.append(i[0])
        
    '''Done to remove 'dates' entry '''
    temp = newDates
    newDates = []
    for i in temp:
        if(i != 'dates'):
            newDates.append(i)
    
    temp = oldDates
    oldDates = []
    for i in temp:
        if(i != 'dates'):
            oldDates.append(i)
#             print(i)
            
#     print(newDates)
    
#     for i in data:
#         print(i)
# 
#     print("")

#     for i in sqlData:
#     print(i)
#     print(newDates)
#     print(oldDates)

    '''Compares dates from new Excel data and old (current) sql data
    This will find if new Excel data doesn't have some previous dates
    or if old (current) data needs to be updated with newer dates'''
    for i in range(0,len(oldDates)):
        if oldDates[i] in newDates:
            continue
        else:
            addDates.append(oldDates[i])
            
#     print(addDates)
         
    '''Variables from downloaded files may differ from those in initial sql. Index of variables
    updated will be added to an index '''
       
    newVariables = []
    oldVariables = sqlData[0]
#     variableIndex = []
    
    for i in data:
        newVariables.append(i[0])
    
#     for i in oldVariables:
#         for j in range(0,len(newVariables)):
#             if(i == newVariables[j]):
#                 variableIndex.append(j)
#                 newVariables[j] = ' '
#                 continue
#     print(variableIndex)
#     for i in data:
#         print(i)     
    
#     print(addDates)
    
    '''Add old data into new data '''
    temp = []
    if(len(addDates) > 0):
        for i in addDates:
            index = 0 
            for j in range(0,len(oldDates)):
                if(i == oldDates[j]):
                    index = j + 1
                    continue
            
            for j in range(0,len(newVariables)):
                varIndex = -1
                for k in range(0,len(oldVariables)):
                    if(newVariables[j] == oldVariables[k]):
                        varIndex = k 
                        continue

                if(varIndex == -1):
                    temp.append('0')
                else:                
                    temp.append(sqlData[index][varIndex])
                    
            for j in range(0,len(data)):
                data[j].append(temp[j])
                    
#     for i in data:
#         print(i)

 
#     '''If newVariables is same as oldVariables AND no new dates to add.
#     Simply return '''
#     if(len(newVariables) == len(oldVariables) and len(addDates) == 0):
# #         print('test')
#         return
#     
#     '''If there are more variables with new data, add whole thing in'''
#     if(len(newVariables) != len(oldVariables)):
#         sql.insertSQL(tickerName,data)
#         return
#     insert = sql.cleanData(data)
    sql.insertSQL(tickerName, data)


# updateTicker('AAPL')

# dlAdd('ATRI')   
# data = excel.getData('ATRI')
# for i in data:
#     print(i)

"""-----------------------------------------------------

Get exact earnings dates so that average price is more accurate. 
First try Zacks.com to get exact earnings dates. 

-------------------------------------------------------"""
def exactEarnings(tickerName):
    exactDates = []
    zacksWebsite = "https://www.zacks.com/stock/research/" + tickerName + "/earnings-announcements"
    
    tempWebFile = request.urlopen(zacksWebsite).read()
    tempData = BeautifulSoup(tempWebFile, "lxml")
    html = tempData.prettify()
    
    lines = tempData.find_all('script')
    keyword = 'var obj ='
    keyword1 = '"earnings_announcements_earnings_table"'
    keyword2 = '"earnings_announcements_webcasts_table"'
    
    '''Will get SQL data too '''
    sqlData = sql.getData(tickerName)
    
    for i in sqlData:
        print(i)
    
    for i in lines:
        stringTemp = str(i)
        keywordIndex = stringTemp.find(keyword)

        payload = ''
        
        if(keywordIndex > -1):
            stringTemp = stringTemp[keywordIndex:]
            keywordIndex1 = stringTemp.find(keyword1)
            keywordIndex2 = stringTemp.find(keyword2)
            
            payload = stringTemp[keywordIndex1 + len(keyword1) + 4 :keywordIndex2]
            
            """Get string with dates. """
            k = 0 
            while(payload[k] != '['):
                k += 1 
            
            payload = payload[k + 1:]
            
            lastBracket = ''           
            for k in range(0, len(payload)):
                if(payload[k] == ']' and lastBracket == ']'):
                    payload = payload[:k].strip()
                    break
            
                if(payload[k] == ']'):
                    lastBracket = ']'
                elif(payload[k] == '['):
                    lastBracket = '['
            break
    
    dates = payload.split(',')
    
    
    for i in dates:
        i = i.replace('"', '')
        i = i.replace('[', '')
        i = i.replace(']', '')
        i = i.strip()
        
        split = i.split('/')
        
        """Dates are in format : MM/DD/YYYY"""
        
        if(len(split) > 2):
            """Dates are reformatted : YYYY/MM/DD """
            newDate = str(split[2]) + '/' + str(split[0]) + '/' + str(split[1])
            exactDates.append(newDate)
    
    sqlDates = []
    
    for i in sqlData:
        if(i[0] != 'dates'):
            sqlDates.append(i[0])
    
    adjustedDates = excel.adjustedDate(sqlDates)[1:]

    """Make sure exactDates matches with actual earnings data. Compare exact dates to adjusted dates by making a 2 month window """
    exactDatesAppend = []

    for i in exactDates: 
        print('i = ' + i)
        temp = i.split('/')
        exactDate = []
        exactDate.append(float(temp[0]))
        exactDate.append(float(temp[1]))
        exactDate.append(float(temp[2]))
        
        for j in adjustedDates: 
            temp = j.split('/')
            adjDate = []
            adjDate.append(float(temp[0]))
            adjDate.append(float(temp[1]))
            adjDate.append(float(temp[2]))
            
            """Create a 2 month window for exact date"""
            """ YYYY/MM/DD """
            left = exactDate[1] - 1
            right = exactDate[1] + 1
            year_left = exactDate[0]
            year_right = exactDate[0]
            
            if(left < 1):
                year_left -= 2
                left += 12
            elif(right > 12):
                year_right += 2
                right -= 12
            
            
            
            if( year_right == adjDate[0]):

                if(left > right):
                    if((left <= adjDate[1] and adjDate[1] <= 12) or (1 <= adjDate[1] and adjDate[1] <= right)):
                        print(str(left) + " : " + str(right) + ' : ' + str(year_left) + ' : ' + str(year_right))
                        print(adjDate)
                        exactDatesAppend.append(i)
                        continue
                else:
                    if(left <= adjDate[1] and adjDate[1] <= right):
                        print(str(left) + " : " + str(right) + ' : ' + str(year_left) + ' : ' + str(year_right))
                        print(adjDate)
                        exactDatesAppend.append(i)
                        continue
                
            
        
    

    print(adjustedDates)    
#     print(sqlDates)
    print(exactDates)
    print(exactDatesAppend)
    
    historicalPrices = excel.getHistoricalPrices(tickerName, exactDates)
    
    
#     for i in historicalPrices:
#         print(i)
    
#     tempData = []    
#     for i in sqlData:
#         for j in i:
#             tempData.append(j)
            
    
#     return exactDates

#     
#         
#         k = 0
#         while(lastBracket == False and payload[k] != ']'):
#             print(payload[k])
        
#         payload = payload.split(',')
#         print(payload)


temp1 = exactEarnings('AAPL')
# for i in temp1:
#     print(i)
