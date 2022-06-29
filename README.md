You have several options for running the coin retriever. Note that the endpoint will change based on which method you choose.

### Option 1: Clone the repository
* If you have [Flask](https://flask.palletsprojects.com/en/2.1.x/) installed, you can do the following:
   * Clone this repository
   * Navigate into the repository
   * Run the following commands:
      ```
      export FLASK_APP=app
      flask run
      ```
   * Copy the url listed in the terminal (e.g., http://127.0.0.1:5000). The endpoint you will use is this url + `/coins` (e.g., http://127.0.0.1:5000/coins)

### Option 2: Pull the publicly-available Docker container
   * Run the following commands in your terminal:
      ```
      docker pull chrispatrick/ah-take-home:0.1.0
      docker run -p 5000:5000 -d chrispatrick/ah-take-home:0.1.0
      ```
   * Check to see that the docker container is running:
      ```
      docker ps | grep chrispatrick
      ```
   * To follow the logs for the docker container, run:
      ```
      docker logs -f <CONTAINER_ID>
      ```
   * Your endpoint will be http://0.0.0.0:5000/coins
   * NOTE: if you're on a Mac, you may have an issue with a service already listening on port 5000. If this is the case, see [this tip](https://progressstory.com/tech/port-5000-already-in-use-macos-monterey-issue/).

In addition to having the ability to send `POST` requests with coin IDs for retrieval to the `/coins` endpoint, you can also request the retrieved coin data at any time by sending a `GET` request to the same endpoint. The data will be returned in the following `json` format:
```
{
   "coins": [
      {
         "exchanges": ["ftx_spot"],
         "id": "0-5x-long-algorand-token",
         "taskRun": 1
      }, {
         "exchanges": [],
         "id": "0-5x-long-altcoin-index-token",
         "taskRun": 2
      }, {
         "exchanges": [],
         "id": "0-5x-long-bitcoin-cash-token",
         "taskRun": 4
      }]
}
```

Note that invalid coins will not be included, nor will duplicated instances of any coins. Also, the result will only include records for coins for which all exchanges have been retrieved. With some of the more popular coins, this may take several minutes to complete.

### Notes
- A big shout out to Manolis Christoforou, whose [Python3 wrapper for CoinGecko](https://github.com/man-c/pycoingecko) I used extensively. I would have imported/used that library, but there were some adjustments I needed to make to allow for requesting all pages of exchanges for a coin that had more than 100 exchanges.

### Future Work
This is a WIP and there is much room for improvement, including the following:
- Coin records are stored to memory. Next step could be to save to file or SQL database.
- There may be duplicated exchanges for a particular coin. We could update the `GET` request to support returning a sorted list of unique exchanges for each coin.
- The service is set up to run a full set of requests once, and does not have an option for clearing the memory upon completion of all requests. One adjustment might be to require the requester to include a `firstBatch` and `lastBatch` indicator so the service knows when a full set of requests are complete, and also responding to the requester with a batch idenitifer on first batch so records are associated with the correct set of requests/requester.