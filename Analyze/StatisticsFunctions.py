import numpy as np
import numpy.linalg as linalg
import math
import Utility

"""-----------------------------------------------------------------------------------

Performs a linear regression of data in the form of y = mx + b. 
Will return m, b, and r2

Test data works. 
# xt = [.99,1.02,1.15,1.29,1.46,1.36,0.87,1.23,1.55,1.40,1.19,1.15,.98,1.01,1.11,1.20,1.26,1.32,1.43,0.95]
# yt = [90.01,89.05,91.43,93.74,96.73,94.45,87.59,91.77,99.42,93.65,93.54,92.52,90.56,89.54,89.85,90.39,93.25,93.41,94.98,87.33]

-----------------------------------------------------------------------------------"""
def linearReg(y,x):
    n = len(y)
    sumX = math.fsum(x)
    sumY = math.fsum(y)
    sumXY = 0
    sumX2 = 0
    sumY2 = 0
    
    for i in range(0,n):
        sumXY += x[i]*y[i]
        sumX2 += x[i]**2
        sumY2 += y[i]**2
     
    m = (sumXY - (sumX*sumY/n)) / (sumX2 - (sumX**2)/n)
    b = (sumY/n) - m*(sumX/n)

    SST = sumY2  - n*(sumY/n)**2
    SSE = SST - m*(sumXY - (sumX*sumY/n))
    r2 = 1 - (SSE/SST)
    
    return [m,b,r2]

'''-----------------------------------------------------------------------------------

Performs multiple linear regression. Will return coefficients and r2adjusted in an array
[coeffs, r2adjusted]. There are some cases where multiple linear regression fails. Failed 
cases will return None. 
  
  # X = [[1, 1263.0, 0.46],
# [1, 1254.0, 0.39],
# [1, 1290.15, -0.44],
# [1, 1032.312, 0.29]]
# 
# Y = [[30.59882825531914],
# [26.040824578125008],
# [24.397237841269835],
# [25.448914603174607]]
# 
# multipleLinear(X,Y)

# X = [[1,2,50],
#      [1,8,110],
#      [1,11,120],
#      [1,10,550],
#      [1,8,295],
#      [1,4,200],
#      [1,2,375],
#      [1,2,52],
#      [1,9,100],
#      [1,8,300],
#      [1,4,412],
#      [1,11,400],
#      [1,12,500],
#      [1,2,360],
#      [1,4,205],
#      [1,4,400],
#      [1,20,600],
#      [1,1,585],
#      [1,10,540],
#      [1,15,250],
#      [1,15,290],
#      [1,16,510],
#      [1,17,590],
#      [1,6,100],
#      [1,5,400]
#      ]
#    
# Y = [[9.95],
#      [24.45],
#      [31.75],
#      [35.00],
#      [25.02],
#      [16.86],
#      [14.38],
#      [9.60],
#      [24.35],
#      [27.50],
#      [17.08],
#      [37.00],
#      [41.95],
#      [11.66],
#      [21.65],
#      [17.89],
#      [69.00],
#      [10.30],
#      [34.93],
#      [46.59],
#      [44.88],
#      [54.12],
#      [56.63],
#      [22.13],
#      [21.15]
#      ]
# print(X)
# print(Y)
# multipleLinear(X,Y)
-----------------------------------------------------------------------------------'''
def multipleLinearReg(X_array, y_array):
    X = np.array(X_array)
    y = np.array(y_array)
#     print(X)
#     print(y)
    
    sigma_y = sum(y)
    n = len(X_array) 
    p = len(X_array[0]) - 1
#     print('n = ' + str(n))
#     print('p = ' + str(p))

    """p cannot be greater than n. Sometimes this happens if there are more regression variables
    than there are observations"""
    if(p >= n):
        return None
    
    XX = np.dot(X.transpose(), X)
    Xy = np.dot(X.transpose(),y)
    
    """Try calculations. If these calculations fail, return None """
    try:
        coeffs= np.dot(linalg.inv(XX),Xy)
        xe = np.dot(coeffs.transpose(),X.transpose())
        """Sum of Square Variables Calculations"""
        """First calculated through matrix multiplication """
        SSe = np.dot(y.transpose(),y) - np.dot(np.dot(coeffs.transpose(),X.transpose()),y)
        SSr = np.dot( np.dot(coeffs.transpose(),X.transpose()),y) - sigma_y**2/n
        SSt = np.dot(y.transpose(),y) - sigma_y**2/n
    except:
        return None
    
    """Now, verify data. Find regressed/fitted values and
    try calculating SSe, SSt, and SSr from iterative methods. For example,
    SSe is (yRegressed/Fitted - y actual)**2 """
    """Get all regressed/fitted values from equation"""
    yFitted = []
    for i in X:
        fittedValue = 0

        for j in range(0,len(coeffs)):
            fittedValue += i[j] * coeffs[j]
    
        yFitted.append(fittedValue)
#     for i in yFitted:
#         print(i)
#     for i in xe[0]:
#         print(i)
#     print(temp)

    """Next calculated through iterative methods"""
    SSe_check = 0 
    for i in range(0,len(yFitted)):
        SSe_check += (yFitted[i] - y[i])**2
    
    SSt_check = 0
    temp = 0 
    for i in range(0,len(yFitted)):
        temp += yFitted[i]
    temp = temp**2/n
    SSt_check = np.dot(y.transpose(),y) - temp
    
    """If there is a large discrepancy between SSe and SSecheck or SSt and SSt_check, return None """
    if(abs(float(SSe) - float(SSe_check)) > .1 or abs(float(SSt) - float(SSt_check)) > .1):
#         print('SSe = ' + str(SSe) + " : SSe_check = " + str(SSe_check))
#         print('SSt = ' + str(SSt) + " : SSt_check = " + str(SSt_check))
#         print('ERROR')
        return None
    
    """SSt should not be zero """
    if(float(SSt) == 0):
        return None
    
#     print(str(SSt) + "  " + str(SSt_check))
    r = 1 - float(SSe)/float(SSt)
    radjusted = 1 - (float(SSe)/(n-p))/(float(SSt)/(n-1))

    """CI not completed as of 31 May 2017 """
    """Develop a confidence interval 
    95% CI approximate t as 2 for 35-40 DF """
    
    """Returns just coeffs and radjusted """
    return [coeffs, radjusted]

