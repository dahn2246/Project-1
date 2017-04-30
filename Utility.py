import time
import gzip
from bs4 import BeautifulSoup
from urllib import request


'''-----------------------------------------------------------------------------------

This function returns current date in MM/DD/YYYY formate. If month is april, m = 4 not 04

-----------------------------------------------------------------------------------'''
def getTodaysDate():
    dateStr = time.strftime("%m/%d/%Y")
    dateSplit = dateStr.split("/")
    
    # strftime gets month and date in MM, DD. If month is april, m = 04. This removes
    # the zero before the actual date. 
    if(dateSplit[0][0] == '0'):
        dateSplit[0] = dateSplit[0][1:]
    if(dateSplit[1][0] == '0'):
        dateSplit[1] = dateSplit[1][1:]
    
    return dateSplit[0] + '/' + dateSplit[1] + '/' + dateSplit[2]

"""----------------------------------------------------------------------------------

Determines if date in parameter is in future of todays date. Parameter date should be in form
MM/DD/YYYY

----------------------------------------------------------------------------------"""
# def pastTodaysDate(date):
#     """MM/DD/YYYY"""
#     todaysDate = getTodaysDate()
#     
#     date.split('/')
#     todaysDate.split('/')
#     
#     if(float(todaysDate[2]) > float(date[2])):
#         return False
#     elif(float(todaysDate[2]) == float(todaysDate[2]) and float(todaysDate[0]) )


'''-----------------------------------------------------------------------------------

This function returns current price of tickerName
Works As of 11/24/2016

-----------------------------------------------------------------------------------'''
def getTodaysPrice(tickerName):
    url2 = "http://finance.yahoo.com/quote/" + tickerName 
    url1 = "https://www.google.com/finance?q=" + tickerName
    todaysPrice = -1.1
    htmlStr = ''
    index0 = 0 
    index1 = 0
    counter = 0
    gotPrice = False

    """Try google finance first """
    tempWebFile = request.urlopen(url1).read()
    tempData = BeautifulSoup(tempWebFile, "lxml")
    html = tempData.prettify()
    
    lines = tempData.find_all('meta')
     
    payload = ''
    price = ''
    for i in lines:
        marker = 'meta content="'
        line = str(i)
        index0 = line.find(marker)
 
        if(index0 != None):
            payload = line[index0 + len(marker):]
#             print(payload)
             
            index2 = payload.find('"')
             
            price = payload[:index2]
            price = price.replace(',','')
             
            try:
                todaysPrice = float(price)
                return todaysPrice
            except:
                pass
            
    """If doesn't work, try Yahoo finance"""
    tempWebFile = request.urlopen(url2).read()
    tempData = BeautifulSoup(tempWebFile,"lxml")
    html = tempData.prettify()  
    
    lines = tempData.find_all('span')
     
    payload = ''
    price = ''
    for i in lines:
#         print(i)
        marker = 'span class="Trsdu(0.3s) Fw(b)'
        line = str(i)
        index0 = line.find(marker)
 
        if(index0 != None):
            payload = line[index0:]
             
            index1 = payload.find('>')
            index2 = payload.find('<')
             
            price = payload[index1+1:index2]
            price = price.replace(',','')
             
            try:
                todaysPrice = float(price)
                return todaysPrice
            except:
                pass
    return -1

# print(getTodaysPrice('AYI'))

"""span class="Trsdu(0.3s) Fw(b)"""
    
#     
#     '''Try Google Finance First'''
#     req = urllib.request.Request(url1)
#     with urllib.request.urlopen(req) as response:
#         webPage = str(response.read())
#         
#     '''Google Finance'''
#     try:
#         stringBeforePrice = 'values:["' + tickerName + '","'
#         index0 = webPage.index(stringBeforePrice) + len(stringBeforePrice)
#         load = webPage[index0:]
#         index1 = load.index('"' + tickerName + '"')
#         load = load[:index1]        
#         values = load.split(',')
#         
#         for i in values:
#             try:
#                 todaysPrice = float(i[1:len(i)-1])
#                 break
#             except:
#                 pass
#     except: 
#         pass
#         
#     if(gotPrice == True):
#         return todaysPrice
# 
#     ''' Try Yahoo finance if that doesn't work'''
#    
#     while(try1 < 10):
#         req = urllib.request.Request(url2)
#         with urllib.request.urlopen(req) as response:
#             webPage = str(response.read())
#         try:
#             stringBeforePrice = 'data-reactid="'
#             index0 = webPage.index(stringBeforePrice) + len(stringBeforePrice)
#             break
#         except:
#             try1 += 1
#          
#     id = 1
#     while(id<500):
#         try:
#             stringBeforePrice = 'data-reactid="' + str(id) + '">'
#             index0 = webPage.index(stringBeforePrice) + len(stringBeforePrice)
#         
#             counter = index0
#             tempChar = webPage[counter]
#              
#             while(tempChar != '.'):
#                 counter += 1
#                 tempChar = webPage[counter]
#              
#             index1 = counter + 3
#          
#             temp = webPage[index0:index1]
#          
#             if(temp[len(temp)-1] == ','):
#                 temp = temp[0:len(temp)-1]
#             
#             try: 
#                 todaysPrice = float(temp)
#                 break
#             except:
#                 id += 1
#         except:
#             id += 1


'''-------------------------------------------------------

Checks to see if two arrays are very similar
Must be same length

---------------------------------------------------------'''      
def similarArrays(x,y):
    similarityCount = 0
    
    for i in range(0,len(x)):
        x_temp = float(x[i])
        y_temp = float(y[i])
               
        if(x_temp == 0):
            x_high = 0.1
            x_low = -0.1
        else: 
            x_high = x_temp + x_temp * 0.1 
            x_low = x_temp - x_temp * 0.1  
            
        if(y_temp == 0):
            y_high = 0.1
            y_low = -0.1
        else:
            y_high = y_temp + y_temp * 0.1
            y_low = y_temp - y_temp * 0.1 
        
        ''' Comparison'''         
        if(x_temp == y_temp):
            similarityCount += 1
            
        elif(y_low <= x_high and x_high <= y_high):
            similarityCount += 1
        
        elif(y_low <= x_low and x_low <= y_high):
            similarityCount += 1
 
    if(similarityCount > (len(x)-(len(x)*.1))):
        return True
    else:
        return False

'''-------------------------------------------------------

Checks to see arrays are mostly zeros

---------------------------------------------------------'''    
def zeroArray(x):
    zeroCount = 0
    
    for i in x:
        if(i > -0.01 and i < 0.01):
            zeroCount += 1
    
    '''If more than 70% of array elements are between -0.01 and 0.01 this method mostly contains zeros '''
    if((zeroCount/len(x)) > 0.70):
        return True
    return False

'''-------------------------------------------------------

Checks to see if array is mostly the same

---------------------------------------------------------'''    
def sameArray(x):
    for i in range(0,len(x)):
        count = 0
        for j in range(0,len(x)):
            if(i == j):
                continue
            
            if(x[j] > -0.001 + x[i] and x[j] < 0.001 + x[i]):
                count += 1
    
        '''If more than 95% of array elements are between -0.01 and 0.01 this method mostly contains zeros '''
        if((count/(len(x)-1)) > 0.98):
            return True
    return False


'''---------Testing -----------'''

# print(getFullName("AHGP"))
# print(getInfo("AAPL"))


