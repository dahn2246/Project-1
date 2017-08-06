from urllib import request
from bs4 import BeautifulSoup
import Utility

"""-----------------------------------------------------------------------

Will get the Sector / Industry of the stock from Yahoo Finance. 

Ex. JCP is Services / Department Stores

------------------------------------------------------------------------"""
def getSector(tickerName):
#     googleSite = "https://www.google.com/finance?q=" + tickerName
    yahooSite = "https://finance.yahoo.com/quote/" + tickerName + "/profile?p=" + tickerName
         
    tempWebFile = request.urlopen(yahooSite).read()
    tempData = BeautifulSoup(tempWebFile, "lxml")
    html = tempData.prettify()
     
#     print(html)
    
    lines = tempData.find_all('strong')
    try:
        sector = Utility.removeTags(str(lines[0]))
        industry = Utility.removeTags(str(lines[1]))
    except:
        return ['', '']
    
    return [sector, industry]
    
#         string = str(i)
#         keyword1 = string.find("Sector:")
#         keyword2 = string.find("Industry:")
#          
#         if(keyword1 > 0 and keyword2 > 0):
#             print(string[keyword1:keyword2+250])
#         print(keyword)
#         if(i.find('Sector') != None or i.find('Industry') != None):
#             print(i)
#         print(i.find('Sector:'))
#     keyword = 'document.obj_data ='
#     keyword1 = '"earnings_announcements_earnings_table"'
#     keyword2 = '"earnings_announcements_webcasts_table"'
     
# print(getSector('WMT'))