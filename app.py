import os
from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Person, Note
from forms import PersonForm, NoteForm
from werkzeug.utils import secure_filename
from fuzzywuzzy import fuzz

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Создаем папку для загрузок, если она не существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

with app.app_context():
    db.create_all()



@app.route('/')
def index():
    query = request.args.get('query')
    people = Person.query.all()

    if query:
        query = query.lower()
        filtered_people = []
        for person in people:
            person_data = f"{person.name} {person.age} {person.main_info} {person.phone_number} {person.address} {person.tags}".lower()
            if fuzz.partial_ratio(query, person_data) > 60:
                filtered_people.append(person)
        
        people = filtered_people

        if people:
            flash(f'Найдено {len(people)} результат(ов) по запросу "{query}".')
        else:
            flash(f'Результаты по запросу "{query}" не найдены.')

    return render_template('index.html', people=people)




@app.route('/person/<int:person_id>', methods=['GET', 'POST'])
def person_detail(person_id):
    person = Person.query.get_or_404(person_id)
    form = NoteForm()
    if form.validate_on_submit():
        new_note = Note(content=form.content.data, person_id=person.id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('person_detail', person_id=person.id))
    return render_template('person.html', person=person, form=form)


@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    form = PersonForm()
    if form.validate_on_submit():
        new_person = Person(
            name=form.name.data,
            age=form.age.data,
            main_info=form.main_info.data,
            phone_number=form.phone_number.data,  # Новое поле
            tags=form.tags.data,  # Поле для тегов
            address=form.address.data  # Новое поле
        )

        photo_file = form.photo.data
        if photo_file:
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            new_person.photo = photo_filename
        else:
            new_person.photo = 'default_profile.png'

        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_person.html', form=form)

@app.route('/edit_person/<int:person_id>', methods=['GET', 'POST'])
def edit_person(person_id):
    person = Person.query.get_or_404(person_id)
    form = PersonForm(obj=person)
    
    if form.validate_on_submit():
        form.populate_obj(person)

        photo_file = form.photo.data
        if isinstance(photo_file, str):
            pass
        elif photo_file:
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            person.photo = photo_filename
        else:
            person.photo = 'default_profile.png'

        db.session.commit()
        return redirect(url_for('person_detail', person_id=person.id))
    
    return render_template('edit_person.html', form=form, person=person)

@app.route('/delete_person/<int:person_id>')
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    person_id = note.person_id
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('person_detail', person_id=person_id))


@app.route('/edit_note', methods=['POST'])
def edit_note():
    note_id = request.form.get('note_id')
    content = request.form.get('content')
    
    note = Note.query.get(note_id)
    if note:
        note.content = content
        db.session.commit()
        return '', 200  # Возвращаем статус успешного ответа
    else:
        return 'Note not found', 404  # Если заметка не найдена, возвращаем ошибку 404


if __name__ == '__main__':
    app.run(debug=True)
