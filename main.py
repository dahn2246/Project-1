import Utility
import Analysis
import Sqlite as sql
import Download
from Variables import *   


def update(ticker):
    data = sql.getData(ticker)
    lastDate = data[1][0].split('/')
    print(lastDate)
    month = float(lastDate[1])
    year = float(lastDate[0])
    
    today = Utility.getTodaysDate().split('/')
    currentMonth = float(today[0])
    currentYear = float(today[2])
    
    difference = 0 
    if(currentYear == year):
        difference = currentMonth - month
    elif((currentYear - 1) == year):
        difference = (12-month) + currentMonth
    
    """If current month and current year is more than 4 months away, try update """
    if(difference > 4):
        print('Attempting update......')
        Download.updateTicker(ticker)
        Analysis.updateDatabase(ticker)
        data = sql.getData(ticker) 
        lastDate = data[1][0].split('/')
        print(lastDate)

def main():
    temp1 = sql.executeReturn('SELECT * FROM list')
    
    dow30 = [] 
    for i in temp1:
        dow30.append(i[0])

    print('Earnings data updated on 5 June 2017')
    count = 1
    for i in dow30:
        try:
            print('#' + str(count))
            """To update stock earnings, uncomment and run next two lines """
#             Download.updateHistoricalPrice(i)
#             update(i)
            Analysis.analyze(i)
        except:
            print(i + ' - Analysis Failed')
        count += 1

if __name__ == "__main__":
    main()