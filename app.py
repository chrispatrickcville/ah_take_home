import os

from flask import Flask, request
from lib.coin_gecko import CoinGeckoAPI
from threading import Thread


ITER = 0
results = {}
cg = CoinGeckoAPI()


app = Flask(__name__)

def process_response(ids):
    global ITER
    global results
    query_ids = []
    for id in ids:
        ITER += 1
        if id not in results:
            results.update({
                id: {
                    'id': id,
                    'taskRun': ITER
                }
            })
            query_ids.append(id)
        else:
            print(f'Coin ID {id} already retrieved or in progress, skipping', flush=True)
    for id in query_ids:
        result = cg.get_exchanges(id)
        if result:
            results[id].update({
                **result
            })
            print(f'Coin ID {id} retrieved!', flush=True)

@app.route('/coins', methods=['GET', 'POST'])
def coins():
    if request.method == 'GET':
        print('Getting coins', flush=True)
        global results
        completed_results = [
            result for result in results.values()
            if 'exchanges' in result
        ]
        return {'coins': completed_results}
    elif request.method == 'POST':
        if request.headers['Content-Type'] == 'text/csv':
            ids = request.data.\
                decode('utf-8').\
                replace('coins\n', '').\
                split('\n')
        elif request.headers['Content-Type'] == 'application/json':
            ids = request.get_json()['coins']

    thread = Thread(target=process_response, kwargs={'ids': ids})
    thread.start()
    return 'Started!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)