from HistoricalPricesData import Interface as historicalPrices #@UnresolvedImport
import Utility
from urllib import request
from bs4 import BeautifulSoup



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
    
    priceHistory = historicalPrices.getHistoricalSplit(tickerName)
    
#     for i in dates:
#         print(i)
#     
#     for i in priceHistory:
#         print(i)
    
    for i in dates:
        '''Skip if first element of array is not a date'''
        if(i == 'dates-adj' or i == 'dates' or i == 'date' or i == 'Exact Dates' or i == 'Exact Date'):
            continue
         
        eps_date = str(i).split("/")
        '''Finds correct price in Yahoo prices sheet''' 
        '''averageDates is index of where dates are found in Yahoo! csv file'''
        for j in range(0 , len(priceHistory)):
            sql_date = priceHistory[j][0].split("/")
            price = str(priceHistory[j][1])
              
            '''0 - year, 1 - month, 2 - day'''
            """Could not find same exact date but went back """
            if(eps_date[0] == sql_date[0] and int(eps_date[1]) == int(sql_date[1]) and int(eps_date[2]) > int(sql_date[2])):
                priceArray.append(str(priceHistory[j-1][1])) 
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
    try:
        prices = getHistoricalPrices(tickerName, exactDatesAppend, 'll')
    except:
        historicalPrices.updateHistoricalPrice(tickerName)
        prices = getHistoricalPrices(tickerName, exactDatesAppend, 'll')
        
    prices[0].insert(0, 'Exact Date')
    
    return prices      






"""---------------------------------------------------------------

Outside call method to update sql data with exact dates. 

---------------------------------------------------------------"""
# def updateWithExactDates(tickerName):
#     sqlData = FundamentalsData.getData(tickerName)
#     quarterlyDates = []
#     
#     for i in sqlData:
#         quarterlyDates.append(i[0])
# 
#     prices = exactEarnings(tickerName, quarterlyDates)
#      
# #     print(quarterlyDates)
# #     for i in prices:
# #         print(i)
# #         print(len((i)))
#     
#     insertData = []
#     for i in range(0,len(sqlData)):
#         temp = []
#         
#         for j in range(0,len(sqlData[i])-3):
#             temp.append(sqlData[i][j])
#         temp.append(prices[0][i])
#         temp.append(prices[1][i])
#         temp.append(prices[2][i])
#         
#         insertData.append(temp)
#     
# #     for i in insertData:
# #         print(i)
# 
# #     sql.insertSQL(tickerName, insertData)
#     return insertData