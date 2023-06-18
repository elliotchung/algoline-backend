import postgresPull as pp
import getExtrema as ge
import trendlineFilters as tf

def algolines(ticker, days_out, wick_percent, M_max, proximity_percent):
    OHLC = pp.pull_data(ticker)
    minima, maxima = ge.get_extrema_formatted(OHLC)
    low_trendlines, high_trendlines = tf.trendlineFilter(OHLC, minima, maxima, days_out, wick_percent, M_max, proximity_percent)

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
        for i in range(len(trendline[0])):
            low_trendlines_list.append({
                "index": trendline[0][i],
                "value": trendline[1][i],
                "time": OHLC[trendline[0][i]]['date']
            })
    for trendline in high_trendlines:
        for i in range(len(trendline[0])):
            high_trendlines_list.append({
                "index": trendline[0][i],
                "value": trendline[1][i],
                "time": OHLC[trendline[0][i]]['date']
            })
    return low_trendlines_list, high_trendlines_list