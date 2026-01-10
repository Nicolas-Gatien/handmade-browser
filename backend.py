from flask import Flask, request, jsonify
import sys

sys.path.append('../')

from search.search import search

app = Flask(__name__)

@app.get("/search")
def main():
    query = request.args.get('query')

    results = search(query)

    response = jsonify({'results': results})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__": 
    app.run(debug=True, port=5555)