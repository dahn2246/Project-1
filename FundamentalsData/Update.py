from FundamentalsData import Download #@UnresolvedImport
from FundamentalsData import GetData #@UnresolvedImport
from FundamentalsData import Interface #@UnresolvedImport
from HistoricalPricesData import Interface as priceInterface #@UnresolvedImport

"""-----------------------------------------------------

Update Just Prices

-------------------------------------------------------"""  
def updateJustPrices(tickerName):
    tempData = GetData.getData(tickerName)
    dates = []
    data = []
    
    for i in tempData: 
        dates.append(i[len(i)-3])
    
    for i in tempData:
        temp = []
        for j in i:
            temp.append(j)
        data.append(temp)
    
    prices = priceInterface.getHistoricalPrices(tickerName, dates)
    
    for i in range(0,len(prices[0])):
        data[i].append(prices[0][i])
        data[i].append(prices[1][i])
        data[i].append(prices[2][i])
        
#     for i in data:
#         print(i)

    return data
#     sql.insertSQL(tickerName, data)
    


"""-----------------------------------------------------

UpdateTicker function will do following:
- Delete Excel files associated with tickerName from stockrow.com and yahoo finance.
- Download new Excel files
- Retrieve current data in sql and extract data from new Excel files. 
- Determine difference between current sql data and new data from Excel files. 
- Perform partial update or total update

-------------------------------------------------------"""  
def update(tickerName):
    Download.deleteAll(tickerName)
    Download.downloadAll(tickerName)

    '''Delete and download excel files. Then gets information off excel files'''
    data = GetData.getData(tickerName)
    '''Will get SQL data too '''
    tempSQLData = Interface.getData(tickerName)
    sqlData = []
         
    """Flip data from tempSQLData diagonally across matrix """
    for i in range(0,len(tempSQLData[0])):
        temp = []
        for j in range(0,len(tempSQLData)):
            temp.append(tempSQLData[j][i])
        sqlData.append(temp)
     
#     for i in data:
#         print(i)
#         print(len(i))
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
            
    """It is possible for new data to have all the data that is in old data with more updates. 
    In this case, len(addDates) is 0 and newDates > oldDates"""
    if(len(addDates) == 0 and len(newDates) > len(oldDates)):
        return data
     
#     print(addDates)
     
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
        return None 
#     elif(len(data[0])-1 == len(sqlData[0])):
# #         print("Data")
#         return data
#     elif((len(data[0]) - len(sqlData[0])) > 5):
#         return data
#     else:
#         return None
 
     
    """Now, create an array called toAddData where missing data from sql data is added to it. """
    toAddData = []
    for i in variableIndex:
        if(i == -1):
            toAddData.append('')
        else:
            toAddData.append(sqlData[i][index])
      
    """Add old data from sqlData to newData """
    for i in range(0, len(data)):
        data[i].append(toAddData[i])
#         print(data[i])
          
    
#     """New data may have holes. Plug them in with the old data """
#     for i in range(1,len(data[0])):
#         date = data[0][i]
#           
#         """Now iterate down new data and plug in holes. Use variableIndex  """
#         for j in range(1,len(data)):
#             if(data[j][i] == '' or data[j][i] == 'None' or data[j][i] == ' '):
#                 variable = data[j][0]
#                   
#                 """Find index (row, column) of date from old data """
#                 index = 0
#                 for h in range(1,len(sqlData[0])):
# #                     print(sqlData[0][j])
#                     if(date == sqlData[0][h]):
#                         break
#                     index = h
# #                 print(index)        
#             
#                 row = -1
#                 for k in range(0,len(sqlData)):
#                     if(sqlData[k][0] == variable):
#                         row = k
#                                         
#                 if(row != -1):
#                     data[j][i] = sqlData[row][index]
#      
#     for i in data:
#         print(len(i))
#         print(i)
#          
#     for i in range(0, len(toAddData)):
#         print(toAddData[i] + " : " + sqlData[i][len(sqlData[i])-1] + " : " + str(data[i][len(data[i])-1]) + " : " + str(data[i][len(data[i])-2]))

    return data


# i = 'LOGI'
# print(i)
# data = Interface.getData(i)
# for j in data:
#     print(len(j))
#     print(j)
#     
# newData = update(i)
# for i in newData:
#     print(len(i))
#     print(i)