from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)  # добавляем возраст
    main_info = db.Column(db.Text, nullable=True)  # добавляем главную информацию
    notes = db.relationship('Note', backref='person', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
