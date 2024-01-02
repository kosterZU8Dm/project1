from flask import Flask, render_template
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
collection_name = os.getenv("COLLECTION_NAME")

@app.route('/')
def index():
    try:
        data_from_mongo = mongo.db[collection_name].find()
        if data_from_mongo.count() == 0:
            return render_template('index.html', message='Нет данных в MongoDB')
        return render_template('index.html', data=data_from_mongo)
    except Exception as e:
        return render_template('index.html', message=f'Ошибка подключения к MongoDB: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
