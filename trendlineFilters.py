import numpy as np

#Long Wick Filter
def longWickFilter(isLow, data, wick_percent):
    def greenCandle(data):
        return True if data['close'] > data['open'] else False
    def redCandle(data):
        return True if data['close'] < data['open'] else False
    def doji(data):
        return True if data['close'] == data['open'] else False
    if isLow:
        return True if (greenCandle(data) and (data['open']-data['low'])/(data['close']-data['open']) >= wick_percent) or (redCandle(data) and (data['close']-data['low'])/(data['open']-data['close']) >= wick_percent) or (doji(data) and (data['open']-data['low'])/(data['high']-data['low']) >= wick_percent) else False
    else:
        return True if (greenCandle(data) and (data['high']-data['close'])/(data['close']-data['open']) >= wick_percent) or (redCandle(data) and (data['high']-data['open'])/(data['open']-data['close']) >= wick_percent) or (doji(data) and (data['high']-data['close'])/(data['high']-data['low']) >= wick_percent) else False

#High Volume Filter
def highVolumeFilter(data):
    return True if data['volume'] > data['vol_50'] else False

#Calculate Gradient and Intercept
def calculate_gradient_intercept(x1, y1, x2, y2):
    # Calculate the gradient (slope)
    M = (y2 - y1) / (x2 - x1)

    # Calculate the intercept
    C = y1 - M * x1

    return M, C

#Gradient Filter
def gradientFilter(M, M_max):
    return True if abs(M) < M_max else False

#Draw Lines
def draw_lines(start, end, M, C):
    x_arr = np.arange(start, end, 1)
    y_arr = M * x_arr + C
    return x_arr, y_arr

#Check intersection
def check_intersection(x_arr, y_arr, ohlcData, days_out, isMin):
    if len(x_arr) <= days_out:
        return True
    else:
        if isMin:
            for i in range(len(x_arr) - days_out):
                if ohlcData[x_arr[i]]['low'] < y_arr[i]:
                    return False
        else:
            for i in range(len(x_arr) - days_out):
                if ohlcData[x_arr[i]]['high'] > y_arr[i]:
                    return False
        return True

#Check for third point
def check_third_point(x_arr, y_arr, ohlcData, isMin, third_point_percent, no_points):
    counter = 0
    if isMin:
        for i in range(len(x_arr) - 1):
          if (ohlcData[i]['low']*(1 - third_point_percent)) > y_arr[i]:
              continue
          else:
              counter += 1
              if counter >= no_points:
                  return True
              break
    else:
        for i in range(len(x_arr) - 1):
          if (ohlcData[i]['high']*(1 + third_point_percent)) < y_arr[i]:
              continue
          else:
              counter += 1
              if counter >= no_points:
                  return True
              break
    return False

#Check Proximity to latest price
def check_proximity(ohlcData, y_arr, isMin, proximity_percent):
    if isMin:
        return False if (ohlcData[-1]['low']*(1 - proximity_percent)) > y_arr[-1] else True
    else:
        return False if (ohlcData[-1]['high']*(1 + proximity_percent)) < y_arr[-1] else True

#Full Trendline Filter
def trendlineFilter(ohlcData, minima, maxima, days_out, wick_percent, M_max, proximity_percent):
    longwick_minima = [x for x in minima if longWickFilter(True, x, wick_percent)]
    longwick_maxima = [x for x in maxima if longWickFilter(False, x, wick_percent)]
    start_minima = [x for x in longwick_minima if highVolumeFilter(x)]
    start_maxima = [x for x in longwick_maxima if highVolumeFilter(x)]
    low_trendlines_keys = []
    high_trendlines_keys = []
    for i in start_maxima:
        for j in longwick_maxima:
            if i['index']<j['index']:
                high_trendlines_keys.append((i['index'], j['index']))
    for i in start_minima:
        for j in longwick_minima:
            if i['index']<j['index']:
                low_trendlines_keys.append((i['index'], j['index']))
    low_trendlines = []
    high_trendlines = []
    for i in low_trendlines_keys:
        M, C = calculate_gradient_intercept(i[0], ohlcData[i[0]]['low'], i[1], ohlcData[i[1]]['low'])
        if gradientFilter(M, M_max):
            x_arr, y_arr = draw_lines(i[0], ohlcData[-1]['index'], M, C)
            if check_intersection(x_arr, y_arr, ohlcData, days_out, True) and check_proximity(ohlcData, y_arr, True, proximity_percent):
                low_trendlines.append([x_arr, y_arr])
    for i in high_trendlines_keys:
        M, C = calculate_gradient_intercept(i[0], ohlcData[i[0]]['high'], i[1], ohlcData[i[1]]['high'])
        if gradientFilter(M, M_max):
            x_arr, y_arr = draw_lines(i[0], ohlcData[-1]['index'], M, C)
            if check_intersection(x_arr, y_arr, ohlcData, days_out, False) and check_proximity(ohlcData, y_arr, False, proximity_percent):
                high_trendlines.append([x_arr, y_arr])
    return low_trendlines, high_trendlines