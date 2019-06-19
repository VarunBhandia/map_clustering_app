from flask import Flask
from flask import render_template
from flask import request

from flask_pymongo import PyMongo
from pymongo import MongoClient

import pandas as pd

app = Flask(__name__)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route("/")
def home_page():
    client = MongoClient('mongodb://localhost:27017/')

    with client:
        db = client.testdb
        myvar = db.collection_names()
    return render_template("index.html", myvar=myvar)


@app.route('/transform', methods=["POST"])
def transform_view():
    file = request.files['data_file']
    if not file:
        return "No file"

    file_contents = file.stream.read().decode("utf-8")
    print(file_contents)

    return render_template("transform.html")


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        data_xls = pd.read_excel(f)
        var_data = data_xls
        return render_template("transform.html", var_data=var_data)
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''


@app.route("/export", methods=['GET'])
def export_records():
    return


if __name__ == '__main__':
    app.run()
