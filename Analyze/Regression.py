import Utility #@UnresolvedImport
from Analyze import StatisticsFunctions as stat #@UnresolvedImport
from RegressionData import Interface as RegressionData #@UnresolvedImport
from Analyze import GetData #@UnresolvedImport

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
            linReg1_m, linReg1_b, linReg1_r2 = stat.linearReg(price,temp)
            linReg2_m, linReg2_b, linReg2_r2 = stat.linearReg(priceAvg,temp)
            
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
                
#         print(temp)
                
        """DATA Checking -- If data is not suitable for use, remove it from X array """
        '''When data is large, divide by 1,000,000 to make data more manageable '''
        if(temp[0] > 1000000 and temp[1] > 1000000):
            for j in range(0,len(temp)):
                temp[j] = float(temp[j] / float(1000000))
        
        X.append(temp)
#         print(temp)
        """Is temp too similar to other data inside? If so remove it"""
        for i in range(0,len(X)-2):
#             print('remove1')
            if(Utility.similarArrays(temp,X[i]) == True):
                X.remove(temp)
                break
        
        """Is temp mostly 0s? Is it mostly negative? If so remove it"""
        if(Utility.zeroArray(temp) == True):
#             print('remove2')
            X.remove(temp)
            """Is temp mostly the same? EX. [0.1,0.1,0.1,0.1] Remove it. Screws up regression."""
        elif(len(X) > 1 and Utility.sameArray(temp) == True):        
#             print('remove3')
            X.remove(temp)
        

 
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
def MLanalysis(tickerName):
    dataReady = GetData.getData(tickerName)
    data, variables, price, priceAvg, ones = dataReady[0], dataReady[1], dataReady[2], dataReady[3], dataReady[4]
    multipleLinear = []
    
#     for i in data:
#         print(i)
     
    keywordsList = [["Revenues-Q","Dividends per Basic Common Share-Q"],
                    ["Revenues-T", "Dividends per Basic Common Share-T"],
                    ["Free Cash Flow-QC","Book Value per Share-QM"],
                    ["Operating Expenses-Q", "Cash and Equivalents-QB"]
        ]
     
    """yready is an array of average prices """
    yready = []
    for i in range(0,len(priceAvg)):
        temp = []
        """NOTE WILL REGRESS 3 month price average NOT price on earnings date. """
        temp.append(priceAvg[i])
        yready.append(temp) 
    yready = yready[1:]
    
#     for i in yready:
#         print(i)
      
    for keywords in keywordsList:
        '''Prepares Xready and Yready '''
        Xready = MLcreateX(ones,variables,keywords, data)
        Xready = Xready[1:]
        
#         for i in Xready:
#             print(i)
          
        """Do an initial ML analysis. If ml analysis returns None, 
        set ml as [None, 0]. Coeffs = None, r2 = 0"""
        ml = stat.multipleLinearReg(Xready,yready) 
        if(ml == None):
            ml = [None, 0]
            continue
          
        maxML = ml
#         print(maxML)
        """Iterate through variables and perform regression again to see if r2-adjusted increases"""
        """Perform ML analysis 3 times"""
        for count in range(0,1):   
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
                    mlTemp = stat.multipleLinearReg(Xready,yready)
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
        Xready = Xready[1:]
        ml = stat.multipleLinearReg(Xready,yready)
#         print(Xregressors)
#         for i in Xready:
#             print(i)
#         print(ml)
#         print(keywords)
          
        """Find a regressed price with Xregressors data"""
        coeffs = ml[0]
        regressedPrice = 0
           
        for i in range(0,len(coeffs)):
            regressedPrice += Xregressors[i] * coeffs[i]
      
#         print(coeffs)
#         print(regressedPrice)
          
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
        
#     for i in multipleLinear:
#         print(i)
          
    RegressionData.insertRegressionData(tickerName, fitsToSQL)
  
    """Returns an array in the following format:
    [coefficients, radjusted, regressedPrice, keywords ] """
#     return multipleLinear

# MLanalysis('SHLD')
# MLanalysis('COST')
# MLanalysis('WMT')