
from Analyze import GetData #@UnresolvedImport
from IndexData import Interface as ListData #@UnresolvedImport
from Analyze import Ratios #@UnresolvedImport
from Analyze import Regression #@UnresolvedImport
from Analyze import DiscountedModel #@UnresolvedImport
from Analyze import Screen #@UnresolvedImport
from HistoricalPricesData import Interface as historical #@UnresolvedImport
import Utility

"""-----------------------------------------------------------------------------------

Update all regression stocks in list

-----------------------------------------------------------------------------------"""   
def updateRegression():
    list = ListData.getList()
    badlist = []
    
    for i in list:
        try:
            print(i)
            Regression.MLanalysis(i)
        except:
            badlist.append(i)
    
    print(badlist)    

# Regression.MLanalysis('AHGP')

#['DMTX', 'NK', 'ODFL', 'TROW', 'PGRE', 'CHKP', 'CIM', 'CCU', 'HSBC', 'OGS', 'RPAI', 'STOR', 'TEGP']

"""-----------------------------------------------------------------------------------

Screens all stocks in list 

-----------------------------------------------------------------------------------"""   
def screenAll():
    list = ListData.getList()
    badlist = []
    
    for i in list:
        try:
#             print(i)
            Screen.screen(i)
        except:
            badlist.append(i)
    
    print(badlist)
# screenAll()

# badList = ['LOGI', 'TTEK', 'ACM', 'CNX', 'ESL', 'HI', 'HRG', 'LEA', 'MWA', 'NFG', 'NJR', 'NGL', 'OSK', 'OC', 'PBH', 'RPM', 'SMG', 'SPB', 'SNX', 'UGI', 'USG']
# for i in badList:
#     Regression.MLanalysis(i)
#     Screen.showAnalysis(i)
# Screen.showAnalysis('LOGI')


"""-----------------------------------------------------------------------------------

Returns ratios (P/E, P/B, etc) and regressed prices in an array. 

-----------------------------------------------------------------------------------"""   
def returnFundamentalData(tickerName):
    todaysPrice, PE_ratioTTM, PS_ratioTTM, PB_ratioTTM, totalDebtToAssetsQ, incomeQualityQ, ROIC, incomeQualityTTM, inventoryTurnoverTTM  = Ratios.getStatistics(tickerName)
    
    returnArr = [todaysPrice, PE_ratioTTM, PS_ratioTTM, PB_ratioTTM, totalDebtToAssetsQ, incomeQualityQ, ROIC, incomeQualityTTM, inventoryTurnoverTTM]
    for i in range(0, len(returnArr)):
        try:
            returnArr[i] = "{0:.2f}".format(returnArr[i])
        except:
            pass
        
    returnArr.insert(0, tickerName)
    
    return returnArr

def showAnalysis(tickerName):
    Screen.showAnalysis(tickerName)


# list = ListData.getList()
# list = ['BECN', 'LOGI', 'PAAS', 'TTWO', 'TSRA', 'TTEK', 'APFH', 'ACM', 'BMO', 'BNS', 'CEB', 'GIB', 'CLC', 'CSC', 'CNX', 'CPG', 'DV', 'ENB', 'ESL', 'FUL', 'HI', 'HRG', 'HSBC', 'LEA', 'LOCK', 'MFS', 'MWA', 'NFG', 'NJR', 'NGL', 'OSK', 'OC', 'PFGC', 'PBH', 'RPM', 'SAIC', 'SMG', 'SMI', 'SPB', 'SR', 'S', 'SXL', 'SYT', 'SNX', 'TAL', 'TMH', 'TECK', 'TEF', 'TU', 'TRQ', 'UGI', 'USG']

# discounted = DiscountedModel.discountedCashFlow('AMTX')
# returnFundamentalData('AAPL')
# bad = []
# for i in list:
#     try:
#         print(i)
# #         Update.fundamentalData(i)
#         discounted = DiscountedModel.discountedCashFlow(i)
#         price = Utility.getTodaysPrice(i)
# #         if(float(price) < float(discounted)):
#         print(i + " : today = " + str(price) + " : model = " + str(discounted))
# #         print(i)
# #         print(returnFundamentalData(i))
#     except:
#         bad.append(i)
#     
# print(bad)