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
    try:
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
    except:
        pass
    

            
    """If doesn't work, try Yahoo finance"""
    try:
        tempWebFile = request.urlopen(url2).read()
        tempData = BeautifulSoup(tempWebFile,"lxml")
        html = tempData.prettify()  
    except:
        return -1
    
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

# print(getTodaysPrice('AAL'))
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
    negCount = 0
    
    for i in x:
        if(i > -0.01 and i < 0.01):
            zeroCount += 1
        if(i < 0):
            negCount += 1
    
    '''If more than 70% of array elements are between -0.01 and 0.01 this method mostly contains zeros '''
    if((zeroCount/len(x)) > 0.70):
        return True
    if((negCount/len(x)) > 0.7):
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

"""---------------------------------------------------------

Checks to see if two strings are mostly similar

---------------------------------------------------------"""
def similarity(str1,str2):
    similarityCount = 0
    largerIndex = 0
    
    if(len(str1) == 0  or len(str2) == 0):
        return False
        
    for i in range(0,len(str1)):
        if(str1[i] in str2):
            similarityCount += 1
    
    if(len(str1) > len(str2)):
        largerIndex = len(str1)
    else:
        largerIndex = len(str2)

    if(similarityCount/largerIndex > .95):   
        return True
    return False


"""---------------------------------------------------------

With an array in the form 

''   WMT   TGT   
PE ...
PB ...

Will make a table to format data.  


---------------------------------------------------------"""
def makeTable(data):
    tempData = data
    data = []
    """Transpose Data """
    for i in range(0, len(tempData[0])):
        tempArr = []
        for j in range(0,len(tempData)):
            tempArr.append(tempData[j][i])
        data.append(tempArr)
        
    
    columnLength = []
     
    for i in range(0,len(data[0])):
        longestLength = 0
        for j in range(0,len(data)):
            if(len(data[j][i]) > longestLength):
                longestLength = len(data[j][i])
        longestLength += 5
        columnLength.append(longestLength)

         

    for i in data:
        formatText = ""
        count = 0

        for j in range(0, len(i)):
            colLength = columnLength[count] 
            count += 1
            formatText += i[j].ljust(colLength)
        print(formatText)
         
    
"""---------------------------------------------------------

remove Tags

Ex: <div>Hello</div>
returns Hello

---------------------------------------------------------"""
def removeTags(string):
    firstTag = string.find('>')
    if(firstTag < 0):
        return None
    
    string = string[firstTag + 1:]
    
    secondTag = string.find('<')
    if(secondTag < 0):
        return None
    
    string = string[:secondTag]
    
    return string
    
# print(removeTags("<div>Hello</div>"))

'''---------Testing -----------'''

# print(getFullName("AHGP"))
# print(getInfo("AAPL"))


