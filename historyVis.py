from flask import Flask, render_template, jsonify, request
import Data_Manager as manager
import json
app = Flask(__name__)

my_data = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/init')
def get_data():
    return jsonify(my_data)


@app.route('/brush_data', methods=['POST', 'GET'])
def post_data():
    data = request.get_json()
    now_json = manager.change_data(data)
    # print json.dumps(now_json, ensure_ascii=False)
    return jsonify(now_json)


if __name__ == '__main__':
    app.debug = True
    manager.transform_data("files/history.json")
    my_data = manager.load_data("files/time_cut_history.json")
    app.run(host='0.0.0.0')

