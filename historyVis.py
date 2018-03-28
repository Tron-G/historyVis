from flask import Flask, render_template, jsonify, request, session
import Data_Manager as manager
import Calculation as calc


my_data = []

app = Flask(__name__)


@app.route('/time_range')
def post_data():
    time_range = manager.load_data('files/cache.json')
    return jsonify(time_range)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/feature', methods=['POST'])
def analyse():
    # return send_file("templates/feature.html")
    return render_template('feature.html')


@app.route('/init')
def get_data():
    return jsonify(my_data)


@app.route('/brush_data', methods=['POST', 'GET'])
def post_pie_data():
    data = request.get_json()
    now_json = manager.change_data(data)  # Extracting data by time
    pie_json = calc.calc_topn(now_json)
    manager.save_cache(data)
    # print json.dumps(now_json, ensure_ascii=False)
    return jsonify(pie_json)


@app.route('/radar_data', methods=['POST', 'GET'])
def post_radar_data():
    data = request.get_json()
    now_json = manager.change_data(data)
    radar_json = calc.count_category(now_json)
    # print json.dumps(now_json, ensure_ascii=False)
    return jsonify(radar_json)


@app.route('/bar_data', methods=['POST', 'GET'])
def post_bar_data():
    data = request.get_json()
    now_json = manager.change_data(data)
    bar_json = calc.bar_data(now_json)
    # print json.dumps(now_json, ensure_ascii=False)
    return jsonify(bar_json)


if __name__ == '__main__':
    app.debug = True
    manager.transform_data("files/history.json")  # Raw data processing
    my_data = manager.load_data("files/time_cut_history.json")
    app.run(host='0.0.0.0')
