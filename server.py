import json
from pathlib import Path

import chevron
import mariadb
from flask import Flask, Response, jsonify, request, session

app = Flask(__name__)
app.secret_key = 'unique_secret_key'

# 01 A simple endpoint returning a text string
# The name of the function, 'index', is irrelevant; only the route counts
@app.route('/')
def index():
    return "Hello World!"


# 02 An HTML page
@app.route('/page')
def page_html():
    return "<html><body style='background-color: yellow;'>This is an <b>html</b> page</body></html>"


# 03 An HTML page read from the filesystem
@app.route('/another-page')
def another_page_html():
    with open('pages/another-page.html') as f:
        page = f.read()
    return page


# 04 An HTML page read from the filesystem, with the name of the page passed as a named parameter
# call url http://localhost:5000/somehow-dynamic-page-html?page-name=another-page
@app.route('/somehow-dynamic-page')
def somehow_dynamic_page_html():
    page_name = request.args.get('page-name')
    with open(page_name + '.html') as f:
        page = f.read()
    return page


# 05 A dynamic HTML page, with data passed injected inside the page
# call url http://localhost:5000/dynamic-page-html?person-name=MickeyMouse
@app.route('/dynamic-page')
def dynamic_page_html():
    person_name = request.args.get('person-name')
    with open('pages/dynamic-page.html') as f:
        page = f.read()
    filled_page = chevron.render(page, {'name': person_name})
    return filled_page


# 06 An image, read from the file system (you must specify the mimetype (content-type))
@app.route('/image')
def get_image():
    with open('images/smiley.png', 'rb') as f:
        data = f.read()
    return Response(data, mimetype='image/png')


# 07 JSON data. Most fundamental way to create an API.
# Note how jsonify() converts the Python dictionary into a JSON message
@app.route('/data')
def get_data():
    data = {
        "hello": "world",
        "age": 4_000_000_000,
        "address": {
            "system": "solar",
            "planet": 3,
            "radius": 6_300_000,
        }
    }
    return jsonify(data)


# 08 JSON data, coming from the database
# Note the usage of 'with ... as ...' instead of '=', guaranteeing the object is properly closed after usage
@app.route('/database-data')
def get_database_data():
    with open(Path.home() / 'database_connection.json') as f:
        connection_parameters = json.load(f)
    with mariadb.connect(**connection_parameters) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, iso2, iso3, denomination FROM countries")
            return jsonify(cursor.fetchall())


# 09 micro application
# /home displays the login page
# /login performs the login, put the username in session and displays the dashboard page on success
# /logout removes the username from the session
@app.route('/home')
def get_home():
    with open('pages/login-page.html') as f:
        return f.read()

@app.route('/login', methods=['POST'])
def post_login():
    username = request.form['username']
    password = request.form['password']
    # check password using the db; if failure, return error page
    if password != '1234':
        with open('pages/error-page.html') as f:
            return chevron.render(f.read(), {'error': 'Invalid password'})
    # put the username in the session
    session['username'] = username
    with open('pages/dashboard-page.html') as f:
        return chevron.render(f.read(), {'username': session['username']})

@app.route('/logout')
def get_logout():
    session.pop('username', None)
    with open('pages/login-page.html') as f:
        return f.read()

if __name__ == '__main__':
    app.run()
