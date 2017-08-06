from Analyze import Interface as Analyze #@UnresolvedImport #@UnusedVariable
from IndexData import Interface as IndexData #@UnresolvedImport #@UnusedVariable
import Utility

def main():
    dow30 = IndexData.getList()
    
    for i in dow30:
        Analyze.showAnalysis(i)
        
    list = ['WMT', 'CAT']
    data = []
    data.append(["Name", "todayP", "PE", "PS", "PB", "Debt To Assets", "Income Quality", "ROIC", "Income Quality TTM", "Inventory Turnover"])
    
    for i in list:
        data.append(Analyze.returnFundamentalData(i))

    Utility.makeTable(data)
    
    
if __name__ == "__main__":
    main()




