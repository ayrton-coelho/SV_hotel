from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from modules.form import HotelForm
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ayrton:password@localhost/sv_hoteles'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = SQLAlchemy(app)

class arribos(db.Model):
    __tablename__ = 'sv_hotel_in'
    id = db.Column(db.String(36), primary_key=True)
    hora_creacion = db.Column(db.Time, nullable=False)
    vuelo = db.Column(db.String(128))
    hora_de_vuelo = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    nro_habitacion = db.Column(db.Integer, nullable=False)
    nro_personas = db.Column(db.Integer, nullable=False)
    origen = db.Column(db.String(128), nullable=False)
    destino = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return 'id: %r\n' % self.id

class partidas(db.Model):
    __tablename__ = 'sv_hotel_out'
    id = db.Column(db.String(36), primary_key=True)
    hora_creacion = db.Column(db.Time, nullable=False)
    vuelo = db.Column(db.String(128))
    hora_de_vuelo = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_pickup = db.Column(db.String(30), nullable=False)
    nro_habitacion = db.Column(db.Integer, nullable=False)
    nro_personas = db.Column(db.Integer, nullable=False)
    nro_valijas = db.Column(db.Integer)
    origen = db.Column(db.String(128), nullable=False)
    destino = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return 'id: %r\n' % self.id


@app.route("/", methods=['GET', 'POST'])
def form():
    form = HotelForm()
    if request.method == 'POST':
        arribo = arribos()
        partida = partidas()
        id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        check = form.check.data
        print("-----------------------------------------")
        print(check)
        print(type(check))
        vuelo = form.vuelo.data
        print(vuelo)
        print(type(vuelo))
        hora = form.hora.data
        print(hora)
        print(type(hora))
        fecha = form.fecha.data
        print(fecha)
        print(type(fecha))
        habitacion = form.habitacion.data
        print(habitacion)
        print(type(habitacion))
        huespedes = form.huespedes.data
        print(huespedes)
        print(type(huespedes))
        valijas = form.valijas.data
        print(valijas)
        print(type(valijas))
        puerto = form.puerto.data
        print(puerto)
        print(type(puerto))
        print("-----------------------------------------")
        hotel = 'random'
        if check == 'Arribo':
            arribo.id = id
            arribo.hora_creacion = created_at
            arribo.vuelo = vuelo
            arribo.hora_de_vuelo = hora
            arribo.fecha = fecha
            arribo.nro_habitacion = habitacion
            arribo.nro_personas = huespedes
            arribo.origen = puerto
            arribo.destino = hotel
            try:
                db.session.add(arribo)
                print(arribo)
                db.session.commit()
            except Exception as e:
                print(e)
        elif check == 'Partida':
            partida.id = id
            partida.hora_creacion = created_at
            partida.vuelo = vuelo
            partida.hora_de_vuelo = hora
            partida.fecha = fecha
            partida.hora_pickup = hora
            partida.nro_habitacion = habitacion
            partida.nro_personas = huespedes
            partida.nro_valijas = valijas
            partida.origen = hotel
            partida.destino = puerto
            try:
                db.session.add(partida)
                db.session.commit()
                print(partida)
            except Exception as e:
                print(e)
        return redirect('/')
    else:
        return render_template('form.html', form=form)

@app.route('/hotel', methods=['GET'])
def hotel():
    viajes_in = arribos.query.order_by(arribos.hora_creacion.desc()).all()
    viajes_out = partidas.query.order_by(partidas.hora_creacion.desc()).all()
    return render_template('hotel.html', viajes_in=viajes_in, viajes_out=viajes_out)

@app.route('/transporte')
def transporte():
    viajes_in = arribos.query.order_by(arribos.hora_creacion.desc()).all()
    viajes_out = partidas.query.order_by(partidas.hora_creacion.desc()).all()
    return render_template('transporte.html', viajes_in=viajes_in, viajes_out=viajes_out)

if __name__ == "__main__":
    app.run(debug=True)