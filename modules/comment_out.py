from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea

class Comment_out(FlaskForm):
    comment = StringField('Añadir comentario', widget=TextArea())

    enviar = SubmitField('Enviar')

# ---------- #