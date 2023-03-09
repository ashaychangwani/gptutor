from flask import Flask, request, Response
from brain import Brain
import json
app = Flask(__name__)

b = Brain()
b.reload_models()
@app.route('/query', methods=['POST'])
def query():
    try:
        print('Got query', request.form['message'],request.form.get('history', None))
        payload = {
            'text': b.answer_query_with_context(request.form['message'], b.text, b.context_embeddings, request.form.get('history', None), True)
        }
    except Exception as e:
        print('Got exception',e)
        payload = {'text':'Received error'}
    print('Query response',payload)
    return Response(json.dumps(payload), status = 200,  mimetype='application/json')

@app.route('/upvote', methods=['PUT'])
def upvote():
    try:
        print('Got upvote',request.form['history'])
        update_text = request.form['history'].split('\n')
        b.text = b.update_text_embeddings(b.context_embeddings, b.text, update_text)
        return Response(json.dumps({'text':'Database has been updated'}), status = 200,  mimetype='application/json')
    except Exception as e:
        print('Received exception in upvote',e)
        return Response(json.dumps({'text':'There was an error'}), status = 500,  mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)