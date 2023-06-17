from findiff import FinDiff
import numpy as np

#Get the momentum and acceleration of an array
def get_mom_acc(arr):
    dx = 1 # 1 day
    dydx = FinDiff(0, dx, 1)
    dydx2 = FinDiff(0, dx, 2)
    mom = dydx(arr)
    acc = dydx2(arr)
    return mom, acc

#find local minima and maxima
def get_extrema(isMin, arr, mom, acc):
    return [
        i for i in range(len(mom))
        if (acc[i] > 0 if isMin else acc[i] < 0) 
        and(
            (mom[i] == 0) #Stationary point
            or (i != len(mom) - 1 and (mom[i] > 0 and mom[i+1] < 0) and (arr[i] >= arr[i+1])) #Exclude the last value, Local Maxima
            or (i != len(mom) - 1 and (mom[i] < 0 and mom[i+1] > 0) and (arr[i] <= arr[i+1])) #exclude the last value, Local Minima
            or (i != 0 and mom[i-1] > 0 and mom[i] < 0 and arr[i-1] < arr[i]) #Exclude the first value, Local Maxima
            or (i != 0 and mom[i-1] < 0 and mom[i] > 0 and arr[i-1] > arr[i]) #Exclude the first value, Local Minima
            )
        ]

#Get nicely formatted extrema
def get_extrema_formatted(ohlcData):
    low_arr = np.array([x['low'] for x in ohlcData])
    high_arr = np.array([x['high'] for x in ohlcData])
    low_mom, low_acc = get_mom_acc(low_arr)
    high_mom, high_acc = get_mom_acc(high_arr)
    minima_index = get_extrema(True, low_arr, low_mom, low_acc)
    maxima_index = get_extrema(False, high_arr, high_mom, high_acc)
    minima = [ohlcData[i] for i in minima_index]
    maxima = [ohlcData[i] for i in maxima_index]
    return minima, maxima