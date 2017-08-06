from Variables import *
from urllib import request

'''-----------------------------------------------------------------------------

Delete all files related to tickerName

--------------------------------------------------------------------------------'''
def deleteAll(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)
    
    for i in fileEnding:
        try:
            os.remove(directory+i)
        except:
            pass
        
"""-----------------------------------------------------------------------------

Downloads price data from Yahoo finance and stockrow.com. Also adds file ending
to excel files. 

--------------------------------------------------------------------------------"""
def downloadAll(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
         
    urlList = fileVariables.returnUrlList(tickerName)
#     print(urlList)
     
    counter = 0
    for i in urlList:
        try:
            request.urlretrieve(i,directory + fileEnding[counter])
            counter += 1
         
        except Exception as inst:
            print(i)
            print(inst)
