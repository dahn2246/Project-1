import xlrd
import xlwt
import csv
import Text
import Utility
from Variables import *

'''-----------------------------------------------------------------------------------

Input is ticker symbol and array of dates which are earnings dates.
Earnings dates are sometimes not accurate and must be approximated by adding +1 to the month
This will return array with columns as follows:
 
 Date, Price on Date, 3 Month Average Price between earnings
 
-----------------------------------------------------------------------------------'''
def getHistoricalPrices(tickerName,dates):
    '''Adjust dates by +1 to month'''
    dates = adjustedDate(dates)
    yahoo_data_array = [] 
    data_index = 1
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
    
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)
    csv_file = open(directory + tickerName+'-Y.csv', "r")

    reader = csv.reader(csv_file, delimiter = ' ')

    for lines in reader:
        yahoo_data_array.append(lines)

    for i in dates:
        '''Skip if first element of array is not a date'''
        if(i == 'dates-adj'):
            continue
        
        eps_date = str(i).split("/")
        
        '''Finds correct price in Yahoo prices sheet''' 
        '''averageDates is index of where dates are found in Yahoo! csv file'''
        for j in range(data_index , len(yahoo_data_array)):
            yahoo_data = str(yahoo_data_array[j][0]).split(",")
            yahoo_date = yahoo_data[0].split("-")
            price = str(yahoo_data[6])
             
            '''0 - year, 1 - month, 2 - day'''
            if(eps_date[0] == yahoo_date[0] and int(eps_date[1]) == int(yahoo_date[1]) and int(eps_date[2]) > int(yahoo_date[2])):
                priceArray.append(price) 
                averageDates.append(j)           
                break
            #'''Same Date'''
            elif(eps_date[0] == yahoo_date[0] and int(eps_date[1]) == int(yahoo_date[1]) and int(eps_date[2]) == int(yahoo_date[2])):
                priceArray.append(price)
                averageDates.append(j)
                break
             
            #'''If month is 1 and rolls back to past year at 12. '''
            elif((int(eps_date[0])-1) == (int(yahoo_date[0])) and int(eps_date[1]) == 1 and int(yahoo_date[1]) == 12):
                priceArray.append(price)
                averageDates.append(j)       
                break
             
            #'''Year is same, but month rolls back 1'''
            elif(eps_date[0] == yahoo_date[0] and int(eps_date[1]) > int(yahoo_date[1])):
                priceArray.append(price)
                averageDates.append(j)
                break
    
    ''' This next section will find the average price over specified 3 months
    
    averageDates ex. ['2016-09-30', '2016-07-01', '2016-04-01', '2015-12-31'] 
    
    First Date will iterate for approximately 3 months''' 
    iterator = averageDates[0] 
    for i in range(0,60):

        yahoo_data = str(yahoo_data_array[iterator][0]).split(",")
                
        try:
            price = float(str(yahoo_data[6]))
        except:
            break
        
        averageSum = averageSum + price
        averageCount += 1
        iterator -= 1
        
    
    averageArray.append(str(averageSum/averageCount))
    
    '''Rest of the dates will iterate between dates'''
    for i in range(1,len(averageDates)):
        averageSum = 0
        averageCount = 0
        for j in range(averageDates[i-1]+1,averageDates[i]+1):
            yahoo_data = str(yahoo_data_array[j][0]).split(",")
                
            try:
                price = float(str(yahoo_data[6]))
            except:
                break
            
            averageSum = averageSum + price
            averageCount += 1
        
        averageArray.append(str(averageSum/averageCount))

        
    
    returnArray.append(dates)
    returnArray.append(priceArray)
    returnArray.append(averageArray)    

    return returnArray

'''-----------------------------------------------------------------------------------

Sometimes date from stockrow is for reported quater, not date of actual of earnings release

This method will attempt to find the correct date that earnings date was release. If stockrow
only gives FY quater dates, this method will skip ahead 15 days, and then try to find a place where
>5% increase or decrease in stock price occured. If it does not find such a date or more than one, it will
just estimate the price at 1 month ahead. 

Note: 10 Dec 2016  - Doesn't work because many jumps exist
As of now, method will simply add 30 days to date. 
 
-----------------------------------------------------------------------------------'''
# def adjustedDate(tickerName, dates):
#     
#     yahoo_data_array = [] 
#     
#     csv_file = open("D:/cmsc/Stock Analysis/ExcelData/" + tickerName+'-Y.csv', "r")
#     reader = csv.reader(csv_file, delimiter = ' ')
#     
#     monthDays = [31,28,31,30,31,30,31,31,30,31,30,31]
#     
#     datefound = False
#     
#     count = 0
#     
#     returnArray = []
#     
#     for lines in reader:
#         yahoo_data_array.append(lines)
#     
#     for i in dates:
#         eps_dateStr = str(i).split("/")
#         eps_dateInt = [int(eps_dateStr[0]), int(eps_dateStr[1]), int(eps_dateStr[2])]
#         
#         ''' Make eps_date go ahead 15 days '''
#         '''0 - Year, 1 - Month, 2 - Day'''
#         while(count < 15):
#             
#             eps_dateInt[2] = eps_dateInt[2] + 1
#             
#             '''If day passes to next month, month will be updated '''
#             if(monthDays[eps_dateInt[1]-1] < eps_dateInt[2]):
#                 eps_dateInt[2] = 1
#                 if(eps_dateInt[1] == 12):
#                     eps_dateInt[1] = 1
#                 else:
#                     eps_dateInt[1] += 1
#             count += 1
#         count  = 0 
#         
#         eps_date = [str(eps_dateInt[0]),str(eps_dateInt[1]),str(eps_dateInt[2])]
#          
#          
#         '''Finds correct price in Yahoo prices sheet for eps_date + 15 ''' 
#         for j in range(1 , len(yahoo_data_array)):
#             yahoo_data = str(yahoo_data_array[j][0]).split(",")
#             yahoo_date = yahoo_data[0].split("-")
#             price = str(yahoo_data[6])
#               
#             #0 - year, 1 - month, 2 - day
#             if(eps_date[0] == yahoo_date[0] and int(eps_date[1]) == int(yahoo_date[1]) and int(eps_date[2]) > int(yahoo_date[2])):
#                 index = j
#                 break
#                
#             #Same Date
#             elif(eps_date[0] == yahoo_date[0] and int(eps_date[1]) == int(yahoo_date[1]) and int(eps_date[2]) == int(yahoo_date[2])):
#                 index = j
#                 break
#               
#             #If month is 1 and rolls back to past year at 12. 
#             elif((int(eps_date[0])-1) == (int(yahoo_date[0])) and int(eps_date[1]) == 1 and int(yahoo_date[1]) == 12):
#                 index = j
#                 break
#               
#             #Year is same, but month rolls back 1
#             elif(eps_date[0] == yahoo_date[0] and int(eps_date[1]) > int(yahoo_date[1])):
#                 index = j
#                 break
#         
#         for index in range(0,15):
#             yahoo_data = str(yahoo_data_array[j][0]).split(",")
#             yahoo_date = yahoo_data[0].split("-")
#             price = str(yahoo_data[6])
#         
#             day1 = float(price)
#             
#             yahoo_data = str(yahoo_data_array[j+1][0]).split(",")
#             yahoo_date = yahoo_data[0].split("-")
#             price = str(yahoo_data[6])
#             day2 = float(price)
#             
#             if(abs(day2-day1)/day1 > .05):
#                 returnArray.append(yahoo_date[0] + "/" + yahoo_date[1] + "/" + yahoo_date[2])
#                 print(str(day1) + " " + str(day2))
#                 datefound = True
#                 break
#         
#         if(datefound == False):
#             while(count < 15):
#                 eps_dateInt = [int(eps_date[0]), int(eps_date[1]), int(eps_date[2])]
#                 eps_dateInt[2] = eps_dateInt[2] + 1
#                 
#                 '''If day passes to next month, month will be updated '''
#                 if(monthDays[eps_dateInt[1]-1] < eps_dateInt[2]):
#                     eps_dateInt[2] = 1
#                     if(eps_dateInt[1] == 12):
#                         eps_dateInt[1] = 1
#                     else:
#                         eps_dateInt[1] += 1
#                 count += 1
#             count  = 0 
#             
#             returnArray.append([str(eps_dateInt[0]),str(eps_dateInt[1]),str(eps_dateInt[2])])
#             
#         datefound = False
#         
#     print(returnArray)
#     
#     return returnArray

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

'''-----------------------------------------------------------------------------------

 This method will create an excel file called tickerName.xls with the output array inside
 that file
  
-----------------------------------------------------------------------------------'''
def write(tickerName, data):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('test')
    
    for i in range(0,len(data)):
        for j in range(0,len(data[i])):
            sheet.write(i,j,data[i][j])
        
    workbook.save("D:/cmsc/Stock Analysis/Analysis/" + tickerName +".xls")

'''-----------------------------------------------------------------------------------

This method will return an array of data from Excel file. Does not work for csv values. 
  
-----------------------------------------------------------------------------------'''
def read(fileName):
    returnArray = []
    workbook = xlrd.open_workbook(fileName)
    sheet = workbook.sheet_by_index(0)

    i = 0 
    text = str(sheet.cell_value(i,0))
    while(text != ''):
        try:
            returnArray.append(text.strip())
            i += 1
            text = str(sheet.cell_value(i,0))
        except:
            text = ''
            
    return returnArray

'''-----------------------------------------------------------------------------------

Method returns array from CSV values
  
-----------------------------------------------------------------------------------'''
def readCSV(fileName):
    returnArray = []

    with open(fileName, newline = '') as csvfile:
        reader = csv.reader(csvfile)
    
        for i in reader:
            returnArray.append(i)
        
    return returnArray
    

def similarity(str1,str2):
    similarityCount = 0
    largerIndex = 0
    
    if(len(str1) == 0  or len(str2) == 0):
        return False
        
    for i in range(0,len(str1)):
        if(str1[i] in str2):
            similarityCount += 1
    
    if(len(str1) > len(str2)):
        largerIndex = len(str1)
    else:
        largerIndex = len(str2)

    if(similarityCount/largerIndex > .95):   
        return True
    return False


'''-----------------------------------------------------------------------------------

 Will get quarterly and ttm data from stock row files. Will put this into a dataArray 
 column that looks as follows:
 
 [MM/DD/YYYY, quarterly, ttm], etc
-----------------------------------------------------------------------------------'''

def getData(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    endings = fileVariables.ending[1:]
    fileEnding = fileVariables.returnFileEnding(tickerName)[1:]
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
        #print(keywords)
        
        '''Goes down row in each sheet and then across each column to get all data'''
        while(i < sheet.nrows):
            tempData = []
            j = 0 
            while(j < sheet.ncols):
                if(j == 0):
                    """Appends keywords with ending"""
                    tempData.append(str(sheet.cell_value(i,j)) + ending)
                else:
                    tempData.append(sheet.cell_value(i,j))
                j += 1
            i += 1
            totalArray.append(tempData)
    
    '''Now get prices '''
    prices = getHistoricalPrices(tickerName, totalArray[0])
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
    
    '''And get rid of empty values '''
    for i in range(0,len(totalArray)):
        for j in range(0,len(totalArray[i])):
            if(totalArray[i][j] == ''):
                totalArray[i][j] = ' '
    
    return totalArray

# data = getData('AAPL')
# for i in data:
#     print(i)



