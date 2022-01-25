from datetime import datetime, date
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, RadioField, TimeField
from wtforms.validators import DataRequired, InputRequired, NumberRange

class HotelForm(FlaskForm):
    check = RadioField('Ingreso',
                        choices=[('Arribo', 'Arribo'), ('Partida', 'Partida')],
                        validators=[InputRequired()])
    vuelo = StringField('Vuelo',
                        validators=[DataRequired()])
    fecha = DateField('Fecha',
                      validators=[InputRequired()],
                      format='%Y-%m-%d')
    hora = TimeField('Hora',
                     validators=[InputRequired()])
    habitacion = IntegerField('N° habitación',
                              validators=[DataRequired(), NumberRange(min=1)])
    huespedes = IntegerField('N° huespedes',
                             validators=[DataRequired(), NumberRange(min=1, max=99)])
    valijas = IntegerField('N° valijas',
                           validators=[DataRequired(), NumberRange(min=0, max=99)])
    puerto = RadioField('Puerto',
                        choices=['Aeropuerto Carrasco', 'Puerto Montevideo', 'Aeropuerto Pde'],
                        validators=[InputRequired()])
    enviar = SubmitField('Enviar')
