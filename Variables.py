import Utility

'''-----------------------------------------------------------------------------------

This class holds multiple variables such as directory, fileEnding

-----------------------------------------------------------------------------------'''
class Variables:
    def __init__(self):
        pass
    
    preDirectory = "D:/cmsc/Stock Analysis/"
    
    directory = preDirectory + "ExcelData/"
    
    textOutputDirectory = preDirectory +  "TextFile/Output.txt"
    textBuyDirectory = preDirectory + "TextFile/Buy.txt"
    textShortDirectory = preDirectory + "TextFile/Short.txt"

    def returnUrlList(self, tickerName):
        
        todaysDate = Utility.getTodaysDate().split("/")
        todaysDate[0] = str(int(todaysDate[0])-1)
        todaysDate[1] = str(int(todaysDate[1])-1)
        
        urlList = ["http://chart.finance.yahoo.com/table.csv?s=" + tickerName + 
            "&d=" + todaysDate[0] + "&e=" + todaysDate[1] + "&f=" + todaysDate[2] + "&g=d&a=" + todaysDate[0] + "&b=" + todaysDate[1] + "&c=2005&ignore=.csv",
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?d=q&s=income",  #Quarterly Income Statement
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?d=t&s=income",  #TTM Income Statement
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?d=q&s=balance",      # Quarterly Balance Sheet
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?d=q&s=cashflow",      # Quarterly Cash Flow
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?d=t&s=cashflow",      # TTM Cash flow
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?d=q&s=metrics",     #Quarterly Metrics
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?d=t&s=metrics",      #TTM Metrics
            
            "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?d=q&s=growth"      #Quarterly Growth
            ]
        
        return urlList
    
    ending = ["-Y" ,        #Yahoo!
                  "-Q",        #Quarterly Income Statement
                  "-T",        #TTM Income Statement
                  "-QB",       #Quarterly Balance Sheet
                  "-QC",       #Quarterly Cash Flow
                  "-TC",       #TTM Cash Flow
                  "-QM",       #Quarterly Metrics
                  "-TM",       #TTM Metrics
                  "-QG"]       #Quarterly Growth
    
    fileEnding = ["-Y.csv" ,        #Yahoo!
                  "-Q.xlsx",        #Quarterly Income Statement
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
    
    
    
