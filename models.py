from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    main_info = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))  # Новое поле
    address = db.Column(db.String(200))  # Новое поле
    photo = db.Column(db.String(100))
    tags = db.Column(db.String(200))  # Поле для тегов
    
    notes = db.relationship('Note', backref='person', lazy=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
