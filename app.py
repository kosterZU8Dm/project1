from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
collection_name = os.getenv("COLLECTION_NAME")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database'
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    text = db.Column(db.String(255))

@app.route('/')
def index():
    try:
        data_from_mongo = mongo.db[collection_name].find()
        if data_from_mongo.count() == 0:
            return render_template('index.html', message='Нет данных в MongoDB')
        return render_template('index.html', data=data_from_mongo)
    except Exception as e:
        return render_template('index.html', message=f'Ошибка подключения к MongoDB: {str(e)}')

@app.route('/func', methods=['GET', 'POST'])
def func():
    if request.method == 'POST':
        numbers = request.form.getlist('number')
        texts = request.form.getlist('text')
        for number, text in zip(numbers, texts):
            entry = Entry(number=number, text=text) # tables
            db.session.add(entry)
        db.session.commit()
        total = sum(map(int, numbers))
        return render_template('func.html', total=total, texts=texts)
    return render_template('func.html')

if __name__ == '__main__':
    db.create_all() # создаст таблицу в базе данных, если её еще нет.
    app.run(debug=True)
