import Utility
from HistoricalPricesData import Interface as priceInterface #@UnresolvedImport
from Analyze import GetData #@UnresolvedImport

def numShares(tickerName):
    data, variables, price, priceAvg, ones = GetData.getData(tickerName)
    todaysPrice = Utility.getTodaysPrice(tickerName)
    if(todaysPrice < 0):
        historicalPrice = priceInterface.getHistoricalSplit(tickerName)
        todaysPrice = historicalPrice[0][1]
    
#     for i in variables:
#         print(i)
    
    """Calculate things like PE_ratio, etc """
    index_EarningsQ, index_EarningsTTM, index_RevenuesTTM, index_BookvalueTTM = 0,0,0,0 
    index_netincomeTTM, index_totalAssetsTTM, index_cashTTM, index_shareHoldersEquityQ = 0, 0, 0 ,0
    index_netincome = 0 
    
    count = 0 
    for i in variables:
        if(i == 'Earnings per Basic Share-T'):
            index_EarningsTTM = count
        if(i == 'Earnings per Basic Share-Q'):
            index_EarningsQ = count
        if(i == 'Revenues-T'):
            index_RevenuesTTM = count
        if(i == 'Net Income-Q'):
            index_netincome = count
        if(i == 'Net Income-T'):
            index_netincomeTTM = count
        count += 1
    
    earningsQ = data[0][index_EarningsQ]
    earningsTTM = data[0][index_EarningsTTM]
    revenuesTTM = data[0][index_RevenuesTTM]
    netIncome = data[0][index_netincome]
    netIncomeT = data[0][index_netincomeTTM]
    
    try:
        return float(netIncome)/float(earningsQ)
    except:
        return float(netIncomeT)/float(earningsTTM)
        
def getDividends(tickerName):
    data, variables, price, priceAvg, ones = GetData.getData(tickerName)
    todaysPrice = Utility.getTodaysPrice(tickerName)
    if(todaysPrice <= 0):
        historicalPrice = priceInterface.getHistoricalSplit(tickerName)
        todaysPrice = historicalPrice[0][1]
    
    dividendQ = 0 
    dividendT = 0
    
#     print(dividendT)
    
    count = 0 
    for i in variables:
        if(i == 'Dividends per Basic Common Share-T'):
            dividendT = data[0][count]
        if(i == 'Dividends per Basic Common Share-Q'):
            dividendQ = data[0][count]
        count += 1
    
    try:
        divPerc = float(dividendT) / float(todaysPrice)
    except:
        divPerc = 0
    
    return [dividendT, divPerc] 

# print(getDividends('AHGP'))
        
"""-----------------------------------------------------------------------------------

This method will return fundamental data and ratios from tickerName. Ratios include 
things like: PE, PB, PS, ROIC, etc

-----------------------------------------------------------------------------------"""      
def getStatistics(tickerName):
    data, variables, price, priceAvg, ones = GetData.getData(tickerName)
    todaysPrice = Utility.getTodaysPrice(tickerName)
    if(todaysPrice < 0):
        historicalPrice = priceInterface.getHistoricalSplit(tickerName)
        todaysPrice = historicalPrice[0][1]

#     for i in variables:
#         print(i)
        
    earningsTTM = 0
    earningsQ = 0
    revenuesTTM = 0
    netIncome = 0
    bookValue = 0
    netIncomeTTM = 0
    totalAssets = 0 
    totalDebtToAssetsQ = 0
    incomeQualityQ = 0
    ROE = 0
    ROIC = 0 
    incomeQualityTTM = 0
    inventoryTurnoverTTM = 0
    
    count = 0 
    for i in variables:
        if(i == 'Earnings per Basic Share-T'):
            earningsTTM = data[0][count]
        if(i == 'Earnings per Basic Share-Q'):
            earningsQ = data[0][count]
        if(i == 'Revenues-T'):
            revenuesTTM = data[0][count]
        if(i == 'Net Income-Q'):
            netIncome = data[0][count]    
        if(i == 'Book Value per Share-QM'):
            bookValue = data[0][count]    
        if(i == 'Net Income-TTM'):
            netIncomeTTM = data[0][count]
        if(i == 'Total Assets-QB'):
            totalAssets = data[0][count]
        if(i == 'Total Debt To Total Assets-QM'):
            totalDebtToAssetsQ = data[0][count]
        if(i == 'Income Quality-QM'):
            incomeQualityQ = data[0][count]
        if(i == 'Return on Average Equity-TM'):
            ROE = data[0][count]
        if(i == 'Return on Invested Capital-TM'):
            ROIC = data[0][count]
        if(i == 'Income Quality-TM'):
            incomeQualityTTM = data[0][count]
        if(i == 'Inventory Turnover-TM'):
            inventoryTurnoverTTM = data[0][count]
        count += 1


    try:
        numShares =float(netIncome)/float(earningsQ)
    except:
        numShares = 0 
        
    try:
        PE_ratioTTM = float(todaysPrice)/float(earningsTTM)
    except:
        PE_ratioTTM = -1
        
    try:
        PS_ratioTTM = float(todaysPrice)/(float(revenuesTTM)/numShares)
    except:
        PS_ratioTTM = -1
    
    try: 
        PB_ratioTTM = float(todaysPrice)/float(bookValue)
    except:
        PB_ratioTTM = -1 

    

    return [todaysPrice, PE_ratioTTM, PS_ratioTTM, PB_ratioTTM, totalDebtToAssetsQ, incomeQualityQ, ROIC, incomeQualityTTM, inventoryTurnoverTTM]

