from Variables import * 
import xlrd
import xlwt
import csv
from urllib import request
from bs4 import BeautifulSoup


"""-----------------------------------------------------------------------------------

Creates historical data array with entry for split only adjusted price. 

-----------------------------------------------------------------------------------"""
def addHistoricalSplit(data):
    tempData = data
    data = []
    
    for i in tempData:
        data.append(i[0:7])
    
    """data is in format: 
    0-date, 1-open, 2-high, 3-low, 4-close, 5-adj-close, 6-volume. 
    """
    data[0].append(data[0][4])
    divisor = 1
    for i in range(1, len(data)):
        currentDayClose = float(data[i-1][4])
        previousDayClose = float(data[i][4])
        pctClose = (currentDayClose-previousDayClose)/currentDayClose
        onePercent = 0.025
        
        currentDayAdj = float(data[i-1][5])
        previousDayAdj = float(data[i][5])
        pctAdj = (currentDayAdj - previousDayAdj)/currentDayAdj
        
        """If there is a difference between pctClose and pctAdj, usually means
        a dividend or split occured. A dividend is not as big as a split so if
        the difference is 2.5%, the difference is classified as a dividend. 
        Anything larger is classified as a split.  """
        if((pctClose - onePercent) <= pctAdj and pctAdj <=  (pctClose + onePercent)):
            pass
        else:
            withoutSplit = currentDayClose * (1 - pctAdj)
            split = previousDayClose / withoutSplit
            divisor *= split
        
        if(divisor != 1): 
            data[i].append(float(data[i][4])/divisor)
        else:
            data[i].append(float(data[i][4]))
    
#     for i in data:
#         print(i)
    return data

"""-----------------------------------------------------------------------------------

Returns historical stock data in array with [date, closing price] 

-----------------------------------------------------------------------------------"""
def getHistoricalPrices(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)

    try:
        csv_file = open(directory + tickerName+'-Y.csv', "r")
        reader = csv.reader(csv_file, delimiter = ' ')
        yahoo_data_array = []
    except:
        try:
            csv_file = open(directory + tickerName+'.csv', "r")
            reader = csv.reader(csv_file, delimiter = ' ')
            yahoo_data_array = []
        except:
            print('Error : File Not Opening')

    switched = False
    for lines in reader:
        if('Date' in lines or 'Date' in lines[0].split(',')):
            split = lines[0].split(',')
            if(split[5] == 'Volume'):
                switched = True
            pass
        else:
            yahoo_data_array.insert(0,lines[0].split(','))
#     print(switched)
        
    """If volume and adj close is switched, switch it around [5] and [6]""" 
    if(switched == True):
        index = 0 
        for i in yahoo_data_array:
            temp = []
            if(i[5] == 'null'):
                del yahoo_data_array[index]
                continue
            for j in range(0,5):
                temp.append(i[j])
            temp.append(i[6])
            temp.append(i[5])
            del yahoo_data_array[index]
            yahoo_data_array.insert(index, temp)
            index += 1
            
        
    for i in yahoo_data_array:
        dates = i[0].split('-')
        i[0] = dates[0] + '/' + dates[1] + '/' + dates[2]

    firstDate = float(yahoo_data_array[0][0].split('/')[0])
    if(firstDate < 2016):
        yahoo_data_array.reverse()
    
    
    i = 0
    while(i < len(yahoo_data_array)):
        if('null' in yahoo_data_array[i]):
            del yahoo_data_array[i]
            i -= 1
        i += 1
        
    yahoo_data_array = addHistoricalSplit(yahoo_data_array)
    
    return yahoo_data_array

    
# insertHistoricalData('AMWD')
# data = interface.getHistoricalClose('AAPL')
# for i in data:
#     print(i)

"""-----------------------------------------------------------------------------------

As of 18 May 2017 getting historical stock prices off of Yahoo Finance does not work. 
What I need to do is make my own database by first downloading excel data from Yahoo 
Finance by hand. This historical closing stock data is then updated by scraping either
Yahoo finance website or Google finance. 

The first method is take historical data downloaded by hand and put them
in stock.db

This method is for scraping and then updating data for stock. 

-----------------------------------------------------------------------------------"""
def updateHistoricalPrice(tickerName, sqlData):  
    yahooFinance = "https://finance.yahoo.com/quote/" + tickerName + "/history?p=" + tickerName
    
    tempWebFile = request.urlopen(yahooFinance).read()
    tempData = BeautifulSoup(tempWebFile, "lxml")
    
    lines = tempData.find_all('div')
    priceInfo = ''
    
    for i in lines:
        if str(i).find('data-test="historical-prices"') > 0:
            priceInfo = str(i)
            
#     print(priceInfo)

    month1 = [["Jan", 1], ["Feb", 2], ["Mar", 3], ["Apr", 4], ["May", 5], ["Jun", 6], ["Jul", 7],
              ["Aug", 8], ["Sep", 9], ["Oct", 10], ["Nov", 11], ["Dec", 12]]

    index = priceInfo.find('>')
    priceHistory = []
    priceDay = []
    foundMonth = False
    added = 0
    while(index > 0):
#         print(priceInfo)
        temp = ''
        while(index < len(priceInfo) and priceInfo[index] != '<'):
            temp += priceInfo[index]
            index += 1
        
        temp = temp[1:]

        """If temp includes a month, add next 7 """
        if(foundMonth == False):
            for i in month1:
                if (temp.find(i[0]) >= 0):
                    month = str(i[1])
                    if(float(month) < 10):
                        month = '0' + month
                    day = ''
                    
                    commaFind = 4
                    while(temp[commaFind] != ','):
                        day += temp[commaFind]
                        commaFind += 1
                    day = day.strip()
                    
                    year = temp.split(',')[1].strip()
                    date = year + '/' + month + '/' + day 
                    priceDay.append(date)

                    priceInfo = priceInfo[index:]
                    added = 0 
                    foundMonth = True  
                    break
        
        elif(foundMonth == True and added < 6):
            if(len(temp) > 0):
                keyword = temp.replace(',','')
                """Skip if the row has "Dividend" in it """
                if(keyword == 'Dividend'):
                    foundMonth = False
                    added = 0
                    priceDay = []
                else:
                    priceDay.append(keyword)
                added += 1
                 
        if(foundMonth == True and added >= 6):
            added = 0
            foundMonth = False
            priceHistory.append(priceDay)
            priceDay = []
                 
        priceInfo = priceInfo[index:]
        index = priceInfo.find('>')
        
    latestSQLDate = sqlData[0][0]
    
    index = 0
    for i in priceHistory:
#         print(i)
        if(latestSQLDate == i[0]):
            break
        index += 1
        
#     print(index)
    
    for i in range(0,index):
        sqlData.insert(i,priceHistory[i])
         
    for i in sqlData:
        if(len(i) < 8):
            i.append(i[4])
    
    sqlData = addHistoricalSplit(sqlData) 
        
    return sqlData
    
