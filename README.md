You have several options for running the coin retriever:

### Option 1: Clone the repository
* If you have [Flask](https://flask.palletsprojects.com/en/2.1.x/) installed, you can do the following:
   * Clone this repository
   * Navigate into the repository
   * Run the following commands:
      ```
      export FLASK_APP=app
      flask run
      ```

### Option 2: Pull the publicly-available Docker container
Run the following commands:
```
docker pull chrispatrick/ah-take-home:0.1.0
docker run -p 5000:5000 -d chrispatrick/ah-take-home:0.1.0
```
You can check to see that the docker container is running with:
```
docker ps | grep chrispatrick
```

Once the Flask app is running (via either method), you will use the following endpoint for sending `POST` coin retrieval tasks:
http://0.0.0.0:5000/coins

You can retrieve the retrieved coin data at any time by sending a `GET` request to the same endpoint. The data will be returned in the following `json` format:
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

Note that invalid coins will not be included, nor will duplicated instances of any coins.