import Utility
import Analysis
import Sqlite as sql
import Download
import Text
from Variables import *   

def main():
    fileVariables = Variables()
    textOutputDirectory = fileVariables.textOutputDirectory
    textBuyDirectory = fileVariables.textBuyDirectory
    textShortDirectory = fileVariables.textShortDirectory
    noupdate = []
    remove = []
    badlist = []

    temp1 = sql.executeReturn('SELECT * FROM list')
    Text.clearText(textOutputDirectory)
    Text.clearText(textBuyDirectory)
    Text.clearText(textShortDirectory)
    
    list = [] 
    for i in temp1:
        list.append(i[0])
        
    temp1 = sql.executeReturn('SELECT * from allstocks')
    allstock = []
    allnames = []
    
    for i in temp1:
        allnames.append(i[1])
        allstock.append(i)

    """-------------Singular Analysis ------------ """
    i = 'AYI'
    print(i)
    data = sql.getData(i)
    lastDate = data[1][0].split('/')
    print(lastDate)
             
#     Download.updateTicker(i)
#     Analysis.updateDatabase(i)
#     Analysis.analyze(i,True,True)

    '''------------Analysis---------------'''  
    list = ['MIDD', 'WASH', 'AZO', 'CVS', 'DG', 'USNA', 'AN', 'BBBY' , 'BMY']
    """-------Stopped at DISCA or ETFC on 15 Apr 2017 """           
    for i in list:
        try:
            print(i)
            data = sql.getData(i)
            lastDate = data[1][0].split('/')
            print(lastDate)
                      
#             Download.updateTicker(i)
#             Analysis.updateDatabase(i)
            Analysis.analyze(i, True, True)
                         
#             if(lastDate[0] == '2016' and float(lastDate[1]) <= 10):
# #                 print('Update')
# #                 Download.updateTicker(i)
# #                 Analysis.analyze(i,False,True)
#                 pass
#             else:
#                 Analysis.analyze(i,False,True)
        except:
            print(i + " : error ")
            badlist.append(i)
               
    print(badlist)
        
    '''----------------Download w/ MarketCap > $200M ------------------------'''
#     count = 0 
#     for i in allstock:
# #         print(i)
#         ticker = i[1].strip()
#         raw = i[3].strip()
#         marketCap = raw[0:len(raw)-1]
#         MorB = raw[len(raw)-1]
#            
#         if(len(marketCap) > 0 and marketCap[len(marketCap)-1] == '.'):
#             marketCap = marketCap[0:len(marketCap)-1]
#         try:
#             marketCap = float(marketCap)
#         except:
#             continue
#    
# #         if(MorB == 'B' or (MorB == 'M' and marketCap > 800)):
#         if(MorB == 'B' and marketCap > 2):
#             if(ticker not in list):
#                 print(ticker)
#                 try:
#                     Download.dlAdd(ticker)
#                     sql.execute("INSERT INTO list (TICKER) VALUES ('" + ticker + "')",None)
#                 except:
#                     print('error ' + ticker)
#                     badlist.append(ticker)
# #     Download.dlAdd('BIDU')
#     print(badlist)
 
# if __name__ == "__main__":
#     main()
    
main()