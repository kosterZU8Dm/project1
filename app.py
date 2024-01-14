from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()

### APP ###
app = Flask(__name__)
### APP ###

### MONGODB ###
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
collection_name = os.getenv("COLLECTION_NAME")
### MONGODB ###

### POSTGRESQL ###
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost/{os.getenv('POSTGRES_DB')}"
db = SQLAlchemy(app)
### POSTGRESQL ###

@app.route('/')
def index():
    try:
        data_from_mongo = mongo.db[collection_name].find()
        if data_from_mongo.count() == 0:
            return render_template('index.html', message='Нет данных в MongoDB')
        return render_template('index.html', data=data_from_mongo)
    except Exception as e:
        return render_template('index.html', message=f'Ошибка подключения к MongoDB: {str(e)}')

@app.route('/calculate', methods=['POST'])
def calculate():
    texts = request.form.getlist('texts[]')
    numbers = [int(num) for num in request.form.getlist('numbers[]')]

    result = {
        'sum': sum(numbers),
        'texts': ', '.join(texts),
    }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    with app.app_context(): # выполнение операций, требующих доступа к приложению.
        db.create_all()  # создаст таблицу в базе данных, если её еще нет.
    app.run(debug=True)
