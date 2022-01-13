from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, RadioField, TimeField
from wtforms.validators import DataRequired, InputRequired

class HotelForm(FlaskForm):
    check = RadioField('Check',
                        choices=['Arribo', 'Partida'],
                        validators=[InputRequired()])

    vuelo = StringField('Vuelo',
                        validators=[DataRequired()])

    fecha = DateField('Start Date',
                      format='%m/%d/%Y',
                      validators=[InputRequired()])

    hora = TimeField('Hora',
                     validators=[InputRequired()])

    habitacion = IntegerField('N° habitación',
                              validators=[DataRequired()])

    huespedes = IntegerField('N° huespedes',
                             validators=[DataRequired()])

    valijas = IntegerField('N° valijas',
                           validators=[DataRequired()])

    puerto = RadioField('Puerto',
                        choices=['Aeropuerto Carrasco', 'Puerto Montevideo', 'Aeropuerto Pde'],
                        validators=[InputRequired()])

    enviar = SubmitField('Enviar')