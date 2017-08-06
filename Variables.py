import Utility
import os

'''-----------------------------------------------------------------------------------

This class holds multiple variables such as directory, fileEnding

-----------------------------------------------------------------------------------'''
class Variables:
    def __init__(self):
        pass
    
    preDirectory = str(os.getcwd()) + "\\"
    keyword = 'Dow30\\'
    length = preDirectory.find(keyword)  + len(keyword)
    preDirectory = preDirectory[0:length]
    
    
    directory = preDirectory + "ExcelData\\"
    
    textOutputDirectory = preDirectory +  "TextFile/Output.txt"
    textBuyDirectory = preDirectory + "TextFile/Buy.txt"
    textShortDirectory = preDirectory + "TextFile/Short.txt"

    def returnUrlList(self, tickerName):
        
        todaysDate = Utility.getTodaysDate().split("/")
        todaysDate[0] = str(int(todaysDate[0])-1)
        todaysDate[1] = str(int(todaysDate[1])-1)
        
        """Yahoo finance is not working as of 20 May 2017 """
#         urlList = ["http://chart.finance.yahoo.com/table.csv?s=" + tickerName + 
#             "&d=" + todaysDate[0] + "&e=" + todaysDate[1] + "&f=" + todaysDate[2] + "&g=d&a=" + todaysDate[0] + "&b=" + todaysDate[1] + "&c=2005&ignore=.csv",
            
        urlList = [ "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Income%20Statement",  #Quarterly Income Statement
            
            "https://stockrow.com/api/companies/" + tickerName +  "/financials.xlsx?dimension=MRT&section=Income%20Statement",  #TTM Income Statement
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Balance%20Sheet",      # Quarterly Balance Sheet
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Cash%20Flow",      # Quarterly Cash Flow
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRT&section=Cash%20Flow",      # TTM Cash flow
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Metrics",     #Quarterly Metrics
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRT&section=Metrics",      #TTM Metrics
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Growth"      #Quarterly Growth
            ]
        
        return urlList
    
#     ending = ["-Y" ,        #Yahoo!
    ending = ["-Q",        #Quarterly Income Statement
                  "-T",        #TTM Income Statement
                  "-QB",       #Quarterly Balance Sheet
                  "-QC",       #Quarterly Cash Flow
                  "-TC",       #TTM Cash Flow
                  "-QM",       #QuarterlyMetrics
                  "-TM",       #TTM Metrics
                  "-QG"]       #Quarterly Growth
    
#     fileEnding = ["-Y.csv" ,        #Yahoo!
    fileEnding = ["-Q.xlsx",        #Quarterly Income Statement
                  "-T.xlsx",        #TTM Income Statement
                  "-QB.xlsx",       #Quarterly Balance Sheet
                  "-QC.xlsx",       #Quarterly Cash Flow
                  "-TC.xlsx",       #TTM Cash Flow
                  "-QM.xlsx",       #Quarterly Metrics
                  "-TM.xlsx",       #TTM Metrics
                  "-QG.xlsx"]       #Quarterly Growth
    
    def returnFileEnding(self, tickerName):
        returnVar = []
        
        for i in range(0,len(self.fileEnding)):
            returnVar.append(tickerName + self.fileEnding[i])
            
        return returnVar
    
    
    
