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
    # Получаем данные из MongoDB
    data_from_mongo = mongo.db[collection_name].find()
    return render_template('index.html', data=data_from_mongo)

if __name__ == '__main__':
    app.run(debug=True)
