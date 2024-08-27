from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed

class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    main_info = TextAreaField('Main Info', validators=[Optional()])
    phone_number = StringField('Phone Number', validators=[Optional()])  # Новое поле
    address = StringField('Address', validators=[Optional()])  # Новое поле
    tags = StringField('Tags', validators=[Optional()])  # Поле для тегов
    
    # Обновляем поле фото с проверкой допустимых типов файлов
    photo = FileField('Photo', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    
    submit = SubmitField('Submit')


class NoteForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Note')
