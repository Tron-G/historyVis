from flask import Flask, render_template, jsonify
import Data_Manager as manager
app = Flask(__name__)

my_data = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/init')
def get_data():
    return jsonify(my_data)


if __name__ == '__main__':
    # manager.transform_data("files/history.json")
    my_data = manager.load_data("files/history.json")
    app.run(debug=True)

