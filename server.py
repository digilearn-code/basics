import json
from pathlib import Path

import chevron
import mariadb
from flask import Flask, Response, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/page')
def page_html():
    return "<html><body style='background-color: yellow;'>This is an <b>html</b> page</body></html>"


@app.route('/another-page')
def another_page_html():
    with open('pages/another-page.html') as f:
        page = f.read()
    return page


@app.route('/somehow-dynamic-page')
def somehow_dynamic_page_html():
    # call url http://localhost:5000/somehow-dynamic-page-html?page-name=another-page
    page_name = request.args.get('page-name')
    with open(page_name + '.html') as f:
        page = f.read()
    return page


@app.route('/dynamic-page')
def dynamic_page_html():
    person_name = request.args.get('person-name')
    with open('pages/dynamic-page.html') as f:
        page = f.read()
    filled_page = chevron.render(page, {'name': person_name})
    return filled_page


@app.route('/image')
def get_image():
    with open('images/smiley.png', 'rb') as f:
        data = f.read()
    return Response(data, mimetype='image/png')


@app.route('/data')
def get_data():
    data = {
        "hello": "world",
        "age": 4000000000,
        "address": {
            "system": "solar",
            "planet": 3,
            "radius": 6300000,
        }
    }
    return jsonify(data)

@app.route('/database-data')
def get_database_data():
    with open(Path.home() / 'database_connection.json') as f:
        connection_parameters = json.load(f)
    with mariadb.connect(**connection_parameters) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, iso2, iso3, denomination FROM countries")
            return jsonify(cursor.fetchall())


if __name__ == '__main__':
    app.run()
