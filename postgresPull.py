import psycopg2
import config
import datetime

conn = psycopg2.connect(database=config.DB_NAME,
                        user=config.DB_USER,
                        password=config.DB_PASS,
                        host=config.DB_HOST,
                        port=config.DB_PORT)
cur = conn.cursor()

#Calculate Moving Average
def calculate_moving_average(data, window):
    for i in range(len(data) - window + 1):
        yield sum(data[i:i+window])/window

#Convert Date to Unix Timestamp
def date_to_unix(date):
    return datetime.datetime(date.year, date.month, date.day).timestamp()

def pull_data(ticker):
    #Get Stock Info from DB
    cur.execute(f"SELECT id, name FROM stock WHERE symbol = '{ticker}';")
    result = cur.fetchall()
    if len(result) == 0:
        return None
    stock_id = result[0][0]
    #Pull Daily Stock Data from DB
    cur.execute(f"SELECT dt, open, high, low, close, volume, AVG(volume) OVER (ORDER BY dt ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS vol_50 FROM daily_stock_price WHERE stock_id = {stock_id} ORDER BY dt ASC;")
    DailyStockData = cur.fetchall()

    #Pull Daily volume Data from DB
    cur.execute(f"SELECT dt, volume FROM daily_volume WHERE stock_id = {stock_id} ORDER BY dt ASC;")
    DailyVolumeData = cur.fetchall()

    #Pull 5 Min Stock Data from DB (Time Bucket 1 day)
    cur.execute(f"select time_bucket(INTERVAL '1 day', dt) AS bucket, first(open, dt), max(high), min(low), last(close, dt) from stock_price where stock_id = {stock_id} group by bucket order by bucket ASC;")
    FiveMinStockData = cur.fetchall()

    dates = [x[0] for x in DailyStockData] + [x[0] for x in DailyVolumeData]
    openPrices = [x[1] for x in DailyStockData] + [x[1] for x in FiveMinStockData]
    highPrices = [x[2] for x in DailyStockData] + [x[2] for x in FiveMinStockData]
    lowPrices = [x[3] for x in DailyStockData] + [x[3] for x in FiveMinStockData]
    closePrices = [x[4] for x in DailyStockData] + [x[4] for x in FiveMinStockData]
    volumes = [x[5] for x in DailyStockData] + [x[1] for x in DailyVolumeData]

    #Calculate Moving Average
    temp_vol = [x[5] for x in DailyStockData][-49:] + [x[1] for x in DailyVolumeData]
    vol_50 = [x[6] for x in DailyStockData] + list(calculate_moving_average(temp_vol, 50))

    #Return Data
    try:
        if len(dates) == len(openPrices) == len(highPrices) == len(lowPrices) == len(closePrices) == len(volumes) == len(vol_50):
            OHLC = [
                {
                    'index': i,
                    'open': float(openPrices[i]),
                    'high': float(highPrices[i]),
                    'low': float(lowPrices[i]),
                    'close': float(closePrices[i]),
                    'volume': float(volumes[i]),
                    'vol_50': float(vol_50[i]),
                    'date': date_to_unix(dates[i]),
                }
                for i in range(len(dates))
            ]
            return OHLC
        else:
            raise Exception("Data Lengths are not equal")
    except Exception as e:
        print(e)
        print('Date Length: ', len(dates), '\nOpen Price Length: ', len(openPrices), '\nHigh Price Length: ', len(highPrices), '\nLow Price Length: ', len(lowPrices), '\nClose Price Length: ', len(closePrices), '\nVolume Length: ', len(volumes), '\nVolume 50 Length: ', len(vol_50))
        return None
