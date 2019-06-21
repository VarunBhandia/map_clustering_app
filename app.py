import urllib.request
import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from pymongo import MongoClient
import pandas as pd

UPLOAD_FOLDER = '/root/PycharmProjects/untitled1/uploads'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/upload_excel_file", methods=['GET', 'POST'])
def upload_excel_file():
    collection = []
    length_of_columns = ''

    file_name = request.files['excel_file']

    dfe = pd.read_excel(file_name)
    data_dict = dfe.to_dict()
    for i in data_dict:
        length_of_columns = len(data_dict[i])

    for j in range(length_of_columns):
        each_row = {}
        for i in data_dict:
            if i in each_row:
                each_row[i].append(data_dict[i][j])
            else:
                each_row[i] = data_dict[i][j]
        collection.append(each_row)
    client = MongoClient('mongodb://localhost:27017/')
    with client:
        db = client.testdb
        db.database_table.insert_many(collection)

    return render_template("data.html", collection=collection)


@app.route("/save_kml_file", methods=['GET', 'POST'])
def upload_kml_file():
    if request.method == 'POST':
        file = request.files['kml_file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded')
        return redirect('/')


if __name__ == '__main__':
    app.run()
