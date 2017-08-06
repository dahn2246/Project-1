from FundamentalsData import PricesAndDates #@UnresolvedImport
from Variables import *
import xlrd 


"""-----------------------------------------------------------------------------------

 Will get quarterly and ttm data from stock row files. Will put this into a dataArray 
 column that looks as follows:
 
 [MM/DD/YYYY, quarterly, ttm], etc
 
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
    prices = PricesAndDates.exactEarnings(tickerName, datesPass)
    if(prices == None):
        """getHistoricalPrices will get adj-dates"""
        prices = PricesAndDates.getHistoricalPrices(tickerName, totalArray[0], None)
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

