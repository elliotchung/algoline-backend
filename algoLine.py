import postgresPull as pp
import getExtrema as ge
import trendlineFilters as tf

def algolines(ticker, days_out, wick_percent, M_max, proximity_percent, third_point_percent, no_points):
    OHLC = pp.pull_data(ticker)
    minima, maxima = ge.get_extrema_formatted(OHLC)
    low_trendlines, high_trendlines = tf.trendlineFilter(OHLC, minima, maxima, days_out, wick_percent, M_max, proximity_percent, third_point_percent, no_points)

    #convert to List
    for trendline in low_trendlines:
        for i in range(len(trendline)):
            trendline[i] = trendline[i].tolist()
    for trendline in high_trendlines:
        for i in range(len(trendline)):
            trendline[i] = trendline[i].tolist()

    #Convert to Dictionary
    low_trendlines_list = []
    high_trendlines_list = []
    for trendline in low_trendlines:
        temp_list = []
        for i in range(len(trendline[0])):
            temp_list.append({
                "index": trendline[0][i],
                "value": trendline[1][i],
                "time": OHLC[trendline[0][i]]['date']
            })
        low_trendlines_list.append(temp_list)
    for trendline in high_trendlines:
        temp_list = []
        for i in range(len(trendline[0])):
            temp_list.append({
                "index": trendline[0][i],
                "value": trendline[1][i],
                "time": OHLC[trendline[0][i]]['date']
            })
        high_trendlines_list.append(temp_list)
    return low_trendlines_list, high_trendlines_list