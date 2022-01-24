from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

class Comment_in(FlaskForm):
    comment = StringField('Añadir comentario', widget=TextArea(), validators=[InputRequired()])

    enviar = SubmitField('Enviar')

# ---------- #
