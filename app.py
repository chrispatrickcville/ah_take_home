import os

from copy import deepcopy
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
    for id in ids:
        ITER += 1
        task_run = deepcopy(ITER)
        if id not in results:
            result = cg.get_exchanges(id)
            if result:
                results.update({
                    id: {
                        **result,
                        'taskRun': task_run
                    }
                })
                print(f'Coin ID {id} retrieved!', flush=True)
        else:
            print(f'Coin ID {id} already retrieved, skipping', flush=True)

@app.route('/coins', methods=['GET', 'POST'])
def coins():
    if request.method == 'GET':
        print('Getting coins')
        global results
        return {'coins': list(results.values())}
    elif request.method == 'POST':
        if request.headers['Content-Type'] == 'text/csv':
            # Need to update once we see what the data looks like
            f = request.files['coins']
            ids = request.headers['coins'].split(',')
        elif request.headers['Content-Type'] == 'application/json':
            ids = request.get_json()['coins']

    thread = Thread(target=process_response, kwargs={'ids': ids})
    thread.start()
    return 'Started!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)