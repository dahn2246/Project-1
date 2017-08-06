from FundamentalsData import Interface #@UnresolvedImport
from FundamentalsData import GetData #@UnresolvedImport
from FundamentalsData import Update #@UnresolvedImport
from FundamentalsData import Download #@UnresolvedImport
from IndexData import Interface as IndexData #@UnresolvedImport

"""-----------------------------------------------------------------------------------

This method gets fundamental data from excel files. 

-----------------------------------------------------------------------------------"""
def fundamentalData(tickerName):
    Download.deleteAll(tickerName)
    Download.downloadAll(tickerName)
    data = GetData.getData(tickerName)
    Interface.insertSQL(tickerName, data)

"""-----------------------------------------------------------------------------------

This method gets updated fundamentals data. 

-----------------------------------------------------------------------------------"""
def updateFundamentalData(tickerName):
    data = Interface.getData(tickerName)
    lastDate = data[1][0].split('/')
    print(lastDate)
    month = float(lastDate[1])
    year = float(lastDate[0])
#      
#     today = Utility.getTodaysDate().split('/')
#     currentMonth = float(today[0])
#     currentYear = float(today[2])
#      
#     difference = 0 
#     if(currentYear == year):
#         difference = currentMonth - month
#     elif((currentYear - 1) == year):
#         difference = (12-month) + currentMonth
#      
#     """If current month and current year is more than 4 months away, try update """
#     if(difference > 4):
#         print('Attempting update......')
#     data = Update.update(tickerName)
#         if(data != None):
#             print('updated')
#     Interface.insertSQL(tickerName, data)
# #             updateRegression(tickerName)
#             data = getData(tickerName)
#             lastDate = data[1][0].split('/')
#             print(lastDate)
#     

# updateFundamentalData('AHGP')

# 
# for i in list:
#     print(i)
#     updateFundamentalData(i)

def updateAll():
    list = IndexData.getList()
    for i in list:
        print(i)
        updateFundamentalData(i)
        
