from flask import Flask
from flask import render_template
from flask import request

from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/upload_excel_file", methods=['GET', 'POST'])
def upload_excel_file():
    collection = []
    length_of_columns = ''

    file_name = request.files['file']

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


if __name__ == '__main__':
    app.run()
