# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    main_info = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    tags = db.Column(db.String(200), nullable=True)
    photo = db.Column(db.String(100), nullable=True)
    notes = db.relationship('Note', backref='person', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255), nullable=True)  # Имя файла вложения
    attachment_type = db.Column(db.String(10), nullable=True)  # Тип вложения: image, video, audio
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
