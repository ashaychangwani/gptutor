from flask import Flask, request, jsonify

app = Flask(__name__)

# @app.route('/') 
# def query():
#     data = jsonify(request.json)
#     print(data)
#     return data


# curl -X GET "http://localhost:5000/?id=3"

@app.route('/query', methods=['POST', 'GET'])
def query():
    if request.method == 'POST': 
        print(request.form['message'])
        return 'POST to "/query"'
    else:
        return 'GET to "/query"'

@app.route('/upvote', methods=['POST', 'GET'])
def upvote():
    if request.method == 'POST': 
        print(request.form['message'])
        return 'POST to "/upvote"'
    else:
        return 'GET to "/upvote"'

@app.route('/downvote', methods=['POST', 'GET'])
def downvote():
    if request.method == 'POST': 
        print(request.form['message'])
        return 'POST to "/downvote"'
    else:
        return 'GET to "/downvote"'