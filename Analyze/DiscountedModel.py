from Analyze import Ratios #@UnresolvedImport
from Analyze import GetData #@UnresolvedImport


def discountedCashFlow(tickerName):
    data, variables, price, priceAvg, ones = GetData.getData(tickerName)
    index_freeCashFlowQ = 0
    index_dividendQ = 0 
    
#     for i in variables:
#         print(i)
    
    count = 0 
    for i in variables:
        if(i == 'Free Cash Flow-QC'):
            index_freeCashFlowQ = count
        if(i == 'Dividends per Basic Common Share-Q'):
            index_dividendQ = count
        count += 1
     
    dates = []
    freeCashFlowQ = []
    dividend = []
    for i in data:
        dates.append(i[0])
        freeCashFlowQ.append(i[index_freeCashFlowQ])
        dividend.append(i[index_dividendQ])        
     
    datesAnnualized = []
    freeCashFlowAnnualized = []
    dividendAnnualized = []
    count = 0
    tempCash = 0      
    tempDividend = 0 
    for i in range(0, len(dates)):
        if(count == 0):
            datesAnnualized.append(dates[i])
         
        if(freeCashFlowQ[i] == '' or freeCashFlowQ[i] == ' '):
            continue
        else:
            tempCash += float(freeCashFlowQ[i])
         
        if(dividend[i] == '' or dividend[i] == ' '):
            continue
        else:
            tempDividend += float(dividend[i])
         
    
        count += 1
        if(count == 4):
            freeCashFlowAnnualized.append(tempCash)
            dividendAnnualized.append(tempDividend)
            tempDividend = 0
            count = 0
            tempCash = 0
     
    for i in range(0, len(freeCashFlowAnnualized)):
        if(i + 1 < len(freeCashFlowAnnualized)):
            change = (freeCashFlowAnnualized[i] - freeCashFlowAnnualized[i + 1]) /  freeCashFlowAnnualized[i+ 1] * 100
        else:
            change = 0
#         print(datesAnnualized[i] + " : " + str(freeCashFlowAnnualized[i]) + " : " + str(change) + " : " + str(dividendAnnualized[i]))

    
    """Discounted Cash Flow Analysis. 
    
    5 years + residual value discounted to present value.
    
    5 years are estimated with a constant growth rate. Future cash flow = current * (1 + growth rate) ^ years
    
    Residual Calculation : (Final Year * ( 1 + long term growth rate)) / (Discount Rate - Long Term Growth Rate) 
    
    Long term growth rate = 2.5 - 3 %
    
    Discouted Rate = 6 - 8 % 
    
    
    Also add dividends into discounted cash flow analysis. 
    5 years dividend out and estimate dividend growth rate. Future dividend = current * (1 + growth rate) ^ years
    
    Discount dividend back to present value/ 
    
    """
    
    """Step 1: Estimate conservative growth rate of cash flow by using trend analysis of last 5 years. If < 0, use ~5 %"""
    
    i = 0
    CAGR = []
    while(i + 5 < len(freeCashFlowAnnualized)):
        if(freeCashFlowAnnualized[i] <= 0 or freeCashFlowAnnualized[i + 5] <= 0):
            i += 1
            continue
        change = (freeCashFlowAnnualized[i] / freeCashFlowAnnualized[i + 5]) ** (1/5) - 1
        CAGR.append(float(change))
        i += 1
        
    """If cashflows are mostly negative, the company's cash flow is considered to not be growing. """
    if(len(CAGR) < 1):
        estimatedGrowth = -1
    else:
        estimatedGrowth = sum(CAGR) / float(len(CAGR))
        
    
    """Calculated estimated growth rate of future cash flow. If estimated growth > 10%, use 10% as growth rate. If
    growth rate is < 0%, use 4% as growth rate.     """
    if(estimatedGrowth > 0.1): 
        estimatedGrowth = 0.08
    elif(estimatedGrowth == -1):
        estimatedGrowth = 0.005
    elif(estimatedGrowth < 0):
        estimatedGrowth = 0.015  

    
    """Estimate long term growth rate at 2.75%. Discount is 7%"""
#     estimatedGrowth = .05
    longTermGrowth = 0.025
    discountedRate = 0.12
    
    """Now calculate discounted cash flow for 5 years """
    fiveYrCash = []
    fiveYrDiscounted = []
    currentCash = freeCashFlowAnnualized[0]
    if(currentCash < 0):
        currentCash = sum(freeCashFlowAnnualized) / float(len(freeCashFlowAnnualized))
        if(currentCash < 0):
            return 0
        
    for i in range(0, 5):
        fiveYrCash.append(currentCash * (1 + estimatedGrowth))
        currentCash = fiveYrCash[i]
    
    for i in range(0, 5):
        fiveYrDiscounted.append(fiveYrCash[i] / (1 + discountedRate)**i )
    
    residual = (fiveYrCash[4] * (1 + longTermGrowth)) / (discountedRate - longTermGrowth)
    discountedResidual = residual / (1 + discountedRate) ** 5
    intrinsic = discountedResidual
    
    for i in fiveYrDiscounted:
        intrinsic += i

    numShares = Ratios.numShares(tickerName)
    """Intrinsic Price w/o dividends  """
    intrinsicPrice = intrinsic/numShares
     
    return intrinsicPrice

    