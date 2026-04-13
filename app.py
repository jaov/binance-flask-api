from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BINANCE_API_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
HEADERS = {
    'clienttype': 'android',
    'lang': 'vi',
    'versioncode': '14004',
    'versionname': '1.40.4',
    'BNC-App-Mode': 'pro',
    'BNC-Time-Zone': 'Asia/Ho_Chi_Minh',
    'BNC-App-Channel': 'play',
    'BNC-UUID': '067042cf79631252f1409a9baf052e1a',
    'referer': 'https://www.binance.com/',
    'Cache-Control': 'no-cache, no-store',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'okhttp/4.9.0'
}

def _fetch_p2p_data(asset, fiat, trade_type, amount='0', pay_types=None, page=1, rows=10):
    if pay_types is None:
        pay_types = []

    payload = {
        'asset': asset,
        'tradeType': trade_type,
        'fiat': fiat,
        'transAmount': amount,
        'payTypes': pay_types,
        'order': '',
        'page': page,
        'rows': rows,
        'filterType': 'all'
    }

    response = requests.post(BINANCE_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    return [
        {
            'price': float(item.get('adv', {}).get('price')),
            'minSingleTransAmount': float(item.get('adv', {}).get('minSingleTransAmount')),
            'dynamicMaxSingleTransAmount': float(item.get('adv', {}).get('dynamicMaxSingleTransAmount')),
            'nickName': item.get('advertiser', {}).get('nickName'),
        }
        for item in (data.get('data') or [])
    ]

@app.route('/api', methods=['GET'])
def exchange():
    asset = request.args.get('asset')
    fiat = request.args.get('fiat')
    trade_type = request.args.get('tradeType')
    amount = request.args.get('amount', '0')
    pay_types_str = request.args.get('payTypes', '')
    pay_types = pay_types_str.split(',') if pay_types_str else []
    page = request.args.get('page', 1, type=int)
    rows = request.args.get('rows', 10, type=int)

    if not all([asset, fiat, trade_type]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        result = _fetch_p2p_data(asset, fiat, trade_type, amount, pay_types, page, rows)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market', methods=['GET'])
def market_data():
    asset = request.args.get('asset')
    fiat = request.args.get('fiat')
    page = request.args.get('page', 1, type=int)
    rows = request.args.get('rows', 10, type=int)

    if not all([asset, fiat]):
        return jsonify({'error': 'Missing required parameters: asset and fiat'}), 400

    try:
        buy_offers = _fetch_p2p_data(asset, fiat, 'BUY', page=page, rows=rows)
        sell_offers = _fetch_p2p_data(asset, fiat, 'SELL', page=page, rows=rows)

        buy_prices = [offer['price'] for offer in buy_offers]
        sell_prices = [offer['price'] for offer in sell_offers]

        best_bid = max(buy_prices) if buy_prices else None
        best_ask = min(sell_prices) if sell_prices else None
        
        spread = None
        if best_bid is not None and best_ask is not None:
            spread = best_ask - best_bid

        return jsonify({
            'asset': asset,
            'fiat': fiat,
            'best_bid': best_bid,
            'best_ask': best_ask,
            'spread': spread,
            'buy_prices_distribution': sorted(buy_prices),
            'sell_prices_distribution': sorted(sell_prices),
            'buy_offers_count': len(buy_offers),
            'sell_offers_count': len(sell_offers)
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)