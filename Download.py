from urllib import request
from bs4 import BeautifulSoup
import os
import Utility
import Sqlite as sql
from Variables import *     
import xlrd
import xlwt
import csv

"""-----------------------------------------------------------------------------------

Sometimes date from stockrow is for reported quater, not date of actual of earnings release

Note: 10 Dec 2016  - Doesn't work because many jumps exist
As of now, method will simply add 30 days to date. Will return array as follows:
['date-adj', date + 30 days..., etc] 
 
-----------------------------------------------------------------------------------"""
def adjustedDate(dates):
    monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
    count = 0
    returnArray = [] 
    returnArray.append('dates-adj')

    for i in dates:
        if(i == 'dates'):
            continue
        
        eps_dateStr = str(i).split("/")
        eps_dateInt = [int(eps_dateStr[0]), int(eps_dateStr[1]), int(eps_dateStr[2])]
         
        ''' Make eps_date go ahead 30 days '''
        '''0 - Year, 1 - Month, 2 - Day'''
        while(count < 30):
            eps_dateInt[2] = eps_dateInt[2] + 1
             
            '''If day passes to next month, month will be updated '''
            if(monthDays[eps_dateInt[1]-1] < eps_dateInt[2]):
                eps_dateInt[2] = 1
                if(eps_dateInt[1] == 12):
                    eps_dateInt[1] = 1
                    eps_dateInt[0] += 1
                else:
                    eps_dateInt[1] += 1
            count += 1
        count  = 0 
         
        returnArray.append(str(eps_dateInt[0]) + '/' + str(eps_dateInt[1]) + '/' +str(eps_dateInt[2]))
    
    return returnArray
#print(getHistoricalPrices('SWKS', ['2016/9/30', '2016/7/1', '2016/4/1', '2016/1/1']))
#print(adjustedDate(['2016/9/30', '2016/7/1', '2016/4/1', '2016/1/1']))

"""-----------------------------------------------------------------------------------

Input is ticker symbol and array of dates which are earnings dates.
Earnings dates are sometimes not accurate and must be approximated by adding +1 to the month
This will return array with columns as follows:

Date, Price on Date, 3 Month Average Price between earnings
Historical Prices will come from sql table with tickerName + '_Historical' NOT excel.

-----------------------------------------------------------------------------------"""
def getHistoricalPrices(tickerName, dates, noAdjust = None):
    """If noAdjust is None, use adjustedDate to add 1 month to quarterly dates to estimate
    when financial data came out. Otherwise, dates is exact dates from Zacks"""
    eps_date = ""
    priceArray = []
    priceArray.append("Price")
    averageArray = []
    averageArray.append("Average Price")
    
    ''' Variables for Average'''
    averageDates = []
    averageSum = 0
    averageCount = 0
    
    returnArray = []
    
    priceHistory = sql.getHistoricalClose(tickerName)

    for i in dates:
        '''Skip if first element of array is not a date'''
        if(i == 'dates-adj' or i == 'dates' or i == 'date'):
            continue
         
        eps_date = str(i).split("/")
         
        '''Finds correct price in Yahoo prices sheet''' 
        '''averageDates is index of where dates are found in Yahoo! csv file'''
        for j in range(0 , len(priceHistory)):
            sql_date = priceHistory[j][0].split("/")
            price = str(priceHistory[j][1])
              
            '''0 - year, 1 - month, 2 - day'''
            if(eps_date[0] == sql_date[0] and int(eps_date[1]) == int(sql_date[1]) and int(eps_date[2]) > int(sql_date[2])):
                priceArray.append(price) 
                averageDates.append(j)           
                break
            #'''Same Date'''
            elif(eps_date[0] == sql_date[0] and int(eps_date[1]) == int(sql_date[1]) and int(eps_date[2]) == int(sql_date[2])):
                priceArray.append(price)
                averageDates.append(j)
                break
              
            #'''If month is 1 and rolls back to past year at 12. '''
            elif((int(eps_date[0])-1) == (int(sql_date[0])) and int(eps_date[1]) == 1 and int(sql_date[1]) == 12):
                priceArray.append(price)
                averageDates.append(j)       
                break
              
            #'''Year is same, but month rolls back 1'''
            elif(eps_date[0] == sql_date[0] and int(eps_date[1]) > int(sql_date[1])):
                priceArray.append(price)
                averageDates.append(j)
                break
    
#     print(dates)
#     for i in priceHistory:
#         print(i)
#     print(priceArray)
#     print(averageDates)
     
    """This next section will find the average price over specified 3 months
    averageDates ex. ['2016-09-30', '2016-07-01', '2016-04-01', '2015-12-31'] 
    First Date will iterate for approximately 3 months"""
    averageCount = 0
    for i in range(0,averageDates[0]):   
        try:
            price = float(str(priceHistory[i][1]))
            averageSum = averageSum + price
            averageCount += 1
        except:
            break
        
    averageArray.append(str(averageSum/averageCount))
     
#     for i in range(0,len(dates)):
#         print(dates[i] + " : " + str(averageDates[i]))
 
    '''Now find average of rest of the dates'''
    for i in range(1,len(averageDates)):
        averageSum = 0
        averageCount = 0
         
#         print(averageDates[i])
         
        for j in range(averageDates[i-1]+1,averageDates[i]+1):
            try:
                price = float(str(priceHistory[j][1]))
            except:
                break
             
            averageSum = averageSum + price
            averageCount += 1
         
        averageArray.append(str(averageSum/averageCount))
 
    returnArray.append(dates)
    returnArray.append(priceArray)
    returnArray.append(averageArray)    
 
    return returnArray

# earnings = sql.getData('CSCO')
# dates = []
# for i in earnings:
#     dates.append(i[0])
# returnArray = getHistoricalPrices('CSCO', dates)
# for i in returnArray:
#     print(len(i))
#     print(i)
"""-----------------------------------------------------------------------------------

Returns historical stock data in array with [date, closing price] 

-----------------------------------------------------------------------------------"""
def insertHistoricalData(tickerName):
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
            return None

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
    
    for i in yahoo_data_array:
        print(i)

    sql.insertHistorical(tickerName, yahoo_data_array)
    return 5
# print(insertHistoricalData('HAS'))

"""-----------------------------------------------------------------------------------

As of 18 May 2017 getting historical stock prices off of Yahoo Finance does not work. 
What I need to do is make my own database by first downloading excel data from Yahoo 
Finance by hand. This historical closing stock data is then updated by scraping either
Yahoo finance website or Google finance. 

The first method is take historical data downloaded by hand and put them
in stock.db

This method is for scraping and then updating data for stock. 

-----------------------------------------------------------------------------------"""
def updateHistoricalPrice(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)
    
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
        
    sqlData = sql.getHistorical(tickerName)
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
         
#     for i in sqlData:
#         print(i)
#         
    sql.insertHistorical(tickerName, sqlData)

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
        
"""-----------------------------------------------------------------------------

Downloads price data from Yahoo finance and stockrow.com. Also adds file ending
to excel files. 

--------------------------------------------------------------------------------"""
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

# deleteAll('PVH')
# downloadAll('PVH')

"""-----------------------------------------------------

Get exact earnings dates so that average price is more accurate. 
First try Zacks.com to get exact earnings dates. 

-------------------------------------------------------"""
def exactEarnings(tickerName, quarterlyDates):
    exactDates = []
    zacksWebsite = "https://www.zacks.com/stock/research/" + tickerName + "/earnings-announcements"
    
    tempWebFile = request.urlopen(zacksWebsite).read()
    tempData = BeautifulSoup(tempWebFile, "lxml")
    html = tempData.prettify()
    
    lines = tempData.find_all('script')
    keyword = 'document.obj_data ='
    keyword1 = '"earnings_announcements_earnings_table"'
    keyword2 = '"earnings_announcements_webcasts_table"'
    
#     '''Will get SQL data too '''
#     sqlData = sql.getData(tickerName)
    
#     for i in sqlData:
#         print(i)
    
    """Get exact earnings dates from Zack's research """
    for i in lines:
#         print(i)
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
    
    if(len(exactDates) < 1):
        return None
    
    if('dates' in quarterlyDates):
        quarterlyDates.remove('dates')
    elif('dates-adj' in quarterlyDates):
        quarterlyDates.remove('dates-adj')
    
    adjustedDates = adjustedDate(quarterlyDates)[1:]

    """Make sure exactDates matches with adjusted earnings data. Compare exact dates to adjusted dates by making a 2 month window """
    """Initially append exact date for later insertion into sql """
    exactDatesAppend = []

    for i in exactDates: 
#         print('i = ' + i)
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
#                         print(str(left) + " : " + str(right) + ' : ' + str(year_left) + ' : ' + str(year_right))
#                         print(adjDate)
                        exactDatesAppend.append(i)
                        continue
                else:
                    if(left <= adjDate[1] and adjDate[1] <= right):
#                         print(str(left) + " : " + str(right) + ' : ' + str(year_left) + ' : ' + str(year_right))
#                         print(adjDate)
                        exactDatesAppend.append(i)
                        continue
    
#     print(exactDates)
    """Data from Zacks may skip a date. If date is skipped, make sure to estimate date """
    start = 0
    end = len(exactDatesAppend)
    #     print(exactDatesAppend)
    missing = []
    """This year"""
    todaysDate = Utility.getTodaysDate().split('/')
    todaysYear = round(float(todaysDate[2]))
    todaysMonth = round(float(todaysDate[0]))
    """ Previous year in loop"""
    previousYear = todaysYear
    """quaterly date template """
    template = []
    four = 0
    
    """Goes through each date. If exactYear = todaysYear skip. Otherwise see if 
    there are 4 entries per year for quarterly dates. Also first full year is made
    as template. First get template for year """
    for i in exactDatesAppend:
        exactYear = round(float(i.split('/')[0]))
        if(exactYear == todaysYear):
            previousYear = todaysYear - 1
            start += 1
            continue
        
        if(exactYear != previousYear):
    #             print('difference')
    #             print(four)
            if(four == 4 and len(template) == 0 and start >= 4):
                template.append(exactDatesAppend[start-1].split('/'))
                template.append(exactDatesAppend[start-2].split('/'))
                template.append(exactDatesAppend[start-3].split('/'))
                template.append(exactDatesAppend[start-4].split('/'))
                break
            four = 0
        previousYear = exactYear
        start += 1
        four += 1
    
    four, start = 0, 0
    """Go through loop all over again and this time plug in missing dates 
    One thing that I may have to add later is to check if current year dates exist. """
    four, start = 0, 0
    while(start < len(exactDatesAppend)):
        exactYear = round(float(exactDatesAppend[start].split('/')[0]))
    #     print(exactDatesAppend[start])
        if(exactYear == todaysYear):
            previousYear = todaysYear - 1
            start += 1
            continue
        
        if(exactYear != previousYear):
    #         print(start)
    #         print(four)
            if(four < 4):
                for back in range(0,4):
                    index = start-(back + 1)
    #                 print(index)
                    check = exactDatesAppend[index].split('/')
                    checkMonth = float(check[1])
                    templateMonth = float(template[back][1])
                    if(templateMonth - 2 <= checkMonth and checkMonth <= templateMonth + 2): 
    #                     print('ok')
                        pass
                    else:
    #                         print(str(exactYear + 1) + '/' + template[back][1] + '/' + template[back][2])
                        exactDatesAppend.insert(index + 1, str(exactYear + 1) + '/' + template[back][1] + '/' + template[back][2])
                        start += 1
                
            four = 0
        previousYear = exactYear
        start += 1
        four += 1
# #     print(todaysYear)
#     exactYear = round(float(exactDatesAppend[start].split('/')[0]))
#     while(exactYear != todaysYear):
    
#     for i in range(0, 4):
#         date = exactDatesAppend[i].split('/')
#         year = round(float(date[0]) - 1)
#         day = float(date[2])
#         month = float(date[1])   #month
#         start = i + 4
#         
#         print('date = ' + str(date))
#         while(start < end):
#             date2 = exactDatesAppend[start].split('/')
# #             print(date2)
#             month2 = float(date2[1]) #month
#             print('date2 = ' + str(date2))
#             if(month2 - 2 <= month and month <= month2 + 2): 
#                 pass
#             else:
#                 temp.append([start, str(year) + '/' + str(round(month)) + '/' + str(round(day))])
# #                 exactDatesAppend.insert(start, str(year) + '/' + str(round(month)) + '/' + str(round(day)))
#             
#             start += 4
#             year -= 1
    
#     count = 0
#     for i in exactDatesAppend:
#         print(i + " : " + str(count))
#         count += 1
#     print(temp)
    
    """ExactDatesAppend from zacks research may not cover EPS data from stockrow. In this case, estimate past
    dates and add to exactDatesAppend """
#     print(exactDatesAppend)
    index = len(exactDatesAppend)
    oldLength = len(exactDatesAppend)
    while(index < len(adjustedDates)):
        index += 1
        exactDatesAppend.append('')
#         print(exactDatesAppend)
    
#     for i in range(0,len(exactDatesAppend)):
#         print(str(i) + ' ' + exactDatesAppend[i])
#     
    """For each quater, estimate date and then add into exact date """
    for i in range(0, 4):
        start = i
            
        while(start < oldLength):
            date = exactDatesAppend[start].split('/')
            year = round(float(date[0]) - 1) #year
            month = date[1]  #month
            day = date[2]    #day

            start += 4
        
#         print(month)
#         print(day)
        
#         print(start)
        while(start < len(exactDatesAppend)):
            exactDatesAppend[start] = str(year) + '/' + month + '/' + day
            year -= 1
            start += 4
    
#     print()
    prices = getHistoricalPrices(tickerName, exactDatesAppend, 'll')
    prices[0].insert(0, 'Exact Date')
      
    return prices           

"""-----------------------------------------------------------------------------------

 Will get quarterly and ttm data from stock row files. Will put this into a dataArray 
 column that looks as follows:
 
 [MM/DD/YYYY, quarterly, ttm], etc
 
 This method will then add average price for 3 months. 
 
 Afterwards should call sql method insertSQL(CSCO,data)
-----------------------------------------------------------------------------------"""
def getData(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    endings = fileVariables.ending
    fileEnding = fileVariables.returnFileEnding(tickerName)
#     print(fileEnding)
    
    ''' ExcelName is a variable with all excel files (directory + tickerName + Q,T,etc.. )'''
    excelName = []
    sheets = []
        
    for i in fileEnding:
        fileNameTemp = directory + i
        tempBook = xlrd.open_workbook(fileNameTemp)
        sheets.append(tempBook.sheet_by_index(0))
        
    i = 0
    j = 0
    dates = []
    dates.append("dates")
     
    '''Get dates from SheetQ - Quarterly Earnings results, which should show dates for all other tables '''
    ''' cell_value(rows | , columns - )'''
    while(j < sheets[0].ncols):
        tempDate = sheets[0].cell_value(0,j)
        j+=1
        if(tempDate != ' ' and tempDate != ''):
            dateTuple = xlrd.xldate_as_tuple(tempDate,0)
#             print(dateTuple)
            dates.append(str(dateTuple[0]) + "/" + str(dateTuple[1]) + "/" + str(dateTuple[2]))
     
    ''' Get keywords from all sheets '''
    j = 0
    totalArray = []
    totalArray.append(dates)
    
    ''' Goes through each sheet'''
    for iterator in range(0,len(sheets)):
        sheet = sheets[iterator]
        ending = endings[iterator]
        i = 1
        '''Goes down row in each sheet and then across each column to get all data'''
        while(i < sheet.nrows):
            tempData = []
            j = 0 
            while(j < sheet.ncols):
                if(j == 0):
                    tempData.append(str(sheet.cell_value(i,j)) + ending)
                else:
                    tempData.append(sheet.cell_value(i,j))
                j += 1
            i += 1
            totalArray.append(tempData)
    
#     for i in totalArray:
#         print(i)
#     
    '''Now get prices '''
    datesPass = []
    for i in totalArray[0]:
        datesPass.append(i)
#     print(datesPass)
    prices = exactEarnings(tickerName, datesPass)
    if(prices == None):
        """getHistoricalPrices will get adj-dates"""
        prices = getHistoricalPrices(tickerName, totalArray[0], None)
    for i in prices:
        totalArray.append(i)
    
    '''Now make sure length of all arrays are the same'''
    longestArray = 0
    for i in totalArray:
        if(len(i) > longestArray):
            longestArray = len(i)
    
    for i in totalArray:
        appendNumber = longestArray - len(i)
        for j in range(0,appendNumber):
            i.append(' ')
    
#     '''And get rid of empty values '''
#     for i in range(0,len(totalArray)):
#         for j in range(0,len(totalArray[i])):
#             if(totalArray[i][j] == '' or totalArray[i][j] == ' '):
#                 del totalArray[i][j]
    
    return totalArray

# data = getData('PVH')
# for i in data:
#     print(len(i))
#     print(i)
"""----------------------------------------------------------------
*******************************************************************
********************Modules to be called outside*******************
*******************************************************************
----------------------------------------------------------------"""
"""-----------------------------------------------------

UpdateTicker function will do following:
- Delete Excel files associated with tickerName from stockrow.com and yahoo finance.
- Download new Excel files
- Retrieve current data in sql and extract data from new Excel files. 
- Determine difference between current sql data and new data from Excel files. 
- Perform partial update or total update

-------------------------------------------------------"""  
def updateTicker(tickerName):
    deleteAll(tickerName)
    downloadAll(tickerName)
    
    '''Delete and download excel files. Then gets information off excel files'''
    data = getData(tickerName)
    '''Will get SQL data too '''
    tempSQLData = sql.getData(tickerName)
    sqlData = []
    
    """Flip data from tempSQLData diagonally across matrix """
    for i in range(0,len(tempSQLData[0])):
        temp = []
        for j in range(0,len(tempSQLData)):
            temp.append(tempSQLData[j][i])
        sqlData.append(temp)
    
#     for i in data:
#         print(i)
#                  
#     for i in sqlData:
#         print(i)
#         print(len(i))

    '''Compare data with sqlData'''
    newDates = data[0]
    oldDates = sqlData[0]
    addDates = []

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

#     print(newDates)
#     print(oldDates)

    """Finds which oldDates are not in the newDates array. The oldDates not there
    will later be added to the newDates"""
    for i in range(0,len(oldDates)):
        if oldDates[i] in newDates:
            continue
        else:
            addDates.append(oldDates[i])
    
    '''Variables from downloaded files may differ from those in initial sql. Index of variables
    updated will be added to an index ''' 
    newVariables = []
    oldVariables = []
    variableIndex = []
     
    for i in sqlData:
#         print(i)
        oldVariables.append(i[0])
       
    for i in data:
#         print(i)
        newVariables.append(i[0])
       
#     print(oldVariables)
#     print(newVariables)    

    """Finds where index of oldVariables is. List index shows where the
    newvariables are on in the old variables array"""
    found = False
    for i in newVariables:
#         print(i)
        found = False
        for j in range(0,len(oldVariables)):
            if(i.strip() == oldVariables[j].strip()):
                variableIndex.append(j)
                found = True
                continue
        if(found == False):
            variableIndex.append(-1)
             
#     print(variableIndex)
#     print(sqlData[0])
   
    """Find where old data column is within 'data' array """
    temp = []
    index = 0 
    if(len(addDates) > 0):
        """Find where addDate columns are in data """
        for i in addDates:
            for j in range(0,len(sqlData[0])):
                if(i == sqlData[0][j]):
                    index = j
                    break
                j += 1
    else:
        return
    
    """Now get an array with new data from column index and variable index
    Get column from new data and variable index from new data"""
    toAddData = []
    for i in variableIndex:
        if(i == -1):
            toAddData.append('')
        else:
            toAddData.append(sqlData[i][index])
    
#     print(toAddData)
     
    """Add old data from sqlData to newData """
    for i in range(0, len(data)):
        data[i].append(toAddData[i])
#         print(data[i])
        
    """New data may have holes. Plug them in with the old data """
    for i in range(1,len(data[0])):
        date = data[0][i]
        
        """Now iterate down new data and plug in holes. Use variableIndex  """
        for j in range(1,len(data)):
            if(data[j][i] == '' or data[j][i] == None or data[j][i] == ' '):
                variable = data[j][0]
                
                """Find index (row, column) of date from old data """
                index = 0
                for h in range(1,len(sqlData[0])):
#                     print(sqlData[0][j])
                    if(date == sqlData[0][h]):
                        break
                    index = h
#                 print(index)        
          
                row = -1
                for k in range(0,len(sqlData)):
                    if(sqlData[k][0] == variable):
                        row = k
                                      
                if(row != -1):
                    data[j][i] = sqlData[row][index]
    
#     for i in data:
#         print(len(i))
#         print(i)

    sql.insertSQL(tickerName, data)

# updateTicker('PVH')

"""----------------------------------------------------------------
Downloads stocks from stockrow, yahoo. 
Extracts Data 
Puts into sqlite

Note: This is not for updating. It will delete sql table with ticker name
and recreate it. 

-----------------------------------------------------------------"""   
def dlAdd(tickerName): 
    deleteAll(tickerName)
    downloadAll(tickerName)
    data = getData(tickerName)
    sql.insertSQL(tickerName, data)
    

"""---------------------------------------------------------------

Outside call method to update sql data with exact dates. 

---------------------------------------------------------------"""
def updateWithExactDates(tickerName):
    sqlData = sql.getData(tickerName)
    quarterlyDates = []
    
    for i in sqlData:
        quarterlyDates.append(i[0])

    prices = exactEarnings(tickerName, quarterlyDates)
    
    insertData = []
    for i in range(0,len(sqlData)):
        temp = []
        
        for j in range(0,len(sqlData[i])-3):
            temp.append(sqlData[i][j])
        temp.append(prices[0][i])
        temp.append(prices[1][i])
        temp.append(prices[2][i])
        
        insertData.append(temp)
    
#     for i in insertData:
#         print(i)

    sql.insertSQL(tickerName, insertData)
