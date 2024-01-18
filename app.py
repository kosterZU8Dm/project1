from flask import Flask, render_template, request, jsonify
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

class YourModel(db.Model):
    __tablename__ = 'your_table'  # Замените 'your_table' на имя вашей таблицы

    id = db.Column(db.Integer, primary_key=True)
    text_column = db.Column(db.String(255))
    number_column = db.Column(db.Integer)

    def __init__(self, text_column, number_column):
        self.text_column = text_column
        self.number_column = number_column

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

    return jsonify({'success': True, 'result': result})

@app.route('/send_to_postgres', methods=['POST'])
def send_to_postgres():
    texts = request.form.getlist('texts[]')
    numbers = [int(num) for num in request.form.getlist('numbers[]')]

    data_to_insert = [{'text_column': text, 'number_column': num} for text, num in zip(texts, numbers)]

    try:
        for data in data_to_insert:
            db.session.add(YourModel(**data))

        db.session.commit()
        return jsonify({'success': True, 'message': 'Данные успешно отправлены в PostgreSQL'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка при отправке данных в PostgreSQL: {str(e)}'})

if __name__ == '__main__':
    with app.app_context(): # выполнение операций, требующих доступа к приложению.
        db.create_all()  # создаст таблицу в базе данных, если её еще нет.
    app.run(debug=True)
