import math
import Utility
import numpy as np
import numpy.linalg as linalg
import Sqlite as sql
from Variables import *
from astropy.units import count

"""-----------------------------------------------------------------------------------

Performs a linear regression of data in the form of y = mx + b. 
Will return m, b, and r2

Test data works. 
# xt = [.99,1.02,1.15,1.29,1.46,1.36,0.87,1.23,1.55,1.40,1.19,1.15,.98,1.01,1.11,1.20,1.26,1.32,1.43,0.95]
# yt = [90.01,89.05,91.43,93.74,96.73,94.45,87.59,91.77,99.42,93.65,93.54,92.52,90.56,89.54,89.85,90.39,93.25,93.41,94.98,87.33]


-----------------------------------------------------------------------------------"""
def linearReg(y,x):
    n = len(y)
    
    sumX = math.fsum(x)
    sumY = math.fsum(y)
    sumXY = 0
    sumX2 = 0
    sumY2 = 0
     
    for i in range(0,n):
        sumXY += x[i]*y[i]
        sumX2 += x[i]**2
        sumY2 += y[i]**2
     
    m = (sumXY - (sumX*sumY/n)) / (sumX2 - (sumX**2)/n)
    b = (sumY/n) - m*(sumX/n)
    #R2 = 1 - (SSe/SSt)
    SST = sumY2  - n*(sumY/n)**2
    SSE = SST - m*(sumXY - (sumX*sumY/n))
    r2 = 1 - (SSE/SST)
    
    return [m,b,r2]

'''-----------------------------------------------------------------------------------

Performs multiple linear regression. Will return coefficients and r2adjusted in an array
[coeffs, r2adjusted]. There are some cases where multiple linear regression fails. Failed 
cases will return None. 
  
  # X = [[1, 1263.0, 0.46],
# [1, 1254.0, 0.39],
# [1, 1290.15, -0.44],
# [1, 1032.312, 0.29]]
# 
# Y = [[30.59882825531914],
# [26.040824578125008],
# [24.397237841269835],
# [25.448914603174607]]
# 
# multipleLinear(X,Y)

# X = [[1,2,50],
#      [1,8,110],
#      [1,11,120],
#      [1,10,550],
#      [1,8,295],
#      [1,4,200],
#      [1,2,375],
#      [1,2,52],
#      [1,9,100],
#      [1,8,300],
#      [1,4,412],
#      [1,11,400],
#      [1,12,500],
#      [1,2,360],
#      [1,4,205],
#      [1,4,400],
#      [1,20,600],
#      [1,1,585],
#      [1,10,540],
#      [1,15,250],
#      [1,15,290],
#      [1,16,510],
#      [1,17,590],
#      [1,6,100],
#      [1,5,400]
#      ]
#    
# Y = [[9.95],
#      [24.45],
#      [31.75],
#      [35.00],
#      [25.02],
#      [16.86],
#      [14.38],
#      [9.60],
#      [24.35],
#      [27.50],
#      [17.08],
#      [37.00],
#      [41.95],
#      [11.66],
#      [21.65],
#      [17.89],
#      [69.00],
#      [10.30],
#      [34.93],
#      [46.59],
#      [44.88],
#      [54.12],
#      [56.63],
#      [22.13],
#      [21.15]
#      ]
# print(X)
# print(Y)
# multipleLinear(X,Y)
-----------------------------------------------------------------------------------'''
def multipleLinearReg(X_array, y_array):

    X = np.array(X_array)
    y = np.array(y_array)
    
#     print(X)
#     print(y)
#       
    sigma_y = sum(y)
    n = len(X_array) 
    p = len(X_array[0]) - 1

#     print('n = ' + str(n))
#     print('p = ' + str(p))

    """"p cannot be greater than n. Sometimes this happens if there are more regression variables
    than there are observations """
    if(p >= n):
        return None
    
    XX = np.dot(X.transpose(), X)
    Xy = np.dot(X.transpose(),y)
    
    """Try calculations. If these calculations fail, return None """
    try:
        coeffs= np.dot(linalg.inv(XX),Xy)
        xe = np.dot(coeffs.transpose(),X.transpose())
        """Sum of Square Variables Calculations"""
        """First calculated through matrix multiplication """
        SSe = np.dot(y.transpose(),y) - np.dot(np.dot(coeffs.transpose(),X.transpose()),y)
        SSr = np.dot( np.dot(coeffs.transpose(),X.transpose()),y) - sigma_y**2/n
        SSt = np.dot(y.transpose(),y) - sigma_y**2/n
    except:
        return None
    
    """Get all fitted values from equation"""
    yFitted = []
    for i in X:
        fittedValue = 0
        
        for j in range(0,len(coeffs)):
            fittedValue += i[j] * coeffs[j]
    
        yFitted.append(fittedValue)
#     for i in yFitted:
#         print(i)
    
#     for i in xe[0]:
#         print(i)
#     print(temp)
    """Next calculated through iterative methods"""
    SSe_check = 0 
    for i in range(0,len(yFitted)):
        SSe_check += (yFitted[i] - y[i])**2
    
    SSt_check = 0
    temp = 0 
    for i in range(0,len(yFitted)):
        temp += yFitted[i]
    temp = temp**2/n
    SSt_check = np.dot(y.transpose(),y) - temp
    
    """If there is a discrepancy between SSe and SSecheck or SSt and SSt_check, return None """
    if(abs(float(SSe) - float(SSe_check)) > .1 or abs(float(SSt) - float(SSt_check)) > .1):
#         print('SSe = ' + str(SSe) + " : SSe_check = " + str(SSe_check))
#         print('SSt = ' + str(SSt) + " : SSt_check = " + str(SSt_check))
#         print('ERROR')
        return None
    
    """SSt should not be zero """
    if(float(SSt) == 0):
        return None

    r = 1 - float(SSe)/float(SSt)
    radjusted = 1 - (float(SSe)/(n-p))/(float(SSt)/(n-1))
    
    """CI not completed as of 31 May 2017 """
    '''Develop a confidence interval '''
    '''95% CI approximate t as 2 for 35-40 DF '''
    x0 = np.array(X_array[0])

    '''Calculates x' (XX')^-1 x '''
    factor = np.dot(x0,np.dot(linalg.inv(XX),x0.transpose()))
    variance = SSe / (n-p)
    root = factor * variance

    """Returns just coeffs and radjusted """
    return [coeffs, radjusted]

"""-----------------------------------------------------------------------------------

This method will call Utility.getTodaysPrice and return todays Price. Then, will get earnings
and try to calculate PE Q and PE TTM 

-----------------------------------------------------------------------------------"""      
def getStatistics(tickerName, dataReady):
    data, variables, price, priceAvg, ones = dataReady[0], dataReady[1], dataReady[2], dataReady[3], dataReady[4]
    todaysPrice = Utility.getTodaysPrice(tickerName)
    if(todaysPrice < 0):
        historicalPrice = sql.getHistoricalClose(tickerName)
        todaysPrice = historicalPrice[0][1]
    
#     print(variables)

    """Calculate things like PE_ratio, etc """
    index_EarningsQ, index_EarningsTTM, index_RevenuesTTM, index_BookvalueTTM = 0,0,0,0 
    index_netincomeTTM, index_totalAssetsTTM, index_cashTTM = 0, 0, 0 
    
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
        if(i == 'Book Value per Share-QM'):
            index_BookvalueTTM = count
        if(i == 'Total Assets-Q'):
            index_totalAssets = count
        if(i == 'Net Income-TTM'):
            index_netincomeTTM = count
        if(i == 'Total Assets-QB'):
            index_totalAssetsTTM = count
        if(i == 'Cash and Equivalents-QB'):
            index_cashTTM = count 
        count += 1

    earningsQ = data[0][index_EarningsQ]
    earningsTTM = data[0][index_EarningsTTM]
    revenuesTTM = data[0][index_RevenuesTTM]
    netIncome = data[0][index_netincome]
    bookValue = data[0][index_BookvalueTTM]
    netIncomeTTM = data[0][index_netincomeTTM]
    totalAssets = data[0][index_totalAssetsTTM]
    totalCash = data[0][index_cashTTM]
    
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
        
    """ROIC = net income / (Total assets - cash) """
    try:
        ROIC = float(netIncome)/(float(totalAssets) - float(totalCash))
    except:
        ROIC = -1
    
#     print(numShares)
    
    return [todaysPrice, PE_ratioTTM, PS_ratioTTM, PB_ratioTTM, ROIC]

'''-------------------------------------------------------

Gets data of ticker name. Returns data, variables, price, priceAvg, and ones arrays

---------------------------------------------------------'''    
def getData(tickerName):
    price, priceAvg = [], []
    ones = []
    
    ''' Data about stock ticker '''
    data = sql.getData(tickerName)
    variables = data[0]
    data = data[1:]
    
#     for i in data:
#         print(i)
    
    '''Extract price, priceAvg, and create ones array '''
    for i in range(0,len(data)):
        temp1 = data[i][len(data[0])-2]
        temp2 = data[i][len(data[0])-1]
        if(temp1 == ' ' or temp2 == ' '):
            break
        price.append(float(temp1))
        priceAvg.append(float(temp2))
        ones.append(1)

#     print([data, variables, price, priceAvg, ones])
    return [data, variables, price, priceAvg, ones]


"""---------------------------------------------------

Returns an array with linear regression analysis for all variables. 

---------------------------------------------------"""
def linearAnalysis(dataReady):
    data, variables, price, priceAvg, ones = dataReady[0], dataReady[1], dataReady[2], dataReady[3], dataReady[4]
    linearFits = []
    
    for i in range(1,len(data[0])-2):
        try:
            temp = []
               
            """Note this for loop goes until the length of price array"""
            """temp will contain variable data (earnings, sales, etc) at index i"""
            for j in range(0,len(price)):
                temp.append(float(data[j][i]))
               
            '''Returns [m,b,r2] ''' 
            linReg1_m, linReg1_b, linReg1_r2 = linearReg(price,temp)
            linReg2_m, linReg2_b, linReg2_r2 = linearReg(priceAvg,temp)
            
            regressedPrice1 = float(temp[0])*linReg1_m + linReg1_b
            regressedPrice2 = float(temp[0])*linReg2_m + linReg2_b
            
            """Will return priceAvg fits. To switch to price, return linReg1_r2 and regressedPrice1 """
            linearFits.append([variables[i], linReg2_r2, regressedPrice2])
        except:
            continue
    
    """ Returns [Regressing Variable, r2, Regressed Price]    """    
    return linearFits
    
"""-----------------------------------------------------

Creates X array for multiple variables regression. This method 
will take keywords and add them to an X array. 

-------------------------------------------------------"""
def MLcreateX(ones, variables, keywords, data):
    coeff = []
    X = []
    X.append(ones)
#     print("ones = ")
#     print(ones)
#     for i in X:
#         print(i)
#     print(keywords)
#     for i in data:
#         print(i)
 
    """Find the index of keyword in variables array. This should be where
    the index is in data"""
    for keyword in keywords:
        tempIndex = 0
        for i in range(0,len(variables)):
            if(variables[i] == keyword):
                coeff.append(i) 
     
    """Adding actual data into X array"""
    for k in coeff:
        temp = []
        for i in range(0,len(X[0])):
            try:
                temp.append(float(data[i][k]))
            except:
                temp.append(0)
                
        """DATA Checking -- If data is not suitable for use, remove it from X array """
        '''When data is large, divide by 1,000,000 to make data more manageable '''
        if(temp[0] > 1000000 and temp[1] > 1000000):
            for j in range(0,len(temp)):
                temp[j] = float(temp[j] / float(1000000))
        
        X.append(temp)
#         print(temp)
        """Is temp too similar to other data inside? If so remove it"""
        for i in range(0,len(X)-1):
            if(Utility.similarArrays(temp,X[i]) == True):
                X.pop()
                break
        
        """Is temp mostly 0s? Is it mostly negative? If so remove it"""
        if(Utility.zeroArray(temp) == True):
            X.pop()
            
        """Is temp mostly the same? EX. [0.1,0.1,0.1,0.1] Remove it. Screws up regression."""
        if(len(X) > 1 and Utility.sameArray(temp) == True):
            X.pop()    
        

 
    """Need to transpose X to prepare for ML analysis. This will be 
    done in a new array called Xready""" 
    Xready = []
    
    if(len(X) == 0):
       return Xready
   
    for i in range(0,len(X[0])):
        temp = []
        for j in range(0,len(X)):
            temp.append(X[j][i]) 
        Xready.append(temp) 

    return Xready

"""---------------------------------------------------------

This method will perform multiple linear analysis and find keywords
that increase r2adjusted. Then, it will add these ML analysis in the 
SQL database. It is called by an outside method. 

--------------------------------------------------------"""
def MLanalysis(tickerName, priceTrue, dataReady):
    data, variables, price, priceAvg, ones = dataReady[0], dataReady[1], dataReady[2], dataReady[3], dataReady[4]
    multipleLinear = []
    
    keywordsList = [["Revenues-Q","Dividends per Basic Common Share-Q", "Revenue Growth-QG"],
                            ["Revenues-T", "Dividends per Basic Common Share-T"],
                            ["Earnings per Diluted Share-Q","Book Value per Share-QM"],
                            ["Operating Expenses-Q", "Cash and Equivalents-QB", "Investments-QB"]
        ]
    
    for keywords in keywordsList:
        '''Prepares Xready and Yready '''
        Xready = MLcreateX(ones,variables,keywords, data)
        yready = []

        for i in range(0,len(priceAvg)):
            temp = []
            """NOTE WILL REGRESS 3 month price average NOT price on earnings date. """
            temp.append(priceAvg[i])
            yready.append(temp) 
        
        Xready = Xready[1:]
        yready = yready[1:]
        
        """Do an initial ML analysis. If ml analysis returns None, 
        set ml as [None, 0]. Coeffs = None, r2 = 0"""
        ml = multipleLinearReg(Xready,yready) 
        if(ml == None):
            ml = [None, 0]
            continue
        
        maxML = ml
#         print(maxML)
        """Iterate through variables and perform regression again to see if r2-adjusted increases"""
        """Perform ML analysis 3 times"""
        for count in range(0,3):   
            maxR2adjusted = maxML[1]
            keyword = ''
            #         print(keywords) 
            for i in variables:
        #         print(i)
                '''Don't want to perform ML on these variables'''
                if(i == 'dates' or i == 'dates-adj' or i == 'Price' or i == 'Average Price' or i == 'rowID'):
                    continue
                keywords.append(i)
                Xready = MLcreateX(ones,variables,keywords,data)
                Xready = Xready[1:]
                  
                try:
                    mlTemp = multipleLinearReg(Xready,yready)
                except:
                    mlTemp = None
                 
#                 for i in Xready:
#                     print(i)
      
                if(mlTemp == None):
                    keywords.pop()
                    continue
                """If r2 is greater than maxR2adjusted and below 1, it is new Max """
                if(mlTemp[1] > maxR2adjusted and mlTemp[1] < 1):
                    maxR2adjusted = mlTemp[1]
                    keyword = i
                    maxML = mlTemp
                keywords.pop()
      
            ml = maxML  
             
            """At this point, keyword with max r2 is added to keywords for final ML and return """
            if(keyword not in keywords and keyword != ''):
                keywords.append(keyword)
#         print(keywords)
    #       print(count)
        
        """Final ML analysis. Xregressors should be most recent data. ML analysis should do
        up to last one. """
        Xready = MLcreateX(ones,variables,keywords,data)
        Xregressors = Xready[0]
#         print(Xregressors)
        Xready = Xready[1:]
#         for i in Xready:
#             print(i)
        ml = multipleLinearReg(Xready,yready)
#         print(ml)
        
        """Find a regressed price with Xregressors data"""
        coeffs = ml[0]
        regressedPrice = 0
         
        for i in range(0,len(coeffs)):
            regressedPrice += Xregressors[i] * coeffs[i]
        
        ml.append(regressedPrice[0])
        ml.append(keywords)
        
        multipleLinear.append(ml)
    
    """ Add ML data into SQL """
    fitsToSQL = [] 
    for i in multipleLinear:
#         print(i)
        """MultipleFits returns [0 - coefficients, 1 - radjusted, 2 - regressedPrice, 3 - keywords ]"""
        radjusted, regressedPrice, keywords = i[1], i[2], i[3]
        fitsToSQL.append([radjusted,regressedPrice, keywords])
        
#     sql.insertML(tickerName, fitsToSQL)

    """Returns an array in the following format:
    [coefficients, radjusted, regressedPrice, keywords ] """
    return multipleLinear
 
"""-----------------------------------------------------

--------------------Outside methods--------------------

-------------------------------------------------------"""

"""----------------------------------------------------

This function will update keywords and regressedPrices information

----------------------------------------------------"""
def updateDatabase(tickerName):
    dataReady = getData(tickerName)
    data, variables, price, priceAvg, ones = dataReady[0], dataReady[1], dataReady[2], dataReady[3], dataReady[4]
    
    if(len(data) <= 1):
        print("Cannot perform regression since data set is too small")
        return
    
    """Keywords for ticker names are created and put into sql through
    MLanalysis function.  """
    MLanalysis(tickerName, True, dataReady)

"""----------------------------------------------------

Analyze will take information from tickerName_ML table for quick analysis. 

----------------------------------------------------"""
def analyze(tickerName):
    dataReady = getData(tickerName)
    tempPrice, PE_ratioTTM, PS_ratioTTM, PB_ratioTTM, ROIC = getStatistics(tickerName, dataReady)
    ROIC *= 100
    
    todaysPrice = Utility.getTodaysPrice(tickerName)
    if(todaysPrice > 0):
        todaysPrice = tempPrice
    
    """Linear Analysis     [Regressing Variable, r2, Regressed Price] """
    linearFits = linearAnalysis(dataReady)
    """Multiple Linear Analysis """
    multipleFits = sql.getML(tickerName)
    
    """--------------------Filters for buy or sell----------------------"""
    tempToday = getStatistics(tickerName, dataReady)
    todaysPrice, PE_ratioTTM = tempToday[0], tempToday[1]
    ''' This price threshold is for buying. Buy if RegPrice > TodaysPrice * 1.05 '''
    price_thresholdBuy = todaysPrice + (todaysPrice * 0.05)
    
    print(tickerName)
    print("Todays Price : " + "{0:.2f}".format(todaysPrice))
    print("P/E : " + "{0:.2f}".format(PE_ratioTTM))
    print("P/S : " + "{0:.2f}".format(PS_ratioTTM))
    print("P/B : " + "{0:.2f}".format(PB_ratioTTM))
    print("ROIC : " + "{0:.2f}".format(ROIC) + '%')
    
    regressedPrices = []
    buy = 0 
    
    for i in multipleFits:
        """MultipleFits returns [0 - radjusted, 1 - regressedPrice, 2 - keywords ]"""
        radjusted, regressedPrice, keywords = i[0], float(i[1]), i[2]
        if(regressedPrice > price_thresholdBuy):
            buy += 1
        regressedPrices.append(regressedPrice)
    regressedPrices.sort()

    print("Multiple linear analysis gives a target price range of " + "{0:.2f}".format(regressedPrices[0]) + " - " 
          + "{0:.2f}".format(regressedPrices[len(regressedPrices) - 1]))
        
    """Buy/Sell/Hold recommendation"""
    if(buy/len(multipleFits) > 0.5):
        print("*** BUY RECOMMENDATION ***")
    print("")

