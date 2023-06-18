from flask import Flask, request
import postgresPull as pp
import algoLine as al
import json

app = Flask(__name__)

#Variables
days_out = 10
wick_percent = 0.01
M_max = 1
proximity_percent = 0.5

@app.route('/OHLC', methods=['POST'])
def api():
    ticker = request.json.get('ticker')
    OHLC = pp.pull_data(ticker)
    response = json.dumps(OHLC)
    return response
@app.route('/algolines', methods=['POST'])
def algolines():
    ticker = request.json.get('ticker')
    low_trendlines_json, high_trendlines_json = al.algolines(ticker, days_out, wick_percent, M_max, proximity_percent)
    response = {
        "low_trendlines": low_trendlines_json,
        "high_trendlines": high_trendlines_json
    }
    response = json.dumps(response)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)