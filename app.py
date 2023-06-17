from flask import Flask, request
import postgresPull as pp
import json
import algoLine as al

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
    low_trendlines_json, high_trendlines_json = al.algoLine(ticker, days_out, wick_percent, M_max, proximity_percent)
    response = json.dumps({
        'low_trendlines': low_trendlines_json,
        'high_trendlines': high_trendlines_json
    })
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)