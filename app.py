from flask import Flask, render_template, redirect, url_for, request
from models import db, Person, Note
from forms import PersonForm, NoteForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    search = request.args.get('search')
    if search:
        people = Person.query.filter(Person.name.like(f'%{search}%')).all()
    else:
        people = Person.query.all()
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
        # Создаем нового персонажа с данными из формы
        new_person = Person(
            name=form.name.data,
            age=form.age.data,  # Поле может быть None
            main_info=form.main_info.data
        )
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_person.html', form=form)


@app.route('/delete_person/<int:person_id>')
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('person_detail', person_id=note.person_id))

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    form = NoteForm()
    if form.validate_on_submit():
        note.content = form.content.data
        db.session.commit()
        return redirect(url_for('person_detail', person_id=note.person_id))
    form.content.data = note.content
    return render_template('edit_note.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
