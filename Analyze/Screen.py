from Analyze import DiscountedModel #@UnresolvedImport
from Analyze import GetData #@UnresolvedImport
from Analyze import Regression #@UnresolvedImport
from Analyze import Ratios #@UnresolvedImport
from RegressionData import Interface as RegressionData #@UnresolvedImport

"""-----------------------------------------------------------------------------------

Stock screener will make buy recommendations by using regressed price, discount cash flow, 
and ratios. 

-----------------------------------------------------------------------------------"""    
def showAnalysis(tickerName):
    multipleFits = RegressionData.getRegressionData(tickerName)
    discountedPrice = float(DiscountedModel.discountedCashFlow(tickerName))
    todaysPrice, PE, PS, PB, totalDebtToAssetsQ, incomeQualityQ, ROIC, incomeQualityTTM, inventoryTurnoverTTM = Ratios.getStatistics(tickerName)
    ROIC = float(ROIC) * 100
    
    """At this point this is a buy """
    print(tickerName)
    print("Todays Price : " + "{0:.2f}".format(todaysPrice))
    print("P/E : " + "{0:.2f}".format(PE))
#     print("P/S : " + "{0:.2f}".format(PS))
#     print("P/B : " + "{0:.2f}".format(PB))
#     print("ROIC : " + "{0:.2f}".format(float(ROIC)) + '%')
    
    regressedPrices = []
    
    for i in multipleFits:
        """MultipleFits returns [0 - radjusted, 1 - regressedPrice, 2 - keywords ]"""
        radjusted, regressedPrice, keywords = i[0], float(i[1]), i[2]
        regressedPrices.append(regressedPrice)
    regressedPrices.sort()

    print("Multiple linear analysis gives a target price between " + "{0:.2f}".format(regressedPrices[0]) + " - " 
          + "{0:.2f}".format(regressedPrices[len(regressedPrices) - 1]))
    print("Multiple linear analysis performed between price and variables such as revenues, dividends, book value, etc")
    
#     print("Todays Price = " + "{0:.2f}".format(todaysPrice))
#     for i in multipleFits:
#         print("R2 = " + "{0:.2f}".format(i[0]) + " | Regressed Price = " + "{0:.2f}".format(i[1]) + " | " + str(i[2]))
    
    print("Discounted price = " + "{0:.2f}".format(discountedPrice))
    print("DCF is done with a conservative 12% discount rate and 2.5% long term growth rate")
    
    fairValue = (sum(regressedPrices)/ len(regressedPrices)) * 0.5 + discountedPrice  * 0.5

        
    print("From Multiple linear analysis and DCF, and approximate fair value is = $" + "{0:.2f}".format(fairValue))
    print("")


"""-----------------------------------------------------------------------------------

Stock screener will make buy recommendations by using regressed price, discount cash flow, 
and ratios. 

-----------------------------------------------------------------------------------"""    
def screen(tickerName):
    multipleFits = RegressionData.getRegressionData(tickerName)
    discountedPrice = float(DiscountedModel.discountedCashFlow(tickerName))
    todaysPrice, PE, PS, PB, totalDebtToAssetsQ, incomeQualityQ, ROIC, incomeQualityTTM, inventoryTurnoverTTM = Ratios.getStatistics(tickerName)
    price_thresholdBuy = todaysPrice + (todaysPrice * 0.05)
    _, dividend = Ratios.getDividends(tickerName)
    
    if(dividend < 0.035):
        return

    print(tickerName + ' Dividend '  + str(dividend))
    

    """Screen multiple fits. [r^2, regressed, variables] """
    buySignals = 0
    for i in multipleFits:
        r2, regressedPrice = i[0], i[1]
        if(r2 > 0.75 and regressedPrice > price_thresholdBuy):
            buySignals += 1
    
    if(buySignals < len(multipleFits)/2):
        return
    
    """Screen discounted price """
    if(discountedPrice > price_thresholdBuy):
        pass
    else:
        return

    """Screen P/E ratio """
    if(PE > 25):
        return
    
    """At this point this is a buy """
    print("----- Buy Signal -----")
    print("Todays Price = " + "{0:.2f}".format(todaysPrice))
    for i in multipleFits:
        print("R2 = " + "{0:.2f}".format(i[0]) + " | Regressed Price = " + "{0:.2f}".format(i[1]) + " | " + str(i[2]))
    print("Discounted price = " + "{0:.2f}".format(discountedPrice) + " | PE = " + "{0:.2f}".format(PE))